from __future__ import annotations

import httpx
import pytest

from anthropic.types.usage import Usage
from anthropic.types.text_block import TextBlock
from anthropic.types.parsed_message import ParsedMessage
from anthropic.types.beta.beta_usage import BetaUsage
from anthropic.lib.streaming._messages import accumulate_event
from anthropic.types.beta.beta_text_block import BetaTextBlock
from anthropic.lib.streaming._beta_messages import accumulate_event as accumulate_beta_event
from anthropic.types.beta.parsed_beta_message import ParsedBetaMessage
from anthropic.types.raw_content_block_start_event import RawContentBlockStartEvent
from anthropic.types.beta.beta_raw_content_block_start_event import BetaRawContentBlockStartEvent


def _snapshot() -> ParsedMessage[None]:
    return ParsedMessage(
        id="msg_123",
        type="message",
        role="assistant",
        content=[],
        model="claude-sonnet-4-5",
        stop_reason=None,
        stop_sequence=None,
        usage=Usage(input_tokens=10, output_tokens=10),
    )


def _start_event(index: int) -> RawContentBlockStartEvent:
    return RawContentBlockStartEvent(
        type="content_block_start",
        index=index,
        content_block=TextBlock(type="text", text=""),
    )


def _beta_snapshot() -> ParsedBetaMessage[None]:
    return ParsedBetaMessage(
        id="msg_123",
        type="message",
        role="assistant",
        content=[],
        model="claude-sonnet-4-5",
        stop_reason=None,
        stop_sequence=None,
        usage=BetaUsage(input_tokens=10, output_tokens=10),
    )


def _beta_start_event(index: int) -> BetaRawContentBlockStartEvent:
    return BetaRawContentBlockStartEvent(
        type="content_block_start",
        index=index,
        content_block=BetaTextBlock(type="text", text=""),
    )


class TestContentBlockIndex:
    def test_sequential_indices_append(self) -> None:
        snapshot = _snapshot()

        snapshot = accumulate_event(event=_start_event(0), current_snapshot=snapshot)
        assert len(snapshot.content) == 1

        snapshot = accumulate_event(event=_start_event(1), current_snapshot=snapshot)
        assert len(snapshot.content) == 2

    def test_unexpected_index_raises(self) -> None:
        # snapshot has no content yet, so the only valid index is 0
        with pytest.raises(RuntimeError, match='Unexpected "content_block_start" index, got 5 but expected 0'):
            accumulate_event(event=_start_event(5), current_snapshot=_snapshot())

    def test_beta_sequential_indices_append(self) -> None:
        headers = httpx.Headers({"some-header": "value"})
        snapshot = _beta_snapshot()

        snapshot = accumulate_beta_event(event=_beta_start_event(0), current_snapshot=snapshot, request_headers=headers)
        assert len(snapshot.content) == 1

        snapshot = accumulate_beta_event(event=_beta_start_event(1), current_snapshot=snapshot, request_headers=headers)
        assert len(snapshot.content) == 2

    def test_beta_unexpected_index_raises(self) -> None:
        with pytest.raises(RuntimeError, match='Unexpected "content_block_start" index, got 5 but expected 0'):
            accumulate_beta_event(
                event=_beta_start_event(5),
                current_snapshot=_beta_snapshot(),
                request_headers=httpx.Headers({"some-header": "value"}),
            )
