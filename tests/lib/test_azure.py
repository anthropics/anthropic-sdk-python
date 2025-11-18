from __future__ import annotations

import pytest

from anthropic._exceptions import AnthropicError
from anthropic.lib.foundry import AnthropicFoundry, AsyncAnthropicFoundry


class TestAnthropicFoundry:
    def test_basic_initialization_with_api_key(self) -> None:
        """Test basic client initialization with API key."""
        client = AnthropicFoundry(
            api_key="test-key",
            resource="example-resource",
        )

        assert client.api_key == "test-key"
        assert str(client.base_url) == "https://example-resource.services.ai.azure.com/anthropic/"

    def test_initialization_with_base_url(self) -> None:
        """Test client initialization with base_url instead of resource."""
        client = AnthropicFoundry(
            api_key="test-key",
            base_url="https://example.services.ai.azure.com/anthropic/",
        )

        assert str(client.base_url) == "https://example.services.ai.azure.com/anthropic/"

    def test_initialization_with_azure_ad_token_provider(self) -> None:
        """Test client initialization with Azure AD token provider."""

        def token_provider() -> str:
            return "test-token"

        client = AnthropicFoundry(
            azure_ad_token_provider=token_provider,
            resource="example-resource",
        )

        assert client._azure_ad_token_provider is not None
        assert client._get_azure_ad_token() == "test-token"

    def test_initialization_from_environment_variables(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test client initialization falls back to environment variables."""
        monkeypatch.setenv("ANTHROPIC_FOUNDRY_API_KEY", "env-key")
        monkeypatch.setenv("ANTHROPIC_API_VERSION", "2023-06-01")
        monkeypatch.setenv("ANTHROPIC_FOUNDRY_RESOURCE", "env-resource")

        client = AnthropicFoundry()

        assert client.api_key == "env-key"
        assert "env-resource.services.ai.azure.com" in str(client.base_url)

    def test_missing_credentials_error(self) -> None:
        """Test error raised when no credentials are provided."""
        with pytest.raises(AnthropicError, match="Missing credentials"):
            AnthropicFoundry(
                resource="example-resource",
            )

    def test_missing_resource_error(self) -> None:
        """Test error raised when neither resource nor base_url is provided."""
        with pytest.raises(ValueError, match="base_url.*resource"):
            AnthropicFoundry(
                api_key="test-key",
            )


class TestAsyncAnthropicFoundry:
    @pytest.mark.asyncio
    async def test_basic_initialization_with_api_key(self) -> None:
        """Test basic async client initialization with API key."""
        client = AsyncAnthropicFoundry(
            api_key="test-key",
            resource="example-resource",
        )

        assert client.api_key == "test-key"
        assert str(client.base_url) == "https://example-resource.services.ai.azure.com/anthropic/"

    @pytest.mark.asyncio
    async def test_async_azure_ad_token_provider(self) -> None:
        """Test async client with async Azure AD token provider."""

        async def async_token_provider() -> str:
            return "async-test-token"

        client = AsyncAnthropicFoundry(
            azure_ad_token_provider=async_token_provider,
            resource="example-resource",
        )

        token = await client._get_azure_ad_token()
        assert token == "async-test-token"

    @pytest.mark.asyncio
    async def test_initialization_from_environment_variables(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test async client initialization falls back to environment variables."""
        monkeypatch.setenv("ANTHROPIC_FOUNDRY_API_KEY", "env-key")
        monkeypatch.setenv("ANTHROPIC_API_VERSION", "2023-06-01")
        monkeypatch.setenv("ANTHROPIC_FOUNDRY_RESOURCE", "env-resource")

        client = AsyncAnthropicFoundry()

        assert client.api_key == "env-key"
        assert "env-resource.services.ai.azure.com" in str(client.base_url)
