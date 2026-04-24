from datetime import datetime
from datetime import timezone

from anthropic.lib.streaming._messages import accumulate_event
from anthropic.types import Message
from anthropic.types import RawMessageDeltaEvent
from anthropic.types import TextBlock
from anthropic.types import Usage


def test_message_delta_propagates_container() -> None:
    message = Message(
        id="msg_123",
        type="message",
        role="assistant",
        container=None,
        content=[TextBlock(type="text", text="hello", citations=None)],
        model="claude-sonnet-4-20250514",
        stop_reason=None,
        stop_sequence=None,
        usage=Usage(input_tokens=1, output_tokens=0),
    )

    updated = accumulate_event(
        event=RawMessageDeltaEvent(
            type="message_delta",
            delta={
                "container": {
                    "id": "container_123",
                    "expires_at": datetime(2026, 4, 21, tzinfo=timezone.utc),
                },
                "stop_reason": "end_turn",
            },
            usage={"output_tokens": 4},
        ),
        current_snapshot=message,
    )

    assert updated.container is not None
    assert updated.container.id == "container_123"
    assert updated.stop_reason == "end_turn"
    assert updated.usage.output_tokens == 4
