from __future__ import annotations

import pytest

from anthropic._models import FinalRequestOptions
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

    def test_copy(self) -> None:
        """Test copy() carries over the client configuration."""

        def token_provider() -> str:
            return "test-token"

        client = AnthropicFoundry(
            azure_ad_token_provider=token_provider,
            resource="example-resource",
            default_headers={"x-app": "1"},
            max_retries=5,
        )

        copied = client.copy()
        assert str(copied.base_url) == str(client.base_url)
        assert copied._azure_ad_token_provider is token_provider
        assert copied.default_headers.get("x-app") == "1"
        assert copied.max_retries == 5
        assert copied._client is client._client

    def test_with_options_overrides(self) -> None:
        """Test with_options() applies overrides while keeping everything else."""
        client = AnthropicFoundry(
            api_key="test-key",
            resource="example-resource",
            default_headers={"x-app": "1"},
        )

        derived = client.with_options(timeout=10, default_headers={"x-extra": "2"})
        assert derived.timeout == 10
        assert derived.api_key == "test-key"
        assert str(derived.base_url) == str(client.base_url)
        assert derived.default_headers.get("x-app") == "1"
        assert derived.default_headers.get("x-extra") == "2"

    def test_copy_x_stainless_helper_header_appends(self) -> None:
        """x-stainless-helper accumulates across copies instead of being clobbered."""
        client = AnthropicFoundry(
            api_key="test-key",
            resource="example-resource",
            default_headers={"x-stainless-helper": "parent"},
        )

        copied = client.with_options(default_headers={"x-stainless-helper": "child"})
        assert copied.default_headers.get("x-stainless-helper") == "parent, child"


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

    def test_copy(self) -> None:
        """Test copy() carries over the client configuration."""

        async def async_token_provider() -> str:
            return "async-test-token"

        client = AsyncAnthropicFoundry(
            azure_ad_token_provider=async_token_provider,
            resource="example-resource",
            max_retries=5,
        )

        copied = client.with_options(timeout=10)
        assert str(copied.base_url) == str(client.base_url)
        assert copied._azure_ad_token_provider is async_token_provider
        assert copied.max_retries == 5
        assert copied.timeout == 10

    def test_copy_x_stainless_helper_header_appends(self) -> None:
        """x-stainless-helper accumulates across copies instead of being clobbered."""
        client = AsyncAnthropicFoundry(
            api_key="test-key",
            resource="example-resource",
            default_headers={"x-stainless-helper": "parent"},
        )

        copied = client.with_options(default_headers={"x-stainless-helper": "child"})
        assert copied.default_headers.get("x-stainless-helper") == "parent, child"


class TestFoundryDoesNotLeakAnthropicAPIKey:
    """A stray ANTHROPIC_API_KEY in the environment must never be sent to the
    Foundry endpoint as X-Api-Key, regardless of which auth mode is in use."""

    def test_no_x_api_key_with_azure_ad_token_provider(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-should-not-leak")
        client = AnthropicFoundry(resource="example-resource", azure_ad_token_provider=lambda: "azure-token")

        options = client._prepare_options(FinalRequestOptions(method="post", url="/v1/messages"))
        headers = client._build_request(options).headers

        assert headers.get("x-api-key") is None
        assert headers.get("authorization") == "Bearer azure-token"

    def test_api_key_mode_sends_foundry_key_as_x_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-should-not-leak")
        client = AnthropicFoundry(api_key="foundry-key", resource="example-resource")

        options = client._prepare_options(FinalRequestOptions(method="post", url="/v1/messages"))
        headers = client._build_request(options).headers

        assert headers.get("x-api-key") == "foundry-key"
        assert headers.get("api-key") == "foundry-key"
        assert "sk-ant-should-not-leak" not in headers.values()

    @pytest.mark.asyncio
    async def test_async_no_x_api_key_with_azure_ad_token_provider(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-should-not-leak")

        async def token_provider() -> str:
            return "azure-token"

        client = AsyncAnthropicFoundry(resource="example-resource", azure_ad_token_provider=token_provider)

        options = await client._prepare_options(FinalRequestOptions(method="post", url="/v1/messages"))
        headers = client._build_request(options).headers

        assert headers.get("x-api-key") is None
        assert headers.get("authorization") == "Bearer azure-token"

    @pytest.mark.asyncio
    async def test_async_api_key_mode_sends_foundry_key_as_x_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-should-not-leak")
        client = AsyncAnthropicFoundry(api_key="foundry-key", resource="example-resource")

        options = await client._prepare_options(FinalRequestOptions(method="post", url="/v1/messages"))
        headers = client._build_request(options).headers

        assert headers.get("x-api-key") == "foundry-key"
        assert headers.get("api-key") == "foundry-key"
        assert "sk-ant-should-not-leak" not in headers.values()
