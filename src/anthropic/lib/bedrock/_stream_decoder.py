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
                    yield message

    async def aiter_bytes(self, iterator: AsyncIterator[bytes]) -> AsyncIterator[ServerSentEvent]:
        """Given an async iterator that yields lines, iterate over it & yield every event encountered"""
        from botocore.eventstream import EventStreamBuffer

        event_stream_buffer = EventStreamBuffer()
        async for chunk in iterator:
            event_stream_buffer.add_data(chunk)
            for event in event_stream_buffer:
                message = self._parse_message_from_event(event)
                if message:
                    yield message

    def _parse_message_from_event(self, event: EventStreamMessage) -> ServerSentEvent | None:
        response_dict = event.to_response_dict()
        parsed_response = self.parser.parse(response_dict, get_response_stream_shape())
        if response_dict["status_code"] != 200:
            # Bedrock surfaces errors as non-200 frames inside the event stream
            # (e.g. internalServerException with status 400 or 500).  Raising a
            # raw ValueError here means callers cannot catch them via the
            # standard anthropic.APIError hierarchy.  Instead we emit an SSE
            # error event so the existing error-handling path in Stream /
            # AsyncStream calls _make_status_error and raises the correct
            # APIStatusError subclass.
            exception_type = response_dict.get("headers", {}).get(":exception-type", "unknown")
            raw_body: bytes | None = response_dict.get("body")
            try:
                body_str = raw_body.decode() if isinstance(raw_body, (bytes, bytearray)) else (raw_body or "")
                body_data = json.loads(body_str)
                err_message = body_data.get("message", body_str)
            except Exception:
                err_message = str(raw_body)

            error_body = json.dumps(
                {
                    "type": "error",
                    "error": {
                        "type": exception_type,
                        "message": err_message,
                    },
                }
            )
            return ServerSentEvent(data=error_body, event="error")

        chunk = parsed_response.get("chunk")
        if not chunk:
            return None

        return ServerSentEvent(data=chunk.get("bytes").decode(), event="completion")  # type: ignore[no-any-return]
