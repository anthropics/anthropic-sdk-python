from __future__ import annotations

import logging
from typing import Any, cast
from collections.abc import Callable

import httpx2
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

from ._utils import MessageCreateBody, get
from ...types import Message, ParsedMessage, RawMessageStartEvent, RawMessageStreamEvent
from ._content import set_message_content
from ._response import set_response, set_time_to_first_chunk
from ..._tracing import FirstEnd, StreamEnd, set_error_status
from ..._streaming import Stream, AsyncStream
from ...types.beta import BetaMessage, BetaRawMessageStartEvent, BetaRawMessageStreamEvent
from ..._exceptions import AnthropicError
from ...types.beta.parsed_beta_message import ParsedBetaMessage

__all__ = ["StreamedMessage", "share_message_snapshot", "withhold_message_snapshot"]

log: logging.Logger = logging.getLogger(__name__)

AnyMessage = Message | BetaMessage
SnapshotReader = Callable[[], AnyMessage | None]
"""Gives the Message that a stream helper has accumulated so far, or `None` before `message_start`."""

Accumulate = Callable[[object, AnyMessage | None], AnyMessage]


class StreamedMessage:
    """Records a streamed Message on the span of its API call as the application reads it, and ends the span.

    The stream helper that reads the stream shares the Message it accumulates (`share_message_snapshot`),
    and in content mode the output content comes from there: the whole Message, or what the helper had
    accumulated of it when the stream ended before `message_stop`. A stream read without a helper gets
    only its `message_start`, `content_block_start` and `message_delta` events accumulated here, which
    carry everything but the content, so its span has no output content.
    """

    def __init__(
        self,
        span: trace.Span,
        body: MessageCreateBody,
        *,
        request_headers: httpx2.Headers,
        content: bool,
        max_content_bytes: int,
        start_time: int,
    ) -> None:
        self._span = span
        self._body = body
        self._request_headers = request_headers
        self._parsed = False
        self._shared_snapshot: SnapshotReader | None = None
        self._snapshot_withheld = False
        self._content = content
        self._max_content_bytes = max_content_bytes
        self._start_time = start_time
        self._first_delta = True
        self._accumulate: Accumulate | None = None
        self._snapshot: AnyMessage | None = None
        self._stopped = False
        self._has_message_delta = False

    def begin(self) -> None:
        self._parsed = True

    def item(self, event: object) -> None:
        try:
            event_type = get(event, "type")
            if event_type == "content_block_delta" and self._first_delta:
                self._first_delta = False
                set_time_to_first_chunk(self._span, self._start_time)

            if event_type == "message_stop":
                self._stopped = True
            # A helper shares its snapshot before it reads the first event.
            elif event_type == "message_start" and self._shared_snapshot is None:
                self._accumulate = accumulator(event, self._request_headers)

            if self._accumulate is not None and event_type in ("message_start", "content_block_start", "message_delta"):
                self._snapshot = self._accumulate(event, self._snapshot)
            # After the accumulation, which can fail and leave the snapshot without what the event has.
            if event_type == "message_delta":
                self._has_message_delta = True
        except Exception:
            log.debug("Could not record a stream event on its span", exc_info=True)

    def end(self, how: StreamEnd, error: BaseException | None = None) -> None:
        try:
            shared = self._shared_snapshot
            # A helper that could not accumulate an event stopped there, with a snapshot that lacks that event.
            withheld = self._snapshot_withheld
            message = self._snapshot if shared is None else shared()
            if message is not None:
                # `message_delta` has the last of what `set_response` reads, so a stream that ends after it lacks nothing.
                set_response(self._span, message, complete=self._has_message_delta and not withheld)
            if self._content:
                # Before `message_stop` the snapshot is partial: a `tool_use` block has the input parsed so far.
                output = message.content if message is not None and shared is not None and not withheld else None
                set_message_content(self._span, self._body, output, limit=self._max_content_bytes)
        except Exception:
            log.debug("Could not record a stream on its span", exc_info=True)

        if error is not None:
            set_error_status(self._span, error)
        # An application that reads the bytes of the body itself leaves the events unknown.
        elif how == "read" and (self._stopped or not self._parsed):
            self._span.set_status(Status(StatusCode.OK))
        elif how == "read":
            # The server cut the stream short. The application sees no error, so only the span fails.
            set_error_status(self._span, AnthropicError("The stream ended before its end event."), "api_error")
        self._span.end()

    def share_snapshot(self, reader: SnapshotReader) -> None:
        self._shared_snapshot = reader

    def withhold_snapshot(self) -> None:
        self._snapshot_withheld = True


def accumulator(event: object, headers: httpx2.Headers) -> Accumulate | None:
    """The stable or the beta `accumulate_event` for a stream whose `message_start` is `event`."""
    # Imported here: the stream helpers import this package.
    from ..streaming._messages import accumulate_event
    from ..streaming._beta_messages import accumulate_event as accumulate_beta_event

    if isinstance(event, BetaRawMessageStartEvent):
        return lambda event, snapshot: accumulate_beta_event(
            event=cast(BetaRawMessageStreamEvent, event),
            current_snapshot=cast("ParsedBetaMessage[None] | None", snapshot),
            json_bufs={},
            request_headers=headers,
        )
    if isinstance(event, RawMessageStartEvent):
        return lambda event, snapshot: accumulate_event(
            event=cast(RawMessageStreamEvent, event),
            current_snapshot=cast("ParsedMessage[None] | None", snapshot),
            json_bufs={},
        )
    return None


def share_message_snapshot(stream: Stream[Any] | AsyncStream[Any], reader: SnapshotReader) -> None:
    """Lets the span of the API call that returned `stream` take its output content from `reader`."""
    if (message := streamed_message(stream)) is not None:
        message.share_snapshot(reader)


def withhold_message_snapshot(stream: Stream[Any] | AsyncStream[Any]) -> None:
    """Keeps the snapshot shared for `stream` out of the output content of the span of its API call.

    The stream helper could not accumulate an event, so its snapshot is not the Message that the events make.
    """
    if (message := streamed_message(stream)) is not None:
        message.withhold_snapshot()


def streamed_message(stream: Stream[Any] | AsyncStream[Any]) -> StreamedMessage | None:
    """What records `stream` on the span of its API call, or `None` when the call has no span."""
    # A stand-in for the stream, as an application's test may give a stream helper, has no observer.
    observer: object = getattr(stream, "_observer", None)
    recorder = observer.inner if isinstance(observer, FirstEnd) else None
    return recorder if isinstance(recorder, StreamedMessage) else None
