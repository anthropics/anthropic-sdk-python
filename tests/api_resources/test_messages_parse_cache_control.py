"""Regression: Messages.parse / AsyncMessages.parse must accept cache_control."""

from __future__ import annotations

import json

import httpx2
import pytest
from pydantic import BaseModel
from respx import MockRouter

from anthropic import Anthropic, AsyncAnthropic, _compat


MESSAGE_JSON = {
    "id": "msg_123",
    "type": "message",
    "role": "assistant",
    "model": "claude-sonnet-4-5",
    "content": [{"text": '{"name": "Ada"}', "type": "text"}],
    "stop_reason": "end_turn",
    "usage": {"input_tokens": 10, "output_tokens": 5},
}


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="parse with Pydantic models requires Pydantic v2")
def test_parse_forwards_cache_control(client: Anthropic, respx_mock: MockRouter) -> None:
    class User(BaseModel):
        name: str

    respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE_JSON))

    client.messages.parse(
        max_tokens=64,
        messages=[{"role": "user", "content": "hi"}],
        model="claude-sonnet-4-5",
        output_format=User,
        cache_control={"type": "ephemeral"},
    )

    body = json.loads(respx_mock.calls.last.request.content)
    assert body["cache_control"] == {"type": "ephemeral"}


@pytest.mark.skipif(_compat.PYDANTIC_V1, reason="parse with Pydantic models requires Pydantic v2")
@pytest.mark.asyncio
async def test_async_parse_forwards_cache_control(
    async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    class User(BaseModel):
        name: str

    respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE_JSON))

    await async_client.messages.parse(
        max_tokens=64,
        messages=[{"role": "user", "content": "hi"}],
        model="claude-sonnet-4-5",
        output_format=User,
        cache_control={"type": "ephemeral"},
    )

    body = json.loads(respx_mock.calls.last.request.content)
    assert body["cache_control"] == {"type": "ephemeral"}
