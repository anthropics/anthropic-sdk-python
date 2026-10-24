from __future__ import annotations

from typing import Any, cast
from datetime import datetime, timezone

import pytest

from anthropic import AnthropicError
from anthropic._models import build
from anthropic.types.beta import (
    BetaManagedAgentsDeltaEvent,
    BetaManagedAgentsStartEvent,
    BetaManagedAgentsDeltaContent,
    BetaManagedAgentsAgentMessagePreview,
    BetaManagedAgentsAgentThinkingPreview,
)
from anthropic.lib.sessions import accumulate_managed_agents_event
from anthropic.types.beta.sessions import BetaManagedAgentsTextBlock, BetaManagedAgentsAgentMessageEvent


def start(event_id: str) -> BetaManagedAgentsStartEvent:
    return BetaManagedAgentsStartEvent(
        type="event_start",
        event=BetaManagedAgentsAgentMessagePreview(id=event_id, type="agent.message"),
    )


def seed(event_id: str) -> BetaManagedAgentsAgentMessageEvent:
    msg = accumulate_managed_agents_event(None, start(event_id))
    assert msg is not None, "expected agent.message seed"
    return msg


def fold(
    msg: BetaManagedAgentsAgentMessageEvent,
    ev: BetaManagedAgentsDeltaEvent,
) -> BetaManagedAgentsAgentMessageEvent:
    next_ = accumulate_managed_agents_event(msg, ev)
    assert next_ is not None, "expected snapshot after delta"
    return next_


def delta(event_id: str, text: str, index: int | None = None) -> BetaManagedAgentsDeltaEvent:
    return BetaManagedAgentsDeltaEvent(
        type="event_delta",
        event_id=event_id,
        delta=build(
            BetaManagedAgentsDeltaContent,
            type="content_delta",
            index=index,
            content=BetaManagedAgentsTextBlock(type="text", text=text),
        ),
    )


def test_event_start_returns_a_fresh_empty_snapshot_from_none() -> None:
    msg = accumulate_managed_agents_event(None, start("evt_1"))
    assert msg is not None
    assert msg.id == "evt_1"
    assert msg.type == "agent.message"
    assert msg.content == []


def test_event_start_for_a_non_agent_message_preview_returns_none() -> None:
    ev = BetaManagedAgentsStartEvent(
        type="event_start",
        event=BetaManagedAgentsAgentThinkingPreview(id="evt_1", type="agent.thinking"),
    )
    assert accumulate_managed_agents_event(None, ev) is None


def test_new_index_inserts_the_fragment_as_a_fresh_block() -> None:
    msg = seed("evt_1")
    next_ = fold(msg, delta("evt_1", "Hello", 0))
    assert next_.content == [BetaManagedAgentsTextBlock(type="text", text="Hello")]


def test_existing_text_index_appends() -> None:
    msg = seed("evt_1")
    msg = fold(msg, delta("evt_1", "Hel", 0))
    msg = fold(msg, delta("evt_1", "lo", 0))
    msg = fold(msg, delta("evt_1", "World", 1))
    assert msg.content == [
        BetaManagedAgentsTextBlock(type="text", text="Hello"),
        BetaManagedAgentsTextBlock(type="text", text="World"),
    ]


def test_defaults_index_to_0() -> None:
    msg = seed("evt_1")
    msg = fold(msg, delta("evt_1", "a"))
    msg = fold(msg, delta("evt_1", "b"))
    assert msg.content == [BetaManagedAgentsTextBlock(type="text", text="ab")]


def test_throws_on_an_index_gap() -> None:
    msg = seed("evt_1")
    with pytest.raises(AnthropicError, match=r"event_delta index 2 is beyond the end of content \(length 0\)"):
        accumulate_managed_agents_event(msg, delta("evt_1", "x", 2))


def test_throws_on_event_delta_with_no_prior_snapshot() -> None:
    with pytest.raises(AnthropicError, match=r"event_delta for evt_1 received before its event_start"):
        accumulate_managed_agents_event(None, delta("evt_1", "x", 0))


def test_next_sequential_index_inserts() -> None:
    msg = seed("evt_1")
    msg = fold(msg, delta("evt_1", "a", 0))
    msg = fold(msg, delta("evt_1", "b", 1))
    assert msg.content == [
        BetaManagedAgentsTextBlock(type="text", text="a"),
        BetaManagedAgentsTextBlock(type="text", text="b"),
    ]


def test_returns_a_new_snapshot_and_does_not_mutate_the_input() -> None:
    msg = seed("evt_1")
    next_ = fold(msg, delta("evt_1", "x", 0))
    assert next_ is not msg
    assert next_.content is not msg.content
    assert msg.content == []

    after = fold(next_, delta("evt_1", "y", 0))
    assert after.content[0] is not next_.content[0]
    assert next_.content == [BetaManagedAgentsTextBlock(type="text", text="x")]


def test_does_not_mutate_the_wire_delta_when_inserting_at_a_new_index() -> None:
    d = delta("evt_1", "x", 0)
    msg = seed("evt_1")
    msg = fold(msg, d)
    msg = fold(msg, delta("evt_1", "y", 0))
    assert d.delta.content.text == "x"


