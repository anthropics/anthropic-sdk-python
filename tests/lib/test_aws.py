import re
from typing import cast
from typing_extensions import Protocol

import httpx
import pytest
from respx import MockRouter

from anthropic import AnthropicAWS, AsyncAnthropicAWS
from anthropic._exceptions import AnthropicError


class MockRequestCall(Protocol):
    request: httpx.Request


# --- Initialization ---


def test_init_api_key_mode() -> None:
    client = AnthropicAWS(api_key="test-key", aws_region="us-east-1", workspace_id="ws-123")
    assert client.api_key == "test-key"
    assert client._use_sigv4 is False


def test_init_sigv4_explicit_creds() -> None:
    client = AnthropicAWS(
        aws_access_key="AKID",
        aws_secret_key="secret",
        aws_region="us-west-2",
        workspace_id="ws-123",
    )
    assert client._use_sigv4 is True
    assert client.api_key is None
    assert client.aws_access_key == "AKID"
    assert client.aws_secret_key == "secret"


def test_init_sigv4_profile() -> None:
    client = AnthropicAWS(aws_profile="my-profile", aws_region="eu-west-1", workspace_id="ws-123")
    assert client._use_sigv4 is True
    assert client.aws_profile == "my-profile"


def test_init_sigv4_default_credential_chain() -> None:
    client = AnthropicAWS(aws_region="us-east-1", workspace_id="ws-123")
    assert client._use_sigv4 is True
    assert client.api_key is None


