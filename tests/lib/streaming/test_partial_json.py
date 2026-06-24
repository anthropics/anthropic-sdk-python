import copy
from typing import List, cast

import httpx
import pytest

from anthropic.types.beta import BetaDirectCaller, BetaToolUseBlock, BetaInputJSONDelta, BetaRawContentBlockDeltaEvent
from anthropic.types.tool_use_block import ToolUseBlock
from anthropic.types.beta.beta_usage import BetaUsage
from anthropic.lib.streaming._beta_messages import accumulate_event
from anthropic.types.beta.parsed_beta_message import ParsedBetaMessage


class TestPartialJson:
    def test_trailing_strings_mode_header(self) -> None:
        """Test behavior differences with and without the beta header for JSON parsing."""
        message = ParsedBetaMessage(
            id="msg_123",
            type="message",
            role="assistant",
            content=[
                BetaToolUseBlock(
                    type="tool_use",
                    input={},
                    id="tool_123",
                    name="test_tool",
                    caller=BetaDirectCaller(type="direct"),
                )
            ],
            model="claude-sonnet-4-5",
            stop_reason=None,
            stop_sequence=None,
            usage=BetaUsage(input_tokens=10, output_tokens=10),
        )

        # Test case 1: Complete JSON
        complete_json = '{"key": "value"}'
        event_complete = BetaRawContentBlockDeltaEvent(
            type="content_block_delta",
            index=0,
            delta=BetaInputJSONDelta(type="input_json_delta", partial_json=complete_json),
        )

        # Both modes should handle complete JSON the same way
        message1 = accumulate_event(
            event=event_complete,
            current_snapshot=copy.deepcopy(message),
            request_headers=httpx.Headers({"some-header": "value"}),
        )
        message2 = accumulate_event(
            event=event_complete,
            current_snapshot=copy.deepcopy(message),
            request_headers=httpx.Headers({"anthropic-beta": "fine-grained-tool-streaming-2025-05-14"}),
        )

        # Both should parse complete JSON correctly
        assert cast(ToolUseBlock, message1.content[0]).input == {"key": "value"}
        assert cast(ToolUseBlock, message2.content[0]).input == {"key": "value"}

        # Test case 2: Incomplete JSON with trailing string that will be treated differently
        # Here we want to create a situation where regular mode and trailing strings mode behave differently
        incomplete_json = '{"items": ["item1", "item2"], "unfinished_field": "incomplete value'
        event_incomplete = BetaRawContentBlockDeltaEvent(
            type="content_block_delta",
            index=0,
            delta=BetaInputJSONDelta(type="input_json_delta", partial_json=incomplete_json),
        )

        # Without beta header (standard mode)
        message_standard = accumulate_event(
            event=event_incomplete,
            current_snapshot=copy.deepcopy(message),
            request_headers=httpx.Headers({"some-header": "value"}),
        )

        # With beta header (trailing strings mode)
        message_trailing = accumulate_event(
            event=event_incomplete,
            current_snapshot=copy.deepcopy(message),
            request_headers=httpx.Headers({"anthropic-beta": "fine-grained-tool-streaming-2025-05-14"}),
        )

        # Get the tool use blocks
        standard_tool = cast(ToolUseBlock, message_standard.content[0])
        trailing_tool = cast(ToolUseBlock, message_trailing.content[0])

        # Both should have the valid complete part of the JSON
        assert isinstance(standard_tool.input, dict)
        assert isinstance(trailing_tool.input, dict)

        standard_input = standard_tool.input  # type: ignore
        trailing_input = trailing_tool.input  # type: ignore

        # The input should have the items array in both cases
        items_standard = cast(List[str], standard_input["items"])
        items_trailing = cast(List[str], trailing_input["items"])
        assert items_standard == ["item1", "item2"]
        assert items_trailing == ["item1", "item2"]

        # The key difference is how they handle the incomplete field:
        # Standard mode should not include the incomplete field
        assert "unfinished_field" not in standard_input

        # Trailing strings mode should include the incomplete field
        assert "unfinished_field" in trailing_input
        assert trailing_input["unfinished_field"] == "incomplete value"

    def test_partial_json_with_invalid_json(self) -> None:
        """Test that invalid JSON raises an error."""
        message = ParsedBetaMessage(
            id="msg_123",
            type="message",
            role="assistant",
            content=[
                BetaToolUseBlock(
                    type="tool_use",
                    input={},
                    id="tool_123",
                    name="test_tool",
                    caller=BetaDirectCaller(type="direct"),
                )
            ],
            model="claude-sonnet-4-5",
            stop_reason=None,
            stop_sequence=None,
            usage=BetaUsage(input_tokens=10, output_tokens=10),
        )

        # Invalid JSON input
        invalid_json = '{"key": "value", "incomplete_field": bad_value'
        event_invalid = BetaRawContentBlockDeltaEvent(
            type="content_block_delta",
            index=0,
            delta=BetaInputJSONDelta(type="input_json_delta", partial_json=invalid_json),
        )
        # Expect an error when trying to accumulate the invalid JSON
        try:
            accumulate_event(
                event=event_invalid,
                current_snapshot=copy.deepcopy(message),
                request_headers=httpx.Headers({"anthropic-beta": "fine-grained-tool-streaming-2025-05-14"}),
            )
            raise AssertionError("Expected ValueError for invalid JSON, but no error was raised.")
        except ValueError as e:
            assert str(e).startswith(
                "Unable to parse tool parameter JSON from model. Please retry your request or adjust your prompt."
            )
        except Exception as e:
            raise AssertionError(f"Unexpected error type: {type(e).__name__} with message: {str(e)}") from e


