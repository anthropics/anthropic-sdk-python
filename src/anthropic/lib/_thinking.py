"""Utilities for managing extended thinking blocks in conversation history.

Extended thinking blocks carry a ``signature`` field that is valid only for
the specific conversation context they were created in.  Long multi-turn
sessions or any operation that reconstructs history from stored messages can
hit a 400 "Invalid ``signature`` in ``thinking`` block" error because the
server-side context that produced the signature no longer matches.
``strip_thinking_blocks`` removes those blocks before the history is replayed,
providing the only documented recovery path.
"""

from __future__ import annotations

from typing import Iterable

from ..types.message_param import MessageParam

__all__ = ["strip_thinking_blocks"]

_THINKING_TYPES = frozenset({"thinking", "redacted_thinking"})


def _block_type(block: object) -> str:
    """Return the ``type`` field of a content block regardless of representation.

    Accepts plain dicts (TypedDict values, JSON-decoded payloads) and Pydantic
    ``BaseModel`` instances (``ThinkingBlock``, ``RedactedThinkingBlock``, …).
    Returns ``""`` for anything that carries no ``type``.
    """
    if isinstance(block, dict):
        return block.get("type", "")
    return getattr(block, "type", "")


def strip_thinking_blocks(
    messages: Iterable[MessageParam],
) -> list[MessageParam]:
    """Return a copy of *messages* with every thinking and redacted-thinking block removed.

    Use this when replaying conversation history fails with
    ``"Invalid `signature` in `thinking` block"``: the ``signature`` stored in
    a ``ThinkingBlock`` is bound to the exact server-side conversation context
    it was created in and is not guaranteed to remain valid after session
    expiry, model upgrades, or history reconstruction from storage.

    Only the ``content`` list is modified; string content and all non-thinking
    blocks are preserved verbatim.  The ``role`` and any other keys on each
    message dict are copied through unchanged.

    Example::

        try:
            response = client.messages.create(model=model, messages=history, ...)
        except anthropic.BadRequestError as exc:
            if "Invalid `signature` in `thinking` block" in str(exc):
                history = strip_thinking_blocks(history)
                response = client.messages.create(model=model, messages=history, ...)
            else:
                raise

    Args:
        messages: The conversation history to clean.  Each entry must be a
            ``MessageParam``-compatible mapping with at least ``role`` and
            ``content`` keys.

    Returns:
        A new ``list[MessageParam]`` in the same order, with thinking and
        redacted-thinking content blocks omitted from every message.
    """
    result: list[MessageParam] = []
    for msg in messages:
        content = msg.get("content")  # type: ignore[attr-defined]
        if isinstance(content, str):
            # Plain-text content carries no thinking blocks.
            result.append(dict(msg))  # type: ignore[arg-type]
            continue
        filtered: list[object] = [
            block for block in content  # type: ignore[union-attr]
            if _block_type(block) not in _THINKING_TYPES
        ]
        result.append({**msg, "content": filtered})  # type: ignore[typeddict-item]
    return result
