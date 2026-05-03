from __future__ import annotations

import json
from typing import TYPE_CHECKING, Iterator, AsyncIterator

import httpx

from ..._utils import lru_cache
from ..._streaming import ServerSentEvent
from ..._exceptions import APIStatusError, InternalServerError, BadRequestError, RateLimitError

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
                    yield ServerSentEvent(data=message, event="completion")

    async def aiter_bytes(self, iterator: AsyncIterator[bytes]) -> AsyncIterator[ServerSentEvent]:
        """Given an async iterator that yields lines, iterate over it & yield every event encountered"""
        from botocore.eventstream import EventStreamBuffer

        event_stream_buffer = EventStreamBuffer()
        async for chunk in iterator:
            event_stream_buffer.add_data(chunk)
            for event in event_stream_buffer:
                message = self._parse_message_from_event(event)
                if message:
                    yield ServerSentEvent(data=message, event="completion")

    def _parse_message_from_event(self, event: EventStreamMessage) -> str | None:
        response_dict = event.to_response_dict()
        parsed_response = self.parser.parse(response_dict, get_response_stream_shape())
        if response_dict["status_code"] != 200:
            self._raise_for_bedrock_stream_error(response_dict)

        chunk = parsed_response.get("chunk")
        if not chunk:
            return None

        return chunk.get("bytes").decode()  # type: ignore[no-any-return]

    def _raise_for_bedrock_stream_error(self, response_dict: dict[str, object]) -> None:
        status_code = int(response_dict["status_code"])  # type: ignore[arg-type]
        body_bytes = response_dict.get("body", b"")
        try:
            body = json.loads(body_bytes)  # type: ignore[arg-type]
        except Exception:
            body = {}

        message = body.get("message") or f"Bedrock event stream error (status {status_code})"

        # Build a minimal synthetic response so APIStatusError is satisfied.
        synthetic_response = httpx.Response(
            status_code=status_code,
            request=httpx.Request("POST", "https://bedrock-runtime.amazonaws.com"),
        )

        if status_code == 429:
            raise RateLimitError(message, response=synthetic_response, body=body)
        if status_code >= 500:
            raise InternalServerError(message, response=synthetic_response, body=body)
        if status_code == 400:
            raise BadRequestError(message, response=synthetic_response, body=body)

        raise APIStatusError(message, response=synthetic_response, body=body)