# Regression tests for https://github.com/anthropics/anthropic-sdk-python/issues/941 (beta path)
#
# When construct_type_unchecked silently returns a raw dict, the beta accumulate_event
# fallback must produce a fully-validated BetaRawContentBlockDeltaEvent so that
# event.delta.type (a typed BetaTextDelta) is accessible, not a raw dict.


class TestBetaRawDictFallback:
    def _make_snapshot(self) -> ParsedBetaMessage:  # type: ignore[type-arg]
        return ParsedBetaMessage(
            id="msg_test_beta_941",
            type="message",
            role="assistant",
            content=[{"type": "text", "text": ""}],
            model="claude-3-opus-latest",
            stop_reason=None,
            stop_sequence=None,
            usage=BetaUsage(input_tokens=10, output_tokens=0),
        )

    def test_raw_dict_text_delta_is_fully_typed(self) -> None:
        """Raw dict content_block_delta must be fully validated so that event.delta is a
        typed BetaTextDelta; otherwise event.delta.type raises AttributeError and the
        text is never appended to the snapshot."""
        snapshot = accumulate_event(
            event={  # type: ignore[arg-type]
                "type": "content_block_delta",
                "index": 0,
                "delta": {"type": "text_delta", "text": "hello"},
            },
            current_snapshot=self._make_snapshot(),
            request_headers=httpx.Headers(),
        )
        assert snapshot.content[0].text == "hello"

    def test_raw_dict_multiple_deltas_accumulate(self) -> None:
        """Multiple raw dict text deltas must each append correctly."""
        snapshot = self._make_snapshot()
        for word in ["Hello", " beta", "!"]:
            snapshot = accumulate_event(
                event={  # type: ignore[arg-type]
                    "type": "content_block_delta",
                    "index": 0,
                    "delta": {"type": "text_delta", "text": word},
                },
                current_snapshot=snapshot,
                request_headers=httpx.Headers(),
            )
        assert snapshot.content[0].text == "Hello beta!"

    def test_raw_dict_unknown_type_still_raises(self) -> None:
        """An unknown event type arriving before message_start must not be silently
        swallowed by the fallback — it must raise either TypeError (if deserialization
        returns a raw dict) or RuntimeError (if it produces a BaseModel with wrong type)."""
        with pytest.raises((TypeError, RuntimeError)):
            accumulate_event(
                event={"type": "unknown_future_event", "data": "x"},  # type: ignore[arg-type]
                current_snapshot=None,
                request_headers=httpx.Headers(),
            )
