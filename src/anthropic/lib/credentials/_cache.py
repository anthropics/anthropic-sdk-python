from __future__ import annotations

import time
import inspect
import logging
import threading
from typing import Union, Generic, TypeVar, Callable, Optional, cast

import anyio
import httpx2

from ._types import AccessToken, AccessTokenProvider, AsyncAccessTokenProvider, is_async_token_provider
from ..._utils import asyncify, signature_without_evaluating_annotations
from ._workload import WorkloadIdentityError
from ._constants import ADVISORY_REFRESH_SECONDS, MANDATORY_REFRESH_SECONDS
from ..._exceptions import AnthropicError

__all__ = ["TokenCache"]

log: logging.Logger = logging.getLogger(__name__)

# Skip advisory refreshes for this many seconds after a failure so a
# token-endpoint outage isn't hammered at request rate. Fixed (no jitter):
# trades fast recovery against fleet load during a sustained outage.
ADVISORY_REFRESH_BACKOFF_SECONDS = 5

_EventT = TypeVar("_EventT", threading.Event, anyio.Event)


def valid_access_token(value: object) -> AccessToken:
    if inspect.iscoroutine(value):
        # Closing it stops Python warning that the coroutine was never awaited.
        value.close()
        raise AnthropicError(
            "credentials provider returned a coroutine instead of an AccessToken; pass the `async def` function itself"
        )
    if not isinstance(value, AccessToken):
        raise AnthropicError(f"credentials provider returned {type(value).__name__} instead of an AccessToken")
    return value


def accepts_force_refresh(provider: Callable[..., object]) -> bool:
    """False for a legacy provider that takes no `force_refresh` argument; it is called without one."""
    try:
        return any(
            parameter.name == "force_refresh" or parameter.kind is inspect.Parameter.VAR_KEYWORD
            for parameter in signature_without_evaluating_annotations(provider).parameters.values()
        )
    except (TypeError, ValueError):
        # No signature to inspect, as for some C callables. Assume the documented contract.
        return True


class Refresh(Generic[_EventT]):
    """What a caller that `TokenCache._next_step` told to call the provider needs to finish up."""

    def __init__(
        self,
        *,
        owned_event: Optional[_EventT],
        force: bool,
        advisory_fallback: Optional[AccessToken],
        remaining_seconds: int,
    ) -> None:
        self.owned_event: Optional[_EventT] = owned_event
        """The single-flight event this caller created and must release. `None` for a
        per-request caller (cached `expires_at=0`), because nobody waits for it."""
        self.force = force
        """Whether to pass `force_refresh=True`. Only the single-flight leader ever forces."""
        self.advisory_fallback = advisory_fallback
        """The cached token to serve if this is an advisory refresh and it fails."""
        self.remaining_seconds = remaining_seconds


