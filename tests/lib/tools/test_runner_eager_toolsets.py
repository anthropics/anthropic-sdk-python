"""A tool runner with `run_tools_eagerly` and a toolset. The runner runs a toolset call while the reply streams, once
the model has moved on from it, and the toolset's `confirm` is asked before the call runs. Once one of a toolset's calls
fails or is held, that toolset's later calls wait for the reply to end. Function tools and other toolsets don't wait.

The replies and the timeline are the ones of `test_runner_eager_tools.py`. `computer={}` and `browser={}` add a
toolset whose calls are written to the timeline, with these options."""

from __future__ import annotations

import os
import json
from typing import Any, Callable

import pytest

from anthropic import beta_tool, beta_async_tool
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools import ToolError
from anthropic.tools.browser import BetaConfirmContext
from anthropic.tools.computer import BetaComputerConfirmContext

from .toolsets._stubs import EchoBrowserToolset, AsyncEchoBrowserToolset
from .test_runner_eager_tools import (  # the fixtures
    Block,
    Setup,
    SetupFactory,
    call,
    done,
    sync as sync,
    reply,
    setup as setup,
    events_of,
    replies_of,
    first_reply,
    results_sent,
    toolset_call,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

pytestmark = [
    pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1"),
    pytest.mark.respx(base_url=base_url),
]


async def test_a_toolset_call_does_not_run_a_function_tool_of_the_same_name(setup: SetupFactory, sync: bool) -> None:
    ran: list[str] = []
    key_tool: Any
    if sync:

        @beta_tool(name="key")
        def sync_key(text: str) -> str:
            """A function tool named like the computer toolset's `key` tool."""
            ran.append(text)
            return "the function tool ran"

        key_tool = sync_key
    else:

        @beta_async_tool(name="key")
        async def async_key(text: str) -> str:
            """A function tool named like the computer toolset's `key` tool."""
            ran.append(text)
            return "the function tool ran"

        key_tool = async_key
    test = setup([reply(toolset_call("k")), done()], computer={}, extra_tools=[key_tool])

    async for stream in replies_of(test.runner):
        async for _event in events_of(stream):
            pass

    results = results_sent(test)
    assert ran == []
    assert test.desktop.calls == ["key"]
    assert [result["tool_use_id"] for result in results] == ["toolu_k"]
    assert "the function tool ran" not in json.dumps(results)


@pytest.mark.parametrize("family", ["computer", "browser"])
async def test_starts_a_toolset_call_once_the_model_has_moved_on_from_it(setup: SetupFactory, family: str) -> None:
    tool_call, started = family_call(family)
    test = setup(
        [reply(call("a"), tool_call, call("b")), done()],
        computer={} if family == "computer" else None,
        browser={} if family == "browser" else None,
    )

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            test.see(event)
        test.timeline.append("loop body ends")

    assert first_reply(test.timeline) == [
        "message_start",
        "a: content_block_start",
        "a: content_block_delta",
        "input_json",
        "a: content_block_stop",
        "k: content_block_start",  # the model has moved on from a
        "lookup(a) STARTS",
        "k: content_block_delta",
        "input_json",
        "k: content_block_stop",
        "b: content_block_start",  # the model has moved on from the toolset call
        started,
        "b: content_block_delta",
        "input_json",
        "b: content_block_stop",
        "message_delta (tool_use)",  # the model has moved on from b
        "lookup(b) STARTS",
        "message_stop",
        "loop body ends",
    ]
    # The results go back in the model's order, and the toolset call ran once.
    results = results_sent(test)
    assert [result["tool_use_id"] for result in results] == ["toolu_a", "toolu_k", "toolu_b"]
    assert not results[1].get("is_error")


@pytest.mark.parametrize("family", ["computer", "browser"])
async def test_asks_confirm_before_a_call_runs_while_the_reply_streams(setup: SetupFactory, family: str) -> None:
    tool_call, started = family_call(family)
    asked: list[str] = []

    def confirm(context: BetaConfirmContext | BetaComputerConfirmContext) -> bool:
        asked.append(context.member)
        test.timeline.append(f"confirm {context.member}")
        return True

    test = setup(
        [reply(tool_call, call("b")), done()],
        computer={"confirm": confirm} if family == "computer" else None,
        browser={"confirm": confirm} if family == "browser" else None,
    )

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            test.see(event)
        test.timeline.append("loop body ends")

    # The toolset call runs while the reply streams, after `confirm` has approved it.
    member = asked[0]
    assert starts(first_reply(test.timeline), also="confirm") == [
        f"confirm {member}",
        started,
        "lookup(b) STARTS",
        "loop body ends",
    ]


@pytest.mark.parametrize("family", ["computer", "browser"])
async def test_does_not_run_a_call_that_confirm_declines_or_the_toolsets_calls_after_it(
    setup: SetupFactory, family: str
) -> None:
    first, _started = family_call(family, "k1")
    second, _started = family_call(family, "k2")

    def confirm(context: BetaConfirmContext | BetaComputerConfirmContext) -> bool:
        test.timeline.append(f"confirm {context.member}")
        return False

    test = setup(
        [reply(first, second), done()],
        computer={"confirm": confirm} if family == "computer" else None,
        browser={"confirm": confirm} if family == "browser" else None,
    )

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            test.see(event)
        test.timeline.append("loop body ends")

    # `confirm` is asked once, no tool starts, and the second call is not run.
    lines = starts(first_reply(test.timeline), also="confirm")
    assert len(lines) == 2 and lines[0].startswith("confirm ") and lines[1] == "loop body ends"
    results = results_sent(test)
    assert [result["tool_use_id"] for result in results] == ["toolu_k1", "toolu_k2"]
    assert results[0]["is_error"] and results[1]["is_error"]
    assert "Not executed" in json.dumps(results[1])


async def test_starts_javascript_exec_like_any_other_call(setup: SetupFactory) -> None:
    test = setup([reply(call("a"), js_call("j"), call("b")), done()], browser=JS_BROWSER)

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            test.see(event)
        test.timeline.append("loop body ends")

    assert starts(first_reply(test.timeline)) == [
        "lookup(a) STARTS",
        "browser javascript_exec STARTS",
        "lookup(b) STARTS",
        "loop body ends",
    ]


async def test_a_toolset_call_that_the_caller_defers_holds_its_toolsets_later_calls_and_no_other_call(
    setup: SetupFactory,
) -> None:
    wait = toolset_call("w", "wait", {"duration": 1}, "browser")
    test = setup(
        [reply(call("a"), toolset_call("k1"), call("f"), wait, toolset_call("k2")), done()],
        computer={},
        browser={},
    )
    see = defer_calls(test, "toolu_k1")

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            see(event)
        test.timeline.append("loop body ends")

    assert starts(first_reply(test.timeline)) == [
        "lookup(a) STARTS",
        "lookup(f) STARTS",  # a function tool doesn't wait for the held call
        "browser wait STARTS",  # nor does another toolset
        "loop body ends",
        "computer key STARTS",  # k1
        "computer key STARTS",  # k2 waited behind it
    ]
    assert [result["tool_use_id"] for result in results_sent(test)] == [
        "toolu_a",
        "toolu_k1",
        "toolu_f",
        "toolu_w",
        "toolu_k2",
    ]


async def test_a_function_call_that_the_caller_defers_holds_no_other_call(setup: SetupFactory) -> None:
    test = setup([reply(call("a"), toolset_call("k"), call("b")), done()], computer={})
    see = defer_calls(test, "toolu_a")

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            see(event)
        test.timeline.append("loop body ends")

    assert starts(first_reply(test.timeline)) == [
        "computer key STARTS",
        "lookup(b) STARTS",
        "loop body ends",
        "lookup(a) STARTS",
    ]


async def test_lists_only_the_call_that_the_caller_defers_and_not_its_toolsets_later_calls(
    setup: SetupFactory,
) -> None:
    test = setup([reply(toolset_call("k1"), toolset_call("k2")), done()], computer={})
    see = defer_calls(test, "toolu_k1")
    listed: list[list[str]] = []

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            see(event)
        listed.append([tool_use.id for tool_use in test.runner.deferred_tool_calls])
        break

    assert listed == [["toolu_k1"]]


async def test_the_hold_ends_with_the_reply(setup: SetupFactory) -> None:
    test = setup([reply(toolset_call("k1"), toolset_call("k2")), reply(toolset_call("k3")), done()], computer={})
    see = defer_calls(test, "toolu_k1")

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            see(event)
        test.timeline.append("loop body ends")

    second_reply = test.timeline[test.timeline.index("request 2") : test.timeline.index("request 3")]
    assert starts(second_reply) == [
        "computer key STARTS",  # the next reply's calls run early again
        "loop body ends",
    ]


async def test_does_not_run_a_call_that_has_not_started_when_the_caller_leaves_the_loop(
    setup: SetupFactory,
) -> None:
    test = setup([reply(toolset_call("k1"), toolset_call("k2")), done()], computer={})

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            test.see(event)
            # The model has moved on from k1, so k1 has run. k2 has not.
            if event.type == "content_block_stop" and event.content_block.type == "tool_use":
                if event.content_block.id == "toolu_k2":
                    break
        break

    assert starts(test.timeline) == ["computer key STARTS"]


async def test_does_not_run_a_held_call_once_one_of_its_toolsets_calls_has_failed(setup: SetupFactory) -> None:
    test = setup([reply(toolset_call("k1"), toolset_call("k2")), done()], computer={})
    test.desktop.fail["key"] = ToolError("no such key")
    see = defer_calls(test, "toolu_k2")

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            see(event)
        test.timeline.append("loop body ends")

    assert starts(first_reply(test.timeline)) == ["computer key STARTS", "loop body ends"]
    results = results_sent(test)
    assert [result["tool_use_id"] for result in results] == ["toolu_k1", "toolu_k2"]
    assert "Not executed" in json.dumps(results[1])


async def test_a_call_named_like_a_toolset_with_no_toolset_name_holds_that_toolsets_later_calls(
    setup: SetupFactory,
) -> None:
    # The runner answers such a call as a malformed toolset call when it builds the tool response. That answers the
    # toolset's later calls with `Not executed`, so none of them may have run.
    malformed = toolset_call("m", "computer", {"action": "key"}, None)
    test = setup([reply(call("a"), malformed, toolset_call("k"), call("b")), done()], computer={})

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            test.see(event)
        test.timeline.append("loop body ends")

    assert starts(first_reply(test.timeline)) == ["lookup(a) STARTS", "lookup(b) STARTS", "loop body ends"]
    results = results_sent(test)
    assert [result["tool_use_id"] for result in results] == ["toolu_a", "toolu_m", "toolu_k", "toolu_b"]
    assert results[1]["is_error"] and results[2]["is_error"] and not results[3].get("is_error")
    assert "Not executed" in json.dumps(results[2])


async def test_a_held_call_named_like_a_toolset_with_no_toolset_name_holds_that_toolsets_later_calls(
    setup: SetupFactory,
) -> None:
    # The caller holds the malformed call. It is still answered as malformed when the tool response is built, and that
    # answers the toolset's later calls with `Not executed`, so none of them may have run.
    malformed = toolset_call("m", "computer", {"action": "key"}, None)
    test = setup([reply(malformed, toolset_call("k"), call("b")), done()], computer={})
    see = defer_calls(test, "toolu_m")

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            see(event)
        test.timeline.append("loop body ends")

    assert starts(first_reply(test.timeline)) == ["lookup(b) STARTS", "loop body ends"]
    results = results_sent(test)
    assert [result["tool_use_id"] for result in results] == ["toolu_m", "toolu_k", "toolu_b"]
    assert "Not executed" in json.dumps(results[1])


async def test_a_call_to_a_toolset_the_runner_does_not_have_is_answered_as_not_found(
    setup: SetupFactory,
) -> None:
    test = setup([reply(call("a"), toolset_call("k"), call("b")), done()])

    with pytest.warns(UserWarning, match="not found in tool runner"):
        async for stream in replies_of(test.runner):
            async for event in events_of(stream):
                test.see(event)
            test.timeline.append("loop body ends")

    assert starts(first_reply(test.timeline)) == ["lookup(a) STARTS", "lookup(b) STARTS", "loop body ends"]
    results = results_sent(test)
    assert [result["tool_use_id"] for result in results] == ["toolu_a", "toolu_k", "toolu_b"]
    assert results[1]["is_error"] and "not found" in json.dumps(results[1])


async def test_runs_no_later_call_of_a_toolset_once_one_of_its_calls_has_failed(setup: SetupFactory) -> None:
    test = setup([reply(toolset_call("k1"), toolset_call("k2"), call("c")), done()], computer={})

    test.desktop.fail["key"] = ToolError("no such key")

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            test.see(event)
        test.timeline.append("loop body ends")

    # k2 doesn't start after k1 failed. It is answered with `Not executed`, and c, which is not a toolset call, runs.
    assert starts(first_reply(test.timeline)) == ["computer key STARTS", "lookup(c) STARTS", "loop body ends"]
    results = results_sent(test)
    assert [result["tool_use_id"] for result in results] == ["toolu_k1", "toolu_k2", "toolu_c"]
    assert results[0]["is_error"] and results[1]["is_error"] and not results[2].get("is_error")
    assert "Not executed" in json.dumps(results[1])


async def test_a_toolset_that_does_not_extend_the_sdks_classes_starts_its_calls_early_too(
    setup: SetupFactory, sync: bool
) -> None:
    echo = EchoBrowserToolset() if sync else AsyncEchoBrowserToolset()
    test = setup(
        [reply(call("a"), toolset_call("w", "wait", {"duration": 1}, "browser"), call("b")), done()],
        extra_tools=[echo],
    )
    ran_while_streaming: list[str] = []

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            test.see(event)
        ran_while_streaming += [name for name, _input in echo.calls]
        test.timeline.append("loop body ends")

    assert ran_while_streaming[:1] == ["wait"]
    assert [name for name, _input in echo.calls] == ["wait"]  # it ran once


# ---------------------------------------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------------------------------------


def allow(_context: BetaConfirmContext | BetaComputerConfirmContext) -> bool:
    """A `confirm` that approves every call."""
    return True


JS_BROWSER: dict[str, Any] = {"confirm": allow, "configs": {"javascript_exec": {"enabled": True}}}
"""Options for a browser toolset that serves `javascript_exec`."""


def js_call(key: str) -> Block:
    """A call to the browser's `javascript_exec`."""
    return toolset_call(key, "javascript_exec", {"text": "1"}, "browser")


def starts(timeline: list[str], *, also: str | None = None) -> list[str]:
    """When each tool started, and when the caller's loop body ended. `also` keeps the lines that start with it too."""
    return [
        line
        for line in timeline
        if "STARTS" in line or line == "loop body ends" or (also is not None and line.startswith(also))
    ]


def family_call(family: str, key: str = "k") -> tuple[Block, str]:
    """A call to a tool of the `family` toolset, and the timeline line for when that tool starts."""
    if family == "computer":
        return toolset_call(key), "computer key STARTS"
    return toolset_call(key, "wait", {"duration": 1}, "browser"), "browser wait STARTS"


def defer_calls(test: Setup, *ids: str) -> Callable[[Any], None]:
    """Defers the calls with these ids, when the caller sees their blocks finish. Pass each event to what it returns."""

    def see(event: Any) -> None:
        test.see(event)
        if event.type == "content_block_stop" and event.content_block.type == "tool_use":
            if event.content_block.id in ids:
                test.runner.defer_tool_call(event.content_block)

    return see
