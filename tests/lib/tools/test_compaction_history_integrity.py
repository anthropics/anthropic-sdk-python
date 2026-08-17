from __future__ import annotations

from types import SimpleNamespace
from typing import Any, cast

import pytest

from anthropic import Anthropic, AsyncAnthropic
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools._beta_runner import BetaAsyncToolRunner, BetaToolRunner
from anthropic.types.beta.beta_message_param import BetaMessageParam


pytestmark = pytest.mark.skipif(
    PYDANTIC_V1,
    reason="tool runner not supported with pydantic v1",
)


def _history() -> list[BetaMessageParam]:
    return [
        {
            "role": "assistant",
            "content": [
                {"type": "text", "text": "I will call the tool."},
                {
                    "type": "tool_use",
                    "id": "toolu_pending",
                    "name": "do_work",
                    "input": {"value": 1},
                },
            ],
        }
    ]


def _last_message() -> Any:
    return SimpleNamespace(
        usage=SimpleNamespace(
            input_tokens=10,
            cache_creation_input_tokens=0,
            cache_read_input_tokens=0,
            output_tokens=10,
        )
    )


def _block_types(message: BetaMessageParam) -> list[object]:
    content = cast("list[dict[str, object]]", message["content"])
    return [block["type"] for block in content]


def _assert_compaction_request_is_sanitized(messages: object) -> None:
    sent = cast("list[BetaMessageParam]", messages)
    assert _block_types(sent[0]) == ["text"]


def test_failed_sync_compaction_does_not_mutate_runner_history() -> None:
    def fail_create(**kwargs: Any) -> None:
        _assert_compaction_request_is_sanitized(kwargs["messages"])
        raise RuntimeError("compaction failed")

    client = cast(
        Anthropic,
        SimpleNamespace(beta=SimpleNamespace(messages=SimpleNamespace(create=fail_create))),
    )
    history = _history()

    with pytest.warns(DeprecationWarning, match="compaction_control.*deprecated"):
        runner = BetaToolRunner(
            params=cast(
                Any,
                {"model": "test-model", "max_tokens": 128, "messages": history},
            ),
            options={},
            tools=[],
            client=client,
            compaction_control={"enabled": True, "context_token_threshold": 1},
        )
    runner._last_message = _last_message()

    with pytest.raises(RuntimeError, match="compaction failed"):
        runner._check_and_compact()

    stored = cast("list[BetaMessageParam]", runner._params["messages"])
    assert stored[0]["content"] == history[0]["content"]
    assert _block_types(stored[0]) == ["text", "tool_use"]


@pytest.mark.asyncio
async def test_failed_async_compaction_does_not_mutate_runner_history() -> None:
    async def fail_create(**kwargs: Any) -> None:
        _assert_compaction_request_is_sanitized(kwargs["messages"])
        raise RuntimeError("compaction failed")

    client = cast(
        AsyncAnthropic,
        SimpleNamespace(beta=SimpleNamespace(messages=SimpleNamespace(create=fail_create))),
    )
    history = _history()

    with pytest.warns(DeprecationWarning, match="compaction_control.*deprecated"):
        runner = BetaAsyncToolRunner(
            params=cast(
                Any,
                {"model": "test-model", "max_tokens": 128, "messages": history},
            ),
            options={},
            tools=[],
            client=client,
            compaction_control={"enabled": True, "context_token_threshold": 1},
        )
    runner._last_message = _last_message()

    with pytest.raises(RuntimeError, match="compaction failed"):
        await runner._check_and_compact()

    stored = cast("list[BetaMessageParam]", runner._params["messages"])
    assert stored[0]["content"] == history[0]["content"]
    assert _block_types(stored[0]) == ["text", "tool_use"]
