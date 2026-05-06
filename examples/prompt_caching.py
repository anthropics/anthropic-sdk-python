#!/usr/bin/env -S uv run python

"""Prompt caching patterns.

Three patterns, each with a "first call" that creates the cache and a
"second call" that hits it. Inspect usage.cache_creation_input_tokens and
usage.cache_read_input_tokens to confirm.

Cache breakpoints are set with cache_control={"type": "ephemeral"} on the
last block of the prefix you want cached. The cache survives ~5 minutes
of inactivity. Up to 4 breakpoints per request.

Run: ANTHROPIC_API_KEY=... ./examples/prompt_caching.py
"""

from __future__ import annotations

import anthropic

MODEL = "claude-sonnet-4-5-20250929"

client = anthropic.Anthropic()


def show_usage(label: str, usage: anthropic.types.Usage) -> None:
    print(
        f"  {label:<14} input={usage.input_tokens:<5} "
        f"cache_create={usage.cache_creation_input_tokens or 0:<5} "
        f"cache_read={usage.cache_read_input_tokens or 0:<5} "
        f"output={usage.output_tokens}"
    )


# ---------------------------------------------------------------------------
# 1. Cache the system prompt
# ---------------------------------------------------------------------------
# Use when: a chatbot or agent reuses the same long instruction set across
# many user turns. Cache the system prompt once; every subsequent turn pays
# only the user message tokens.

LONG_SYSTEM_PROMPT = (
    "You are a senior staff software engineer reviewing pull requests. "
    "Apply these rules in order:\n"
    "1. Correctness over style. Flag bugs first; suggest cleaner phrasing only after.\n"
    "2. Prefer concrete suggestions with code over abstract advice.\n"
    "3. Cite the file and line. Never review code you can't see.\n"
    "4. If a change introduces a behavior shift, ask for a test.\n"
    "5. Reject PRs that mix unrelated concerns; ask for a split.\n"
    "6. Treat tests as first-class — a failing test is a real bug.\n"
    "7. Don't restate the diff. Tell the author what they can't see.\n"
    # Pad to ~1024 tokens minimum — caches must exceed the per-model floor.
    + ("Keep responses pragmatic, not exhaustive. " * 80)
)


def example_1_system_prompt() -> None:
    print("\n[1] cache the system prompt")

    first = client.messages.create(
        model=MODEL,
        max_tokens=256,
        system=[
            {
                "type": "text",
                "text": LONG_SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": "Review: `if (x = 5) { ... }`"}],
    )
    show_usage("first call", first.usage)

    second = client.messages.create(
        model=MODEL,
        max_tokens=256,
        system=[
            {
                "type": "text",
                "text": LONG_SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": "Review: `for (let i = 0; i < arr.length; i++)`"}],
    )
    show_usage("second call", second.usage)


# ---------------------------------------------------------------------------
# 2. Cache system prompt + tool definitions
# ---------------------------------------------------------------------------
# Use when: an agent loop calls the same model with the same tools turn
# after turn. Tool definitions are usually larger than the system prompt;
# caching them is the bigger win. Set the breakpoint on the final tool.

TOOLS: list[anthropic.types.ToolParam] = [
    {
        "name": "search_orders",
        "description": "Search the orders database by customer email, date range, or status.",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_email": {"type": "string"},
                "since": {"type": "string", "format": "date"},
                "until": {"type": "string", "format": "date"},
                "status": {
                    "type": "string",
                    "enum": ["pending", "shipped", "delivered", "cancelled"],
                },
            },
        },
    },
    {
        "name": "get_order_detail",
        "description": "Fetch the full detail of a single order by its reference number.",
        "input_schema": {
            "type": "object",
            "properties": {"reference_number": {"type": "string"}},
            "required": ["reference_number"],
        },
    },
    {
        "name": "issue_refund",
        "description": "Issue a refund against an order. Requires a reason code.",
        "input_schema": {
            "type": "object",
            "properties": {
                "reference_number": {"type": "string"},
                "amount_cents": {"type": "integer"},
                "reason_code": {
                    "type": "string",
                    "enum": ["damaged", "wrong_item", "lost_in_transit", "customer_request"],
                },
            },
            "required": ["reference_number", "amount_cents", "reason_code"],
            "cache_control": {"type": "ephemeral"},
        },
    },
]


def example_2_system_plus_tools() -> None:
    print("\n[2] cache system prompt + tool definitions")

    first = client.messages.create(
        model=MODEL,
        max_tokens=256,
        system=[
            {
                "type": "text",
                "text": LONG_SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        tools=TOOLS,
        messages=[{"role": "user", "content": "Find all pending orders for alice@example.com"}],
    )
    show_usage("first call", first.usage)

    second = client.messages.create(
        model=MODEL,
        max_tokens=256,
        system=[
            {
                "type": "text",
                "text": LONG_SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        tools=TOOLS,
        messages=[{"role": "user", "content": "Refund order #4421 — wrong item shipped, $1240"}],
    )
    show_usage("second call", second.usage)


# ---------------------------------------------------------------------------
# 3. Cache long static context before user turns
# ---------------------------------------------------------------------------
# Use when: Q&A over a fixed document, codebase, or knowledge base. Put the
# document in a user-message text block with cache_control on it; the
# follow-up question goes in a second block. Repeated questions on the same
# document hit the cache.

DOCUMENT = (
    "RAVEN-001 — Network Topology Reference\n"
    "===========================================\n\n"
    "Sun (10.10.100.235) is the primary daily driver.\n"
    "Moon (Tailscale 100.101.247.79) is the backup laptop.\n"
    "Mercury (100.88.76.14) is the heavy compute workhorse.\n"
    "Corvin (100.120.236.120) hosts the Raven AI services.\n"
    "corvin-server (100.114.209.83) hosts *-api.raven-cargo.app.\n"
    "Venus (100.107.135.17) is the Mac mini.\n"
    # Pad to exceed the cache floor.
    + ("Each host advertises its services over Tailscale and the local LAN. " * 200)
)


def example_3_long_context() -> None:
    print("\n[3] cache a long static document")

    first = client.messages.create(
        model=MODEL,
        max_tokens=256,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": DOCUMENT,
                        "cache_control": {"type": "ephemeral"},
                    },
                    {"type": "text", "text": "Which host is the daily driver?"},
                ],
            }
        ],
    )
    show_usage("first call", first.usage)

    second = client.messages.create(
        model=MODEL,
        max_tokens=256,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": DOCUMENT,
                        "cache_control": {"type": "ephemeral"},
                    },
                    {"type": "text", "text": "What hosts the Raven APIs?"},
                ],
            }
        ],
    )
    show_usage("second call", second.usage)


if __name__ == "__main__":
    example_1_system_prompt()
    example_2_system_plus_tools()
    example_3_long_context()
