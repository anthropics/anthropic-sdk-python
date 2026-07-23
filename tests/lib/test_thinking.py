"""Tests for strip_thinking_blocks (:mod:`anthropic.lib._thinking`).

Extended thinking block signatures are tied to the conversation context they
were created in and may become invalid when replaying stored history.
``strip_thinking_blocks`` removes those blocks so the history can be re-sent
without a 400 error.
"""

from __future__ import annotations

from anthropic.lib._thinking import strip_thinking_blocks

# ---------------------------------------------------------------------------
# Helpers — build content blocks as plain dicts (the most common representation
# callers have) and as minimal object stubs (mimicking BaseModel responses).
# ---------------------------------------------------------------------------


def _thinking(text: str = "thinking…") -> dict:
    return {"type": "thinking", "thinking": text, "signature": "sig_abc"}


def _redacted() -> dict:
    return {"type": "redacted_thinking", "data": "opaque"}


def _text(text: str = "hello") -> dict:
    return {"type": "text", "text": text}


def _tool_use() -> dict:
    return {"type": "tool_use", "id": "tu_1", "name": "my_tool", "input": {}}


class _FakeThinkingBlock:
    """Minimal stub that looks like a ThinkingBlock BaseModel instance."""

    type = "thinking"
    thinking = "deep thought"
    signature = "sig_xyz"


class _FakeRedactedBlock:
    type = "redacted_thinking"
    data = "bytes"


class _FakeTextBlock:
    type = "text"
    text = "plain text"


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_string_content_passes_through_unchanged() -> None:
    messages = [{"role": "user", "content": "hello"}]
    result = strip_thinking_blocks(messages)
    assert result == [{"role": "user", "content": "hello"}]


def test_thinking_block_removed_from_assistant() -> None:
    messages = [
        {
            "role": "assistant",
            "content": [_thinking(), _text("answer")],
        }
    ]
    result = strip_thinking_blocks(messages)
    assert len(result[0]["content"]) == 1  # type: ignore[arg-type]
    assert result[0]["content"][0]["type"] == "text"  # type: ignore[index]


def test_redacted_thinking_block_removed() -> None:
    messages = [
        {
            "role": "assistant",
            "content": [_redacted(), _text("answer")],
        }
    ]
    result = strip_thinking_blocks(messages)
    assert len(result[0]["content"]) == 1  # type: ignore[arg-type]
    assert result[0]["content"][0]["type"] == "text"  # type: ignore[index]


def test_mixed_content_only_removes_thinking_types() -> None:
    messages = [
        {
            "role": "assistant",
            "content": [_thinking(), _text("A"), _tool_use(), _redacted(), _text("B")],
        }
    ]
    result = strip_thinking_blocks(messages)
    content = result[0]["content"]  # type: ignore[index]
    assert len(content) == 3  # type: ignore[arg-type]
    types = [b["type"] for b in content]  # type: ignore[index]
    assert types == ["text", "tool_use", "text"]


def test_user_messages_without_thinking_unchanged() -> None:
    messages = [
        {"role": "user", "content": [_text("what?")]},
    ]
    result = strip_thinking_blocks(messages)
    assert result[0]["content"] == [_text("what?")]  # type: ignore[index]


def test_non_thinking_blocks_preserved_verbatim() -> None:
    blocks = [_text("one"), _tool_use(), _text("two")]
    messages = [{"role": "assistant", "content": blocks}]
    result = strip_thinking_blocks(messages)
    assert result[0]["content"] == blocks  # type: ignore[index]


def test_all_thinking_produces_empty_content_list() -> None:
    # Edge case: a message whose entire content is thinking blocks.
    messages = [{"role": "assistant", "content": [_thinking(), _redacted()]}]
    result = strip_thinking_blocks(messages)
    assert result[0]["content"] == []  # type: ignore[index]


def test_empty_messages_list() -> None:
    assert strip_thinking_blocks([]) == []


def test_multiple_messages_processed_independently() -> None:
    messages = [
        {"role": "user", "content": "first"},
        {"role": "assistant", "content": [_thinking(), _text("first answer")]},
        {"role": "user", "content": "second"},
        {"role": "assistant", "content": [_thinking(), _text("second answer")]},
    ]
    result = strip_thinking_blocks(messages)
    assert result[0]["content"] == "first"
    assert result[1]["content"] == [_text("first answer")]  # type: ignore[index]
    assert result[2]["content"] == "second"
    assert result[3]["content"] == [_text("second answer")]  # type: ignore[index]


def test_basemodel_instances_stripped() -> None:
    # When blocks are BaseModel instances (as returned by the SDK), the type
    # attribute is accessed via getattr rather than dict lookup.
    messages = [
        {
            "role": "assistant",
            "content": [_FakeThinkingBlock(), _FakeTextBlock()],
        }
    ]
    result = strip_thinking_blocks(messages)
    content = result[0]["content"]  # type: ignore[index]
    assert len(content) == 1  # type: ignore[arg-type]
    assert content[0].type == "text"  # type: ignore[index]


def test_redacted_basemodel_instance_stripped() -> None:
    messages = [
        {
            "role": "assistant",
            "content": [_FakeRedactedBlock(), _FakeTextBlock()],
        }
    ]
    result = strip_thinking_blocks(messages)
    assert len(result[0]["content"]) == 1  # type: ignore[arg-type]


def test_does_not_mutate_original_messages() -> None:
    original_content = [_thinking(), _text("answer")]
    messages = [{"role": "assistant", "content": original_content}]
    strip_thinking_blocks(messages)
    # The original list must be unchanged.
    assert len(original_content) == 2
    assert original_content[0]["type"] == "thinking"


def test_role_and_other_keys_preserved() -> None:
    messages = [
        {
            "role": "assistant",
            "content": [_thinking(), _text("hi")],
        }
    ]
    result = strip_thinking_blocks(messages)
    assert result[0]["role"] == "assistant"


def test_idempotent() -> None:
    messages = [
        {"role": "assistant", "content": [_thinking(), _text("hi")]},
    ]
    once = strip_thinking_blocks(messages)
    twice = strip_thinking_blocks(once)
    assert once == twice
