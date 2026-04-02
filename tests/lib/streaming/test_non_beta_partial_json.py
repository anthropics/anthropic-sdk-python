import copy

import pytest

from anthropic.types.usage import Usage
from anthropic.types.message import Message
from anthropic.types.tool_use_block import ToolUseBlock
from anthropic.types.input_json_delta import InputJSONDelta
from anthropic.lib.streaming._messages import accumulate_event
from anthropic.types.raw_content_block_delta_event import RawContentBlockDeltaEvent


class TestNonBetaPartialJson:
    """Tests for the non-beta streaming accumulate_event JSON parsing."""

    def _make_snapshot(self) -> Message:
        return Message(
            id="msg_123",
            type="message",
            role="assistant",
            content=[
                ToolUseBlock(
                    type="tool_use",
                    input={},
                    id="tool_123",
                    name="test_tool",
                )
            ],
            model="claude-sonnet-4-5",
            stop_reason=None,
            stop_sequence=None,
            usage=Usage(input_tokens=10, output_tokens=10),
        )

    def test_valid_json_parses_correctly(self) -> None:
        """Valid JSON input should be parsed normally."""
        snapshot = self._make_snapshot()
        event = RawContentBlockDeltaEvent(
            type="content_block_delta",
            index=0,
            delta=InputJSONDelta(type="input_json_delta", partial_json='{"key": "value"}'),
        )

        result = accumulate_event(
            event=event,
            current_snapshot=copy.deepcopy(snapshot),
        )

        assert isinstance(result.content[0], ToolUseBlock)
        assert result.content[0].input == {"key": "value"}

    def test_invalid_json_raises_helpful_error(self) -> None:
        """Invalid JSON should raise ValueError with a helpful message, not a raw parser error."""
        snapshot = self._make_snapshot()
        event = RawContentBlockDeltaEvent(
            type="content_block_delta",
            index=0,
            delta=InputJSONDelta(
                type="input_json_delta",
                partial_json='{"city": INVALID_VALUE}',
            ),
        )

        with pytest.raises(ValueError) as exc_info:
            accumulate_event(
                event=event,
                current_snapshot=copy.deepcopy(snapshot),
            )

        error_msg = str(exc_info.value)
        assert "Unable to parse tool parameter JSON from model" in error_msg
        assert "INVALID_VALUE" in error_msg

    def test_invalid_json_chained_from_original(self) -> None:
        """The error should be chained from the original ValueError."""
        snapshot = self._make_snapshot()
        event = RawContentBlockDeltaEvent(
            type="content_block_delta",
            index=0,
            delta=InputJSONDelta(
                type="input_json_delta",
                partial_json='{"bad": syntax}',
            ),
        )

        with pytest.raises(ValueError) as exc_info:
            accumulate_event(
                event=event,
                current_snapshot=copy.deepcopy(snapshot),
            )

        assert exc_info.value.__cause__ is not None
