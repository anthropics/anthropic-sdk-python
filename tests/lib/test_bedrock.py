import re
import json
import typing as t
import tempfile
import threading
from typing import TypedDict, cast
from typing_extensions import Protocol

import httpx
import pytest
from respx import MockRouter

from anthropic import AnthropicBedrock, AsyncAnthropicBedrock, beta_tool, beta_async_tool
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.bedrock._stream_decoder import _chunk_bytes_to_sse

sync_client = AnthropicBedrock(
    aws_region="us-east-1",
    aws_access_key="example-access-key",
    aws_secret_key="example-secret-key",
)
async_client = AsyncAnthropicBedrock(
    aws_region="us-east-1",
    aws_access_key="example-access-key",
    aws_secret_key="example-secret-key",
)


class MockRequestCall(Protocol):
    request: httpx.Request


class AwsConfigProfile(TypedDict):
    # Available regions: https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html#available-regions
    name: t.Union[t.Literal["default"], str]
    region: str


def profile_to_ini(profile: AwsConfigProfile) -> str:
    """
    Convert an AWS config profile to an INI format string.
    """

    profile_name = profile["name"] if profile["name"] == "default" else f"profile {profile['name']}"
    return f"[{profile_name}]\nregion = {profile['region']}\n"


@pytest.fixture
def profiles() -> t.List[AwsConfigProfile]:
    return [
        {"name": "default", "region": "us-east-2"},
    ]


@pytest.fixture
def mock_aws_config(
    profiles: t.List[AwsConfigProfile],
    monkeypatch: t.Any,
) -> t.Iterable[None]:
    with tempfile.NamedTemporaryFile(mode="w+", delete=True) as temp_file:
        for profile in profiles:
            temp_file.write(profile_to_ini(profile))
        temp_file.flush()
        monkeypatch.setenv("AWS_CONFIG_FILE", str(temp_file.name))
        yield


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
def test_messages_retries(respx_mock: MockRouter) -> None:
    respx_mock.post(re.compile(r"https://bedrock-runtime\.us-east-1\.amazonaws\.com/model/.*/invoke")).mock(
        side_effect=[
            httpx.Response(500, json={"error": "server error"}, headers={"retry-after-ms": "10"}),
            httpx.Response(200, json={"foo": "bar"}),
        ]
    )

    sync_client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Say hello there!",
            }
        ],
        model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    )

    calls = cast("list[MockRequestCall]", respx_mock.calls)

    assert len(calls) == 2

    assert (
        calls[0].request.url
        == "https://bedrock-runtime.us-east-1.amazonaws.com/model/anthropic.claude-3-5-sonnet-20241022-v2:0/invoke"
    )
    assert (
        calls[1].request.url
        == "https://bedrock-runtime.us-east-1.amazonaws.com/model/anthropic.claude-3-5-sonnet-20241022-v2:0/invoke"
    )


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
@pytest.mark.asyncio()
async def test_messages_retries_async(respx_mock: MockRouter) -> None:
    respx_mock.post(re.compile(r"https://bedrock-runtime\.us-east-1\.amazonaws\.com/model/.*/invoke")).mock(
        side_effect=[
            httpx.Response(500, json={"error": "server error"}, headers={"retry-after-ms": "10"}),
            httpx.Response(200, json={"foo": "bar"}),
        ]
    )

    await async_client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Say hello there!",
            }
        ],
        model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    )

    calls = cast("list[MockRequestCall]", respx_mock.calls)

    assert len(calls) == 2

    assert (
        calls[0].request.url
        == "https://bedrock-runtime.us-east-1.amazonaws.com/model/anthropic.claude-3-5-sonnet-20241022-v2:0/invoke"
    )
    assert (
        calls[1].request.url
        == "https://bedrock-runtime.us-east-1.amazonaws.com/model/anthropic.claude-3-5-sonnet-20241022-v2:0/invoke"
    )


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
def test_application_inference_profile(respx_mock: MockRouter) -> None:
    respx_mock.post(re.compile(r"https://bedrock-runtime\.us-east-1\.amazonaws\.com/model/.*/invoke")).mock(
        side_effect=[
            httpx.Response(500, json={"error": "server error"}, headers={"retry-after-ms": "10"}),
            httpx.Response(200, json={"foo": "bar"}),
        ]
    )

    sync_client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Say hello there!",
            }
        ],
        model="arn:aws:bedrock:us-east-1:123456789012:application-inference-profile/jf2sje1c0jnb",
    )

    calls = cast("list[MockRequestCall]", respx_mock.calls)
    assert len(calls) == 2

    assert (
        calls[0].request.url
        == "https://bedrock-runtime.us-east-1.amazonaws.com/model/arn:aws:bedrock:us-east-1:123456789012:application-inference-profile%2Fjf2sje1c0jnb/invoke"
    )
    assert (
        calls[1].request.url
        == "https://bedrock-runtime.us-east-1.amazonaws.com/model/arn:aws:bedrock:us-east-1:123456789012:application-inference-profile%2Fjf2sje1c0jnb/invoke"
    )