def test_init_requires_region_for_sigv4(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AWS_REGION", raising=False)
    with pytest.raises(AnthropicError, match="No AWS region was provided"):
        AnthropicAWS(aws_access_key="AKID", aws_secret_key="secret", workspace_id="ws-123")


def test_init_requires_workspace_id(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_AWS_WORKSPACE_ID", raising=False)
    with pytest.raises(AnthropicError, match="No workspace ID found"):
        AnthropicAWS(api_key="test-key", aws_region="us-east-1")


def test_init_workspace_id_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_AWS_WORKSPACE_ID", "env-workspace")
    client = AnthropicAWS(api_key="test-key", aws_region="us-east-1")
    assert client.workspace_id == "env-workspace"


def test_init_async_api_key_mode() -> None:
    client = AsyncAnthropicAWS(api_key="test-key", aws_region="us-east-1", workspace_id="ws-123")
    assert client.api_key == "test-key"
    assert client._use_sigv4 is False


def test_init_async_sigv4() -> None:
    client = AsyncAnthropicAWS(
        aws_access_key="AKID",
        aws_secret_key="secret",
        aws_region="us-west-2",
        workspace_id="ws-123",
    )
    assert client._use_sigv4 is True


def test_init_async_requires_workspace_id(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_AWS_WORKSPACE_ID", raising=False)
    with pytest.raises(AnthropicError, match="No workspace ID found"):
        AsyncAnthropicAWS(api_key="test-key", aws_region="us-east-1")


# --- Partial credential validation ---


def test_partial_creds_access_key_only() -> None:
    with pytest.raises(ValueError, match="aws_access_key.*without.*aws_secret_key"):
        AnthropicAWS(aws_access_key="AKID", aws_region="us-east-1", workspace_id="ws-123")


def test_partial_creds_secret_key_only() -> None:
    with pytest.raises(ValueError, match="aws_secret_key.*without.*aws_access_key"):
        AnthropicAWS(aws_secret_key="secret", aws_region="us-east-1", workspace_id="ws-123")


def test_partial_creds_async_access_key_only() -> None:
    with pytest.raises(ValueError, match="aws_access_key.*without.*aws_secret_key"):
        AsyncAnthropicAWS(aws_access_key="AKID", aws_region="us-east-1", workspace_id="ws-123")


# --- skipAuth ---


def test_skip_auth_no_workspace_required(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_AWS_WORKSPACE_ID", raising=False)
    client = AnthropicAWS(skip_auth=True, base_url="https://custom.example.com")
    assert client._skip_auth is True
    assert client._use_sigv4 is False
    assert client.workspace_id is None


def test_skip_auth_no_region_or_base_url_required(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AWS_REGION", raising=False)
    monkeypatch.delenv("ANTHROPIC_AWS_BASE_URL", raising=False)
    monkeypatch.delenv("ANTHROPIC_AWS_WORKSPACE_ID", raising=False)
    client = AnthropicAWS(skip_auth=True)
    assert client._skip_auth is True


def test_skip_auth_async(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_AWS_WORKSPACE_ID", raising=False)
    client = AsyncAnthropicAWS(skip_auth=True, base_url="https://custom.example.com")
    assert client._skip_auth is True
    assert client._use_sigv4 is False


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
def test_skip_auth_no_auth_headers(respx_mock: MockRouter) -> None:
    respx_mock.post(re.compile(r"https://custom\.example\.com/.*")).mock(
        return_value=httpx.Response(200, json={"foo": "bar"})
    )

    client = AnthropicAWS(skip_auth=True, base_url="https://custom.example.com")
    client.messages.create(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}],
        model="claude-sonnet-4-20250514",
    )

    calls = cast("list[MockRequestCall]", respx_mock.calls)
    assert len(calls) == 1
    assert "X-Api-Key" not in calls[0].request.headers
    assert "Authorization" not in calls[0].request.headers
    assert "X-Amz-Date" not in calls[0].request.headers
    assert "anthropic-workspace-id" not in calls[0].request.headers


# --- Environment Variables ---


def test_env_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_AWS_API_KEY", "env-key")
    monkeypatch.delenv("AWS_REGION", raising=False)
    client = AnthropicAWS(base_url="https://example.com", workspace_id="ws-123")
    assert client.api_key == "env-key"
    assert client._use_sigv4 is False


def test_env_region(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AWS_REGION", "ap-southeast-1")
    client = AnthropicAWS(api_key="test-key", workspace_id="ws-123")
    assert client.aws_region == "ap-southeast-1"


def test_env_base_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_AWS_BASE_URL", "https://custom-gateway.example.com")
    client = AnthropicAWS(api_key="test-key", workspace_id="ws-123")
    assert str(client.base_url).rstrip("/") == "https://custom-gateway.example.com"


# --- Auth Precedence ---


def test_api_key_arg_takes_precedence_over_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_AWS_API_KEY", "env-key")
    client = AnthropicAWS(api_key="arg-key", aws_region="us-east-1", workspace_id="ws-123")
    assert client.api_key == "arg-key"
    assert client._use_sigv4 is False


def test_explicit_aws_creds_suppress_env_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """Explicit SigV4 constructor args should suppress ANTHROPIC_AWS_API_KEY env var."""
    monkeypatch.setenv("ANTHROPIC_AWS_API_KEY", "env-key")
    client = AnthropicAWS(
        aws_access_key="AKID",
        aws_secret_key="secret",
        aws_region="us-east-1",
        workspace_id="ws-123",
    )
    assert client._use_sigv4 is True
    assert client.api_key is None


def test_aws_profile_suppresses_env_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_AWS_API_KEY", "env-key")
    client = AnthropicAWS(aws_profile="my-profile", aws_region="us-east-1", workspace_id="ws-123")
    assert client._use_sigv4 is True
    assert client.api_key is None


# --- Region / Base URL ---


def test_region_from_constructor() -> None:
    client = AnthropicAWS(api_key="test-key", aws_region="eu-central-1", workspace_id="ws-123")
    assert client.aws_region == "eu-central-1"
    assert str(client.base_url).rstrip("/") == "https://aws-external-anthropic.eu-central-1.api.aws"


def test_region_constructor_overrides_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AWS_REGION", "us-west-2")
    client = AnthropicAWS(api_key="test-key", aws_region="eu-west-1", workspace_id="ws-123")
    assert client.aws_region == "eu-west-1"
    assert str(client.base_url).rstrip("/") == "https://aws-external-anthropic.eu-west-1.api.aws"


def test_base_url_override() -> None:
    client = AnthropicAWS(
        api_key="test-key",
        aws_region="us-east-1",
        base_url="https://custom.example.com",
        workspace_id="ws-123",
    )
    assert str(client.base_url).rstrip("/") == "https://custom.example.com"


def test_api_key_mode_no_region_with_base_url() -> None:
    """API key mode should work without a region if base_url is provided."""
    client = AnthropicAWS(api_key="test-key", base_url="https://custom.example.com", workspace_id="ws-123")
    assert client.aws_region is None
    assert client._use_sigv4 is False


def test_api_key_mode_no_region_no_base_url_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    """API key mode without region or base_url should error."""
    monkeypatch.delenv("AWS_REGION", raising=False)
    monkeypatch.delenv("ANTHROPIC_AWS_BASE_URL", raising=False)
    with pytest.raises(AnthropicError, match="No AWS region was provided and no base_url"):
        AnthropicAWS(api_key="test-key", workspace_id="ws-123")


# --- Resources ---


def test_has_all_resources() -> None:
    client = AnthropicAWS(api_key="test-key", aws_region="us-east-1", workspace_id="ws-123")
    assert client.messages is not None
    assert client.beta is not None
    assert client.models is not None
    assert client.completions is not None


def test_async_has_all_resources() -> None:
    client = AsyncAnthropicAWS(api_key="test-key", aws_region="us-east-1", workspace_id="ws-123")
    assert client.messages is not None
    assert client.beta is not None
    assert client.models is not None
    assert client.completions is not None


# --- Request behavior (API key mode) ---


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
def test_api_key_request(respx_mock: MockRouter) -> None:
    respx_mock.post(re.compile(r"https://aws-external-anthropic\.us-east-1\.api\.aws/.*")).mock(
        return_value=httpx.Response(200, json={"foo": "bar"})
    )

    client = AnthropicAWS(api_key="test-key", aws_region="us-east-1", workspace_id="ws-123")
    client.messages.create(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}],
        model="claude-sonnet-4-20250514",
    )

    calls = cast("list[MockRequestCall]", respx_mock.calls)
    assert len(calls) == 1
    assert str(calls[0].request.url) == "https://aws-external-anthropic.us-east-1.api.aws/v1/messages"
    assert calls[0].request.headers["X-Api-Key"] == "test-key"


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
@pytest.mark.asyncio()
async def test_api_key_request_async(respx_mock: MockRouter) -> None:
    respx_mock.post(re.compile(r"https://aws-external-anthropic\.us-east-1\.api\.aws/.*")).mock(
        return_value=httpx.Response(200, json={"foo": "bar"})
    )

    client = AsyncAnthropicAWS(api_key="test-key", aws_region="us-east-1", workspace_id="ws-123")
    await client.messages.create(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}],
        model="claude-sonnet-4-20250514",
    )

    calls = cast("list[MockRequestCall]", respx_mock.calls)
    assert len(calls) == 1
    assert str(calls[0].request.url) == "https://aws-external-anthropic.us-east-1.api.aws/v1/messages"
    assert calls[0].request.headers["X-Api-Key"] == "test-key"


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
def test_retries(respx_mock: MockRouter) -> None:
    respx_mock.post(re.compile(r"https://aws-external-anthropic\.us-east-1\.api\.aws/.*")).mock(
        side_effect=[
            httpx.Response(500, json={"error": "server error"}, headers={"retry-after-ms": "10"}),
            httpx.Response(200, json={"foo": "bar"}),
        ]
    )

    client = AnthropicAWS(api_key="test-key", aws_region="us-east-1", workspace_id="ws-123")
    client.messages.create(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}],
        model="claude-sonnet-4-20250514",
    )

    calls = cast("list[MockRequestCall]", respx_mock.calls)
    assert len(calls) == 2


