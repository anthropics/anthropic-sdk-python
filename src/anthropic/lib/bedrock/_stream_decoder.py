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
                sse = self._parse_message_from_event(event)
                if sse:
                    yield sse

    async def aiter_bytes(self, iterator: AsyncIterator[bytes]) -> AsyncIterator[ServerSentEvent]:
        """Given an async iterator that yields lines, iterate over it & yield every event encountered"""
        from botocore.eventstream import EventStreamBuffer

        event_stream_buffer = EventStreamBuffer()
        async for chunk in iterator:
            event_stream_buffer.add_data(chunk)
            for event in event_stream_buffer:
                sse = self._parse_message_from_event(event)
                if sse:
                    yield sse

    def _parse_message_from_event(self, event: EventStreamMessage) -> ServerSentEvent | None:
        response_dict = event.to_response_dict()
        parsed_response = self.parser.parse(response_dict, get_response_stream_shape())
        if response_dict["status_code"] != 200:
            # Yield an "error" SSE event so the Stream error handler can convert
            # it to a proper APIStatusError instead of raising a raw ValueError.
            body = response_dict.get("body", b"")
            if isinstance(body, bytes):
                body = body.decode("utf-8", errors="replace")

            try:
                error_body = json.loads(body)
                message = error_body.get("message", body)
            except (json.JSONDecodeError, TypeError):
                message = body or f"Bad response code: {response_dict['status_code']}"

            error_data = json.dumps({
                "type": "error",
                "error": {
                    "type": "api_error",
                    "message": message,
                },
            })
            return ServerSentEvent(data=error_data, event="error")

        chunk = parsed_response.get("chunk")
        if not chunk:
            return None

        return ServerSentEvent(data=chunk.get("bytes").decode(), event="completion")  # type: ignore[no-any-return]