sync_api_key_client = AnthropicBedrock(
    aws_region="us-east-1",
    api_key="test-api-key",
)
async_api_key_client = AsyncAnthropicBedrock(
    aws_region="us-east-1",
    api_key="test-api-key",
)


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
def test_api_key_auth(respx_mock: MockRouter) -> None:
    respx_mock.post(re.compile(r"https://bedrock-runtime\.us-east-1\.amazonaws\.com/model/.*/invoke")).mock(
        return_value=httpx.Response(200, json={"foo": "bar"}),
    )

    sync_api_key_client.messages.create(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Say hello there!"}],
        model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    )

    calls = cast("list[MockRequestCall]", respx_mock.calls)
    assert len(calls) == 1
    assert calls[0].request.headers["Authorization"] == "Bearer test-api-key"


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
@pytest.mark.asyncio()
async def test_api_key_auth_async(respx_mock: MockRouter) -> None:
    respx_mock.post(re.compile(r"https://bedrock-runtime\.us-east-1\.amazonaws\.com/model/.*/invoke")).mock(
        return_value=httpx.Response(200, json={"foo": "bar"}),
    )

    await async_api_key_client.messages.create(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Say hello there!"}],
        model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    )

    calls = cast("list[MockRequestCall]", respx_mock.calls)
    assert len(calls) == 1
    assert calls[0].request.headers["Authorization"] == "Bearer test-api-key"


def test_api_key_from_env(monkeypatch: t.Any) -> None:
    monkeypatch.setenv("AWS_BEARER_TOKEN_BEDROCK", "env-api-key")
    client = AnthropicBedrock(aws_region="us-east-1")
    assert client.api_key == "env-api-key"


def test_api_key_mutual_exclusion() -> None:
    with pytest.raises(ValueError, match="Cannot specify both"):
        AnthropicBedrock(
            aws_region="us-east-1",
            api_key="test-api-key",
            aws_access_key="example-access-key",
        )


def test_api_key_mutual_exclusion_async() -> None:
    with pytest.raises(ValueError, match="Cannot specify both"):
        AsyncAnthropicBedrock(
            aws_region="us-east-1",
            api_key="test-api-key",
            aws_secret_key="example-secret-key",
        )


def test_api_key_env_mutual_exclusion(monkeypatch: t.Any) -> None:
    monkeypatch.setenv("AWS_BEARER_TOKEN_BEDROCK", "env-api-key")
    with pytest.raises(ValueError, match="Cannot specify both"):
        AnthropicBedrock(
            aws_region="us-east-1",
            aws_access_key="example-access-key",
        )


def test_region_infer_from_profile(
    mock_aws_config: None,  # noqa: ARG001
    profiles: t.List[AwsConfigProfile],
) -> None:
    client = AnthropicBedrock()
    assert client.aws_region == profiles[0]["region"]


@pytest.mark.parametrize(
    "profiles, aws_profile",
    [
        pytest.param([{"name": "default", "region": "us-east-2"}], "default", id="default profile"),
        pytest.param(
            [{"name": "default", "region": "us-east-2"}, {"name": "custom", "region": "us-west-1"}],
            "custom",
            id="custom profile",
        ),
    ],
)
def test_region_infer_from_specified_profile(
    mock_aws_config: None,  # noqa: ARG001
    profiles: t.List[AwsConfigProfile],
    aws_profile: str,
    monkeypatch: t.Any,
) -> None:
    monkeypatch.setenv("AWS_PROFILE", aws_profile)
    client = AnthropicBedrock()

    assert client.aws_region == next(profile for profile in profiles if profile["name"] == aws_profile)["region"]


def test_chunk_bytes_to_sse_typed_event() -> None:
    raw = (
        b'{"type":"message_start","message":{"id":"msg_123","type":"message","role":"assistant",'
        b'"content":[],"model":"claude-x","stop_reason":null,"stop_sequence":null,'
        b'"usage":{"input_tokens":1,"output_tokens":1}}}'
    )
    sse = _chunk_bytes_to_sse(raw)
    assert sse is not None
    assert sse.event == "message_start"
    assert sse.data == raw.decode()


def test_chunk_bytes_to_sse_legacy_completion() -> None:
    raw = b'{"completion":" Hello","stop_reason":null,"model":"claude-2"}'
    sse = _chunk_bytes_to_sse(raw)
    assert sse is not None
    assert sse.event == "completion"


def test_chunk_bytes_to_sse_legacy_completion_with_metrics() -> None:
    raw = (
        b'{"completion":" Hello","stop_reason":"stop_sequence","model":"claude-2",'
        b'"amazon-bedrock-invocationMetrics":{"inputTokenCount":1,"outputTokenCount":1}}'
    )
    sse = _chunk_bytes_to_sse(raw)
    assert sse is not None
    assert sse.event == "completion"


def test_copy_x_stainless_helper_header_appends() -> None:
    # `x-stainless-helper` accumulates across copies instead of being clobbered
    client = sync_client.with_options(default_headers={"x-stainless-helper": "parent"})
    copied = client.with_options(default_headers={"x-stainless-helper": "child"})
    assert copied.default_headers["x-stainless-helper"] == "parent, child"


