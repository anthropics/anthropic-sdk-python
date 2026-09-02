import re
import threading
from typing import Dict, List, Type, Union, Optional, cast
from typing_extensions import Protocol

import httpx2
import pytest
from respx import MockRouter

from anthropic import AnthropicAWS, AsyncAnthropicAWS, omit
from anthropic._exceptions import AnthropicError
from anthropic.lib.credentials import StaticToken


class MockRequestCall(Protocol):
    request: httpx2.Request


_AWSClientClass = Union[Type[AnthropicAWS], Type[AsyncAnthropicAWS]]
_aws_client_classes = pytest.mark.parametrize("client_cls", [AnthropicAWS, AsyncAnthropicAWS], ids=["sync", "async"])


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


def _clear_aws_url_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for var in (
        "AWS_REGION",
        "AWS_DEFAULT_REGION",
        "AWS_PROFILE",
        "ANTHROPIC_AWS_BASE_URL",
        "ANTHROPIC_AWS_WORKSPACE_ID",
        "ANTHROPIC_BASE_URL",
    ):
        monkeypatch.delenv(var, raising=False)


def _set_ambient_first_party_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "ambient-key")
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "ambient-token")


@_aws_client_classes
def test_skip_auth_requires_region_or_base_url(client_cls: _AWSClientClass, monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_aws_url_env(monkeypatch)
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://first-party.example.com")
    with pytest.raises(AnthropicError, match="No AWS region was provided and no base_url"):
        client_cls(skip_auth=True)


@_aws_client_classes
def test_skip_auth_base_url_from_region_arg(client_cls: _AWSClientClass, monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_aws_url_env(monkeypatch)
    client = client_cls(skip_auth=True, aws_region="eu-west-1")
    assert client.aws_region == "eu-west-1"
    assert str(client.base_url).rstrip("/") == "https://aws-external-anthropic.eu-west-1.api.aws"


@_aws_client_classes
def test_skip_auth_base_url_from_region_env(client_cls: _AWSClientClass, monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_aws_url_env(monkeypatch)
    monkeypatch.setenv("AWS_REGION", "ap-southeast-1")
    client = client_cls(skip_auth=True)
    assert str(client.base_url).rstrip("/") == "https://aws-external-anthropic.ap-southeast-1.api.aws"


@_aws_client_classes
def test_skip_auth_base_url_env_overrides_region(client_cls: _AWSClientClass, monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_aws_url_env(monkeypatch)
    monkeypatch.setenv("ANTHROPIC_AWS_BASE_URL", "https://custom-gateway.example.com")
    client = client_cls(skip_auth=True, aws_region="eu-west-1")
    assert str(client.base_url).rstrip("/") == "https://custom-gateway.example.com"


@_aws_client_classes
def test_skip_auth_explicit_base_url_wins(client_cls: _AWSClientClass, monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_aws_url_env(monkeypatch)
    monkeypatch.setenv("ANTHROPIC_AWS_BASE_URL", "https://custom-gateway.example.com")
    client = client_cls(skip_auth=True, aws_region="eu-west-1", base_url="https://custom.example.com")
    assert str(client.base_url).rstrip("/") == "https://custom.example.com"


def test_skip_auth_async(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_AWS_WORKSPACE_ID", raising=False)
    client = AsyncAnthropicAWS(skip_auth=True, base_url="https://custom.example.com")
    assert client._skip_auth is True
    assert client._use_sigv4 is False


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
def test_skip_auth_no_auth_headers(respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch) -> None:
    _set_ambient_first_party_credentials(monkeypatch)
    respx_mock.post(re.compile(r"https://custom\.example\.com/.*")).mock(
        return_value=httpx2.Response(200, json={"foo": "bar"})
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


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
@pytest.mark.asyncio()
@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_skip_auth_region_request_url(
    sync: bool, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
) -> None:
    _clear_aws_url_env(monkeypatch)
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://first-party.example.com")
    _set_ambient_first_party_credentials(monkeypatch)
    respx_mock.post(re.compile(r"https://aws-external-anthropic\.eu-west-1\.api\.aws/.*")).mock(
        return_value=httpx2.Response(200, json={"foo": "bar"})
    )

    if sync:
        AnthropicAWS(skip_auth=True, aws_region="eu-west-1", workspace_id="ws-123").messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-sonnet-4-20250514",
        )
    else:
        await AsyncAnthropicAWS(skip_auth=True, aws_region="eu-west-1", workspace_id="ws-123").messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-sonnet-4-20250514",
        )

    calls = cast("list[MockRequestCall]", respx_mock.calls)
    assert len(calls) == 1
    assert str(calls[0].request.url) == "https://aws-external-anthropic.eu-west-1.api.aws/v1/messages"
    assert calls[0].request.headers["anthropic-workspace-id"] == "ws-123"
    assert "X-Api-Key" not in calls[0].request.headers
    assert "Authorization" not in calls[0].request.headers


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
@pytest.mark.asyncio()
@pytest.mark.parametrize("via", ["copy", "scoped_helper"])
@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_skip_auth_explicit_auth_token_on_copy_is_sent(
    sync: bool, via: str, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
) -> None:
    from anthropic.lib._scoped_client import _copy_client_with_bearer_auth

    _clear_aws_url_env(monkeypatch)
    _set_ambient_first_party_credentials(monkeypatch)
    respx_mock.post(re.compile(r"https://aws-external-anthropic\.eu-west-1\.api\.aws/.*")).mock(
        return_value=httpx2.Response(200, json={"foo": "bar"})
    )

    if sync:
        client = AnthropicAWS(skip_auth=True, aws_region="eu-west-1", workspace_id="ws-123")
        scoped = (
            client.copy(auth_token="scoped-token")
            if via == "copy"
            else _copy_client_with_bearer_auth(client, auth_token="scoped-token", helper="environments-worker")
        )
        scoped.messages.create(
            max_tokens=1024, messages=[{"role": "user", "content": "Hello"}], model="claude-sonnet-4-20250514"
        )
    else:
        async_client = AsyncAnthropicAWS(skip_auth=True, aws_region="eu-west-1", workspace_id="ws-123")
        async_scoped = (
            async_client.copy(auth_token="scoped-token")
            if via == "copy"
            else _copy_client_with_bearer_auth(async_client, auth_token="scoped-token", helper="environments-worker")
        )
        await async_scoped.messages.create(
            max_tokens=1024, messages=[{"role": "user", "content": "Hello"}], model="claude-sonnet-4-20250514"
        )

    calls = cast("list[MockRequestCall]", respx_mock.calls)
    assert len(calls) == 1
    assert calls[0].request.headers["Authorization"] == "Bearer scoped-token"
    assert "X-Api-Key" not in calls[0].request.headers


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


def test_async_has_all_resources() -> None:
    client = AsyncAnthropicAWS(api_key="test-key", aws_region="us-east-1", workspace_id="ws-123")
    assert client.messages is not None
    assert client.beta is not None
    assert client.models is not None


# --- Request behavior (API key mode) ---


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
def test_api_key_request(respx_mock: MockRouter) -> None:
    respx_mock.post(re.compile(r"https://aws-external-anthropic\.us-east-1\.api\.aws/.*")).mock(
        return_value=httpx2.Response(200, json={"foo": "bar"})
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
        return_value=httpx2.Response(200, json={"foo": "bar"})
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
@pytest.mark.parametrize(
    "request_workspace_id, expected",
    [(None, "ws-client"), ("ws-request", "ws-request")],
)
def test_workspace_id_header(respx_mock: MockRouter, request_workspace_id: Optional[str], expected: str) -> None:
    respx_mock.post(re.compile(r"https://aws-external-anthropic\.us-east-1\.api\.aws/.*")).mock(
        return_value=httpx2.Response(200, json={"foo": "bar"})
    )

    client = AnthropicAWS(api_key="test-key", aws_region="us-east-1", workspace_id="ws-client")
    client.messages.create(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}],
        model="claude-sonnet-4-20250514",
        workspace_id=request_workspace_id if request_workspace_id is not None else omit,
    )

    calls = cast("list[MockRequestCall]", respx_mock.calls)
    assert calls[0].request.headers.get("anthropic-workspace-id") == expected


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "request_workspace_id, expected",
    [(None, "ws-client"), ("ws-request", "ws-request")],
)
async def test_workspace_id_header_async(
    respx_mock: MockRouter, request_workspace_id: Optional[str], expected: str
) -> None:
    respx_mock.post(re.compile(r"https://aws-external-anthropic\.us-east-1\.api\.aws/.*")).mock(
        return_value=httpx2.Response(200, json={"foo": "bar"})
    )

    client = AsyncAnthropicAWS(api_key="test-key", aws_region="us-east-1", workspace_id="ws-client")
    await client.messages.create(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}],
        model="claude-sonnet-4-20250514",
        workspace_id=request_workspace_id if request_workspace_id is not None else omit,
    )

    calls = cast("list[MockRequestCall]", respx_mock.calls)
    assert calls[0].request.headers.get("anthropic-workspace-id") == expected


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
def test_retries(respx_mock: MockRouter) -> None:
    respx_mock.post(re.compile(r"https://aws-external-anthropic\.us-east-1\.api\.aws/.*")).mock(
        side_effect=[
            httpx2.Response(500, json={"error": "server error"}, headers={"retry-after-ms": "10"}),
            httpx2.Response(200, json={"foo": "bar"}),
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


# --- Request behavior (SigV4 mode) ---


@pytest.mark.respx()
@pytest.mark.asyncio()
@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_sigv4_binary_file_upload(sync: bool, respx_mock: MockRouter) -> None:
    respx_mock.post(re.compile(r"https://aws-external-anthropic\.us-east-1\.api\.aws/.*")).mock(
        return_value=httpx2.Response(200, json={"id": "file_123", "type": "file"})
    )
    png = b"\x89PNG\r\n\x1a\n\x00\xff\xfe"

    if sync:
        AnthropicAWS(
            aws_access_key="AKID", aws_secret_key="secret", aws_region="us-east-1", workspace_id="ws-123"
        ).files.upload(file=("x.png", png, "image/png"))
    else:
        await AsyncAnthropicAWS(
            aws_access_key="AKID", aws_secret_key="secret", aws_region="us-east-1", workspace_id="ws-123"
        ).files.upload(file=("x.png", png, "image/png"))

    calls = cast("list[MockRequestCall]", respx_mock.calls)
    assert len(calls) == 1
    assert str(calls[0].request.url) == "https://aws-external-anthropic.us-east-1.api.aws/v1/files"
    assert png in calls[0].request.content
    assert calls[0].request.headers["Authorization"].startswith("AWS4-HMAC-SHA256 ")


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
@pytest.mark.asyncio()
@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_sigv4_with_options_ignores_ambient_first_party_credentials(
    sync: bool, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
) -> None:
    _clear_aws_url_env(monkeypatch)
    _set_ambient_first_party_credentials(monkeypatch)
    respx_mock.post(re.compile(r"https://aws-external-anthropic\.us-west-2\.api\.aws/.*")).mock(
        return_value=httpx2.Response(200, json={"foo": "bar"})
    )

    if sync:
        client = AnthropicAWS(
            aws_access_key="AKID", aws_secret_key="secret", aws_region="eu-west-1", workspace_id="ws-123"
        )
        assert client.api_key is None
        assert client.auth_token is None
        client.with_options(aws_region="us-west-2").messages.create(
            max_tokens=1024, messages=[{"role": "user", "content": "Hello"}], model="claude-sonnet-4-20250514"
        )
    else:
        async_client = AsyncAnthropicAWS(
            aws_access_key="AKID", aws_secret_key="secret", aws_region="eu-west-1", workspace_id="ws-123"
        )
        assert async_client.api_key is None
        assert async_client.auth_token is None
        await async_client.with_options(aws_region="us-west-2").messages.create(
            max_tokens=1024, messages=[{"role": "user", "content": "Hello"}], model="claude-sonnet-4-20250514"
        )

    calls = cast("list[MockRequestCall]", respx_mock.calls)
    assert len(calls) == 1
    assert str(calls[0].request.url) == "https://aws-external-anthropic.us-west-2.api.aws/v1/messages"
    authorization = calls[0].request.headers["Authorization"]
    assert authorization.startswith("AWS4-HMAC-SHA256 ")
    assert "/us-west-2/" in authorization
    assert "X-Api-Key" not in calls[0].request.headers


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
    copied = client.copy(aws_access_key="AKID2", aws_secret_key="secret2", workspace_id="ws-456")
    assert copied.aws_access_key == "AKID2"
    assert copied.aws_secret_key == "secret2"
    assert copied.workspace_id == "ws-456"
    assert copied.aws_region == "us-east-1"
    assert str(copied.base_url).rstrip("/") == "https://aws-external-anthropic.us-east-1.api.aws"


@_aws_client_classes
def test_copy_region_change_rederives_base_url(client_cls: _AWSClientClass, monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_aws_url_env(monkeypatch)
    _set_ambient_first_party_credentials(monkeypatch)
    client = client_cls(aws_access_key="AKID", aws_secret_key="secret", aws_region="eu-west-1", workspace_id="ws-123")
    assert str(client.base_url).rstrip("/") == "https://aws-external-anthropic.eu-west-1.api.aws"

    copied = client.with_options(aws_region="us-west-2")
    assert copied.aws_region == "us-west-2"
    assert str(copied.base_url).rstrip("/") == "https://aws-external-anthropic.us-west-2.api.aws"
    assert copied.api_key is None and copied.auth_token is None
    assert client.aws_region == "eu-west-1"
    assert str(client.base_url).rstrip("/") == "https://aws-external-anthropic.eu-west-1.api.aws"

    chained = copied.with_options(aws_region="ap-northeast-1")
    assert str(chained.base_url).rstrip("/") == "https://aws-external-anthropic.ap-northeast-1.api.aws"


@_aws_client_classes
def test_copy_region_change_rederives_base_url_api_key_mode(
    client_cls: _AWSClientClass, monkeypatch: pytest.MonkeyPatch
) -> None:
    _clear_aws_url_env(monkeypatch)
    client = client_cls(api_key="test-key", aws_region="eu-west-1", workspace_id="ws-123")
    copied = client.with_options(aws_region="us-west-2")
    assert str(copied.base_url).rstrip("/") == "https://aws-external-anthropic.us-west-2.api.aws"


@_aws_client_classes
def test_copy_region_change_rederives_base_url_skip_auth(
    client_cls: _AWSClientClass, monkeypatch: pytest.MonkeyPatch
) -> None:
    _clear_aws_url_env(monkeypatch)
    _set_ambient_first_party_credentials(monkeypatch)
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://first-party.example.com")
    client = client_cls(skip_auth=True, aws_region="eu-west-1")
    copied = client.with_options(aws_region="us-west-2")
    assert copied.aws_region == "us-west-2"
    assert str(copied.base_url).rstrip("/") == "https://aws-external-anthropic.us-west-2.api.aws"
    assert copied.api_key is None and copied.auth_token is None


@_aws_client_classes
def test_copy_region_change_explicit_base_url_wins(
    client_cls: _AWSClientClass, monkeypatch: pytest.MonkeyPatch
) -> None:
    _clear_aws_url_env(monkeypatch)
    client = client_cls(aws_access_key="AKID", aws_secret_key="secret", aws_region="eu-west-1", workspace_id="ws-123")
    copied = client.with_options(aws_region="us-west-2", base_url="https://custom.example.com")
    assert copied.aws_region == "us-west-2"
    assert str(copied.base_url).rstrip("/") == "https://custom.example.com"

    chained = copied.with_options(aws_region="ap-northeast-1")
    assert chained.aws_region == "ap-northeast-1"
    assert str(chained.base_url).rstrip("/") == "https://custom.example.com"


@_aws_client_classes
def test_copy_region_change_keeps_custom_base_url(client_cls: _AWSClientClass, monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_aws_url_env(monkeypatch)
    client = client_cls(
        aws_access_key="AKID",
        aws_secret_key="secret",
        aws_region="eu-west-1",
        base_url="https://custom.example.com",
        workspace_id="ws-123",
    )
    copied = client.with_options(aws_region="us-west-2")
    assert copied.aws_region == "us-west-2"
    assert str(copied.base_url).rstrip("/") == "https://custom.example.com"
    assert str(client.with_options(workspace_id="ws-456").base_url).rstrip("/") == "https://custom.example.com"


@_aws_client_classes
def test_copy_region_change_keeps_env_base_url(client_cls: _AWSClientClass, monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_aws_url_env(monkeypatch)
    monkeypatch.setenv("ANTHROPIC_AWS_BASE_URL", "https://custom-gateway.example.com")
    client = client_cls(aws_access_key="AKID", aws_secret_key="secret", aws_region="eu-west-1", workspace_id="ws-123")
    copied = client.with_options(aws_region="us-west-2")
    assert copied.aws_region == "us-west-2"
    assert str(copied.base_url).rstrip("/") == "https://custom-gateway.example.com"


@_aws_client_classes
def test_copy_region_change_keeps_base_url_assigned_after_construction(
    client_cls: _AWSClientClass, monkeypatch: pytest.MonkeyPatch
) -> None:
    _clear_aws_url_env(monkeypatch)
    client = client_cls(aws_access_key="AKID", aws_secret_key="secret", aws_region="eu-west-1", workspace_id="ws-123")
    client.base_url = "https://gateway.example.com"
    copied = client.with_options(aws_region="us-west-2")
    assert copied.aws_region == "us-west-2"
    assert str(copied.base_url).rstrip("/") == "https://gateway.example.com"


def test_copy_accepts_credentials_none_noop() -> None:
    # `credentials=None` is accepted as a no-op: the AWS client authenticates with
    # SigV4, not a token provider, so there is nothing to clear. The copy stays SigV4.
    client = AnthropicAWS(
        aws_access_key="AKID",
        aws_secret_key="secret",
        aws_region="us-east-1",
        workspace_id="ws-123",
    )
    copied = client.copy(credentials=None)
    assert copied._use_sigv4 is True
    assert copied.workspace_id == "ws-123"
    assert copied.aws_region == "us-east-1"


def test_copy_accepts_credentials_none_noop_async() -> None:
    client = AsyncAnthropicAWS(
        aws_access_key="AKID",
        aws_secret_key="secret",
        aws_region="us-east-1",
        workspace_id="ws-123",
    )
    copied = client.copy(credentials=None)
    assert copied._use_sigv4 is True
    assert copied.workspace_id == "ws-123"
    assert copied.aws_region == "us-east-1"


def test_copy_rejects_real_credentials_provider() -> None:
    client = AnthropicAWS(
        aws_access_key="AKID",
        aws_secret_key="secret",
        aws_region="us-east-1",
        workspace_id="ws-123",
    )
    with pytest.raises(TypeError, match="does not support a `credentials` provider"):
        client.copy(credentials=StaticToken("token"))


def test_copy_rejects_real_credentials_provider_async() -> None:
    client = AsyncAnthropicAWS(
        aws_access_key="AKID",
        aws_secret_key="secret",
        aws_region="us-east-1",
        workspace_id="ws-123",
    )
    with pytest.raises(TypeError, match="does not support a `credentials` provider"):
        client.copy(credentials=StaticToken("token"))


def test_scoped_bearer_client_helper_on_aws() -> None:
    # Regression: the environment poller / worker / session-tool-runner build a
    # scoped sub-client via `_copy_client_with_bearer_auth`, which calls
    # `client.copy(credentials=None, ...)`. That must work on the AWS client and
    # yield a client that still signs with SigV4 (the bearer token is unused).
    from anthropic.lib._scoped_client import _copy_client_with_bearer_auth

    client = AnthropicAWS(
        aws_access_key="AKID",
        aws_secret_key="secret",
        aws_region="us-east-1",
        workspace_id="ws-123",
    )
    scoped = _copy_client_with_bearer_auth(client, auth_token="unused-under-sigv4", helper="environments-work-poller")
    assert isinstance(scoped, AnthropicAWS)
    assert scoped._use_sigv4 is True
    assert scoped.workspace_id == "ws-123"


def test_scoped_bearer_client_helper_on_aws_async() -> None:
    from anthropic.lib._scoped_client import _copy_client_with_bearer_auth

    client = AsyncAnthropicAWS(
        aws_access_key="AKID",
        aws_secret_key="secret",
        aws_region="us-east-1",
        workspace_id="ws-123",
    )
    scoped = _copy_client_with_bearer_auth(client, auth_token="unused-under-sigv4", helper="environments-worker")
    assert isinstance(scoped, AsyncAnthropicAWS)
    assert scoped._use_sigv4 is True
    assert scoped.workspace_id == "ws-123"


@pytest.mark.asyncio()
async def test_sigv4_signing_runs_off_event_loop_async(monkeypatch: pytest.MonkeyPatch) -> None:
    client = AsyncAnthropicAWS(
        aws_access_key="AKID",
        aws_secret_key="secret",
        aws_region="us-east-1",
        workspace_id="ws-123",
    )
    signing_threads: List[int] = []

    def fake_get_auth_headers(**_: object) -> Dict[str, str]:
        signing_threads.append(threading.get_ident())
        return {"Authorization": "AWS4-HMAC-SHA256 stub"}

    monkeypatch.setattr("anthropic.lib.aws._auth.get_auth_headers", fake_get_auth_headers)

    request = httpx2.Request("POST", "https://aws-external-anthropic.us-east-1.api.aws/v1/messages", content=b"{}")
    await client._prepare_request(request)

    assert len(signing_threads) == 1
    assert signing_threads[0] != threading.get_ident()
    assert request.headers["Authorization"] == "AWS4-HMAC-SHA256 stub"
