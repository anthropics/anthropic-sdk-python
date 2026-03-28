import re
import typing as t
import inspect
import tempfile
from typing import Any, TypedDict, cast
from contextlib import AbstractContextManager, AbstractAsyncContextManager
from typing_extensions import Protocol

import httpx
import pytest
from respx import MockRouter

from anthropic import AnthropicBedrock, AsyncAnthropicBedrock
from anthropic.lib.streaming._beta_messages import (
    BetaMessageStreamManager,
    BetaAsyncMessageStreamManager,
)

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


def test_region_infer_from_profile(
    mock_aws_config: None,  # noqa: ARG001
    profiles: t.List[AwsConfigProfile],
) -> None:
    client = AnthropicBedrock()
    assert client.aws_region == profiles[0]["region"]


def test_beta_messages_stream_exists_sync() -> None:
    stream_ctx = sync_client.beta.messages.stream(
        max_tokens=1,
        messages=[{"role": "user", "content": "hello"}],
        model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    )

    assert isinstance(stream_ctx, AbstractContextManager)
    assert isinstance(stream_ctx, BetaMessageStreamManager)


@pytest.mark.asyncio()
async def test_beta_messages_stream_exists_async() -> None:
    stream_ctx = async_client.beta.messages.stream(
        max_tokens=1,
        messages=[{"role": "user", "content": "hello"}],
        model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    )

    assert isinstance(stream_ctx, AbstractAsyncContextManager)
    assert isinstance(stream_ctx, BetaAsyncMessageStreamManager)


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


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
def test_beta_messages_stream_method_parity(sync: bool) -> None:
    """
    Regression test: verify that beta.messages.stream exists and has the same
    signature as beta.messages.create (parity with first-party client).

    This ensures that code using client.beta.messages.stream() works when
    switching from Anthropic() to AnthropicBedrock().
    """
    client: Any = sync_client if sync else async_client

    sig = inspect.signature(client.beta.messages.stream)
    generated_sig = inspect.signature(client.beta.messages.create)

    errors: list[str] = []

    for name, generated_param in generated_sig.parameters.items():
        if name == "stream":
            # intentionally excluded
            continue

        if name == "output_format":
            continue

        custom_param = sig.parameters.get(name)
        if not custom_param:
            errors.append(f"the `{name}` param is missing")
            continue

        if custom_param.annotation != generated_param.annotation:
            errors.append(
                f"types for the `{name}` param do not match; generated={repr(generated_param.annotation)} custom={repr(custom_param.annotation)}"
            )
            continue

    if errors:
        raise AssertionError(
            f"{len(errors)} errors encountered with the {'sync' if sync else 'async'} client `beta.messages.stream()` method:\n\n"
            + "\n\n".join(errors)
        )


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
def test_bedrock_beta_messages_stream_returns_stream_manager_and_correct_interface(
    respx_mock: MockRouter,
) -> None:
    """Regression test: Bedrock beta.messages.stream() returns BetaMessageStreamManager
    with the correct context-manager interface.

    This verifies the full shape of the returned object (context manager protocol,
    text_stream, response, get_final_message, etc.), not just that it exists.
    """
    respx_mock.post(re.compile(r"https://bedrock-runtime\.us-east-1\.amazonaws\.com/model/.*/invoke-with-response-stream")).mock(
        return_value=httpx.Response(200, json={"foo": "bar"})
    )

    stream_manager = sync_client.beta.messages.stream(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Say hello"}],
        model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    )

    assert isinstance(stream_manager, BetaMessageStreamManager)

    assert hasattr(stream_manager, "__enter__")
    assert hasattr(stream_manager, "__exit__")
    assert callable(stream_manager.__enter__)  # type: ignore[misc]
    assert callable(stream_manager.__exit__)  # type: ignore[misc]

    with stream_manager as stream:
        assert hasattr(stream, "text_stream")
        assert hasattr(stream, "response")
        assert hasattr(stream, "get_final_message")
        assert hasattr(stream, "get_final_text")
        assert hasattr(stream, "until_done")
        assert hasattr(stream, "close")
        assert hasattr(stream, "__iter__")
        assert hasattr(stream, "__next__")


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.respx()
@pytest.mark.asyncio()
async def test_bedrock_beta_messages_stream_async_returns_stream_manager_and_correct_interface(
    respx_mock: MockRouter,
) -> None:
    """Async variant: verify async Bedrock beta.messages.stream() returns
    BetaAsyncMessageStreamManager with the correct async-context-manager interface.
    """
    respx_mock.post(re.compile(r"https://bedrock-runtime\.us-east-1\.amazonaws\.com/model/.*/invoke-with-response-stream")).mock(
        return_value=httpx.Response(200, json={"foo": "bar"})
    )

    stream_manager = async_client.beta.messages.stream(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Say hello"}],
        model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    )

    assert isinstance(stream_manager, BetaAsyncMessageStreamManager)

    assert hasattr(stream_manager, "__aenter__")
    assert hasattr(stream_manager, "__aexit__")
    assert callable(stream_manager.__aenter__)  # type: ignore[misc]
    assert callable(stream_manager.__aexit__)  # type: ignore[misc]

    async with stream_manager as stream:
        assert hasattr(stream, "text_stream")
        assert hasattr(stream, "response")
        assert hasattr(stream, "get_final_message")
        assert hasattr(stream, "get_final_text")
        assert hasattr(stream, "until_done")
        assert hasattr(stream, "close")
        assert hasattr(stream, "__aiter__")
        assert hasattr(stream, "__anext__")


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
def test_beta_messages_stream_returns_stream_manager_type(sync: bool) -> None:
    """
    Regression test: verify beta.messages.stream() returns the exact stream-manager
    type (BetaMessageStreamManager / BetaAsyncMessageStreamManager) via type annotation.
    """
    import typing

    client: Any = sync_client if sync else async_client
    expected_cls = BetaMessageStreamManager if sync else BetaAsyncMessageStreamManager

    assert client.beta.messages.stream is not None
    assert callable(client.beta.messages.stream)

    hints = typing.get_type_hints(client.beta.messages.stream)
    return_type = hints.get("return")
    assert return_type is not None
    origin = getattr(return_type, "__origin__", return_type)
    assert origin == expected_cls


