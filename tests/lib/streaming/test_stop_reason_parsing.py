from __future__ import annotations

import os
import json

import httpx
import pytest
from respx import MockRouter
from pydantic import BaseModel, ValidationError

from anthropic import Anthropic
from anthropic._compat import PYDANTIC_V1

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
sync_client = Anthropic(base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True)

pytestmark = pytest.mark.skipif(PYDANTIC_V1, reason="structured outputs not supported with pydantic v1")


class ParsedValue(BaseModel):
    value: int


def _stream_response(*, text: str, stop_reason: str) -> httpx.Response:
    events = [
        {
            "type": "message_start",
            "message": {
                "id": "msg_test",
                "type": "message",
                "role": "assistant",
                "content": [],
                "model": "claude-test",
                "stop_reason": None,
                "stop_sequence": None,
                "usage": {"input_tokens": 10, "output_tokens": 1},
            },
        },
        {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}},
        {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": text}},
        {"type": "content_block_stop", "index": 0},
        {
            "type": "message_delta",
            "delta": {"stop_reason": stop_reason, "stop_sequence": None},
            "usage": {"output_tokens": 8},
        },
        {"type": "message_stop"},
    ]
    body = "".join(f"event: {event['type']}\ndata: {json.dumps(event)}\n\n" for event in events)
    return httpx.Response(200, headers={"content-type": "text/event-stream"}, content=body.encode())


@pytest.mark.respx(base_url=base_url)
def test_messages_stream_preserves_max_tokens_stop_reason(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(return_value=_stream_response(text='{"value":', stop_reason="max_tokens"))

    with sync_client.messages.stream(
        model="claude-test",
        max_tokens=8,
        output_format=ParsedValue,
        messages=[{"role": "user", "content": "x"}],
    ) as stream:
        message = stream.get_final_message()

    assert message.stop_reason == "max_tokens"
    assert message.content[0].type == "text"
    assert message.content[0].text == '{"value":'
    assert message.parsed_output is None


@pytest.mark.respx(base_url=base_url)
def test_beta_messages_stream_preserves_max_tokens_stop_reason(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages?beta=true").mock(
        return_value=_stream_response(text='{"value":', stop_reason="max_tokens")
    )

    with pytest.warns(DeprecationWarning, match="output_format.*deprecated"):
        manager = sync_client.beta.messages.stream(
            model="claude-test",
            max_tokens=8,
            output_format=ParsedValue,
            messages=[{"role": "user", "content": "x"}],
        )

    with manager as stream:
        message = stream.get_final_message()

    assert message.stop_reason == "max_tokens"
    assert message.content[0].type == "text"
    assert message.content[0].text == '{"value":'
    assert message.parsed_output is None


@pytest.mark.respx(base_url=base_url)
def test_messages_stream_still_parses_completed_output(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(return_value=_stream_response(text='{"value": 7}', stop_reason="end_turn"))

    with sync_client.messages.stream(
        model="claude-test",
        max_tokens=8,
        output_format=ParsedValue,
        messages=[{"role": "user", "content": "x"}],
    ) as stream:
        message = stream.get_final_message()

    assert message.stop_reason == "end_turn"
    assert message.parsed_output == ParsedValue(value=7)


@pytest.mark.respx(base_url=base_url)
def test_messages_stream_still_rejects_invalid_completed_output(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(return_value=_stream_response(text="not json", stop_reason="end_turn"))

    with pytest.raises(ValidationError):
        with sync_client.messages.stream(
            model="claude-test",
            max_tokens=8,
            output_format=ParsedValue,
            messages=[{"role": "user", "content": "x"}],
        ) as stream:
            stream.get_final_message()
