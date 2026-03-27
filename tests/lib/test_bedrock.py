import re
import typing as t
import inspect
import tempfile
from contextlib import AbstractAsyncContextManager, AbstractContextManager
from typing import Any, TypedDict, cast
from typing_extensions import Protocol

import httpx
import pytest
from respx import MockRouter

from anthropic import AnthropicBedrock, AsyncAnthropicBedrock

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


@pytest.mark.asyncio()
async def test_beta_messages_stream_exists_async() -> None:
    stream_ctx = async_client.beta.messages.stream(
        max_tokens=1,
        messages=[{"role": "user", "content": "hello"}],
        model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    )

    assert isinstance(stream_ctx, AbstractAsyncContextManager)


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
