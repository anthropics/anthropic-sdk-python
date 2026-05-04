from __future__ import annotations

import time
import logging
import threading
from typing import Callable, Optional

import httpx

from ._types import AccessToken, AccessTokenProvider
from ._workload import WorkloadIdentityError
from ._constants import ADVISORY_REFRESH_SECONDS, MANDATORY_REFRESH_SECONDS
from ..._exceptions import AnthropicError

__all__ = ["TokenCache"]

log: logging.Logger = logging.getLogger(__name__)

# Skip advisory refreshes for this many seconds after a failure so a
# token-endpoint outage isn't hammered at request rate. Fixed (no jitter):
# trades fast recovery against fleet load during a sustained outage.
ADVISORY_REFRESH_BACKOFF_SECONDS = 5


class TokenCache:
    """Thread-safe cache wrapping an :class:`AccessTokenProvider` with two-tier
    proactive refresh and single-flight semantics.

    Refresh policy on each :meth:`get_token` call:

    * No cached token → call provider (blocking), cache, return.
    * Cached with ``expires_at=None`` → return cached forever (never refresh).
    * More than ``advisory_refresh_seconds`` remaining → return cached.
    * Between ``mandatory_refresh_seconds`` and ``advisory_refresh_seconds``
      remaining (advisory window) → try provider; on success swap cache; on
      failure log a warning and return the stale cached token. If another
      caller is already refreshing, the advisory caller just returns the
      cached token — no second refresh, no waiting.
    * Less than ``mandatory_refresh_seconds`` remaining or already expired
      (mandatory window) → call provider; on failure RAISE. Concurrent
      mandatory callers wait on a shared ``Event`` so exactly one provider
      call is in flight.

    The lock is released before the provider call so a 30-second HTTP POST
    doesn't serialize unrelated callers through a single thread. This matters
    under async: ``asyncify(get_token)`` runs on the thread pool, and holding
    the lock across the network call would pin an async worker for the whole
    exchange.
    """

    def __init__(
        self,
        provider: AccessTokenProvider,
        *,
        advisory_refresh_seconds: int = ADVISORY_REFRESH_SECONDS,
        mandatory_refresh_seconds: int = MANDATORY_REFRESH_SECONDS,
        time_source: Callable[[], float] = time.time,
    ) -> None:
        self._provider = provider
        self._advisory = advisory_refresh_seconds
        self._mandatory = mandatory_refresh_seconds
        self._time_source = time_source
        self._lock = threading.Lock()
        self._cached: Optional[AccessToken] = None
        # Set when a refresh is in flight. Waiters in the mandatory window
        # block on this event; the leader clears it after publishing the
        # fresh token (or on failure).
        self._refresh_event: Optional[threading.Event] = None
        # One-shot: invalidate() sets it; next provider call passes
        # force_refresh=True so on-disk providers don't re-serve a stale token.
        self._next_force = False
        # Time of last advisory-refresh failure (never reset on success —
        # only distance-from-now matters).
        self._last_advisory_failure_time: float = 0.0

    def _invoke_provider(self, *, force: bool) -> AccessToken:
        """Invoke ``self._provider``, tolerating legacy zero-arg callables."""
        try:
            return self._provider(force_refresh=force)
        except TypeError as err:
            # Back-compat for legacy zero-arg providers. Argument-binding
            # TypeErrors fire before the body runs, so this can't double-invoke;
            # a TypeError from inside the provider won't mention the kwarg name.
            if "force_refresh" not in str(err):
                raise
            return self._provider()  # type: ignore[call-arg]

    def _call_provider(self) -> AccessToken:
        """Call the provider, retrying once on a 401 from the token endpoint."""
        # Read but don't clear yet — clearing only on success keeps the flag
        # alive across a transient failure so the retry still forces.
        with self._lock:
            force = self._next_force
        try:
            result = self._invoke_provider(force=force)
        except WorkloadIdentityError as err:
            if err.status_code != 401:
                raise
            log.debug("Token provider returned 401; retrying once")
            result = self._invoke_provider(force=True)
        with self._lock:
            self._next_force = False
        return result

    def get_token(self) -> str:
        """Return a valid bearer token, refreshing if necessary."""
        while True:
            advisory_fallback: Optional[AccessToken] = None
            remaining_seconds = 0
            with self._lock:
                cached = self._cached
                if cached is not None:
                    if cached.expires_at is None:
                        return cached.token
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
                    waiter_event: Optional[threading.Event] = self._refresh_event
                else:
                    # We're the leader.
                    self._refresh_event = threading.Event()
                    waiter_event = None

            if waiter_event is not None:
                waiter_event.wait()
                # Loop back and re-read the cache — the refresh may have
                # succeeded (return fresh token), failed (start a new
                # refresh ourselves), or been invalidated in between.
                continue

            # Leader: run the provider outside the lock. The except catches
            # BaseException (not a narrow tuple) so the refresh event is
            # always released — a user-supplied provider raising e.g.
            # RuntimeError must not deadlock mandatory-window waiters.
            try:
                fresh = self._call_provider()
            except BaseException as err:
                with self._lock:
                    released = self._refresh_event
                    self._refresh_event = None
                assert released is not None
                released.set()
                if advisory_fallback is not None and isinstance(err, (AnthropicError, httpx.HTTPError)):
                    log.warning(
                        "Advisory token refresh failed (%ds remaining); serving cached token: %s",
                        remaining_seconds,
                        err,
                    )
                    with self._lock:
                        self._last_advisory_failure_time = self._time_source()
                    return advisory_fallback.token
                raise

            with self._lock:
                self._cached = fresh
                released = self._refresh_event
                self._refresh_event = None
            assert released is not None
            released.set()
            return fresh.token

    def invalidate(self) -> None:
        """Clear the cached token so the next :meth:`get_token` re-invokes the provider.

        Also sets a one-shot ``force_refresh`` flag so on-disk providers skip
        their freshness short-circuit instead of re-serving the revoked token.
        """
        with self._lock:
            self._cached = None
            self._next_force = True
