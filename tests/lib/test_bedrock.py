import re
import typing as t
import tempfile
from typing import TypedDict, cast
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


class TestAnthropicBedrock:
    client = AnthropicBedrock(
        aws_region="us-east-1",
        aws_access_key="example-access-key",
        aws_secret_key="example-secret-key",
    )

    def test_copy(self) -> None:
        copied = self.client.copy()
        assert id(copied) != id(self.client)

        copied = self.client.copy(
            aws_region="us-west-2",
            aws_access_key="another-access-key",
            aws_secret_key="another-secret-key",
        )
        assert copied.aws_region == "us-west-2"
        assert self.client.aws_region == "us-east-1"
        assert copied.aws_access_key == "another-access-key"
        assert self.client.aws_access_key == "example-access-key"
        assert copied.aws_secret_key == "another-secret-key"
        assert self.client.aws_secret_key == "example-secret-key"

    def test_with_options(self) -> None:
        copied = self.client.with_options(
            aws_region="us-west-2",
            aws_access_key="another-access-key",
            aws_secret_key="another-secret-key",
        )
        assert copied.aws_region == "us-west-2"
        assert self.client.aws_region == "us-east-1"
        assert copied.aws_access_key == "another-access-key"
        assert self.client.aws_access_key == "example-access-key"
        assert copied.aws_secret_key == "another-secret-key"
        assert self.client.aws_secret_key == "example-secret-key"

    def test_copy_default_options(self) -> None:
        # options that have a default are overridden correctly
        copied = self.client.copy(max_retries=7)
        assert copied.max_retries == 7
        assert self.client.max_retries == 2

        copied2 = copied.copy(max_retries=6)
        assert copied2.max_retries == 6
        assert copied.max_retries == 7

        # timeout
        assert isinstance(self.client.timeout, httpx.Timeout)
        copied = self.client.copy(timeout=None)
        assert copied.timeout is None
        assert isinstance(self.client.timeout, httpx.Timeout)

    def test_copy_default_headers(self) -> None:
        client = AnthropicBedrock(
            aws_region="us-east-1",
            aws_access_key="example-access-key",
            aws_secret_key="example-secret-key",
            default_headers={"X-Foo": "bar"},
        )
        assert client.default_headers["X-Foo"] == "bar"

        # does not override the already given value when not specified
        copied = client.copy()
        assert copied.default_headers["X-Foo"] == "bar"

        # merges already given headers
        copied = client.copy(default_headers={"X-Bar": "stainless"})
        assert copied.default_headers["X-Foo"] == "bar"
        assert copied.default_headers["X-Bar"] == "stainless"

        # uses new values for any already given headers
        copied = client.copy(default_headers={"X-Foo": "stainless"})
        assert copied.default_headers["X-Foo"] == "stainless"

        # set_default_headers

        # completely overrides already set values
        copied = client.copy(set_default_headers={})
        assert copied.default_headers.get("X-Foo") is None

        copied = client.copy(set_default_headers={"X-Bar": "Robert"})
        assert copied.default_headers["X-Bar"] == "Robert"

        with pytest.raises(
            ValueError,
            match="`default_headers` and `set_default_headers` arguments are mutually exclusive",
        ):
            client.copy(set_default_headers={}, default_headers={"X-Foo": "Bar"})

    def test_copy_default_query(self) -> None:
        client = AnthropicBedrock(
            aws_region="us-east-1",
            aws_access_key="example-access-key",
            aws_secret_key="example-secret-key",
            default_query={"foo": "bar"},
        )
        assert client.default_query["foo"] == "bar"

        # does not override the already given value when not specified
        copied = client.copy()
        assert copied.default_query["foo"] == "bar"

        # merges already given params
        copied = client.copy(default_query={"bar": "stainless"})
        assert copied.default_query["foo"] == "bar"
        assert copied.default_query["bar"] == "stainless"

        # uses new values for any already given params
        copied = client.copy(default_query={"foo": "stainless"})
        assert copied.default_query["foo"] == "stainless"

        # set_default_query

        # completely overrides already set values
        copied = client.copy(set_default_query={})
        assert copied.default_query == {}

        copied = client.copy(set_default_query={"bar": "Robert"})
        assert copied.default_query["bar"] == "Robert"

        with pytest.raises(
            ValueError,
            match="`default_query` and `set_default_query` arguments are mutually exclusive",
        ):
            client.copy(set_default_query={}, default_query={"foo": "Bar"})


