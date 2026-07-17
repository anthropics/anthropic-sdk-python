from __future__ import annotations

import httpx
import pytest

from anthropic import Anthropic, AsyncAnthropic

httpx2 = pytest.importorskip("httpx2")

base_url = "http://127.0.0.1:4010"
api_key = "my-anthropic-api-key"


def test_accepts_httpx2_sync_client() -> None:
    with httpx2.Client() as http_client:
        client = Anthropic(
            base_url=base_url,
            api_key=api_key,
            _strict_response_validation=True,
            http_client=http_client,
        )
        assert isinstance(client._client, httpx2.Client)


async def test_accepts_httpx2_async_client() -> None:
    async with httpx2.AsyncClient() as http_client:
        client = AsyncAnthropic(
            base_url=base_url,
            api_key=api_key,
            _strict_response_validation=True,
            http_client=http_client,
        )
        assert isinstance(client._client, httpx2.AsyncClient)


def test_httpx2_sync_round_trip() -> None:
    def handler(_request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(200, json={"ok": True})

    with httpx2.Client(transport=httpx2.MockTransport(handler)) as http_client:
        with Anthropic(
            base_url=base_url,
            api_key=api_key,
            _strict_response_validation=True,
            http_client=http_client,
        ) as client:
            response = client.get("/foo", cast_to=httpx.Response)
            assert response.status_code == 200


async def test_httpx2_async_round_trip() -> None:
    def handler(_request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(200, json={"ok": True})

    async with httpx2.AsyncClient(transport=httpx2.MockTransport(handler)) as http_client:
        async with AsyncAnthropic(
            base_url=base_url,
            api_key=api_key,
            _strict_response_validation=True,
            http_client=http_client,
        ) as client:
            response = await client.get("/foo", cast_to=httpx.Response)
            assert response.status_code == 200
