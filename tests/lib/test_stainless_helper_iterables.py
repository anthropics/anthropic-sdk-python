from __future__ import annotations

import json
from typing import cast

import httpx
import respx
import pytest

from anthropic import Anthropic
from anthropic.types.beta import BetaToolParam
from anthropic.lib._stainless_helpers import STAINLESS_HELPER_HEADER, tag_helper, stainless_helper_header

from ..conftest import base_url


class _TaggedDict(dict):  # type: ignore[type-arg]
    pass


def _message_json() -> dict[str, object]:
    return {
        "id": "msg_abc123",
        "type": "message",
        "role": "assistant",
        "model": "claude-sonnet-4-5",
        "content": [{"type": "text", "text": "hi"}],
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "usage": {"input_tokens": 1, "output_tokens": 1},
    }


def test_helper_collection_does_not_consume_generator() -> None:
    tool = cast("BetaToolParam", _TaggedDict({"name": "t", "input_schema": {"type": "object"}}))
    tag_helper(tool, "mcp_tool")
    tools = (item for item in [tool])

    assert stainless_helper_header(tools=tools) == {}
    assert list(tools) == [tool]


def test_helper_collection_still_reads_replayable_sequences() -> None:
    tool = cast("BetaToolParam", _TaggedDict({"name": "t", "input_schema": {"type": "object"}}))
    tag_helper(tool, "mcp_tool")

    assert stainless_helper_header(tools=[tool]) == {STAINLESS_HELPER_HEADER: "mcp_tool"}


@pytest.mark.respx(base_url=base_url)
def test_message_generator_reaches_request_body(client: Anthropic, respx_mock: respx.MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=_message_json()))

    messages = ({"role": "user", "content": text} for text in ["hello"])
    client.beta.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=16,
        messages=messages,
    )

    body = json.loads(respx_mock.calls.last.request.content)
    assert body["messages"] == [{"role": "user", "content": "hello"}]


@pytest.mark.respx(base_url=base_url)
def test_tool_generator_reaches_request_body(client: Anthropic, respx_mock: respx.MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=_message_json()))

    tool = cast(
        "BetaToolParam",
        _TaggedDict({"name": "t", "description": "d", "input_schema": {"type": "object"}}),
    )
    tag_helper(tool, "mcp_tool")
    tools = (item for item in [tool])

    client.beta.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=16,
        messages=[{"role": "user", "content": "hello"}],
        tools=tools,
    )

    body = json.loads(respx_mock.calls.last.request.content)
    assert body["tools"] == [{"name": "t", "description": "d", "input_schema": {"type": "object"}}]
