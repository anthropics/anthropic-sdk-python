import re
from typing import cast
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
        model="anthropic.claude-3-sonnet-20240229-v1:0",
    )

    calls = cast("list[MockRequestCall]", respx_mock.calls)

    assert len(calls) == 2

    assert (
        calls[0].request.url
        == "https://bedrock-runtime.us-east-1.amazonaws.com/model/anthropic.claude-3-sonnet-20240229-v1:0/invoke"
    )
    assert (
        calls[1].request.url
        == "https://bedrock-runtime.us-east-1.amazonaws.com/model/anthropic.claude-3-sonnet-20240229-v1:0/invoke"
    )


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
        model="anthropic.claude-3-sonnet-20240229-v1:0",
    )

    calls = cast("list[MockRequestCall]", respx_mock.calls)

    assert len(calls) == 2

    assert (
        calls[0].request.url
        == "https://bedrock-runtime.us-east-1.amazonaws.com/model/anthropic.claude-3-sonnet-20240229-v1:0/invoke"
    )
    assert (
        calls[1].request.url
        == "https://bedrock-runtime.us-east-1.amazonaws.com/model/anthropic.claude-3-sonnet-20240229-v1:0/invoke"
    )
