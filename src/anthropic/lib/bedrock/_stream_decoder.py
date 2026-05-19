from __future__ import annotations

import json
from typing import TYPE_CHECKING, Iterator, AsyncIterator

from ..._utils import lru_cache
from ..._streaming import ServerSentEvent

if TYPE_CHECKING:
    from botocore.model import Shape
    from botocore.eventstream import EventStreamMessage


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
                message = self._parse_message_from_event(event)
                if message:
                    yield ServerSentEvent(data=message, event=self._sse_event_type(message))

    async def aiter_bytes(self, iterator: AsyncIterator[bytes]) -> AsyncIterator[ServerSentEvent]:
        """Given an async iterator that yields lines, iterate over it & yield every event encountered"""
        from botocore.eventstream import EventStreamBuffer

        event_stream_buffer = EventStreamBuffer()
        async for chunk in iterator:
            event_stream_buffer.add_data(chunk)
            for event in event_stream_buffer:
                message = self._parse_message_from_event(event)
                if message:
                    yield ServerSentEvent(data=message, event=self._sse_event_type(message))

    def _sse_event_type(self, message: str) -> str:
        """Return the SSE event type for a decoded Bedrock message string.

        Bedrock wraps all SSE payloads (including error events) in its binary
        event-stream framing and delivers them over HTTP 200.  We need to
        inspect the ``type`` field of the inner JSON so that error payloads are
        surfaced as ``event="error"`` rather than ``event="completion"``.  The
        standard ``_streaming.py`` error-handling path already converts
        ``event="error"`` into the correct ``APIStatusError``.
        """
        try:
            data = json.loads(message)
            if isinstance(data, dict) and data.get("type") == "error":
                return "error"
        except Exception:
            pass
        return "completion"

    def _parse_message_from_event(self, event: EventStreamMessage) -> str | None:
        response_dict = event.to_response_dict()
        parsed_response = self.parser.parse(response_dict, get_response_stream_shape())
        if response_dict["status_code"] != 200:
            raise ValueError(f"Bad response code, expected 200: {response_dict}")

        chunk = parsed_response.get("chunk")
        if not chunk:
            return None

        return chunk.get("bytes").decode()  # type: ignore[no-any-return]
