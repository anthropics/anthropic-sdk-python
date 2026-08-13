from __future__ import annotations

import threading

import httpx
import pytest

from anthropic import AnthropicBedrockMantle, AsyncAnthropicBedrockMantle

MANTLE_MESSAGES_URL = "https://bedrock-mantle.us-east-1.api.aws/anthropic/v1/messages"


class GetAuthHeadersRecorder:
    """Stands in for `anthropic.lib.bedrock._mantle.get_auth_headers` and records each call's kwargs."""

    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def __call__(self, **kwargs: object) -> dict[str, str]:
        self.calls.append(kwargs)
        return {"Authorization": "AWS4-HMAC-SHA256 ...", "X-Amz-Date": "20260327T000000Z"}


@pytest.fixture
def get_auth_headers_recorder(monkeypatch: pytest.MonkeyPatch) -> GetAuthHeadersRecorder:
    recorder = GetAuthHeadersRecorder()
    monkeypatch.setattr("anthropic.lib.bedrock._mantle.get_auth_headers", recorder)
    return recorder


class TestBaseURL:
    def test_derives_base_url_from_region(self) -> None:
        client = AnthropicBedrockMantle(
            api_key="test-key",
            aws_region="us-east-1",
        )
        assert str(client.base_url).startswith("https://bedrock-mantle.us-east-1.api.aws/anthropic")

    def test_different_region(self) -> None:
        client = AnthropicBedrockMantle(
            api_key="test-key",
            aws_region="us-west-2",
        )
        assert str(client.base_url).startswith("https://bedrock-mantle.us-west-2.api.aws/anthropic")

    def test_uses_base_url_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_BEDROCK_MANTLE_BASE_URL", "https://custom.example.com")
        client = AnthropicBedrockMantle(
            api_key="test-key",
        )
        assert str(client.base_url).startswith("https://custom.example.com")

    def test_base_url_arg_takes_precedence_over_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_BEDROCK_MANTLE_BASE_URL", "https://from-env.example.com")
        client = AnthropicBedrockMantle(
            api_key="test-key",
            base_url="https://from-arg.example.com",
        )
        assert str(client.base_url).startswith("https://from-arg.example.com")

    def test_raises_without_region_or_base_url(self) -> None:
        with pytest.raises(Exception, match="No AWS region or base URL found"):
            AnthropicBedrockMantle(
                api_key="test-key",
            )


class TestSigV4ServiceName:
    def test_uses_bedrock_mantle_service_name(self, get_auth_headers_recorder: GetAuthHeadersRecorder) -> None:
        client = AnthropicBedrockMantle(
            aws_access_key="AKID",
            aws_secret_key="secret",
            aws_region="us-east-1",
        )

        request = httpx.Request(
            "POST",
            MANTLE_MESSAGES_URL,
            headers={"content-type": "application/json"},
            content=b'{"model": "claude-sonnet-4-20250514"}',
        )
        client._prepare_request(request)

        assert len(get_auth_headers_recorder.calls) == 1
        assert get_auth_headers_recorder.calls[0]["service_name"] == "bedrock-mantle"
        assert request.headers["Authorization"] == "AWS4-HMAC-SHA256 ..."


