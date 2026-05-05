from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Mapping, Iterator, AsyncIterator

from ..._utils import is_dict, lru_cache
from ..._streaming import ServerSentEvent

if TYPE_CHECKING:
    from botocore.model import Shape
    from botocore.eventstream import EventStreamMessage


# Bedrock's `:exception-type` header is the source of truth for error classification.
# The `status_code` botocore puts on the parsed event is hardcoded to 400 for any
# `:message-type: exception` frame, so we ignore it for mapping purposes.
#
# Stream-level error variants are documented at:
# https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ResponseStream.html
_BEDROCK_EXCEPTION_TYPE_TO_ANTHROPIC_ERROR_TYPE: Mapping[str, str] = {
    "throttlingException": "rate_limit_error",
    "serviceUnavailableException": "overloaded_error",
    "internalServerException": "api_error",
    "modelStreamErrorException": "api_error",
    "modelTimeoutException": "api_error",
    "validationException": "invalid_request_error",
}


@lru_cache(maxsize=None)
def get_response_stream_shape() -> Shape:
    from botocore.model import ServiceModel
    from botocore.loaders import Loader

    loader = Loader()
    bedrock_service_dict = loader.load_service_model("bedrock-runtime", "service-2")
    bedrock_service_model = ServiceModel(bedrock_service_dict)
    return bedrock_service_model.shape_for("ResponseStream")


class AWSEventStreamDecoder:
    def __init__(self) -> None:
        from botocore.parsers import EventStreamJSONParser

        self.parser = EventStreamJSONParser()

    def iter_bytes(self, iterator: Iterator[bytes]) -> Iterator[ServerSentEvent]:
        """Given an iterator that yields lines, iterate over it & yield every event encountered"""
        from botocore.eventstream import EventStreamBuffer

        event_stream_buffer = EventStreamBuffer()
        for chunk in iterator:
            event_stream_buffer.add_data(chunk)
            for event in event_stream_buffer:
                sse = self._sse_from_event(event)
                if sse is not None:
                    yield sse

    async def aiter_bytes(self, iterator: AsyncIterator[bytes]) -> AsyncIterator[ServerSentEvent]:
        """Given an async iterator that yields lines, iterate over it & yield every event encountered"""
        from botocore.eventstream import EventStreamBuffer

        event_stream_buffer = EventStreamBuffer()
        async for chunk in iterator:
            event_stream_buffer.add_data(chunk)
            for event in event_stream_buffer:
                sse = self._sse_from_event(event)
                if sse is not None:
                    yield sse

    def _sse_from_event(self, event: EventStreamMessage) -> ServerSentEvent | None:
        response_dict = event.to_response_dict()

        # Out-of-band stream errors: botocore flags exception/error frames with
        # status_code != 200. Translate them into an Anthropic-shaped error
        # envelope so the streaming layer raises a typed APIStatusError.
        if response_dict.get("status_code") != 200:
            return ServerSentEvent(event="error", data=_format_bedrock_error(response_dict))

        parsed_response = self.parser.parse(response_dict, get_response_stream_shape())
        chunk = parsed_response.get("chunk")
        if not chunk:
            return None

        data: str = chunk["bytes"].decode()

        # In-band stream errors: HTTP 200 stream where the chunk payload itself
        # is an error frame (e.g. cross-region inference profile rate limit).
        # Route these through the existing error handler instead of decoding
        # them as a `RawMessageStartEvent` with `message=None`.
        if _is_inband_error(data):
            return ServerSentEvent(event="error", data=data)

        return ServerSentEvent(event="completion", data=data)


def _is_inband_error(data: str) -> bool:
    try:
        payload = json.loads(data)
    except Exception:
        return False
    return is_dict(payload) and payload.get("type") == "error"


def _format_bedrock_error(response_dict: Mapping[str, Any]) -> str:
    headers: Mapping[str, Any] = response_dict.get("headers") or {}
    body_bytes: bytes = response_dict.get("body") or b""

    raw_exception_type = _header_value(headers.get(":exception-type")) or "bedrock_error"
    error_type = _BEDROCK_EXCEPTION_TYPE_TO_ANTHROPIC_ERROR_TYPE.get(raw_exception_type, raw_exception_type)

    message = ""
    if body_bytes:
        try:
            body = json.loads(body_bytes.decode("utf-8"))
        except Exception:
            message = body_bytes.decode("utf-8", errors="replace")
        else:
            if is_dict(body):
                message = str(body.get("message") or body.get("Message") or "")
            else:
                message = str(body)

    return json.dumps(
        {
            "type": "error",
            "error": {
                "type": error_type,
                "message": message or f"Bedrock stream error: {raw_exception_type}",
            },
        }
    )


def _header_value(value: object) -> str | None:
    """Coerce a botocore header value (str or `EventStreamHeaderValue`) to str."""
    if value is None:
        return None
    if isinstance(value, str):
        return value
    inner = getattr(value, "value", None)
    return inner if isinstance(inner, str) else str(value)
