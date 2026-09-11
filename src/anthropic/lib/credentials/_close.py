from __future__ import annotations

import inspect
from typing import Protocol
from typing_extensions import runtime_checkable

from ._types import unwrap_partial

__all__ = ["close_credentials", "async_close_credentials", "has_async_close"]


@runtime_checkable
class SupportsClose(Protocol):
    def close(self) -> object: ...


@runtime_checkable
class SupportsAsyncClose(Protocol):
    def aclose(self) -> object: ...


# `credentials` is typed `object` in all three: `close()` / `aclose()` are not part of
# the provider protocols, so the checks below are the only thing that knows they are there.
# A functools.partial hides the provider's own hooks, so each looks at the object it wraps.


def has_async_close(credentials: object) -> bool:
    """True if the provider's `close()` is `async def`, which only `AsyncAnthropic` can await."""
    provider = unwrap_partial(credentials)
    return isinstance(provider, SupportsClose) and inspect.iscoroutinefunction(provider.close)


def close_credentials(credentials: object) -> None:
    """Release any resources owned by a credential provider, if it exposes `close()`."""
    provider = unwrap_partial(credentials)
    if isinstance(provider, SupportsClose):
        provider.close()


async def async_close_credentials(credentials: object) -> None:
    """Async `close_credentials`: awaits the provider's `aclose()` if it has one, else calls `close()`."""
    provider = unwrap_partial(credentials)
    if isinstance(provider, SupportsAsyncClose):
        closing = provider.aclose()
    elif isinstance(provider, SupportsClose):
        closing = provider.close()
    else:
        return
    # Awaited only if there is something to await. close() may itself be `async def`, as on
    # aiohttp-style clients; aclose() may be a plain method, and a `Mock` provider has both hooks
    # and returns another `Mock` from each. Closing a client should not fail on any of them.
    if inspect.isawaitable(closing):
        await closing