class TestEnvironmentVariables:
    def test_uses_mantle_api_key_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AWS_BEARER_TOKEN_BEDROCK", "mantle-key")
        client = AnthropicBedrockMantle(
            base_url="https://example.com",
        )
        assert client.api_key == "mantle-key"

    def test_falls_back_to_aws_api_key_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ANTHROPIC_AWS_API_KEY", "aws-key")
        client = AnthropicBedrockMantle(
            base_url="https://example.com",
        )
        assert client.api_key == "aws-key"

    def test_mantle_api_key_takes_precedence_over_aws(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AWS_BEARER_TOKEN_BEDROCK", "mantle-key")
        monkeypatch.setenv("ANTHROPIC_AWS_API_KEY", "aws-key")
        client = AnthropicBedrockMantle(
            base_url="https://example.com",
        )
        assert client.api_key == "mantle-key"

    def test_region_from_aws_region_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("AWS_REGION", "eu-west-1")
        client = AnthropicBedrockMantle(
            api_key="test-key",
        )
        assert client.aws_region == "eu-west-1"
        assert client.base_url == "https://bedrock-mantle.eu-west-1.api.aws/anthropic/"

    def test_region_from_aws_default_region_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("AWS_REGION", raising=False)
        monkeypatch.setenv("AWS_DEFAULT_REGION", "ap-southeast-1")
        client = AnthropicBedrockMantle(
            api_key="test-key",
        )
        assert client.aws_region == "ap-southeast-1"


class TestEndpointRestrictions:
    def _make_client(self) -> AnthropicBedrockMantle:
        return AnthropicBedrockMantle(
            api_key="test-key",
            base_url="https://example.com",
        )

    def test_completions_not_available(self) -> None:
        client = self._make_client()
        assert not hasattr(client, "completions")

    def test_models_not_available(self) -> None:
        client = self._make_client()
        assert not hasattr(client, "models")

    def test_messages_available(self) -> None:
        client = self._make_client()
        assert client.messages is not None

    def test_beta_messages_available(self) -> None:
        client = self._make_client()
        assert client.beta.messages is not None

    def test_beta_models_not_available(self) -> None:
        client = self._make_client()
        assert not hasattr(client.beta, "models")

    def test_beta_files_not_available(self) -> None:
        client = self._make_client()
        assert not hasattr(client.beta, "files")

    def test_beta_skills_not_available(self) -> None:
        client = self._make_client()
        assert not hasattr(client.beta, "skills")


class TestAuthPrecedence:
    def test_api_key_arg_uses_api_key_mode(self) -> None:
        client = AnthropicBedrockMantle(
            api_key="my-key",
            aws_region="us-east-1",
        )
        assert client._use_sigv4 is False
        assert client.api_key == "my-key"

    def test_aws_creds_use_sigv4_mode(self) -> None:
        client = AnthropicBedrockMantle(
            aws_access_key="AKID",
            aws_secret_key="secret",
            aws_region="us-east-1",
        )
        assert client._use_sigv4 is True
        assert client.api_key is None

    def test_api_key_mode_returns_bearer_auth_header(self) -> None:
        client = AnthropicBedrockMantle(
            api_key="my-key",
            aws_region="us-east-1",
        )
        assert client.auth_headers == {"Authorization": "Bearer my-key"}

    def test_sigv4_mode_returns_empty_auth_headers(self) -> None:
        client = AnthropicBedrockMantle(
            aws_access_key="AKID",
            aws_secret_key="secret",
            aws_region="us-east-1",
        )
        assert client.auth_headers == {}

    def test_skip_auth_returns_empty_auth_headers(self) -> None:
        client = AnthropicBedrockMantle(
            skip_auth=True,
            base_url="https://example.com",
        )
        assert client.auth_headers == {}


class TestSkipAuth:
    def test_skip_auth_does_not_sign_request(self, get_auth_headers_recorder: GetAuthHeadersRecorder) -> None:
        client = AnthropicBedrockMantle(
            skip_auth=True,
            base_url="https://example.com",
        )

        request = httpx.Request("POST", "https://example.com/v1/messages", content=b"{}")
        client._prepare_request(request)

        assert get_auth_headers_recorder.calls == []
        assert "Authorization" not in request.headers


class TestPartialCredentials:
    def test_access_key_only_raises(self) -> None:
        with pytest.raises(ValueError, match="aws_access_key.*without.*aws_secret_key"):
            AnthropicBedrockMantle(
                aws_access_key="AKID",
                aws_region="us-east-1",
            )

    def test_secret_key_only_raises(self) -> None:
        with pytest.raises(ValueError, match="aws_secret_key.*without.*aws_access_key"):
            AnthropicBedrockMantle(
                aws_secret_key="secret",
                aws_region="us-east-1",
            )


class TestAsyncClient:
    def test_async_client_has_same_restrictions(self) -> None:
        client = AsyncAnthropicBedrockMantle(
            api_key="test-key",
            base_url="https://example.com",
        )
        assert not hasattr(client, "completions")
        assert not hasattr(client, "models")
        assert client.messages is not None
        assert client.beta.messages is not None
        assert not hasattr(client.beta, "models")
        assert not hasattr(client.beta, "files")
        assert not hasattr(client.beta, "skills")

    def test_async_base_url_from_region(self) -> None:
        client = AsyncAnthropicBedrockMantle(
            api_key="test-key",
            aws_region="us-east-1",
        )
        assert client.base_url == "https://bedrock-mantle.us-east-1.api.aws/anthropic/"

    @pytest.mark.asyncio()
    async def test_sigv4_signing_runs_off_event_loop(self, monkeypatch: pytest.MonkeyPatch) -> None:
        client = AsyncAnthropicBedrockMantle(
            aws_access_key="AKID",
            aws_secret_key="secret",
            aws_region="us-east-1",
        )
        signing_threads: list[int] = []

        def fake_get_auth_headers(**_: object) -> dict[str, str]:
            signing_threads.append(threading.get_ident())
            return {"Authorization": "AWS4-HMAC-SHA256 stub"}

        monkeypatch.setattr("anthropic.lib.bedrock._mantle.get_auth_headers", fake_get_auth_headers)

        request = httpx.Request("POST", "https://bedrock-mantle.us-east-1.api.aws/anthropic/v1/messages", content=b"{}")
        await client._prepare_request(request)

        assert len(signing_threads) == 1
        assert signing_threads[0] != threading.get_ident()
        assert request.headers["Authorization"] == "AWS4-HMAC-SHA256 stub"


class TestCopy:
    def test_copy_preserves_config(self) -> None:
        client = AnthropicBedrockMantle(
            api_key="test-key",
            aws_region="us-east-1",
        )
        copied = client.copy()
        assert copied.base_url == client.base_url
        assert copied.aws_region == client.aws_region

    def test_copy_overrides_region(self) -> None:
        client = AnthropicBedrockMantle(
            api_key="test-key",
            aws_region="us-east-1",
        )
        copied = client.copy(aws_region="us-west-2")
        assert copied.aws_region == "us-west-2"

    def test_copy_x_stainless_helper_header_appends(self) -> None:
        # `x-stainless-helper` accumulates across copies instead of being clobbered
        client = AnthropicBedrockMantle(
            api_key="test-key",
            aws_region="us-east-1",
            default_headers={"x-stainless-helper": "parent"},
        )
        copied = client.copy(default_headers={"x-stainless-helper": "child"})
        assert copied.default_headers["x-stainless-helper"] == "parent, child"

    def test_async_copy_x_stainless_helper_header_appends(self) -> None:
        # `x-stainless-helper` accumulates across copies instead of being clobbered
        client = AsyncAnthropicBedrockMantle(
            api_key="test-key",
            aws_region="us-east-1",
            default_headers={"x-stainless-helper": "parent"},
        )
        copied = client.copy(default_headers={"x-stainless-helper": "child"})
        assert copied.default_headers["x-stainless-helper"] == "parent, child"