def test_beta_messages_stream_with_raw_response_no_stream_alias() -> None:
    """
    Regression test: beta.messages.with_raw_response does NOT expose stream().
    """
    sync_wrappers = sync_client.beta.messages.with_raw_response
    assert hasattr(sync_wrappers, "create")
    assert not hasattr(sync_wrappers, "stream")

    async_wrappers = async_client.beta.messages.with_raw_response
    assert hasattr(async_wrappers, "create")
    assert not hasattr(async_wrappers, "stream")


def test_beta_messages_stream_with_streaming_response_no_stream_alias() -> None:
    """
    Regression test: beta.messages.with_streaming_response does NOT expose stream().
    """
    sync_wrappers = sync_client.beta.messages.with_streaming_response
    assert hasattr(sync_wrappers, "create")
    assert not hasattr(sync_wrappers, "stream")

    async_wrappers = async_client.beta.messages.with_streaming_response
    assert hasattr(async_wrappers, "create")
    assert not hasattr(async_wrappers, "stream")


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
def test_beta_messages_stream_is_first_party_alias(sync: bool) -> None:
    """
    Regression test: Bedrock beta.messages.stream is an alias of
    FirstPartyMessagesAPI.stream for the sync client.

    For async, the Bedrock stream() has a custom implementation
    (_DeferredAsyncStreamRequest pattern) because AsyncAPIResource._post is an
    async method that must be awaited inside the async with block.
    """
    from anthropic.resources.beta import Messages as FirstPartyMessages, AsyncMessages as FirstPartyAsyncMessages

    client: Any = sync_client if sync else async_client

    instance_stream = client.beta.messages.stream
    first_party_stream = FirstPartyMessages.stream if sync else FirstPartyAsyncMessages.stream

    if sync:
        instance_func = getattr(instance_stream, "__func__", instance_stream)
        assert instance_func is first_party_stream
    else:
        assert callable(instance_stream)


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
def test_beta_messages_stream_on_all_three_wrappers(sync: bool) -> None:
    """
    Regression test: verify stream() is accessible from:
      1. client.beta.messages.stream
      2. client.beta.messages.with_raw_response.stream (NOT, matches first-party)
      3. client.beta.messages.with_streaming_response.stream (NOT, matches first-party)
    """
    client: Any = sync_client if sync else async_client

    assert hasattr(client.beta.messages, "stream")
    assert callable(client.beta.messages.stream)

    assert not hasattr(client.beta.messages.with_raw_response, "stream")
    assert not hasattr(client.beta.messages.with_streaming_response, "stream")


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
def test_beta_messages_stream_return_annotation(sync: bool) -> None:
    """
    Regression test: verify the return type annotation of beta.messages.stream()
    is BetaMessageStreamManager / BetaAsyncMessageStreamManager.
    """
    import typing

    client: Any = sync_client if sync else async_client
    hints = typing.get_type_hints(client.beta.messages.stream)

    return_type = hints.get("return", None)
    assert return_type is not None
    repr_str = repr(return_type)
    assert "MessageStreamManager" in repr_str
