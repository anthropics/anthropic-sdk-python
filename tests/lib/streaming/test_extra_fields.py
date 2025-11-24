"""Tests for accumulating extra fields in streaming responses.

This tests that pydantic extra fields (fields not in the schema) are properly
accumulated during streaming, without exposing specific field names in the SDK.
"""

from __future__ import annotations

from typing import Any, cast

from anthropic.types import Usage, Message, TextBlock, TextDelta
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.streaming._messages import accumulate_event
from anthropic.types.message_delta_usage import MessageDeltaUsage
from anthropic.types.raw_message_delta_event import Delta, RawMessageDeltaEvent
from anthropic.types.raw_message_start_event import RawMessageStartEvent
from anthropic.types.raw_content_block_delta_event import RawContentBlockDeltaEvent
from anthropic.types.raw_content_block_start_event import RawContentBlockStartEvent


class TestExtraFieldsAccumulation:
    def test_extra_fields_accumulation(self) -> None:
        """Test that extra fields are accumulated across streaming events."""
        # Build message with extra field via message_start
        message_start = RawMessageStartEvent(
            type="message_start",
            message=Message(
                id="msg_123",
                type="message",
                role="assistant",
                content=[],
                model="claude-3-opus-latest",
                stop_reason=None,
                stop_sequence=None,
                usage=Usage(input_tokens=11, output_tokens=1),
                # Extra field with nested structure
                private_field={"nested": {"values": [1, 2]}},  # type: ignore[call-arg]
            ),
        )
        snapshot = accumulate_event(event=message_start, current_snapshot=None)

        # content_block_start
        content_block_start = RawContentBlockStartEvent(
            type="content_block_start",
            index=0,
            content_block=TextBlock(type="text", text=""),
        )
        snapshot = accumulate_event(event=content_block_start, current_snapshot=snapshot)

        # First content_block_delta with extra field
        delta1 = RawContentBlockDeltaEvent(
            type="content_block_delta",
            index=0,
            delta=TextDelta(type="text_delta", text="Hello"),
            private_field={"nested": {"values": [3], "metadata": "chunk1"}},  # type: ignore[call-arg]
        )
        snapshot = accumulate_event(event=delta1, current_snapshot=snapshot)

        # Second content_block_delta with extra field
        delta2 = RawContentBlockDeltaEvent(
            type="content_block_delta",
            index=0,
            delta=TextDelta(type="text_delta", text="!"),
            private_field={"nested": {"values": [4, 5], "metadata": "chunk2"}},  # type: ignore[call-arg]
        )
        snapshot = accumulate_event(event=delta2, current_snapshot=snapshot)

        # message_delta with extra field
        message_delta = RawMessageDeltaEvent(
            type="message_delta",
            delta=Delta(stop_reason="end_turn", stop_sequence=None),
            usage=MessageDeltaUsage(output_tokens=3),
            private_field={"nested": {"values": [6]}},  # type: ignore[call-arg]
        )
        snapshot = accumulate_event(event=message_delta, current_snapshot=snapshot)

        # This feature requires Pydantic v2
        if PYDANTIC_V1:
            return

        # Verify extra fields were accumulated
        assert hasattr(snapshot, "__pydantic_extra__"), "Message should have __pydantic_extra__"
        extra = snapshot.__pydantic_extra__
        assert extra is not None
        assert "private_field" in extra, "Extra fields should be accumulated"

        private_field = cast(dict[str, Any], extra["private_field"])
        assert "nested" in private_field

        nested = cast(dict[str, Any], private_field["nested"])
        assert "values" in nested

        # Lists should be extended across all events: [1,2] + [3] + [4,5] + [6]
        assert nested["values"] == [1, 2, 3, 4, 5, 6], "Lists should be extended, not replaced"

        # Dict values should use the last value
        assert nested.get("metadata") == "chunk2", "Dict values should be merged"


def test_deep_merge_extra_fields_function() -> None:
    """Test the _deep_merge_extra_fields helper function directly."""
    from anthropic.lib.streaming._messages import _deep_merge_extra_fields

    # Test dict merging
    existing = {"a": 1, "b": {"c": 2}}
    new = {"b": {"d": 3}, "e": 4}
    result = _deep_merge_extra_fields(existing, new)
    assert result == {"a": 1, "b": {"c": 2, "d": 3}, "e": 4}
    assert result is existing, "Should mutate in place"

    # Test list extending
    existing_list = [1, 2, 3]
    new_list = [4, 5]
    result_list = _deep_merge_extra_fields(existing_list, new_list)
    assert result_list == [1, 2, 3, 4, 5]
    assert result_list is existing_list, "Should mutate in place"

    # Test nested dict with lists
    existing_nested = {"data": {"values": [1, 2]}}
    new_nested = {"data": {"values": [3, 4], "count": 4}}
    result_nested = _deep_merge_extra_fields(existing_nested, new_nested)
    assert result_nested == {"data": {"values": [1, 2, 3, 4], "count": 4}}
    assert result_nested is existing_nested, "Should mutate in place"

    # Test scalar replacement
    assert _deep_merge_extra_fields(1, 2) == 2
    assert _deep_merge_extra_fields("old", "new") == "new"
    assert _deep_merge_extra_fields(None, {"a": 1}) == {"a": 1}
