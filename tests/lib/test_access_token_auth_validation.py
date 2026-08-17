from __future__ import annotations

from typing import Any, cast

import httpx
import pytest

from anthropic import AnthropicError
from anthropic.lib.credentials._auth import AccessTokenAuth
from anthropic.lib.credentials._cache import TokenCache


class _TokenCacheStub:
    def __init__(self, token: Any) -> None:
        self.token = token
        self.calls = 0

    def get_token(self) -> str:
        self.calls += 1
        return cast(str, self.token)


def _auth(token: Any) -> tuple[AccessTokenAuth, _TokenCacheStub]:
    cache = _TokenCacheStub(token)
    return AccessTokenAuth(cast(TokenCache, cache)), cache


@pytest.mark.parametrize("token", ["", " token", "token ", "\ttoken"])
def test_sync_auth_rejects_invalid_provider_tokens(token: str) -> None:
    auth, cache = _auth(token)
    request = httpx.Request("GET", "https://api.anthropic.com/v1/models")

    with pytest.raises(AnthropicError, match="invalid access token"):
        list(auth.sync_auth_flow(request))

    assert cache.calls == 1
    assert "Authorization" not in request.headers


@pytest.mark.asyncio
@pytest.mark.parametrize("token", ["", " token", "token ", "\ttoken"])
async def test_async_auth_rejects_invalid_provider_tokens(token: str) -> None:
    auth, cache = _auth(token)
    request = httpx.Request("GET", "https://api.anthropic.com/v1/models")

    with pytest.raises(AnthropicError, match="invalid access token"):
        [item async for item in auth.async_auth_flow(request)]

    assert cache.calls == 1
    assert "Authorization" not in request.headers


def test_valid_provider_token_is_applied() -> None:
    auth, cache = _auth("access-token")
    request = httpx.Request("GET", "https://api.anthropic.com/v1/models")

    yielded = list(auth.sync_auth_flow(request))

    assert yielded == [request]
    assert cache.calls == 1
    assert request.headers["Authorization"] == "Bearer access-token"
    assert "oauth-2025-04-20" in request.headers["anthropic-beta"]


def test_static_authorization_still_bypasses_provider_validation() -> None:
    auth, cache = _auth("")
    request = httpx.Request(
        "GET",
        "https://api.anthropic.com/v1/models",
        headers={"Authorization": "Bearer explicit-token"},
    )

    yielded = list(auth.sync_auth_flow(request))

    assert yielded == [request]
    assert cache.calls == 0
    assert request.headers["Authorization"] == "Bearer explicit-token"
