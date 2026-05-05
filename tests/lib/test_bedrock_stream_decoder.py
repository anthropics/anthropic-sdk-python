from __future__ import annotations

import json
from typing import Any, List, AsyncIterator

import pytest
from botocore.eventstream import MessagePrelude, EventStreamMessage

from anthropic._streaming import ServerSentEvent
from anthropic.lib.bedrock._stream_decoder import AWSEventStreamDecoder


def _make_event(headers: dict[str, Any], payload: bytes) -> EventStreamMessage:
    """Construct an EventStreamMessage directly. Prelude/crc aren't read by
    to_response_dict() or the JSON parser, so we use minimal placeholders.
    botocore ships no type stubs, so pyright infers `int` for these args."""
    prelude = MessagePrelude(total_length=0, headers_length=0, crc=0)  # pyright: ignore[reportArgumentType]
    return EventStreamMessage(
        prelude=prelude,  # pyright: ignore[reportArgumentType]
        headers=headers,  # pyright: ignore[reportArgumentType]
        payload=payload,
        crc=0,
    )


def _chunk_event(body: dict[str, Any]) -> EventStreamMessage:
    """A normal Bedrock chunk: ResponseStream wraps the model bytes in a
    `chunk` member whose value is `{"bytes": <base64 of payload>}`. The
    EventStreamJSONParser uses the `:event-type` header to pick the union
    arm and base64-decodes the payload."""
    import base64

    return _make_event(
        headers={
            ":message-type": "event",
            ":event-type": "chunk",
            ":content-type": "application/json",
        },
        payload=json.dumps({"bytes": base64.b64encode(json.dumps(body).encode()).decode()}).encode(),
    )


def _exception_event(exception_type: str, message: str = "boom") -> EventStreamMessage:
    """An out-of-band exception frame. botocore's to_response_dict() returns
    status_code=400 for any `:message-type: exception` event."""
    return _make_event(
        headers={
            ":message-type": "exception",
            ":exception-type": exception_type,
            ":content-type": "application/json",
        },
        payload=json.dumps({"message": message}).encode(),
    )


def _drain(decoder: AWSEventStreamDecoder, events: list[EventStreamMessage]) -> List[ServerSentEvent]:
    out: List[ServerSentEvent] = []
    for event in events:
        sse = decoder._sse_from_event(event)
        if sse is not None:
            out.append(sse)
    return out


class TestInBand:
    def test_normal_chunk_is_completion(self) -> None:
        decoder = AWSEventStreamDecoder()
        body = {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "hi"}}

        result = decoder._sse_from_event(_chunk_event(body))

        assert result is not None
        assert result.event == "completion"
        assert result.json() == body

    def test_inband_error_routed_to_error_event(self) -> None:
        decoder = AWSEventStreamDecoder()
        body = {
            "type": "error",
            "error": {"type": "rate_limit_error", "message": "Rate limited"},
            "request_id": "req_123",
        }

        result = decoder._sse_from_event(_chunk_event(body))

        assert result is not None
        assert result.event == "error"
        # Payload preserved verbatim — streaming layer parses it for us.
        assert result.json() == body

    def test_inband_chunk_with_message_type_is_completion(self) -> None:
        decoder = AWSEventStreamDecoder()
        body = {"type": "message_start", "message": {"id": "msg_1", "model": "claude-..."}}

        result = decoder._sse_from_event(_chunk_event(body))

        assert result is not None
        assert result.event == "completion"

    def test_inband_payload_without_type_field_is_completion(self) -> None:
        decoder = AWSEventStreamDecoder()

        result = decoder._sse_from_event(_chunk_event({"foo": "bar"}))

        assert result is not None
        assert result.event == "completion"


_BEDROCK_EXCEPTION_MAPPING_CASES = [
    ("throttlingException", "rate_limit_error"),
    ("serviceUnavailableException", "overloaded_error"),
    ("internalServerException", "api_error"),
    ("modelStreamErrorException", "api_error"),
    ("modelTimeoutException", "api_error"),
    ("validationException", "invalid_request_error"),
]