class TestAsyncAnthropicBedrock:
    client = AsyncAnthropicBedrock(
        aws_region="us-east-1",
        aws_access_key="example-access-key",
        aws_secret_key="example-secret-key",
    )

    def test_copy(self) -> None:
        copied = self.client.copy()
        assert id(copied) != id(self.client)

        copied = self.client.copy(
            aws_region="us-west-2",
            aws_access_key="another-access-key",
            aws_secret_key="another-secret-key",
        )
        assert copied.aws_region == "us-west-2"
        assert self.client.aws_region == "us-east-1"
        assert copied.aws_access_key == "another-access-key"
        assert self.client.aws_access_key == "example-access-key"
        assert copied.aws_secret_key == "another-secret-key"
        assert self.client.aws_secret_key == "example-secret-key"

    def test_with_options(self) -> None:
        copied = self.client.with_options(
            aws_region="us-west-2",
            aws_access_key="another-access-key",
            aws_secret_key="another-secret-key",
        )
        assert copied.aws_region == "us-west-2"
        assert self.client.aws_region == "us-east-1"
        assert copied.aws_access_key == "another-access-key"
        assert self.client.aws_access_key == "example-access-key"
        assert copied.aws_secret_key == "another-secret-key"
        assert self.client.aws_secret_key == "example-secret-key"

    def test_copy_default_options(self) -> None:
        # options that have a default are overridden correctly
        copied = self.client.copy(max_retries=7)
        assert copied.max_retries == 7
        assert self.client.max_retries == 2

        copied2 = copied.copy(max_retries=6)
        assert copied2.max_retries == 6
        assert copied.max_retries == 7

        # timeout
        assert isinstance(self.client.timeout, httpx.Timeout)
        copied = self.client.copy(timeout=None)
        assert copied.timeout is None
        assert isinstance(self.client.timeout, httpx.Timeout)

    def test_copy_default_headers(self) -> None:
        client = AsyncAnthropicBedrock(
            aws_region="us-east-1",
            aws_access_key="example-access-key",
            aws_secret_key="example-secret-key",
            default_headers={"X-Foo": "bar"},
        )
        assert client.default_headers["X-Foo"] == "bar"

        # does not override the already given value when not specified
        copied = client.copy()
        assert copied.default_headers["X-Foo"] == "bar"

        # merges already given headers
        copied = client.copy(default_headers={"X-Bar": "stainless"})
        assert copied.default_headers["X-Foo"] == "bar"
        assert copied.default_headers["X-Bar"] == "stainless"

        # uses new values for any already given headers
        copied = client.copy(default_headers={"X-Foo": "stainless"})
        assert copied.default_headers["X-Foo"] == "stainless"

        # set_default_headers

        # completely overrides already set values
        copied = client.copy(set_default_headers={})
        assert copied.default_headers.get("X-Foo") is None

        copied = client.copy(set_default_headers={"X-Bar": "Robert"})
        assert copied.default_headers["X-Bar"] == "Robert"

        with pytest.raises(
            ValueError,
            match="`default_headers` and `set_default_headers` arguments are mutually exclusive",
        ):
            client.copy(set_default_headers={}, default_headers={"X-Foo": "Bar"})

    def test_copy_default_query(self) -> None:
        client = AsyncAnthropicBedrock(
            aws_region="us-east-1",
            aws_access_key="example-access-key",
            aws_secret_key="example-secret-key",
            default_query={"foo": "bar"},
        )
        assert client.default_query["foo"] == "bar"

        # does not override the already given value when not specified
        copied = client.copy()
        assert copied.default_query["foo"] == "bar"

        # merges already given params
        copied = client.copy(default_query={"bar": "stainless"})
        assert copied.default_query["foo"] == "bar"
        assert copied.default_query["bar"] == "stainless"

        # uses new values for any already given params
        copied = client.copy(default_query={"foo": "stainless"})
        assert copied.default_query["foo"] == "stainless"

        # set_default_query

        # completely overrides already set values
        copied = client.copy(set_default_query={})
        assert copied.default_query == {}

        copied = client.copy(set_default_query={"bar": "Robert"})
        assert copied.default_query["bar"] == "Robert"

        with pytest.raises(
            ValueError,
            match="`default_query` and `set_default_query` arguments are mutually exclusive",
        ):
            client.copy(set_default_query={}, default_query={"foo": "Bar"})
