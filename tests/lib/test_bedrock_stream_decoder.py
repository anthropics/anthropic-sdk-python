from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from anthropic._streaming import ServerSentEvent
from anthropic.lib.bedrock._stream_decoder import AWSEventStreamDecoder


def make_mock_event(status_code: int, body: bytes, headers: dict[str, str] | None = None) -> MagicMock:
    """Create a mock botocore EventStreamMessage with the given response dict."""
    event = MagicMock()
    event.to_response_dict.return_value = {
        "status_code": status_code,
        "headers": headers or {},
        "body": body,
    }
    return event


class TestParseMessageFromEvent:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        with patch("anthropic.lib.bedrock._stream_decoder.AWSEventStreamDecoder.__init__", lambda _self: None):
            self.decoder = AWSEventStreamDecoder()
            self.decoder.parser = MagicMock()

    def test_success_returns_completion_event(self) -> None:
        chunk_data = json.dumps({"type": "message_start"}).encode()
        self.decoder.parser.parse.return_value = {"chunk": {"bytes": chunk_data}}

        event = make_mock_event(200, b"")
        result = self.decoder._parse_message_from_event(event)

        assert result is not None
        assert result.event == "completion"
        assert result.data == chunk_data.decode()

    def test_success_no_chunk_returns_none(self) -> None:
        self.decoder.parser.parse.return_value = {}

        event = make_mock_event(200, b"")
        result = self.decoder._parse_message_from_event(event)

        assert result is None

    def test_non_200_returns_error_event(self) -> None:
        error_body = json.dumps({"message": "The system encountered an unexpected error"}).encode()
        self.decoder.parser.parse.return_value = {}

        event = make_mock_event(
            400,
            error_body,
            headers={":exception-type": "internalServerException", ":content-type": "application/json"},
        )
        result = self.decoder._parse_message_from_event(event)

        assert result is not None
        assert result.event == "error"
        parsed = result.json()
        assert parsed["type"] == "error"
        assert parsed["error"]["type"] == "api_error"
        assert parsed["error"]["message"] == "The system encountered an unexpected error"

    def test_non_200_with_non_json_body(self) -> None:
        self.decoder.parser.parse.return_value = {}

        event = make_mock_event(500, b"Internal Server Error")
        result = self.decoder._parse_message_from_event(event)

        assert result is not None
        assert result.event == "error"
        parsed = result.json()
        assert parsed["type"] == "error"
        assert parsed["error"]["message"] == "Internal Server Error"

    def test_non_200_with_empty_body(self) -> None:
        self.decoder.parser.parse.return_value = {}

        event = make_mock_event(429, b"")
        result = self.decoder._parse_message_from_event(event)

        assert result is not None
        assert result.event == "error"
        parsed = result.json()
        assert parsed["type"] == "error"
        assert parsed["error"]["message"] == "Bad response code: 429"

    def test_non_200_does_not_raise_value_error(self) -> None:
        """Regression test for issue #1477: non-200 should yield an error event, not raise ValueError."""
        error_body = json.dumps({"message": "Rate limited"}).encode()
        self.decoder.parser.parse.return_value = {}

        event = make_mock_event(
            400,
            error_body,
            headers={":exception-type": "throttlingException"},
        )

        # Should NOT raise ValueError — should return an error ServerSentEvent
        result = self.decoder._parse_message_from_event(event)
        assert result is not None
        assert isinstance(result, ServerSentEvent)
        assert result.event == "error"
