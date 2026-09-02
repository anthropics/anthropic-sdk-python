from __future__ import annotations

import pytest

from anthropic._models import FinalRequestOptions
from anthropic.lib.foundry import AnthropicFoundry, AsyncAnthropicFoundry, MutuallyExclusiveAuthError


BASE_URL = "https://foundry.example.test/anthropic/"


def _options() -> FinalRequestOptions:
    return FinalRequestOptions.construct(method="post", url="v1/messages", headers={})


def _azure_token() -> str:
    return "azure-token"


def test_sync_copy_api_key_replaces_inherited_azure_ad_provider() -> None:
    client = AnthropicFoundry(base_url=BASE_URL, azure_ad_token_provider=_azure_token)
    clone = client.copy(api_key="foundry-key")
    try:
        assert clone.api_key == "foundry-key"
        assert clone._azure_ad_token_provider is None

        options = clone._prepare_options(_options())
        assert options.headers["x-api-key"] == "foundry-key"
        assert options.headers["api-key"] == "foundry-key"
        assert "Authorization" not in options.headers
    finally:
        clone.close()
        client.close()


def test_sync_copy_azure_ad_provider_replaces_inherited_api_key() -> None:
    client = AnthropicFoundry(base_url=BASE_URL, api_key="foundry-key")
    clone = client.copy(azure_ad_token_provider=_azure_token)
    try:
        assert clone.api_key is None
        assert clone._azure_ad_token_provider is _azure_token

        options = clone._prepare_options(_options())
        assert options.headers["Authorization"] == "Bearer azure-token"
        assert "x-api-key" not in options.headers
        assert "api-key" not in options.headers
    finally:
        clone.close()
        client.close()


def test_sync_rejects_two_explicit_auth_methods() -> None:
    with pytest.raises(MutuallyExclusiveAuthError):
        AnthropicFoundry(
            base_url=BASE_URL,
            api_key="foundry-key",
            azure_ad_token_provider=_azure_token,
        )


def test_azure_ad_auth_ignores_first_party_api_key_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "first-party-key")
    client = AnthropicFoundry(base_url=BASE_URL, azure_ad_token_provider=_azure_token)
    try:
        assert client.api_key is None
        assert client.auth_token is None
    finally:
        client.close()


@pytest.mark.asyncio()
async def test_async_copy_api_key_replaces_inherited_azure_ad_provider() -> None:
    async def provider() -> str:
        return "azure-token"

    client = AsyncAnthropicFoundry(base_url=BASE_URL, azure_ad_token_provider=provider)
    clone = client.copy(api_key="foundry-key")
    try:
        assert clone.api_key == "foundry-key"
        assert clone._azure_ad_token_provider is None

        options = await clone._prepare_options(_options())
        assert options.headers["x-api-key"] == "foundry-key"
        assert options.headers["api-key"] == "foundry-key"
        assert "Authorization" not in options.headers
    finally:
        await clone.close()
        await client.close()


@pytest.mark.asyncio()
async def test_async_copy_azure_ad_provider_replaces_inherited_api_key() -> None:
    async def provider() -> str:
        return "azure-token"

    client = AsyncAnthropicFoundry(base_url=BASE_URL, api_key="foundry-key")
    clone = client.copy(azure_ad_token_provider=provider)
    try:
        assert clone.api_key is None
        assert clone._azure_ad_token_provider is provider

        options = await clone._prepare_options(_options())
        assert options.headers["Authorization"] == "Bearer azure-token"
        assert "x-api-key" not in options.headers
        assert "api-key" not in options.headers
    finally:
        await clone.close()
        await client.close()
