"""Example: Using ConversationManager and AsyncConversationManager.

Demonstrates:
1. Sync ConversationManager — two-turn conversation, print usage, reset.
2. Async AsyncConversationManager — same flow with asyncio.run().

Requirements:
    ANTHROPIC_API_KEY environment variable must be set.

Usage::

    python examples/helpers/conversation_example.py
"""

from __future__ import annotations

import asyncio

import anthropic
from anthropic.helpers import AsyncConversationManager, ConversationManager


# ---------------------------------------------------------------------------
# 1. Sync example
# ---------------------------------------------------------------------------


def sync_example() -> None:
    print("=" * 60)
    print("Sync ConversationManager")
    print("=" * 60)

    client = anthropic.Anthropic()

    mgr = ConversationManager(
        client,
        model="claude-opus-4-5",
        max_tokens=256,
        system="You are a helpful assistant. Be concise.",
        context_window_limit=200_000,
        token_budget_headroom=0.10,
    )

    print(repr(mgr))

    # Turn 1
    response = mgr.get_response("What is the capital of France?")
    print(f"\n[Turn 1] User: What is the capital of France?")
    print(f"[Turn 1] Assistant: {response.content[0].text}")
    print(f"[Turn 1] Usage: {mgr.last_usage}")

    # Turn 2
    response = mgr.get_response("And what language do they speak there?")
    print(f"\n[Turn 2] User: And what language do they speak there?")
    print(f"[Turn 2] Assistant: {response.content[0].text}")
    print(f"[Turn 2] Usage: {mgr.last_usage}")

    print(f"\nHistory length: {len(mgr.history)} messages")
    print(repr(mgr))

    # Reset
    mgr.reset()
    print(f"\nAfter reset — history length: {len(mgr.history)}, last_usage: {mgr.last_usage}")


# ---------------------------------------------------------------------------
# 2. Async example
# ---------------------------------------------------------------------------


async def async_example() -> None:
    print("\n" + "=" * 60)
    print("Async AsyncConversationManager")
    print("=" * 60)

    client = anthropic.AsyncAnthropic()

    mgr = AsyncConversationManager(
        client,
        model="claude-opus-4-5",
        max_tokens=256,
        system="You are a helpful assistant. Be concise.",
        context_window_limit=200_000,
        token_budget_headroom=0.10,
    )

    print(repr(mgr))

    # Turn 1
    response = await mgr.get_response("What is the tallest mountain on Earth?")
    print(f"\n[Turn 1] User: What is the tallest mountain on Earth?")
    print(f"[Turn 1] Assistant: {response.content[0].text}")
    print(f"[Turn 1] Usage: {mgr.last_usage}")

    # Turn 2
    response = await mgr.get_response("How tall is it in feet?")
    print(f"\n[Turn 2] User: How tall is it in feet?")
    print(f"[Turn 2] Assistant: {response.content[0].text}")
    print(f"[Turn 2] Usage: {mgr.last_usage}")

    print(f"\nHistory length: {len(mgr.history)} messages")
    print(repr(mgr))

    # Reset
    mgr.reset()
    print(f"\nAfter reset — history length: {len(mgr.history)}, last_usage: {mgr.last_usage}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    sync_example()
    asyncio.run(async_example())