# --- copy / with_options ---


def test_copy_preserves_aws_options() -> None:
    client = AnthropicAWS(
        aws_access_key="AKID",
        aws_secret_key="secret",
        aws_region="us-east-1",
        aws_profile="my-profile",
        aws_session_token="token",
        workspace_id="ws-123",
    )
    copied = client.copy()
    assert copied.aws_access_key == "AKID"
    assert copied.aws_secret_key == "secret"
    assert copied.aws_region == "us-east-1"
    assert copied.aws_profile == "my-profile"
    assert copied.aws_session_token == "token"
    assert copied._use_sigv4 is True


def test_copy_overrides_aws_options() -> None:
    client = AnthropicAWS(
        aws_access_key="AKID",
        aws_secret_key="secret",
        aws_region="us-east-1",
        workspace_id="ws-123",
    )
    copied = client.copy(aws_region="eu-west-1")
    assert copied.aws_region == "eu-west-1"
    # base_url is not re-derived from region on copy — must be overridden explicitly
    assert str(copied.base_url).rstrip("/") == "https://aws-external-anthropic.us-east-1.api.aws"

    copied2 = client.copy(
        aws_region="eu-west-1",
        base_url="https://aws-external-anthropic.eu-west-1.api.aws",
    )
    assert str(copied2.base_url).rstrip("/") == "https://aws-external-anthropic.eu-west-1.api.aws"