class TestOutOfBand:
    @pytest.mark.parametrize(("bedrock_exception", "expected_error_type"), _BEDROCK_EXCEPTION_MAPPING_CASES)
    def test_exception_maps_to_anthropic_error_type(
        self, bedrock_exception: str, expected_error_type: str
    ) -> None:
        decoder = AWSEventStreamDecoder()

        result = decoder._sse_from_event(_exception_event(bedrock_exception, "boom"))

        assert result is not None
        assert result.event == "error"
        body = result.json()
        assert body["type"] == "error"
        assert body["error"]["type"] == expected_error_type
        assert body["error"]["message"] == "boom"

    def test_unknown_exception_type_passes_through_verbatim(self) -> None:
        decoder = AWSEventStreamDecoder()

        result = decoder._sse_from_event(_exception_event("someFutureException", "huh"))

        assert result is not None
        body = result.json()
        # We don't invent a mapping — the body-aware dispatcher in _client.py
        # will fall through to a generic APIStatusError, which is correct.
        assert body["error"]["type"] == "someFutureException"
        assert body["error"]["message"] == "huh"

    def test_exception_with_empty_body_synthesizes_message(self) -> None:
        decoder = AWSEventStreamDecoder()
        event = _make_event(
            headers={
                ":message-type": "exception",
                ":exception-type": "internalServerException",
                ":content-type": "application/json",
            },
            payload=b"",
        )

        result = decoder._sse_from_event(event)

        assert result is not None
        body = result.json()
        assert body["error"]["type"] == "api_error"
        assert body["error"]["message"]  # non-empty fallback


class TestIteration:
    def test_iter_bytes_emits_completion_then_error(self) -> None:
        # Use a real EventStreamBuffer fed with our hand-built frames is too
        # heavy for a unit test; instead we drive the decoder by stubbing
        # iter_bytes' inner loop. The integration test in
        # tests/lib/streaming/test_bedrock_stream_errors.py covers real bytes.
        decoder = AWSEventStreamDecoder()
        events = [
            _chunk_event({"type": "message_start", "message": {"id": "m"}}),
            _exception_event("throttlingException"),
        ]

        results = _drain(decoder, events)

        assert [sse.event for sse in results] == ["completion", "error"]

    @pytest.mark.asyncio
    async def test_sse_from_event_works_inside_async_loop(self) -> None:
        # Sanity: `_sse_from_event` is sync but called from `aiter_bytes`'s
        # `async for`. The real `aiter_bytes` byte-pipeline is exercised by
        # tests/lib/streaming/test_bedrock_stream_errors.py.
        decoder = AWSEventStreamDecoder()
        events = [
            _chunk_event({"type": "content_block_delta", "delta": {"type": "text_delta", "text": "x"}}),
            _exception_event("internalServerException"),
        ]

        async def gen() -> AsyncIterator[EventStreamMessage]:
            for e in events:
                yield e

        out: List[ServerSentEvent] = []
        async for event in gen():
            sse = decoder._sse_from_event(event)
            if sse is not None:
                out.append(sse)

        assert [sse.event for sse in out] == ["completion", "error"]
        assert out[1].json()["error"]["type"] == "api_error"


class TestMalformed:
    def test_chunk_with_invalid_json_payload_is_completion_not_crash(self) -> None:
        # If the model bytes inside the chunk aren't valid JSON, we shouldn't
        # mistake them for an error frame — emit completion and let the
        # streaming layer surface a parse error if the client cares.
        import base64

        decoder = AWSEventStreamDecoder()
        event = _make_event(
            headers={
                ":message-type": "event",
                ":event-type": "chunk",
                ":content-type": "application/json",
            },
            payload=json.dumps({"bytes": base64.b64encode(b"not json").decode()}).encode(),
        )

        result = decoder._sse_from_event(event)

        assert result is not None
        assert result.event == "completion"
