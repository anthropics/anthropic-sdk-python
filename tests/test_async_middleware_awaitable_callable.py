from __future__ import annotations

from typing import Any, Awaitable

import anyio
import httpx
import pytest

from anthropic import AsyncAnthropic
from anthropic._middleware import AsyncCallNext
from anthropic._request import APIRequest


def test_async_client_accepts_sync_wrapper_returning_awaitable() -> None:
    seen: list[str] = []

    def middleware(request: APIRequest, call_next: AsyncCallNext) -> Awaitable[Any]:
        seen.append(request.url)
        return call_next(request)

    async def run() -> None:
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"ok": True}, request=request)

        client = AsyncAnthropic(
            api_key="test",
            base_url="https://example.test",
            middleware=[middleware],
            http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        )
        try:
            result = await client.get("/probe", cast_to=object)
        finally:
            await client.close()

        assert result == {"ok": True}

    anyio.run(run)
    assert seen == ["/probe"]


def test_async_client_accepts_sync_callable_object_returning_awaitable() -> None:
    class MiddlewareWrapper:
        def __init__(self) -> None:
            self.calls = 0

        def __call__(self, request: APIRequest, call_next: AsyncCallNext) -> Awaitable[Any]:
            self.calls += 1
            return call_next(request)

    wrapper = MiddlewareWrapper()

    async def run() -> None:
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"ok": True}, request=request)

        client = AsyncAnthropic(
            api_key="test",
            base_url="https://example.test",
            middleware=[wrapper],
            http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        )
        try:
            assert await client.get("/probe", cast_to=object) == {"ok": True}
        finally:
            await client.close()

    anyio.run(run)
    assert wrapper.calls == 1


def test_async_client_still_rejects_non_callable_middleware() -> None:
    with pytest.raises(TypeError, match="is not callable"):
        AsyncAnthropic(api_key="test", middleware=[object()])  # type: ignore[list-item]