class TokenCache:
    """Thread-safe cache wrapping an `AccessTokenProvider` or an
    `AsyncAccessTokenProvider` with two-tier proactive refresh and
    single-flight semantics.

    `async_get_token` applies the same policy as `get_token`: an async
    provider is awaited on the event loop, a sync one runs `get_token` in a
    worker thread.

    Refresh policy on each `get_token` call:

    * No cached token → call provider (blocking), cache, return.
    * Cached with `expires_at=None` → return cached forever (never refresh).
    * More than `advisory_refresh_seconds` remaining → return cached.
    * Between `mandatory_refresh_seconds` and `advisory_refresh_seconds`
      remaining (advisory window) → try provider; on success swap cache; on
      failure log a warning and return the stale cached token. If another
      caller is already refreshing, the advisory caller just returns the
      cached token — no second refresh, no waiting.
    * Less than `mandatory_refresh_seconds` remaining or already expired
      (mandatory window) → call provider; on failure RAISE. Concurrent
      mandatory callers wait on a shared `Event` so exactly one provider
      call is in flight.
    * Cached with `expires_at=0` → never served. The provider does its own
      caching, so every call asks it again and concurrent callers each make
      their own call, so the provider must be safe to call concurrently. Only
      exactly `0` does this; any other past value is an expired token and is
      refreshed one call at a time. After a 401 empties the cache, one caller
      makes the `force_refresh=True` call and callers that arrive after the
      401 wait for it; calls already in flight finish on their own and do not
      repopulate the cache. Normal caching resumes once the provider returns a
      token with a real expiry.

    The lock is released before the provider call so a 30-second HTTP POST
    doesn't serialize unrelated callers through a single thread. This matters
    under async: `asyncify(get_token)` runs on the thread pool, and holding
    the lock across the network call would pin an async worker for the whole
    exchange.
    """

    def __init__(
        self,
        provider: AccessTokenProvider | AsyncAccessTokenProvider,
        *,
        advisory_refresh_seconds: int = ADVISORY_REFRESH_SECONDS,
        mandatory_refresh_seconds: int = MANDATORY_REFRESH_SECONDS,
        time_source: Callable[[], float] = time.time,
    ) -> None:
        self._provider: Optional[AccessTokenProvider] = None
        self._async_provider: Optional[AsyncAccessTokenProvider] = None
        if is_async_token_provider(provider):
            self._async_provider = provider
        else:
            self._provider = provider
        self._accepts_force_refresh = accepts_force_refresh(provider)
        self._advisory = advisory_refresh_seconds
        self._mandatory = mandatory_refresh_seconds
        self._time_source = time_source
        self._lock = threading.Lock()
        self._cached: Optional[AccessToken] = None
        # Set while a single-flight refresh is in flight. Waiters in the
        # mandatory window block on this event; the leader clears it after
        # publishing the fresh token (or on failure). An anyio.Event belongs to
        # the loop that created it, so a cache with an async provider is single-loop.
        self._refresh_event: Optional[Union[threading.Event, anyio.Event]] = None
        # One-shot: invalidate() sets it; the next single-flight leader passes
        # force_refresh=True so on-disk providers don't re-serve a stale token.
        self._next_force = False
        # Time of last advisory-refresh failure (never reset on success —
        # only distance-from-now matters).
        self._last_advisory_failure_time: float = 0.0

    def _invoke_provider(self, provider: AccessTokenProvider, *, force: bool) -> AccessToken:
        """Invoke `provider`, leaving out `force_refresh` for a legacy provider that doesn't take it."""
        if not self._accepts_force_refresh:
            return provider()
        return provider(force_refresh=force)

    async def _async_invoke_provider(self, provider: AsyncAccessTokenProvider, *, force: bool) -> AccessToken:
        """Async version of `_invoke_provider`."""
        if not self._accepts_force_refresh:
            return await provider()
        return await provider(force_refresh=force)

    def _call_provider(self, provider: AccessTokenProvider, *, force: bool) -> AccessToken:
        """Call the provider, retrying once on a 401 from the token endpoint."""
        try:
            return valid_access_token(self._invoke_provider(provider, force=force))
        except WorkloadIdentityError as err:
            if err.status_code != 401:
                raise
            log.debug("Token provider returned 401; retrying once")
            return valid_access_token(self._invoke_provider(provider, force=True))

    async def _async_call_provider(self, provider: AsyncAccessTokenProvider, *, force: bool) -> AccessToken:
        """Async version of `_call_provider`."""
        try:
            return valid_access_token(await self._async_invoke_provider(provider, force=force))
        except WorkloadIdentityError as err:
            if err.status_code != 401:
                raise
            log.debug("Token provider returned 401; retrying once")
            return valid_access_token(await self._async_invoke_provider(provider, force=True))

    def get_token(self) -> str:
        """Return a valid bearer token, refreshing if necessary."""
        provider = self._provider
        if provider is None:
            raise RuntimeError(
                "This `TokenCache` wraps an async provider; call `async_get_token()` instead of `get_token()`."
            )
        while True:
            step = self._next_step(threading.Event)
            if isinstance(step, str):
                return step
            if isinstance(step, threading.Event):
                step.wait()
                # Loop back and re-read the cache — the refresh may have
                # succeeded (return fresh token), failed (start a new
                # refresh ourselves), or been invalidated in between.
                continue

            # Run the provider outside the lock. The except catches
            # BaseException (not a narrow tuple) so the refresh event is
            # always released — a user-supplied provider raising e.g.
            # RuntimeError must not deadlock mandatory-window waiters.
            try:
                fresh = self._call_provider(provider, force=step.force)
            except BaseException as err:
                stale_token = self._end_failed_refresh(err, step)
                if stale_token is None:
                    raise
                return stale_token
            return self._end_refresh(fresh, step)

    async def async_get_token(self) -> str:
        """Async version of `get_token`.

        An async provider is awaited on the event loop. A sync provider runs
        `get_token` in a worker thread.
        """
        provider = self._async_provider
        if provider is None:
            return await asyncify(self.get_token)()
        while True:
            step = self._next_step(anyio.Event)
            if isinstance(step, str):
                return step
            if isinstance(step, anyio.Event):
                await step.wait()
                continue
            # CancelledError lands in the except too. Nothing in there awaits,
            # so a cancelled leader still releases its waiters.
            try:
                fresh = await self._async_call_provider(provider, force=step.force)
            except BaseException as err:
                stale_token = self._end_failed_refresh(err, step)
                if stale_token is None:
                    raise
                return stale_token
            return self._end_refresh(fresh, step)

    def _next_step(self, event_class: Callable[[], _EventT]) -> Union[str, _EventT, Refresh[_EventT]]:
        """Decide under the lock what the caller does next.

        A `str` is the token to serve. An event is a refresh in flight to wait on
        before asking again. A `Refresh` means call the provider, then
        `_end_refresh` or `_end_failed_refresh`.
        """
        advisory_fallback: Optional[AccessToken] = None
        remaining_seconds = 0
        with self._lock:
            cached = self._cached
            if cached is not None:
                if cached.expires_at is None:
                    return cached.token
                if cached.expires_at == 0:
                    # Per-request: no single-flight, and never forced. invalidate() empties
                    # the cache, so the forced call after a 401 is always made by a leader.
                    return Refresh(owned_event=None, force=False, advisory_fallback=None, remaining_seconds=0)
                remaining = cached.expires_at - self._time_source()
                if remaining > self._advisory:
                    return cached.token
                if remaining > self._mandatory:
                    # Advisory window. If a refresh is already running,
                    # keep serving the cached token — don't queue and
                    # don't start a second refresh.
                    if self._refresh_event is not None:
                        return cached.token
                    # Backoff: skip refresh and serve cached after a
                    # recent advisory failure.
                    if self._time_source() - self._last_advisory_failure_time < ADVISORY_REFRESH_BACKOFF_SECONDS:
                        return cached.token
                    advisory_fallback = cached
                    remaining_seconds = int(remaining)

            if self._refresh_event is not None:
                # Mandatory-window caller with a refresh in flight: wait.
                # cast: neither checker can know that one cache only ever creates one kind of event.
                return cast(_EventT, self._refresh_event)
            # We're the leader. The force flag is read in the same lock hold that elects the
            # leader, so a per-request call that started before an invalidate() can't take it.
            owned_event = self._refresh_event = event_class()
            return Refresh(
                owned_event=owned_event,
                force=self._next_force,
                advisory_fallback=advisory_fallback,
                remaining_seconds=remaining_seconds,
            )

    def _end_refresh(self, fresh: AccessToken, refresh: Refresh[_EventT]) -> str:
        with self._lock:
            if refresh.owned_event is None:
                # A per-request caller may only overwrite another per-request token. After
                # invalidate() the cache has to stay empty, so that the next caller makes
                # the forced call and everyone else waits for it.
                if self._cached is not None and self._cached.expires_at == 0:
                    self._cached = fresh
            else:
                # The same goes for a leader whose unforced call overlapped an invalidate():
                # its token may be the rejected one, so it is used for this request only.
                if refresh.force or not self._next_force:
                    self._cached = fresh
                if refresh.force:
                    # Cleared only after a forced call succeeds, so a failure still forces the next call.
                    self._next_force = False
                self._refresh_event = None
        if refresh.owned_event is not None:
            refresh.owned_event.set()
        return fresh.token

    def _end_failed_refresh(self, err: BaseException, refresh: Refresh[_EventT]) -> Optional[str]:
        """Release any waiters. Returns the stale token to serve if this was an advisory
        refresh, or `None` if the caller should re-raise `err`."""
        if refresh.owned_event is not None:
            with self._lock:
                self._refresh_event = None
            refresh.owned_event.set()
        if refresh.advisory_fallback is None or not isinstance(err, (AnthropicError, httpx2.HTTPError)):
            return None
        log.warning(
            "Advisory token refresh failed (%ds remaining); serving cached token: %s",
            refresh.remaining_seconds,
            err,
        )
        with self._lock:
            self._last_advisory_failure_time = self._time_source()
        return refresh.advisory_fallback.token

    def invalidate(self) -> None:
        """Clear the cached token so the next `get_token` re-invokes the provider.

        Also sets a one-shot `force_refresh` flag so on-disk providers skip
        their freshness short-circuit instead of re-serving the revoked token.
        """
        with self._lock:
            self._cached = None
            self._next_force = True
