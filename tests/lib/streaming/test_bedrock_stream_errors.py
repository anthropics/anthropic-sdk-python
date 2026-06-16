"""End-to-end tests for Bedrock streaming error handling.

Drives the full pipeline (httpx response → AWSEventStreamDecoder → Stream → _make_status_error)
to verify that both in-band (HTTP 200 with error frame) and out-of-band (eventstream
exception) errors surface as the correct typed `APIStatusError` subclasses.
"""

from __future__ import annotations

import json
import zlib
import base64
import struct
from typing import Any

import httpx
import pytest

from anthropic import (
    APIStatusError,
    RateLimitError,
    BadRequestError,
    AnthropicBedrock,
    InternalServerError,
    AsyncAnthropicBedrock,
)
from anthropic._exceptions import OverloadedError


def _encode_event(headers: dict[str, str], payload: bytes) -> bytes:
    """Encode a single event-stream message (https://docs.aws.amazon.com/transcribe/latest/dg/event-stream.html)."""
    headers_bytes = b""
    for name, value in headers.items():
        name_bytes = name.encode("utf-8")
        value_bytes = value.encode("utf-8")
        headers_bytes += struct.pack(">B", len(name_bytes))
        headers_bytes += name_bytes
        headers_bytes += struct.pack(">B", 7)  # 7 = utf8 string header value
        headers_bytes += struct.pack(">H", len(value_bytes))
        headers_bytes += value_bytes

    headers_length = len(headers_bytes)
    total_length = 12 + headers_length + len(payload) + 4

    prelude_no_crc = struct.pack(">II", total_length, headers_length)
    prelude_crc = zlib.crc32(prelude_no_crc) & 0xFFFFFFFF
    prelude = prelude_no_crc + struct.pack(">I", prelude_crc)

    msg_no_crc = prelude + headers_bytes + payload
    msg_crc = zlib.crc32(msg_no_crc) & 0xFFFFFFFF
    return msg_no_crc + struct.pack(">I", msg_crc)


def _chunk_frame(body: dict[str, Any]) -> bytes:
    """A normal Bedrock chunk frame carrying a model-emitted SSE payload."""
    return _encode_event(
        {
            ":message-type": "event",
            ":event-type": "chunk",
            ":content-type": "application/json",
        },
        json.dumps({"bytes": base64.b64encode(json.dumps(body).encode()).decode()}).encode(),
    )


def _exception_frame(exception_type: str, message: str = "boom") -> bytes:
    return _encode_event(
        {
            ":message-type": "exception",
            ":exception-type": exception_type,
            ":content-type": "application/json",
        },
        json.dumps({"message": message}).encode(),
    )


def _make_client(transport: httpx.BaseTransport) -> AnthropicBedrock:
    return AnthropicBedrock(
        aws_region="us-east-1",
        api_key="test-api-key",  # api_key path skips SigV4 signing
        http_client=httpx.Client(transport=transport),
    )


def _make_async_client(transport: httpx.AsyncBaseTransport) -> AsyncAnthropicBedrock:
    return AsyncAnthropicBedrock(
        aws_region="us-east-1",
        api_key="test-api-key",
        http_client=httpx.AsyncClient(transport=transport),
    )


def _stream_response(body_bytes: bytes, status_code: int = 200) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        headers={"content-type": "application/vnd.amazon.eventstream"},
        content=body_bytes,
    )


def _consume_stream(body: bytes) -> None:
    transport = httpx.MockTransport(lambda _request: _stream_response(body))
    stream = _make_client(transport).messages.create(
        max_tokens=64,
        messages=[{"role": "user", "content": "hi"}],
        model="anthropic.claude-3-5-sonnet-20241022-v2:0",
        stream=True,
    )
    for _ in stream:
        pass


async def _aconsume_stream(body: bytes) -> None:
    transport = httpx.MockTransport(lambda _request: _stream_response(body))
    stream = await _make_async_client(transport).messages.create(
        max_tokens=64,
        messages=[{"role": "user", "content": "hi"}],
        model="anthropic.claude-3-5-sonnet-20241022-v2:0",
        stream=True,
    )
    async for _ in stream:
        pass


_STREAM_ERROR_CASES: list[tuple[str, str, type[APIStatusError]]] = [
    ("inband", "rate_limit_error", RateLimitError),
    ("inband", "overloaded_error", OverloadedError),
    ("inband", "invalid_request_error", BadRequestError),
    ("outofband", "throttlingException", RateLimitError),
    ("outofband", "internalServerException", InternalServerError),
    ("outofband", "serviceUnavailableException", OverloadedError),
]


def _error_body(kind: str, identifier: str, message: str = "boom") -> bytes:
    if kind == "inband":
        return _chunk_frame({"type": "error", "error": {"type": identifier, "message": message}})
    return _exception_frame(identifier, message)


class TestStreamErrors:
    @pytest.mark.parametrize(("kind", "identifier", "expected_exception"), _STREAM_ERROR_CASES)
    def test_error_raises_correct_class(
        self, kind: str, identifier: str, expected_exception: type[APIStatusError]
    ) -> None:
        with pytest.raises(expected_exception) as exc_info:
            _consume_stream(_error_body(kind, identifier))

        assert "boom" in str(exc_info.value)

    def test_rate_limit_via_messages_stream_context_manager(self) -> None:
        # `messages.stream(...)` is a separate API surface from `messages.create(stream=True)`
        # and was the path in the original bug report (#1472). Keep one explicit test for it.
        body = _chunk_frame(
            {
                "type": "error",
                "error": {"type": "rate_limit_error", "message": "Rate limited"},
                "request_id": "req_123",
            }
        )
        transport = httpx.MockTransport(lambda _request: _stream_response(body))
        client = _make_client(transport)

        with pytest.raises(RateLimitError) as exc_info:
            with client.messages.stream(
                max_tokens=64,
                messages=[{"role": "user", "content": "hi"}],
                model="anthropic.claude-3-5-sonnet-20241022-v2:0",
            ) as stream:
                for _ in stream:
                    pass

        assert exc_info.value.type == "rate_limit_error"

    def test_unknown_exception_type_raises_generic_api_status_error(self) -> None:
        body = _exception_frame("someFutureException", "huh")

        with pytest.raises(APIStatusError) as exc_info:
            _consume_stream(body)

        assert exc_info.value.type == "someFutureException"
        assert not isinstance(exc_info.value, (RateLimitError, OverloadedError, BadRequestError, InternalServerError))


class TestStatusCodeParity:
    def test_http_529_maps_to_overloaded_error(self) -> None:
        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                status_code=529,
                json={"message": "Overloaded"},
            )

        transport = httpx.MockTransport(handler)
        client = _make_client(transport)

        with pytest.raises(OverloadedError):
            client.messages.create(
                max_tokens=64,
                messages=[{"role": "user", "content": "hi"}],
                model="anthropic.claude-3-5-sonnet-20241022-v2:0",
            )


class TestAsync:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(("kind", "identifier", "expected_exception"), _STREAM_ERROR_CASES)
    async def test_async_error_raises_correct_class(
        self, kind: str, identifier: str, expected_exception: type[APIStatusError]
    ) -> None:
        with pytest.raises(expected_exception):
            await _aconsume_stream(_error_body(kind, identifier))
