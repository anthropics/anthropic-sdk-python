from __future__ import annotations

import inspect
import functools
from typing import Dict, Callable, Optional, Protocol
from dataclasses import field, dataclass
from typing_extensions import TypeIs, override, runtime_checkable


def _empty_headers() -> Dict[str, str]:
    return {}


__all__ = [
    "AccessToken",
    "AccessTokenProvider",
    "AsyncAccessTokenProvider",
    "BaseURLBoundProvider",
    "IdentityTokenProvider",
    "CredentialResult",
]


@dataclass(frozen=True)
class AccessToken:
    """An Anthropic API access token with optional expiry.

    `expires_at` is unix seconds; `None` means no expiry information
    (the token will be treated as never-expires by `TokenCache`).
    Exactly `0` means the provider does its own caching, so the client asks it
    again before every request, concurrently if requests are concurrent. Any
    other past value is an expired token and is refreshed one call at a time.

    `repr()` masks the token (at most its last four characters) so a frame
    or log line holding an `AccessToken` never exposes the raw value —
    crash reporters that capture traceback locals render their `repr`.
    """

    token: str
    expires_at: Optional[int] = None

    @override
    def __repr__(self) -> str:
        # str() first: a malformed token endpoint can hand us a non-str token
        # and a repr must never raise (crash reporters call it blindly).
        token = str(self.token)
        masked = f"...{token[-4:]}" if len(token) >= 12 else "**********"
        return f"AccessToken(token='{masked}', expires_at={self.expires_at!r})"


class AccessTokenProvider(Protocol):
    """Callable that mints or returns a cached access token.

    Re-invoking the provider IS the refresh mechanism — providers have no
    separate `refresh()` method. Providers may be stateful (hold config /
    paths) but the *cache* lives in `TokenCache`, not here.

    The optional `force_refresh` flag is set by
    `TokenCache.invalidate` after a 401: providers with on-disk caches
    (user_oauth, oidc_federation) must bypass their freshness short-circuit
    and always fetch fresh when it is True. Providers without a cache can
    accept and ignore the flag.
    """

    def __call__(self, *, force_refresh: bool = False) -> AccessToken: ...


class AsyncAccessTokenProvider(Protocol):
    """Async twin of `AccessTokenProvider`, with the same `force_refresh` contract.

    It must be an `async def` function, or an object whose `__call__` is one;
    `AsyncAnthropic` awaits it on the event loop and caches the result like a
    sync provider's.
    """

    async def __call__(self, *, force_refresh: bool = False) -> AccessToken: ...


def unwrap_partial(obj: object) -> object:
    while isinstance(obj, functools.partial):
        obj = obj.func
    return obj


def is_async_token_provider(provider: object) -> TypeIs[AsyncAccessTokenProvider]:
    """True for an `async def` function, an object whose `__call__` is one, or a `functools.partial` of either."""
    # iscoroutinefunction looks through a partial of a function but not of a callable object.
    provider = unwrap_partial(provider)
    return inspect.iscoroutinefunction(provider) or inspect.iscoroutinefunction(getattr(provider, "__call__", None))  # noqa: B004


@runtime_checkable
class BaseURLBoundProvider(AccessTokenProvider, Protocol):
    """A provider whose token exchange targets a specific deployment.

    The client calls `for_base_url` with its own `base_url` at
    construction. Providers that don't implement this resolve their own
    exchange endpoint and are used as-is.
    """

    def for_base_url(self, base_url: str) -> AccessTokenProvider:
        """Return the provider a client with `base_url` should exchange through.

        Either `self`, bound to `base_url`, or — if another client already
        bound `self` to a different deployment — a separate provider bound to
        `base_url`, so that client's binding is left alone.
        """
        ...


# Innermost layer: returns the raw external JWT string (used as the
# `identity_token_provider` argument to `WorkloadIdentityCredentials`).
IdentityTokenProvider = Callable[[], str]


@dataclass(frozen=True)
class CredentialResult:
    """Bundles an `AccessTokenProvider` with config-level metadata.

    Returned by `default_credentials`. The `extra_headers` dict
    carries headers that should be set on every API request (e.g.
    `anthropic-workspace-id`). The client merges these into its default
    headers at construction time.

    `base_url` is the API host the resolved profile is configured for
    (e.g. a staging endpoint). The client adopts it as its request
    `base_url` *only* when the user did not supply one explicitly via
    the `base_url=` kwarg or `ANTHROPIC_BASE_URL` — see the
    constructor in `_client.py`. `None` means the profile did not
    specify a host and the client keeps its own default.
    """

    provider: AccessTokenProvider
    extra_headers: Dict[str, str] = field(default_factory=_empty_headers)
    base_url: Optional[str] = None
