from __future__ import annotations

from types import TracebackType
from typing import TYPE_CHECKING, Any
from collections.abc import Iterable, Iterator, AsyncIterator
from typing_extensions import override

from ._params import TurnOverrides
from ...types.beta import BetaMessage, BetaMessageParam
from ..streaming._beta_types import ParsedBetaMessageStreamEvent
from ..streaming._beta_messages import (
    BetaMessageStream,
    BetaAsyncMessageStream,
    BetaMessageStreamManager,
    BetaAsyncMessageStreamManager,
)
from ...types.beta.parsed_beta_message import ResponseFormatT

if TYPE_CHECKING:
    from ._beta_threads import BetaMessageThread, BetaAsyncMessageThread


class ThreadMessageStreamManager(BetaMessageStreamManager[ResponseFormatT]):
    """A stream over one turn of a thread. The turn ends when the stream's events run out or fail, and on leaving the
    block at the latest."""

    def __init__(
        self,
        thread: BetaMessageThread[ResponseFormatT],
        messages: Iterable[BetaMessageParam | BetaMessage],
        overrides: TurnOverrides,
    ) -> None:
        super().__init__(lambda: thread._open_stream(messages, overrides), output_format=thread._state.output_format)
        self._thread = thread
        self._stream: BetaMessageStream[ResponseFormatT]
        self._turn_ended = False
        """Whether the stream has been recorded and the thread freed, which happens once."""

    @override
    def __enter__(self) -> BetaMessageStream[ResponseFormatT]:
        self._stream = super().__enter__()
        self._turn_ended = False
        self._stream._iterator = self._end_turn_after(self._stream._iterator)
        return self._stream

    @override
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        try:
            super().__exit__(exc_type, exc, exc_tb)
        finally:
            _end_turn(self)

    def _end_turn_after(
        self, events: Iterator[ParsedBetaMessageStreamEvent[ResponseFormatT]]
    ) -> Iterator[ParsedBetaMessageStreamEvent[ResponseFormatT]]:
        stream = self._stream
        try:
            yield from events
        finally:
            if stream is self._stream:
                _end_turn(self)


class AsyncThreadMessageStreamManager(BetaAsyncMessageStreamManager[ResponseFormatT]):
    """A stream over one turn of a thread. The turn ends when the stream's events run out or fail, and on leaving the
    block at the latest."""

    def __init__(
        self,
        thread: BetaAsyncMessageThread[ResponseFormatT],
        messages: Iterable[BetaMessageParam | BetaMessage],
        overrides: TurnOverrides,
    ) -> None:
        super().__init__(thread._open_stream(messages, overrides), output_format=thread._state.output_format)
        self._thread = thread
        self._stream: BetaAsyncMessageStream[ResponseFormatT]
        self._turn_ended = False
        """Whether the stream has been recorded and the thread freed, which happens once."""

    @override
    async def __aenter__(self) -> BetaAsyncMessageStream[ResponseFormatT]:
        self._stream = await super().__aenter__()
        self._stream._iterator = self._end_turn_after(self._stream._iterator)
        return self._stream

    @override
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        try:
            await super().__aexit__(exc_type, exc, exc_tb)
        finally:
            _end_turn(self)

    async def _end_turn_after(
        self, events: AsyncIterator[ParsedBetaMessageStreamEvent[ResponseFormatT]]
    ) -> AsyncIterator[ParsedBetaMessageStreamEvent[ResponseFormatT]]:
        try:
            async for event in events:
                yield event
        finally:
            _end_turn(self)


def _end_turn(manager: ThreadMessageStreamManager[Any] | AsyncThreadMessageStreamManager[Any]) -> None:
    """Record the stream and free the thread, unless the turn has ended already: the whole reply if the stream reached
    `message_stop`, the partial reply and a new thread if it ended after `message_start`, and nothing if it ended
    before that."""
    if manager._turn_ended:
        return
    manager._turn_ended = True
    state = manager._thread._state
    try:
        stream = manager._stream
        snapshot = stream._current_snapshot_or_none()
        if snapshot is not None:
            if stream._message_complete:
                state.record_reply(snapshot)
            else:
                state.record_partial_reply(snapshot, stream._completed_blocks)
    finally:
        state.end_turn()
