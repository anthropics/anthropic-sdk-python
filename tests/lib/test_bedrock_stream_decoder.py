from __future__ import annotations

import json

from anthropic.lib.bedrock._stream_decoder import AWSEventStreamDecoder


class TestGetSseEventType:
    def test_error_event_returns_error(self) -> None:
        decoder = _make_decoder()
        message = json.dumps(
            {
                "type": "error",
                "error": {"type": "rate_limit_error", "message": "Rate limited", "details": None},
                "request_id": "req_123",
            }
        )
        assert decoder._get_sse_event_type(message) == "error"

    def test_message_start_event_returns_completion(self) -> None:
        decoder = _make_decoder()
        message = json.dumps(
            {
                "type": "message_start",
                "message": {
                    "id": "msg_123",
                    "type": "message",
                    "role": "assistant",
                    "content": [],
                    "model": "claude-opus-4-7",
                    "stop_reason": None,
                    "stop_sequence": None,
                    "usage": {"input_tokens": 10, "output_tokens": 0},
                },
            }
        )
        assert decoder._get_sse_event_type(message) == "completion"

    def test_content_block_delta_returns_completion(self) -> None:
        decoder = _make_decoder()
        message = json.dumps(
            {
                "type": "content_block_delta",
                "index": 0,
                "delta": {"type": "text_delta", "text": "Hello"},
            }
        )
        assert decoder._get_sse_event_type(message) == "completion"

    def test_invalid_json_returns_completion(self) -> None:
        decoder = _make_decoder()
        assert decoder._get_sse_event_type("not json") == "completion"

    def test_non_dict_json_returns_completion(self) -> None:
        decoder = _make_decoder()
        assert decoder._get_sse_event_type('"just a string"') == "completion"

    def test_dict_without_type_returns_completion(self) -> None:
        decoder = _make_decoder()
        assert decoder._get_sse_event_type('{"foo": "bar"}') == "completion"


def _make_decoder() -> AWSEventStreamDecoder:
    return AWSEventStreamDecoder()