def test_agent_message_replaces_the_preview_with_a_copy_of_the_final_event() -> None:
    msg = seed("evt_1")
    msg = fold(msg, delta("evt_1", "partial", 0))
    final = BetaManagedAgentsAgentMessageEvent(
        id="evt_1",
        type="agent.message",
        content=[BetaManagedAgentsTextBlock(type="text", text="complete")],
        processed_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )
    result = accumulate_managed_agents_event(msg, final)
    assert result == final
    assert result is not final
    assert result.content is not final.content
    assert result.content[0] is not final.content[0]


def test_agent_message_accepts_none_snapshot() -> None:
    final = BetaManagedAgentsAgentMessageEvent(
        id="evt_1",
        type="agent.message",
        content=[BetaManagedAgentsTextBlock(type="text", text="complete")],
        processed_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )
    assert accumulate_managed_agents_event(None, final) == final


def test_unknown_block_type_pair_is_a_noop_forward_compat() -> None:
    msg = seed("evt_1")
    # Existing block of a future, non-text type:
    future_block = BetaManagedAgentsTextBlock.model_construct(type="tool_use", id="t", name="n", input={})
    before = future_block.model_dump()
    msg.content.append(cast(Any, future_block))
    next_ = fold(msg, delta("evt_1", "ignored", 0))
    assert next_.content[0].model_dump() == before


def test_unknown_event_type_passes_the_snapshot_through_forward_compat() -> None:
    msg = seed("evt_1")
    msg = fold(msg, delta("evt_1", "x", 0))
    # An event of a future type this SDK version does not know about:
    future_event = BetaManagedAgentsAgentMessageEvent.model_construct(type="agent.future_event", id="evt_2")
    assert accumulate_managed_agents_event(msg, cast(Any, future_event)) is msg
    assert accumulate_managed_agents_event(None, cast(Any, future_event)) is None


def test_unknown_fragment_type_on_an_existing_index_is_a_noop_forward_compat() -> None:
    msg = seed("evt_1")
    msg = fold(msg, delta("evt_1", "x", 0))
    # A delta fragment of a future, non-text type:
    future_fragment = BetaManagedAgentsTextBlock.model_construct(type="citation", url="u")
    ev = BetaManagedAgentsDeltaEvent(
        type="event_delta",
        event_id="evt_1",
        delta=build(BetaManagedAgentsDeltaContent, type="content_delta", index=0, content=cast(Any, future_fragment)),
    )
    next_ = fold(msg, ev)
    assert next_.content == [BetaManagedAgentsTextBlock(type="text", text="x")]


@pytest.mark.parametrize("completed", [False, True])
def test_repeated_start_preserves_the_existing_snapshot(completed: bool) -> None:
    snapshot = fold(seed("evt_1"), delta("evt_1", "partial", 0))
    if completed:
        snapshot = accumulate_managed_agents_event(
            snapshot,
            BetaManagedAgentsAgentMessageEvent(
                id="evt_1",
                type="agent.message",
                content=[BetaManagedAgentsTextBlock(type="text", text="complete")],
                processed_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
            ),
        )
    before = snapshot.model_dump()
    for _ in range(3):
        result = accumulate_managed_agents_event(snapshot, start("evt_1"))
        assert result is snapshot
        assert result is not None
        assert result.model_dump() == before


def test_repeated_start_keeps_all_preview_content_indices() -> None:
    snapshot = fold(seed("evt_1"), delta("evt_1", "first", 0))
    snapshot = fold(snapshot, delta("evt_1", "second", 1))
    restarted = accumulate_managed_agents_event(snapshot, start("evt_1"))
    assert restarted is not None
    result = fold(restarted, delta("evt_1", " appended", 1))
    assert result.content == [
        BetaManagedAgentsTextBlock(type="text", text="first"),
        BetaManagedAgentsTextBlock(type="text", text="second appended"),
    ]
    assert snapshot.content[1] == BetaManagedAgentsTextBlock(type="text", text="second")


@pytest.mark.parametrize(
    "timestamp", [datetime(1970, 1, 1, tzinfo=timezone.utc), datetime(2024, 1, 1, tzinfo=timezone.utc)]
)
def test_final_message_before_any_preview_survives_repeated_start(timestamp: datetime) -> None:
    final = BetaManagedAgentsAgentMessageEvent(
        id="evt_1",
        type="agent.message",
        content=[BetaManagedAgentsTextBlock(type="text", text="canonical")],
        processed_at=timestamp,
    )
    snapshot = accumulate_managed_agents_event(None, final)
    assert snapshot is not final
    result = accumulate_managed_agents_event(snapshot, start("evt_1"))
    assert result == final
    assert result is snapshot


@pytest.mark.parametrize("completed", [False, True])
def test_start_for_a_different_id_still_opens_a_new_preview(completed: bool) -> None:
    snapshot = fold(seed("evt_1"), delta("evt_1", "old", 0))
    if completed:
        snapshot.processed_at = datetime(2024, 1, 1, tzinfo=timezone.utc)
    result = accumulate_managed_agents_event(snapshot, start("evt_2"))
    assert result is not None
    assert result is not snapshot
    assert result.id == "evt_2"
    assert result.content == []
    assert snapshot.content == [BetaManagedAgentsTextBlock(type="text", text="old")]
