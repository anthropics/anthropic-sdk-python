from __future__ import annotations

import json
import threading
from typing import cast
from collections.abc import Callable, Awaitable
from typing_extensions import Protocol

import httpx2
import pytest
from respx import MockRouter

from anthropic import Omit, Anthropic, AnthropicBedrockMantle, AsyncAnthropicBedrockMantle, omit
from anthropic._compat import PYDANTIC_V1

MANTLE_MESSAGES_URL = "https://bedrock-mantle.us-east-1.api.aws/anthropic/v1/messages"

MODEL = "anthropic.claude-sonnet-4-5"


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

        request = httpx2.Request(
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

    def test_user_profiles_not_available(self) -> None:
        client = self._make_client()
        assert not hasattr(client, "user_profiles")
        assert not hasattr(client.beta, "user_profiles")


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


class TestVersionHeader:
    def test_matches_the_first_party_client(self) -> None:
        expected = Anthropic(api_key="test-key").default_headers["anthropic-version"]
        client = AnthropicBedrockMantle(api_key="test-key", aws_region="us-east-1")
        assert client.default_headers["anthropic-version"] == expected

    def test_async_matches_the_first_party_client(self) -> None:
        expected = Anthropic(api_key="test-key").default_headers["anthropic-version"]
        client = AsyncAnthropicBedrockMantle(api_key="test-key", aws_region="us-east-1")
        assert client.default_headers["anthropic-version"] == expected


class TestSkipAuth:
    def test_skip_auth_does_not_sign_request(self, get_auth_headers_recorder: GetAuthHeadersRecorder) -> None:
        client = AnthropicBedrockMantle(
            skip_auth=True,
            base_url="https://example.com",
        )

        request = httpx2.Request("POST", "https://example.com/v1/messages", content=b"{}")
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
        assert not hasattr(client, "user_profiles")
        assert not hasattr(client.beta, "user_profiles")

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

        request = httpx2.Request(
            "POST", "https://bedrock-mantle.us-east-1.api.aws/anthropic/v1/messages", content=b"{}"
        )
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


MESSAGE = {
    "id": "msg_test",
    "type": "message",
    "role": "assistant",
    "model": MODEL,
    "content": [{"type": "text", "text": "Hello"}],
    "stop_reason": "end_turn",
    "stop_sequence": None,
    "usage": {"input_tokens": 1, "output_tokens": 1},
}

MESSAGE_SSE = "".join(
    f"event: {event['type']}\ndata: {json.dumps(event)}\n\n"
    for event in ({"type": "message_start", "message": MESSAGE}, {"type": "message_stop"})
)


def respond_with_message(request: httpx2.Request) -> httpx2.Response:
    if request.url.path.endswith("/count_tokens"):
        return httpx2.Response(200, json={"input_tokens": 1})
    if json.loads(request.content).get("stream"):
        return httpx2.Response(200, headers={"content-type": "text/event-stream"}, content=MESSAGE_SSE)
    return httpx2.Response(200, json=MESSAGE)


class MockRequestCall(Protocol):
    request: httpx2.Request


def sent_requests(respx_mock: MockRouter) -> list[httpx2.Request]:
    return [call.request for call in cast("list[MockRequestCall]", respx_mock.calls)]


def create(client: AnthropicBedrockMantle, user_profile_id: str | Omit, extra_body: object) -> None:
    client.messages.create(
        max_tokens=16,
        messages=[{"role": "user", "content": "Hi"}],
        model=MODEL,
        user_profile_id=user_profile_id,
        extra_body=extra_body,
    )


def stream(client: AnthropicBedrockMantle, user_profile_id: str | Omit, extra_body: object) -> None:
    with client.messages.stream(
        max_tokens=16,
        messages=[{"role": "user", "content": "Hi"}],
        model=MODEL,
        user_profile_id=user_profile_id,
        extra_body=extra_body,
    ) as message_stream:
        message_stream.until_done()


def beta_create(client: AnthropicBedrockMantle, user_profile_id: str | Omit, extra_body: object) -> None:
    client.beta.messages.create(
        max_tokens=16,
        messages=[{"role": "user", "content": "Hi"}],
        model=MODEL,
        user_profile_id=user_profile_id,
        extra_body=extra_body,
    )


def beta_stream(client: AnthropicBedrockMantle, user_profile_id: str | Omit, extra_body: object) -> None:
    with client.beta.messages.stream(
        max_tokens=16,
        messages=[{"role": "user", "content": "Hi"}],
        model=MODEL,
        user_profile_id=user_profile_id,
        extra_body=extra_body,
    ) as message_stream:
        message_stream.until_done()


def beta_parse(client: AnthropicBedrockMantle, user_profile_id: str | Omit, extra_body: object) -> None:
    client.beta.messages.parse(
        max_tokens=16,
        messages=[{"role": "user", "content": "Hi"}],
        model=MODEL,
        user_profile_id=user_profile_id,
        extra_body=extra_body,
    )


def beta_tool_runner(client: AnthropicBedrockMantle, user_profile_id: str | Omit, extra_body: object) -> None:
    client.beta.messages.tool_runner(
        max_tokens=16,
        messages=[{"role": "user", "content": "Hi"}],
        model=MODEL,
        tools=[],
        user_profile_id=user_profile_id,
        extra_body=extra_body,
    ).until_done()


async def async_create(client: AsyncAnthropicBedrockMantle, user_profile_id: str | Omit, extra_body: object) -> None:
    await client.messages.create(
        max_tokens=16,
        messages=[{"role": "user", "content": "Hi"}],
        model=MODEL,
        user_profile_id=user_profile_id,
        extra_body=extra_body,
    )


async def async_stream(client: AsyncAnthropicBedrockMantle, user_profile_id: str | Omit, extra_body: object) -> None:
    async with client.messages.stream(
        max_tokens=16,
        messages=[{"role": "user", "content": "Hi"}],
        model=MODEL,
        user_profile_id=user_profile_id,
        extra_body=extra_body,
    ) as message_stream:
        await message_stream.until_done()


async def async_beta_create(
    client: AsyncAnthropicBedrockMantle, user_profile_id: str | Omit, extra_body: object
) -> None:
    await client.beta.messages.create(
        max_tokens=16,
        messages=[{"role": "user", "content": "Hi"}],
        model=MODEL,
        user_profile_id=user_profile_id,
        extra_body=extra_body,
    )


async def async_beta_stream(
    client: AsyncAnthropicBedrockMantle, user_profile_id: str | Omit, extra_body: object
) -> None:
    async with client.beta.messages.stream(
        max_tokens=16,
        messages=[{"role": "user", "content": "Hi"}],
        model=MODEL,
        user_profile_id=user_profile_id,
        extra_body=extra_body,
    ) as message_stream:
        await message_stream.until_done()


async def async_beta_parse(
    client: AsyncAnthropicBedrockMantle, user_profile_id: str | Omit, extra_body: object
) -> None:
    await client.beta.messages.parse(
        max_tokens=16,
        messages=[{"role": "user", "content": "Hi"}],
        model=MODEL,
        user_profile_id=user_profile_id,
        extra_body=extra_body,
    )


async def async_beta_tool_runner(
    client: AsyncAnthropicBedrockMantle, user_profile_id: str | Omit, extra_body: object
) -> None:
    await client.beta.messages.tool_runner(
        max_tokens=16,
        messages=[{"role": "user", "content": "Hi"}],
        model=MODEL,
        tools=[],
        user_profile_id=user_profile_id,
        extra_body=extra_body,
    ).until_done()


def count_tokens(client: AnthropicBedrockMantle, user_profile_id: str | Omit, extra_body: object) -> None:
    client.messages.count_tokens(
        messages=[{"role": "user", "content": "Hi"}],
        model=MODEL,
        user_profile_id=user_profile_id,
        extra_body=extra_body,
    )


def beta_count_tokens(client: AnthropicBedrockMantle, user_profile_id: str | Omit, extra_body: object) -> None:
    client.beta.messages.count_tokens(
        messages=[{"role": "user", "content": "Hi"}],
        model=MODEL,
        user_profile_id=user_profile_id,
        extra_body=extra_body,
    )


async def async_count_tokens(
    client: AsyncAnthropicBedrockMantle, user_profile_id: str | Omit, extra_body: object
) -> None:
    await client.messages.count_tokens(
        messages=[{"role": "user", "content": "Hi"}],
        model=MODEL,
        user_profile_id=user_profile_id,
        extra_body=extra_body,
    )


async def async_beta_count_tokens(
    client: AsyncAnthropicBedrockMantle, user_profile_id: str | Omit, extra_body: object
) -> None:
    await client.beta.messages.count_tokens(
        messages=[{"role": "user", "content": "Hi"}],
        model=MODEL,
        user_profile_id=user_profile_id,
        extra_body=extra_body,
    )


def create_batch(client: AnthropicBedrockMantle, user_profile_id: str | Omit) -> None:
    client.messages.batches.create(requests=[], user_profile_id=user_profile_id)


def beta_create_batch(client: AnthropicBedrockMantle, user_profile_id: str | Omit) -> None:
    client.beta.messages.batches.create(requests=[], user_profile_id=user_profile_id)


async def async_create_batch(client: AsyncAnthropicBedrockMantle, user_profile_id: str | Omit) -> None:
    await client.messages.batches.create(requests=[], user_profile_id=user_profile_id)


async def async_beta_create_batch(client: AsyncAnthropicBedrockMantle, user_profile_id: str | Omit) -> None:
    await client.beta.messages.batches.create(requests=[], user_profile_id=user_profile_id)


SendMessage = Callable[[AnthropicBedrockMantle, str | Omit, object], None]
AsyncSendMessage = Callable[[AsyncAnthropicBedrockMantle, str | Omit, object], Awaitable[None]]
SendBatch = Callable[[AnthropicBedrockMantle, str | Omit], None]
AsyncSendBatch = Callable[[AsyncAnthropicBedrockMantle, str | Omit], Awaitable[None]]

needs_pydantic_v2 = pytest.mark.skipif(PYDANTIC_V1, reason="parse and the tool runner need pydantic v2")

send_message = pytest.mark.parametrize(
    "send",
    [
        create,
        stream,
        beta_create,
        beta_stream,
        pytest.param(beta_parse, marks=needs_pydantic_v2),
        pytest.param(beta_tool_runner, marks=needs_pydantic_v2),
        count_tokens,
        beta_count_tokens,
    ],
)
async_send_message = pytest.mark.parametrize(
    "send",
    [
        async_create,
        async_stream,
        async_beta_create,
        async_beta_stream,
        pytest.param(async_beta_parse, marks=needs_pydantic_v2),
        pytest.param(async_beta_tool_runner, marks=needs_pydantic_v2),
        async_count_tokens,
        async_beta_count_tokens,
    ],
)


class TestUserProfileID:
    @pytest.fixture
    def client(self) -> AnthropicBedrockMantle:
        return AnthropicBedrockMantle(api_key="test-key", aws_region="us-east-1")

    @pytest.fixture
    def async_client(self) -> AsyncAnthropicBedrockMantle:
        return AsyncAnthropicBedrockMantle(api_key="test-key", aws_region="us-east-1")

    @send_message
    @pytest.mark.respx()
    def test_sent_in_body_instead_of_header(
        self, send: SendMessage, client: AnthropicBedrockMantle, respx_mock: MockRouter
    ) -> None:
        respx_mock.post(url__startswith=MANTLE_MESSAGES_URL).mock(side_effect=respond_with_message)

        send(client, "uprof_test", None)

        [request] = sent_requests(respx_mock)
        assert json.loads(request.content)["user_profile_id"] == "uprof_test"
        assert "anthropic-user-profile-id" not in request.headers

    @async_send_message
    @pytest.mark.respx()
    async def test_async_sent_in_body_instead_of_header(
        self, send: AsyncSendMessage, async_client: AsyncAnthropicBedrockMantle, respx_mock: MockRouter
    ) -> None:
        respx_mock.post(url__startswith=MANTLE_MESSAGES_URL).mock(side_effect=respond_with_message)

        await send(async_client, "uprof_test", None)

        [request] = sent_requests(respx_mock)
        assert json.loads(request.content)["user_profile_id"] == "uprof_test"
        assert "anthropic-user-profile-id" not in request.headers

    @pytest.mark.parametrize("user_profile_id", ["uprof_first,uprof_second", "uprof_first, uprof_second", ""])
    @pytest.mark.respx()
    def test_value_is_sent_as_given(
        self, user_profile_id: str, client: AnthropicBedrockMantle, respx_mock: MockRouter
    ) -> None:
        respx_mock.post(url__startswith=MANTLE_MESSAGES_URL).mock(side_effect=respond_with_message)

        create(client, user_profile_id, None)

        [request] = sent_requests(respx_mock)
        assert json.loads(request.content)["user_profile_id"] == user_profile_id
        assert "anthropic-user-profile-id" not in request.headers

    @pytest.mark.respx()
    def test_absent_from_body_when_not_given(self, client: AnthropicBedrockMantle, respx_mock: MockRouter) -> None:
        respx_mock.post(url__startswith=MANTLE_MESSAGES_URL).mock(side_effect=respond_with_message)

        create(client, omit, None)

        [request] = sent_requests(respx_mock)
        assert "user_profile_id" not in json.loads(request.content)
        assert "anthropic-user-profile-id" not in request.headers

    @pytest.mark.respx()
    def test_extra_body_value_wins(self, client: AnthropicBedrockMantle, respx_mock: MockRouter) -> None:
        respx_mock.post(url__startswith=MANTLE_MESSAGES_URL).mock(side_effect=respond_with_message)

        create(client, "uprof_argument", {"user_profile_id": "uprof_extra_body"})

        [request] = sent_requests(respx_mock)
        assert json.loads(request.content)["user_profile_id"] == "uprof_extra_body"
        assert "anthropic-user-profile-id" not in request.headers

    @pytest.mark.respx()
    def test_extra_headers_value_is_sent_in_body(self, client: AnthropicBedrockMantle, respx_mock: MockRouter) -> None:
        respx_mock.post(url__startswith=MANTLE_MESSAGES_URL).mock(side_effect=respond_with_message)

        client.messages.create(
            max_tokens=16,
            messages=[{"role": "user", "content": "Hi"}],
            model=MODEL,
            user_profile_id="uprof_argument",
            extra_headers={"Anthropic-User-Profile-Id": "uprof_extra_headers"},
        )

        [request] = sent_requests(respx_mock)
        assert json.loads(request.content)["user_profile_id"] == "uprof_extra_headers"
        assert "anthropic-user-profile-id" not in request.headers

    @pytest.mark.parametrize(
        ("user_profile_id", "sent"), [(omit, "uprof_default"), ("uprof_argument", "uprof_argument")]
    )
    @pytest.mark.respx()
    def test_client_default_header_is_sent_in_body_unless_the_request_names_one(
        self, user_profile_id: str | Omit, sent: str, client: AnthropicBedrockMantle, respx_mock: MockRouter
    ) -> None:
        respx_mock.post(url__startswith=MANTLE_MESSAGES_URL).mock(side_effect=respond_with_message)
        client = client.with_options(default_headers={"Anthropic-User-Profile-Id": "uprof_default"})

        create(client, user_profile_id, None)

        [request] = sent_requests(respx_mock)
        assert json.loads(request.content)["user_profile_id"] == sent
        assert "anthropic-user-profile-id" not in request.headers

    @pytest.mark.parametrize("send", [create_batch, beta_create_batch])
    @pytest.mark.respx()
    def test_batches_keep_the_header(
        self, send: SendBatch, client: AnthropicBedrockMantle, respx_mock: MockRouter
    ) -> None:
        respx_mock.post(url__startswith=MANTLE_MESSAGES_URL).mock(return_value=httpx2.Response(200, json={}))

        send(client, "uprof_test")

        [request] = sent_requests(respx_mock)
        assert request.headers["anthropic-user-profile-id"] == "uprof_test"
        assert "user_profile_id" not in json.loads(request.content)

    @pytest.mark.parametrize("send", [async_create_batch, async_beta_create_batch])
    @pytest.mark.respx()
    async def test_async_batches_keep_the_header(
        self, send: AsyncSendBatch, async_client: AsyncAnthropicBedrockMantle, respx_mock: MockRouter
    ) -> None:
        respx_mock.post(url__startswith=MANTLE_MESSAGES_URL).mock(return_value=httpx2.Response(200, json={}))

        await send(async_client, "uprof_test")

        [request] = sent_requests(respx_mock)
        assert request.headers["anthropic-user-profile-id"] == "uprof_test"
        assert "user_profile_id" not in json.loads(request.content)

    @pytest.mark.parametrize("send", [create_batch, beta_create_batch])
    @pytest.mark.respx()
    def test_batches_send_no_header_when_no_profile_is_set(
        self, send: SendBatch, client: AnthropicBedrockMantle, respx_mock: MockRouter
    ) -> None:
        respx_mock.post(url__startswith=MANTLE_MESSAGES_URL).mock(return_value=httpx2.Response(200, json={}))

        send(client, omit)

        [request] = sent_requests(respx_mock)
        assert "anthropic-user-profile-id" not in request.headers
        assert "user_profile_id" not in json.loads(request.content)

    @pytest.mark.parametrize("send", [async_create_batch, async_beta_create_batch])
    @pytest.mark.respx()
    async def test_async_batches_send_no_header_when_no_profile_is_set(
        self, send: AsyncSendBatch, async_client: AsyncAnthropicBedrockMantle, respx_mock: MockRouter
    ) -> None:
        respx_mock.post(url__startswith=MANTLE_MESSAGES_URL).mock(return_value=httpx2.Response(200, json={}))

        await send(async_client, omit)

        [request] = sent_requests(respx_mock)
        assert "anthropic-user-profile-id" not in request.headers
        assert "user_profile_id" not in json.loads(request.content)

    @pytest.mark.parametrize(
        ("user_profile_id", "sent"), [(omit, "uprof_default"), ("uprof_argument", "uprof_argument")]
    )
    @pytest.mark.parametrize("send", [create_batch, beta_create_batch])
    @pytest.mark.respx()
    def test_batches_send_the_client_default_header_unless_the_request_names_one(
        self,
        send: SendBatch,
        user_profile_id: str | Omit,
        sent: str,
        client: AnthropicBedrockMantle,
        respx_mock: MockRouter,
    ) -> None:
        respx_mock.post(url__startswith=MANTLE_MESSAGES_URL).mock(return_value=httpx2.Response(200, json={}))
        client = client.with_options(default_headers={"Anthropic-User-Profile-Id": "uprof_default"})

        send(client, user_profile_id)

        [request] = sent_requests(respx_mock)
        assert request.headers["anthropic-user-profile-id"] == sent
        assert "user_profile_id" not in json.loads(request.content)

    @pytest.mark.parametrize(
        ("user_profile_id", "sent"), [(omit, "uprof_default"), ("uprof_argument", "uprof_argument")]
    )
    @pytest.mark.parametrize("send", [async_create_batch, async_beta_create_batch])
    @pytest.mark.respx()
    async def test_async_batches_send_the_client_default_header_unless_the_request_names_one(
        self,
        send: AsyncSendBatch,
        user_profile_id: str | Omit,
        sent: str,
        async_client: AsyncAnthropicBedrockMantle,
        respx_mock: MockRouter,
    ) -> None:
        respx_mock.post(url__startswith=MANTLE_MESSAGES_URL).mock(return_value=httpx2.Response(200, json={}))
        async_client = async_client.with_options(default_headers={"Anthropic-User-Profile-Id": "uprof_default"})

        await send(async_client, user_profile_id)

        [request] = sent_requests(respx_mock)
        assert request.headers["anthropic-user-profile-id"] == sent
        assert "user_profile_id" not in json.loads(request.content)

    @pytest.mark.respx()
    def test_client_workspace_id_is_kept(self, client: AnthropicBedrockMantle, respx_mock: MockRouter) -> None:
        respx_mock.post(url__startswith=MANTLE_MESSAGES_URL).mock(side_effect=respond_with_message)
        client = client.with_options(default_headers={"Anthropic-Workspace-Id": "wrkspc_default"})

        client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "Hi"}], model=MODEL)
        client.messages.create(
            max_tokens=16, messages=[{"role": "user", "content": "Hi"}], model=MODEL, workspace_id="wrkspc_argument"
        )
        client.messages.batches.create(requests=[])

        default_request, argument_request, batch_request = sent_requests(respx_mock)
        assert default_request.headers["anthropic-workspace-id"] == "wrkspc_default"
        assert argument_request.headers["anthropic-workspace-id"] == "wrkspc_argument"
        assert batch_request.headers["anthropic-workspace-id"] == "wrkspc_default"

    @pytest.mark.respx()
    async def test_async_client_workspace_id_is_kept(
        self, async_client: AsyncAnthropicBedrockMantle, respx_mock: MockRouter
    ) -> None:
        respx_mock.post(url__startswith=MANTLE_MESSAGES_URL).mock(side_effect=respond_with_message)
        async_client = async_client.with_options(default_headers={"Anthropic-Workspace-Id": "wrkspc_default"})

        await async_client.messages.create(max_tokens=16, messages=[{"role": "user", "content": "Hi"}], model=MODEL)
        await async_client.messages.create(
            max_tokens=16, messages=[{"role": "user", "content": "Hi"}], model=MODEL, workspace_id="wrkspc_argument"
        )
        await async_client.messages.batches.create(requests=[])

        default_request, argument_request, batch_request = sent_requests(respx_mock)
        assert default_request.headers["anthropic-workspace-id"] == "wrkspc_default"
        assert argument_request.headers["anthropic-workspace-id"] == "wrkspc_argument"
        assert batch_request.headers["anthropic-workspace-id"] == "wrkspc_default"

    @pytest.mark.respx()
    def test_per_request_omit_keeps_the_client_default(
        self, client: AnthropicBedrockMantle, respx_mock: MockRouter
    ) -> None:
        respx_mock.post(url__startswith=MANTLE_MESSAGES_URL).mock(side_effect=respond_with_message)
        client = client.with_options(default_headers={"Anthropic-User-Profile-Id": "uprof_default"})

        client.messages.create(
            max_tokens=16,
            messages=[{"role": "user", "content": "Hi"}],
            model=MODEL,
            extra_headers={"Anthropic-User-Profile-Id": omit},
        )
        client.messages.batches.create(requests=[], extra_headers={"Anthropic-User-Profile-Id": omit})

        message_request, batch_request = sent_requests(respx_mock)
        assert json.loads(message_request.content)["user_profile_id"] == "uprof_default"
        assert batch_request.headers["anthropic-user-profile-id"] == "uprof_default"

    @pytest.mark.respx()
    async def test_async_per_request_omit_keeps_the_client_default(
        self, async_client: AsyncAnthropicBedrockMantle, respx_mock: MockRouter
    ) -> None:
        respx_mock.post(url__startswith=MANTLE_MESSAGES_URL).mock(side_effect=respond_with_message)
        async_client = async_client.with_options(default_headers={"Anthropic-User-Profile-Id": "uprof_default"})

        await async_client.messages.create(
            max_tokens=16,
            messages=[{"role": "user", "content": "Hi"}],
            model=MODEL,
            extra_headers={"Anthropic-User-Profile-Id": omit},
        )
        await async_client.messages.batches.create(requests=[], extra_headers={"Anthropic-User-Profile-Id": omit})

        message_request, batch_request = sent_requests(respx_mock)
        assert json.loads(message_request.content)["user_profile_id"] == "uprof_default"
        assert batch_request.headers["anthropic-user-profile-id"] == "uprof_default"
