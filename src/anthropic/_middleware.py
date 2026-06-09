from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, Union, Callable, Iterable, Awaitable
from typing_extensions import TypeAlias

from ._request import APIRequest

if TYPE_CHECKING:
    from ._response import APIResponse, AsyncAPIResponse

__all__ = [
    "Middleware",
    "CallNext",
    "AsyncCallNext",
    "MiddlewareCallable",
    "AsyncMiddlewareCallable",
    "MiddlewareInput",
]

CallNext: TypeAlias = Callable[[APIRequest], "APIResponse[Any]"]
"""Invokes the rest of the middleware chain and, ultimately, a single HTTP attempt.

The middleware chain runs inside the SDK's retry loop, once per attempt, and
returns the `APIResponse` for every HTTP response, including 4xx/5xx — inspect
`response.status_code` to react to API errors; the SDK raises its typed errors
for the original caller after the chain. Connection failures have no response to
return, so they raise (`APITimeoutError`, `APIConnectionError`).

Returns the `APIResponse` wrapper; call `.parse()` on it to get the typed model.
"""

AsyncCallNext: TypeAlias = Callable[[APIRequest], Awaitable["AsyncAPIResponse[Any]"]]
"""Invokes the rest of the middleware chain and, ultimately, a single HTTP attempt.

The middleware chain runs inside the SDK's retry loop, once per attempt, and
returns the `AsyncAPIResponse` for every HTTP response, including 4xx/5xx — inspect
`response.status_code` to react to API errors; the SDK raises its typed errors
for the original caller after the chain. Connection failures have no response to
return, so they raise (`APITimeoutError`, `APIConnectionError`).

Returns the `AsyncAPIResponse` wrapper; call `await .parse()` on it to get the typed model.
"""


class Middleware:
    """Base class for client-level middleware.

    Subclass and override `handle` (used by the sync client) and/or `handle_async`
    (used by the async client). The default implementations delegate straight to
    the rest of the chain.
    """

    def handle(self, request: APIRequest, call_next: CallNext) -> APIResponse[Any]:
        return call_next(request)

    async def handle_async(self, request: APIRequest, call_next: AsyncCallNext) -> AsyncAPIResponse[Any]:
        return await call_next(request)


MiddlewareCallable: TypeAlias = Callable[[APIRequest, CallNext], "APIResponse[Any]"]
AsyncMiddlewareCallable: TypeAlias = Callable[[APIRequest, AsyncCallNext], Awaitable["AsyncAPIResponse[Any]"]]
MiddlewareInput: TypeAlias = Union[Middleware, MiddlewareCallable, AsyncMiddlewareCallable]


def _middleware_name(middleware: object) -> str:
    if isinstance(middleware, Middleware):
        return type(middleware).__name__
    name = getattr(middleware, "__name__", None)
    return name if isinstance(name, str) else repr(middleware)


def _is_async_callable(obj: object) -> bool:
    """Whether calling the given object returns a coroutine.

    Unlike `inspect.iscoroutinefunction(obj)` this also handles class instances
    that define an async `__call__` method.
    """
    if inspect.iscoroutinefunction(obj):
        return True
    call = getattr(obj, "__call__", None)  # noqa: B004
    return call is not None and inspect.iscoroutinefunction(call)


def validate_sync_middleware(middleware: Iterable[MiddlewareInput]) -> None:
    for entry in middleware:
        if isinstance(entry, Middleware):
            if type(entry).handle is Middleware.handle:
                raise TypeError(
                    f"middleware {_middleware_name(entry)} does not implement `handle()`; "
                    "the synchronous client requires sync-capable middleware"
                )
            if inspect.iscoroutinefunction(type(entry).handle):
                raise TypeError(
                    f"middleware {_middleware_name(entry)} defines `handle()` as an async function; "
                    "the synchronous client requires `handle()` to be a sync function"
                )
        elif not callable(entry):
            raise TypeError(f"middleware {_middleware_name(entry)} is not callable")
        elif _is_async_callable(entry):
            raise TypeError(
                f"middleware {_middleware_name(entry)} is an async function; "
                "the synchronous client requires sync middleware functions"
            )


def validate_async_middleware(middleware: Iterable[MiddlewareInput]) -> None:
    for entry in middleware:
        if isinstance(entry, Middleware):
            if type(entry).handle_async is Middleware.handle_async:
                raise TypeError(
                    f"middleware {_middleware_name(entry)} does not implement `handle_async()`; "
                    "the asynchronous client requires async-capable middleware"
                )
            if not inspect.iscoroutinefunction(type(entry).handle_async):
                raise TypeError(
                    f"middleware {_middleware_name(entry)} defines `handle_async()` as a sync function; "
                    "the asynchronous client requires `handle_async()` to be an async function"
                )
        elif not callable(entry):
            raise TypeError(f"middleware {_middleware_name(entry)} is not callable")
        elif not _is_async_callable(entry):
            raise TypeError(
                f"middleware {_middleware_name(entry)} is not an async function; "
                "the asynchronous client requires async middleware functions"
            )
