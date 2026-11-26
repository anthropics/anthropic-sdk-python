
import asyncio

import httpx2

from anthropic.lib.credentials._auth import BearerTokenAuth, AsyncBearerTokenAuth


def test_bearer_token_auth_adds_authorization_header() -> None:
    auth = BearerTokenAuth(lambda: "test-token")
    request = httpx2.Request("GET", "https://example.com")

    result = list(auth.sync_auth_flow(request))

    assert result[0].headers["Authorization"] == "Bearer test-token"
    assert "anthropic-beta" not in result[0].headers


def test_bearer_token_auth_preserves_existing_authorization() -> None:
    auth = BearerTokenAuth(lambda: "new-token")
    request = httpx2.Request(
        "GET",
        "https://example.com",
        headers={"Authorization": "Bearer existing-token"},
    )

    result = list(auth.sync_auth_flow(request))

    assert result[0].headers["Authorization"] == "Bearer existing-token"


def test_bearer_token_auth_preserves_api_key() -> None:
    auth = BearerTokenAuth(lambda: "new-token")
    request = httpx2.Request(
        "GET",
        "https://example.com",
        headers={"X-Api-Key": "existing-key"},
    )

    result = list(auth.sync_auth_flow(request))

    assert result[0].headers["X-Api-Key"] == "existing-key"
    assert "Authorization" not in result[0].headers


def test_async_bearer_token_auth_adds_authorization_header() -> None:
    async def get_token() -> str:
        return "async-test-token"

    async def run() -> httpx2.Request:
        auth = AsyncBearerTokenAuth(get_token)
        request = httpx2.Request("GET", "https://example.com")

        async for result in auth.async_auth_flow(request):
            return result

        raise AssertionError("Authentication flow did not yield a request")

    result = asyncio.run(run())

    assert result.headers["Authorization"] == "Bearer async-test-token"
    assert "anthropic-beta" not in result.headers


def test_async_bearer_token_auth_preserves_existing_authorization() -> None:
    async def get_token() -> str:
        return "new-token"

    async def run() -> httpx2.Request:
        auth = AsyncBearerTokenAuth(get_token)
        request = httpx2.Request(
            "GET",
            "https://example.com",
            headers={"Authorization": "Bearer existing-token"},
        )

        async for result in auth.async_auth_flow(request):
            return result

        raise AssertionError("Authentication flow did not yield a request")

    result = asyncio.run(run())

    assert result.headers["Authorization"] == "Bearer existing-token"