def test_async_copy_x_stainless_helper_header_appends() -> None:
    # `x-stainless-helper` accumulates across copies instead of being clobbered
    client = async_client.with_options(default_headers={"x-stainless-helper": "parent"})
    copied = client.with_options(default_headers={"x-stainless-helper": "child"})
    assert copied.default_headers["x-stainless-helper"] == "parent, child"


def _bedrock_message(content: t.List[t.Dict[str, t.Any]], stop_reason: str) -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "id": "msg_01",
            "type": "message",
            "role": "assistant",
            "model": "claude",
            "content": content,
            "stop_reason": stop_reason,
            "stop_sequence": None,
            "usage": {"input_tokens": 10, "output_tokens": 5},
        },
    )


def _tool_runner_responses() -> t.List[httpx.Response]:
    return [
        _bedrock_message(
            [{"type": "tool_use", "id": "toolu_01", "name": "get_weather", "input": {"city": "Paris"}}],
            "tool_use",
        ),
        _bedrock_message([{"type": "text", "text": "It is sunny in Paris."}], "end_turn"),
    ]


def _assert_tool_runner_calls(calls: t.List[MockRequestCall]) -> None:
    assert len(calls) == 2
    for call in calls:
        assert call.request.url.path == "/model/anthropic.claude-haiku-4-5-20251001-v1:0/invoke"
        assert call.request.headers["Authorization"].startswith("AWS4-HMAC-SHA256 ")
        assert "x-amz-date" in call.request.headers
        body = json.loads(call.request.content)
        assert "model" not in body and "stream" not in body and "output_format" not in body
        assert body["anthropic_version"] == "bedrock-2023-05-31"
    second = json.loads(calls[1].request.content)
    assert [m["role"] for m in second["messages"]] == ["user", "assistant", "user"]
    assert second["messages"][1]["content"][0]["type"] == "tool_use"
    assert second["messages"][2]["content"][0] == {
        "type": "tool_result",
        "tool_use_id": "toolu_01",
        "content": "sunny in Paris",
    }


@pytest.mark.skipif(PYDANTIC_V1, reason="tool functions are only supported with pydantic v2")
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
def test_beta_tool_runner_routes_through_invoke(respx_mock: MockRouter) -> None:
    @beta_tool
    def get_weather(city: str) -> str:
        """Get the weather.

        Args:
            city: city name
        """
        return f"sunny in {city}"

    respx_mock.post(re.compile(r"https://bedrock-runtime\.us-east-1\.amazonaws\.com/model/.*")).mock(
        side_effect=_tool_runner_responses()
    )

    final = sync_client.beta.messages.tool_runner(
        model="anthropic.claude-haiku-4-5-20251001-v1:0",
        max_tokens=256,
        messages=[{"role": "user", "content": "weather in Paris?"}],
        tools=[get_weather],
    ).until_done()

    assert final.stop_reason == "end_turn"
    _assert_tool_runner_calls(cast("list[MockRequestCall]", respx_mock.calls))


@pytest.mark.skipif(PYDANTIC_V1, reason="tool functions are only supported with pydantic v2")
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
@pytest.mark.asyncio()
async def test_beta_tool_runner_routes_through_invoke_async(respx_mock: MockRouter) -> None:
    @beta_async_tool
    async def get_weather(city: str) -> str:
        """Get the weather.

        Args:
            city: city name
        """
        return f"sunny in {city}"

    respx_mock.post(re.compile(r"https://bedrock-runtime\.us-east-1\.amazonaws\.com/model/.*")).mock(
        side_effect=_tool_runner_responses()
    )

    final = await async_client.beta.messages.tool_runner(
        model="anthropic.claude-haiku-4-5-20251001-v1:0",
        max_tokens=256,
        messages=[{"role": "user", "content": "weather in Paris?"}],
        tools=[get_weather],
    ).until_done()

    assert final.stop_reason == "end_turn"
    _assert_tool_runner_calls(cast("list[MockRequestCall]", respx_mock.calls))


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_beta_messages_helpers_are_bound() -> None:
    for client in (sync_client, async_client):
        for name in ("create", "parse", "stream", "tool_runner"):
            assert callable(getattr(client.beta.messages, name))


@pytest.mark.asyncio()
async def test_sigv4_signing_runs_off_event_loop_async(monkeypatch: pytest.MonkeyPatch) -> None:
    signing_threads: t.List[int] = []

    def fake_get_auth_headers(**_: object) -> t.Dict[str, str]:
        signing_threads.append(threading.get_ident())
        return {"Authorization": "AWS4-HMAC-SHA256 stub"}

    monkeypatch.setattr("anthropic.lib.bedrock._auth.get_auth_headers", fake_get_auth_headers)

    request = httpx.Request("POST", "https://bedrock-runtime.us-east-1.amazonaws.com/model/x/invoke", content=b"{}")
    await async_client._prepare_request(request)

    assert len(signing_threads) == 1
    assert signing_threads[0] != threading.get_ident()
    assert request.headers["Authorization"] == "AWS4-HMAC-SHA256 stub"
