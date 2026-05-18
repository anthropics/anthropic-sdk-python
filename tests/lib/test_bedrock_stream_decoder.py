from __future__ import annotations

import json
from unittest.mock import MagicMock

import httpx
import pytest

from anthropic import _exceptions
from anthropic.lib.bedrock._stream_decoder import AWSEventStreamDecoder


def _make_decoder() -> AWSEventStreamDecoder:
    decoder = AWSEventStreamDecoder()
    decoder.parser = MagicMock()
    decoder.parser.parse.return_value = {}
    return decoder


def _make_event(status_code: int, exception_type: str, body: bytes) -> MagicMock:
    event = MagicMock()
    event.to_response_dict.return_value = {
        "status_code": status_code,
        "headers": {":exception-type": exception_type},
        "body": body,
    }
    return event


class TestAWSEventStreamDecoderErrors:
    def test_non_200_frame_emits_error_sse(self) -> None:
        decoder = _make_decoder()
        body = json.dumps({"message": "Service unavailable"}).encode()
        event = _make_event(529, "overloadedException", body)

        sse = decoder._parse_message_from_event(event)

        assert sse is not None
        assert sse.event == "error"
        data = json.loads(sse.data)
        assert data["_bedrock_status"] == 529
        assert data["error"]["type"] == "overloadedException"
        assert data["error"]["message"] == "Service unavailable"

    def test_non_200_frame_500_internal_error(self) -> None:
        decoder = _make_decoder()
        body = json.dumps({"message": "Internal failure"}).encode()
        event = _make_event(500, "internalServerException", body)

        sse = decoder._parse_message_from_event(event)

        assert sse is not None
        data = json.loads(sse.data)
        assert data["_bedrock_status"] == 500
        assert data["error"]["type"] == "internalServerException"

    def test_non_200_frame_invalid_utf8_body(self) -> None:
        decoder = _make_decoder()
        body = b"\xff\xfe not valid utf-8 or json"
        event = _make_event(500, "internalServerException", body)

        sse = decoder._parse_message_from_event(event)

        assert sse is not None
        data = json.loads(sse.data)
        assert data["_bedrock_status"] == 500
        assert isinstance(data["error"]["message"], str)


class TestBaseBedrockClientMakeStatusError:
    def _make_client(self):
        from anthropic import AnthropicBedrock
        return AnthropicBedrock(
            aws_region="us-east-1",
            aws_access_key="test-key",
            aws_secret_key="test-secret",
        )

    def test_bedrock_status_400_maps_to_bad_request(self) -> None:
        client = self._make_client()
        response = httpx.Response(200)
        body = {
            "type": "error",
            "error": {"type": "validationException", "message": "invalid input"},
            "_bedrock_status": 400,
        }
        err = client._make_status_error("invalid input", body=body, response=response)
        assert isinstance(err, _exceptions.BadRequestError)

    def test_bedrock_status_429_maps_to_rate_limit(self) -> None:
        client = self._make_client()
        response = httpx.Response(200)
        body = {
            "type": "error",
            "error": {"type": "throttlingException", "message": "rate limited"},
            "_bedrock_status": 429,
        }
        err = client._make_status_error("rate limited", body=body, response=response)
        assert isinstance(err, _exceptions.RateLimitError)

    def test_bedrock_status_500_maps_to_internal_server_error(self) -> None:
        client = self._make_client()
        response = httpx.Response(200)
        body = {
            "type": "error",
            "error": {"type": "internalServerException", "message": "internal"},
            "_bedrock_status": 500,
        }
        err = client._make_status_error("internal", body=body, response=response)
        assert isinstance(err, _exceptions.InternalServerError)

    def test_no_bedrock_status_uses_response_status(self) -> None:
        client = self._make_client()
        response = httpx.Response(403)
        body = {"type": "error", "error": {"type": "accessDeniedException"}}
        err = client._make_status_error("forbidden", body=body, response=response)
        assert isinstance(err, _exceptions.PermissionDeniedError)
