"""How a tool runner with `run_tools_eagerly` runs tool calls. `setup()` turns the option on.

Most tests here assert a timeline: what the caller saw, in order, and where each tool started.

    "a: content_block_stop"   the caller got this stream event
    "lookup(a) STARTS"        the runner called the tool
    "loop body ends"          the caller finished its `for stream in runner` body

Every reply is made of `call("a")`, which is the model calling `lookup(key="a")` with the id `toolu_a`, and
`text("...")`. Every test runs on the sync and on the async runner: `replies_of()`, `events_of()` and `settled()`
let one test body drive both. The first five tests are the behavior in short.
"""

from __future__ import annotations

import os
import json
import inspect
from typing import Any, TypeVar, NamedTuple
from collections.abc import Callable, Iterator, Awaitable, AsyncIterator
from typing_extensions import override

import httpx2
import pytest
from respx import MockRouter

from anthropic import Anthropic, AsyncAnthropic, beta_tool, beta_async_tool
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools import ToolError
from anthropic.types.beta import BetaMessageParam
from anthropic.lib.streaming import BetaMessageStream, BetaAsyncMessageStream

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

pytestmark = [
    pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1"),
    pytest.mark.respx(base_url=base_url),
]

_T = TypeVar("_T")


async def test_runs_each_tool_once_the_model_has_moved_on_from_its_call(setup: SetupFactory) -> None:
    test = setup([reply(call("a"), call("b")), done()])

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
        "b: content_block_start",  # the model has moved on from a
        "lookup(a) STARTS",
        "b: content_block_delta",
        "input_json",
        "b: content_block_stop",
        "message_delta (tool_use)",  # the model has moved on from b
        "lookup(b) STARTS",
        "message_stop",
        "loop body ends",
    ]


async def test_runs_every_tool_after_the_loop_body_when_not_streaming_as_before(setup: SetupFactory) -> None:
    test = setup([reply(call("a"), call("b")), done()], stream=False)

    async for _message in replies_of(test.runner):
        test.timeline.append("loop body ends")

    assert first_reply(test.timeline) == ["loop body ends", "lookup(a) STARTS", "lookup(b) STARTS"]


async def test_holds_a_call_that_the_caller_defers_until_the_loop_body_ends(setup: SetupFactory) -> None:
    test = setup([reply(call("a"), call("b"), call("c")), done()])

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            test.see(event)
            if event.type == "content_block_stop" and event.content_block.type == "tool_use":
                if event.content_block.id == "toolu_b":
                    test.runner.defer_tool_call(event.content_block)
        test.timeline.append("loop body ends")

    assert first_reply(test.timeline) == [
        "message_start",
        "a: content_block_start",
        "a: content_block_delta",
        "input_json",
        "a: content_block_stop",
        "b: content_block_start",
        "lookup(a) STARTS",
        "b: content_block_delta",
        "input_json",
        "b: content_block_stop",  # the caller defers b here
        "c: content_block_start",  # b would have run after this event
        "c: content_block_delta",
        "input_json",
        "c: content_block_stop",
        "message_delta (tool_use)",
        "lookup(c) STARTS",
        "message_stop",
        "loop body ends",
        "lookup(b) STARTS",
    ]
    # The results go back in the model's order, whatever order the calls ran in.
    assert results_sent(test) == [
        {"type": "tool_result", "tool_use_id": "toolu_a", "content": "value of a"},
        {"type": "tool_result", "tool_use_id": "toolu_b", "content": "value of b"},
        {"type": "tool_result", "tool_use_id": "toolu_c", "content": "value of c"},
    ]


async def test_lists_the_calls_that_are_being_held_so_that_the_caller_can_decide_about_them(
    setup: SetupFactory,
) -> None:
    test = setup([reply(call("a"), call("b")), done()])

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            if event.type == "content_block_start" and event.content_block.type == "tool_use":
                if event.content_block.id == "toolu_b":
                    test.runner.defer_tool_call(event.content_block)

        held = test.runner.deferred_tool_calls

        assert [tool_use.to_dict() for tool_use in held] == [
            {"type": "tool_use", "id": "toolu_b", "name": "lookup", "input": {"key": "b"}}
        ]
        break  # the caller decides against b

    assert test.timeline == ["lookup(a) STARTS"]


async def test_runs_each_call_once(setup: SetupFactory) -> None:
    test = setup([reply(call("a"), call("b"))])

    async for stream in replies_of(test.runner):
        test.runner.defer_tool_call("toolu_a")
        message = await settled(stream.get_final_message())

        response = await settled(test.runner.generate_tool_call_response())
        # append_messages() drops the cached response, so the second call answers the reply again.
        test.runner.append_messages(message, response)
        assert await settled(test.runner.generate_tool_call_response()) == response
        break

    assert test.timeline == ["lookup(b) STARTS", "lookup(a) STARTS"]


# ---------------------------------------------------------------------------------------------------------
# without `run_tools_eagerly`
# ---------------------------------------------------------------------------------------------------------


async def test_without_the_option_every_tool_runs_after_the_loop_body_as_before(setup: SetupFactory) -> None:
    test = setup([reply(call("a"), call("b")), done()], run_tools_eagerly=False)

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
        "b: content_block_start",
        "b: content_block_delta",
        "input_json",
        "b: content_block_stop",
        "message_delta (tool_use)",
        "message_stop",
        "loop body ends",
        "lookup(a) STARTS",
        "lookup(b) STARTS",
    ]


async def test_without_the_option_there_is_nothing_to_defer(setup: SetupFactory) -> None:
    test = setup([reply(call("a")), done()], run_tools_eagerly=False)

    async for stream in replies_of(test.runner):
        test.runner.defer_tool_call("toolu_a")
        await settled(stream.get_final_message())
        assert test.runner.deferred_tool_calls == []
        test.timeline.append("loop body ends")

    assert first_reply(test.timeline) == ["loop body ends", "lookup(a) STARTS"]


async def test_without_the_option_the_tools_run_again_after_append_messages_as_before(setup: SetupFactory) -> None:
    test = setup([reply(call("a"))], run_tools_eagerly=False)

    async for _stream in replies_of(test.runner):
        await settled(test.runner.generate_tool_call_response())
        test.runner.append_messages({"role": "user", "content": "Go on."})
        await settled(test.runner.generate_tool_call_response())
        break

    assert test.timeline == ["lookup(a) STARTS", "lookup(a) STARTS"]


# ---------------------------------------------------------------------------------------------------------
# the `run_tools_eagerly` option
# ---------------------------------------------------------------------------------------------------------


async def test_the_option_is_not_sent_to_the_api(setup: SetupFactory) -> None:
    test = setup([reply_ending("compaction", compaction()), reply(call("a")), done()])

    test.runner.compact_before_next_turn()
    await settled(test.runner.until_done())

    assert ["compaction" in request for request in test.requests] == [True, False, False]
    assert ["run_tools_eagerly" in request for request in test.requests] == [False, False, False]


async def test_yields_the_stream_that_messages_stream_returns(setup: SetupFactory) -> None:
    test = setup([done()])

    async for stream in replies_of(test.runner):
        assert type(stream) is (BetaMessageStream if test.sync else BetaAsyncMessageStream)
        assert (await settled(stream.get_final_message())).stop_reason == "end_turn"

    assert test.requests[0]["stream"] is True


@pytest.mark.parametrize("stream", [False, None], ids=["stream=False", "stream left out"])
def test_the_option_needs_stream(
    sync: bool, client: Anthropic, async_client: AsyncAnthropic, stream: bool | None
) -> None:
    tool_runner: Any = (client if sync else async_client).beta.messages.tool_runner
    options = {} if stream is None else {"stream": stream}

    with pytest.raises(ValueError, match="`run_tools_eagerly=True` and `stream=False` are mutually exclusive"):
        tool_runner(**PARAMS, tools=[], run_tools_eagerly=True, **options)

    tool_runner(**PARAMS, tools=[], run_tools_eagerly=False, **options)


# ---------------------------------------------------------------------------------------------------------
# when a tool call runs
# ---------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("read", ["events", "text_stream", "get_final_message", "until_done"])
async def test_runs_the_calls_while_the_caller_reads_the_stream_however_it_reads_it(
    setup: SetupFactory, read: str
) -> None:
    test = setup([reply(call("a"), text("Found a."), call("b")), done()])

    async for stream in replies_of(test.runner):
        if read == "events":
            async for _event in events_of(stream):
                pass
        elif read == "text_stream":
            async for _text in events_of(stream.text_stream):
                pass
        elif read == "get_final_message":
            await settled(stream.get_final_message())
        else:
            await settled(stream.until_done())
        test.timeline.append("loop body ends")

    assert first_reply(test.timeline) == ["lookup(a) STARTS", "lookup(b) STARTS", "loop body ends"]


async def test_runs_the_calls_after_the_loop_body_when_the_caller_does_not_read_the_stream(
    setup: SetupFactory,
) -> None:
    test = setup([reply(call("a"), call("b")), done()])

    async for _stream in replies_of(test.runner):
        test.timeline.append("loop body ends")

    assert first_reply(test.timeline) == ["loop body ends", "lookup(a) STARTS", "lookup(b) STARTS"]


async def test_runs_the_remaining_calls_after_the_loop_body_when_the_caller_stops_reading_early(
    setup: SetupFactory,
) -> None:
    test = setup([reply(call("a"), call("b"), call("c")), done()])

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            test.see(event)
            if event.type == "content_block_delta" and event.index == 1:
                break
        test.timeline.append("loop body ends")

    assert first_reply(test.timeline)[-5:] == [
        "lookup(a) STARTS",
        "b: content_block_delta",
        "loop body ends",
        "lookup(b) STARTS",
        "lookup(c) STARTS",
    ]
    assert [result["tool_use_id"] for result in results_sent(test)] == ["toolu_a", "toolu_b", "toolu_c"]


async def test_does_not_wait_for_the_reply_to_end(setup: SetupFactory) -> None:
    test = setup([event_by_event(reply(call("a"), text("Found a."), call("b"))), done()])

    await settled(test.runner.until_done())

    assert first_reply(test.timeline) == [
        "server sends message_start",
        "server sends a: content_block_start",
        "server sends a: content_block_delta",
        "server sends a: content_block_stop",
        "server sends text: content_block_start",  # the model has moved on from a
        "server sends text: content_block_delta",
        "lookup(a) STARTS",
        "server sends text: content_block_stop",
        "server sends b: content_block_start",
        "server sends b: content_block_delta",
        "server sends b: content_block_stop",
        "server sends message_delta (tool_use)",  # the model has moved on from b
        "server sends message_stop",
        "lookup(b) STARTS",
    ]


async def test_runs_no_call_once_reading_the_reply_has_failed(setup: SetupFactory) -> None:
    test = setup([event_by_event(reply(call("a"), call("b")), fails_before="b: content_block_delta")])

    with pytest.raises(httpx2.ReadError):
        async for stream in replies_of(test.runner):
            async for event in events_of(stream):
                test.see(event)

    # The model had moved on from a, and the caller was done with the event that showed it.
    assert test.timeline[-3:] == [
        "server sends b: content_block_start",
        "b: content_block_start",
        "server fails",
    ]


async def test_runs_the_calls_one_at_a_time(setup: SetupFactory) -> None:
    test = setup([reply(call("a"), call("b")), done()], log_returns=True)

    await settled(test.runner.until_done())

    assert first_reply(test.timeline) == [
        "lookup(a) STARTS",
        "lookup(a) returns",
        "lookup(b) STARTS",
        "lookup(b) returns",
    ]


async def test_sends_the_error_result_of_a_call_that_failed_while_the_reply_streamed(setup: SetupFactory) -> None:
    def fail(key: str) -> str:
        raise ToolError(f"No value for {key}.")

    test = setup([reply(call("a"), text("Looking.")), done()], lookup=fail)

    async for stream in replies_of(test.runner):
        await settled(stream.get_final_message())
        test.timeline.append("loop body ends")

    assert first_reply(test.timeline) == ["lookup(a) STARTS", "loop body ends"]
    assert results_sent(test) == [
        {"type": "tool_result", "tool_use_id": "toolu_a", "content": "No value for a.", "is_error": True}
    ]


# ---------------------------------------------------------------------------------------------------------
# defer_tool_call()
# ---------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("argument", ["the block", "the id"])
async def test_defer_tool_call_takes(setup: SetupFactory, argument: str) -> None:
    test = setup([reply(call("a"), call("b")), done()])

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            if event.type == "content_block_stop" and event.content_block.type == "tool_use":
                if event.content_block.id == "toolu_a":
                    block = event.content_block
                    test.runner.defer_tool_call(block if argument == "the block" else block.id)
        test.timeline.append("loop body ends")

    assert first_reply(test.timeline) == ["lookup(b) STARTS", "loop body ends", "lookup(a) STARTS"]


@pytest.mark.parametrize(
    "at",
    ["a: content_block_start", "a: content_block_stop", "b: content_block_start"],
    ids=["when the call starts streaming", "when the call has streamed", "when the model moves on from the call"],
)
async def test_holds_a_call_that_is_deferred(setup: SetupFactory, at: str) -> None:
    test = setup([reply(call("a"), call("b")), done()])

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            if test.label(event) == at:
                test.runner.defer_tool_call("toolu_a")
        test.timeline.append("loop body ends")

    assert first_reply(test.timeline) == ["lookup(b) STARTS", "loop body ends", "lookup(a) STARTS"]


async def test_gives_the_timing_from_before_when_the_caller_defers_every_call(setup: SetupFactory) -> None:
    test = setup([reply(call("a"), call("b")), done()])

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            test.see(event)
            if event.type == "content_block_start" and event.content_block.type == "tool_use":
                test.runner.defer_tool_call(event.content_block)
        test.timeline.append("loop body ends")

    assert first_reply(test.timeline) == [
        "message_start",
        "a: content_block_start",
        "a: content_block_delta",
        "input_json",
        "a: content_block_stop",
        "b: content_block_start",
        "b: content_block_delta",
        "input_json",
        "b: content_block_stop",
        "message_delta (tool_use)",
        "message_stop",
        "loop body ends",
        "lookup(a) STARTS",
        "lookup(b) STARTS",
    ]


async def test_defer_tool_call_does_nothing_before_the_loop_starts_because_there_is_no_reply_yet(
    setup: SetupFactory,
) -> None:
    test = setup([reply(call("a")), done()])

    test.runner.defer_tool_call("toolu_a")
    assert test.runner.deferred_tool_calls == []

    async for stream in replies_of(test.runner):
        await settled(stream.get_final_message())
        test.timeline.append("loop body ends")

    assert first_reply(test.timeline) == ["lookup(a) STARTS", "loop body ends"]
    assert test.runner.deferred_tool_calls == []


async def test_defer_tool_call_changes_nothing_for_a_call_that_has_run(setup: SetupFactory) -> None:
    test = setup([reply(call("a"), call("b")), done()])

    held: list[list[str]] = []
    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            if test.label(event) == "b: content_block_delta":
                test.timeline.append("defer_tool_call(a)")
                test.runner.defer_tool_call("toolu_a")
                test.runner.defer_tool_call("toolu_b")
        held.append(ids(test.runner.deferred_tool_calls))
        test.timeline.append("loop body ends")

    assert first_reply(test.timeline) == [
        "lookup(a) STARTS",
        "defer_tool_call(a)",
        "loop body ends",
        "lookup(b) STARTS",
    ]
    assert held[0] == ["toolu_b"]
    assert [result["tool_use_id"] for result in results_sent(test)] == ["toolu_a", "toolu_b"]


async def test_defer_tool_call_lasts_for_one_reply(setup: SetupFactory) -> None:
    # The second reply reuses the id of the call that was held in the first.
    test = setup([reply(call("a")), reply(call("a")), done()])

    held: list[list[str]] = []
    async for stream in replies_of(test.runner):
        if not held:
            test.runner.defer_tool_call("toolu_a")
        await settled(stream.get_final_message())
        held.append(ids(test.runner.deferred_tool_calls))
        test.timeline.append("loop body ends")

    assert test.timeline == [
        "loop body ends",
        "lookup(a) STARTS",  # held in the first reply
        "request 2",
        "lookup(a) STARTS",  # not held in the second
        "loop body ends",
        "request 3",
        "loop body ends",
    ]
    assert held == [["toolu_a"], [], []]


async def test_lets_the_caller_refuse_a_held_call_by_removing_its_tool(setup: SetupFactory) -> None:
    test = setup([reply(call("a"), call("b")), done()])

    with pytest.warns(UserWarning, match="Tool 'lookup' not found in tool runner"):
        async for stream in replies_of(test.runner):
            async for event in events_of(stream):
                if test.label(event) == "b: content_block_start":
                    test.runner.defer_tool_call(event.content_block)
            test.runner.remove_tools("lookup")

    assert first_reply(test.timeline) == ["lookup(a) STARTS"]
    assert results_sent(test) == [
        {"type": "tool_result", "tool_use_id": "toolu_a", "content": "value of a"},
        not_found("toolu_b"),
    ]


async def test_runs_a_held_call_when_the_caller_asks_for_the_tool_response(setup: SetupFactory) -> None:
    test = setup([reply(call("a"), call("b"))])

    async for stream in replies_of(test.runner):
        test.runner.defer_tool_call("toolu_a")
        await settled(stream.get_final_message())
        test.timeline.append("generate_tool_call_response()")
        response = await settled(test.runner.generate_tool_call_response())

        assert [result["tool_use_id"] for result in tool_results(response)] == ["toolu_a", "toolu_b"]
        break

    assert test.timeline == ["lookup(b) STARTS", "generate_tool_call_response()", "lookup(a) STARTS"]


# ---------------------------------------------------------------------------------------------------------
# deferred_tool_calls
# ---------------------------------------------------------------------------------------------------------


async def test_deferred_tool_calls_lists_the_held_calls_in_the_models_order_with_their_whole_input(
    setup: SetupFactory,
) -> None:
    test = setup([reply(call("a"), call("b"), call("c"))])

    async for stream in replies_of(test.runner):
        # c is deferred by id before its block has streamed, and before b.
        test.runner.defer_tool_call("toolu_c")
        async for event in events_of(stream):
            if test.label(event) == "b: content_block_stop":
                test.runner.defer_tool_call("toolu_b")

        assert [tool_use.to_dict() for tool_use in test.runner.deferred_tool_calls] == [
            {"type": "tool_use", "id": "toolu_b", "name": "lookup", "input": {"key": "b"}},
            {"type": "tool_use", "id": "toolu_c", "name": "lookup", "input": {"key": "c"}},
        ]
        break


async def test_deferred_tool_calls_lists_a_held_call_from_when_its_block_has_finished_streaming(
    setup: SetupFactory,
) -> None:
    test = setup([reply(call("a"), call("b"))])
    held: list[str] = []

    async for stream in replies_of(test.runner):
        test.runner.defer_tool_call("toolu_a")
        test.runner.defer_tool_call("toolu_b")
        async for event in events_of(stream):
            held.append(f"{test.label(event)} -> {ids(test.runner.deferred_tool_calls)}")
        break

    assert held == [
        "message_start -> []",
        "a: content_block_start -> []",
        "a: content_block_delta -> []",
        "input_json -> []",
        "a: content_block_stop -> ['toolu_a']",
        "b: content_block_start -> ['toolu_a']",
        "b: content_block_delta -> ['toolu_a']",
        "input_json -> ['toolu_a']",
        "b: content_block_stop -> ['toolu_a', 'toolu_b']",
        "message_delta (tool_use) -> ['toolu_a', 'toolu_b']",
        "message_stop -> ['toolu_a', 'toolu_b']",
    ]


async def test_deferred_tool_calls_is_empty_once_generate_tool_call_response_has_run_the_held_calls(
    setup: SetupFactory,
) -> None:
    test = setup([reply(call("a"))])

    async for stream in replies_of(test.runner):
        test.runner.defer_tool_call("toolu_a")
        await settled(stream.get_final_message())
        assert ids(test.runner.deferred_tool_calls) == ["toolu_a"]

        await settled(test.runner.generate_tool_call_response())

        assert test.runner.deferred_tool_calls == []
        break


async def test_deferred_tool_calls_lists_the_held_calls_of_a_reply_that_is_cut_off(setup: SetupFactory) -> None:
    # The runner runs no tools for such a reply, but generate_tool_call_response() does.
    test = setup([reply_ending("max_tokens", call("a"), call("b"))])

    async for stream in replies_of(test.runner):
        test.runner.defer_tool_call("toolu_a")
        test.runner.defer_tool_call("toolu_b")
        await settled(stream.get_final_message())

        assert ids(test.runner.deferred_tool_calls) == ["toolu_a", "toolu_b"]
        assert test.timeline == []

        await settled(test.runner.generate_tool_call_response())
        break

    assert test.timeline == ["lookup(a) STARTS", "lookup(b) STARTS"]


# ---------------------------------------------------------------------------------------------------------
# a reply that is cut off
# ---------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "cut_off_reply",
    [
        pytest.param(lambda: reply_ending("refusal", call("a"), call("b", '{"key": "b"')), id="a refusal"),
        pytest.param(
            lambda: reply_ending("end_turn", call("a"), call("b", '{"key": "b"'), fallback(), text("Here it is.")),
            id="a refusal that hands the reply to a fallback model",
        ),
        pytest.param(
            # What arrived of the input is enough to call the tool with.
            lambda: reply_ending("max_tokens", call("a"), call("b", '{"key": "b", "note": "unfinis')),
            id="max_tokens",
        ),
    ],
)
async def test_never_runs_the_call_that_was_cut_off_by(setup: SetupFactory, cut_off_reply: Callable[[], Reply]) -> None:
    test = setup([cut_off_reply()])

    await settled(test.runner.until_done())

    assert test.timeline == ["lookup(a) STARTS"]
    assert len(test.requests) == 1


async def test_runs_the_calls_after_a_fallback_block_once_the_loop_body_ends_in_order(setup: SetupFactory) -> None:
    test = setup([reply(call("a"), call("b"), fallback(), call("c")), done()])

    async for stream in replies_of(test.runner):
        await settled(stream.get_final_message())
        test.timeline.append("loop body ends")

    # The fallback block started while b was still waiting for the model to move on.
    assert first_reply(test.timeline) == [
        "lookup(a) STARTS",
        "loop body ends",
        "lookup(b) STARTS",
        "lookup(c) STARTS",
    ]
    assert [result["tool_use_id"] for result in results_sent(test)] == ["toolu_a", "toolu_b", "toolu_c"]


async def test_runs_no_later_call_once_the_caller_leaves_the_loop(setup: SetupFactory) -> None:
    test = setup([reply(call("a"), call("b"))])

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            if test.label(event) == "b: content_block_delta":
                break
        break

    assert test.timeline == ["lookup(a) STARTS"]
    assert len(test.requests) == 1


# ---------------------------------------------------------------------------------------------------------
# a call that has run
# ---------------------------------------------------------------------------------------------------------


async def test_a_call_that_has_run_keeps_its_result_after_remove_tools_which_refuses_a_call_that_has_not(
    setup: SetupFactory,
) -> None:
    test = setup([reply(call("a"), call("b")), done()])

    with pytest.warns(UserWarning, match="Tool 'lookup' not found in tool runner"):
        async for stream in replies_of(test.runner):
            async for event in events_of(stream):
                if test.label(event) == "b: content_block_delta":
                    test.runner.remove_tools("lookup")

    assert first_reply(test.timeline) == ["lookup(a) STARTS"]
    assert results_sent(test) == [
        {"type": "tool_result", "tool_use_id": "toolu_a", "content": "value of a"},
        not_found("toolu_b"),
    ]


async def test_a_call_that_has_run_keeps_its_result_after_add_tools_replaces_its_tool(setup: SetupFactory) -> None:
    test = setup([reply(call("a"), call("b")), done()])
    replacement = lookup_tool(test.sync, [], lookup=lambda key: f"new value of {key}")

    async for stream in replies_of(test.runner):
        async for event in events_of(stream):
            if test.label(event) == "b: content_block_delta":
                test.runner.add_tools(replacement)

    assert results_sent(test) == [
        {"type": "tool_result", "tool_use_id": "toolu_a", "content": "value of a"},
        {"type": "tool_result", "tool_use_id": "toolu_b", "content": "new value of b"},
    ]


async def test_a_call_to_a_tool_removed_earlier_in_the_conversation_gets_a_not_found_result(
    setup: SetupFactory,
) -> None:
    test = setup(
        [reply(call("a"), text("Looking.")), done()],
        messages=[
            {"role": "user", "content": "Look this up."},
            {
                "role": "system",
                "content": [{"type": "tool_removal", "tool": {"type": "tool_reference", "name": "lookup"}}],
            },
        ],
    )

    with pytest.warns(UserWarning, match="Tool 'lookup' not found in tool runner"):
        await settled(test.runner.until_done())

    assert first_reply(test.timeline) == []
    assert results_sent(test) == [not_found("toolu_a")]


async def test_a_call_that_has_run_does_not_answer_a_later_reply_that_reuses_its_id(setup: SetupFactory) -> None:
    # The second reply's call comes after a fallback block, so it runs after the loop body.
    test = setup([reply(call("a")), reply(fallback(), call("a", json.dumps({"key": "again"}))), done()])

    await settled(test.runner.until_done())

    assert [result["content"] for result in tool_results(test.requests[2]["messages"][-1])] == ["value of again"]


# ---------------------------------------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------------------------------------

Block = dict[str, Any]
"""One content block of a canned reply."""

PARAMS: dict[str, Any] = {
    "model": "claude-haiku-4-5",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Look these up."}],
}


class Reply(NamedTuple):
    blocks: tuple[Block, ...]
    stop_reason: str


def call(key: str, json_input: str | None = None) -> Block:
    """The model calls `lookup(key=key)` with the id `toolu_<key>`. `json_input` is the input as sent, which may be
    cut off."""
    return {"type": "tool_use", "key": key, "json": json.dumps({"key": key}) if json_input is None else json_input}


def text(value: str) -> Block:
    return {"type": "text", "text": value}


def fallback() -> Block:
    """The block a refusal starts when it hands the reply to a fallback model."""
    return {
        "type": "fallback",
        "from": {"model": "claude-haiku-4-5"},
        "to": {"model": "claude-opus-4-8"},
        "trigger": {"type": "refusal", "category": None},
    }


def compaction() -> Block:
    """The block that a compaction request is answered with."""
    return {"type": "compaction", "content": "Summary so far.", "signature": "sig_01"}


def reply(*blocks: Block) -> Reply:
    """A reply that asks for tool results."""
    return Reply(blocks, "tool_use")


def reply_ending(stop_reason: str, *blocks: Block) -> Reply:
    """A reply that ends for another reason."""
    return Reply(blocks, stop_reason)


def done() -> Reply:
    """The reply that ends the conversation."""
    return reply_ending("end_turn", text("Done."))


def not_found(tool_use_id: str) -> dict[str, Any]:
    return {
        "type": "tool_result",
        "tool_use_id": tool_use_id,
        "content": "Error: Tool 'lookup' not found",
        "is_error": True,
    }


def ids(tool_uses: list[Any]) -> list[str]:
    return [tool_use.id for tool_use in tool_uses]


def first_reply(timeline: list[str]) -> list[str]:
    """The timeline up to the second request, which is everything about the first reply."""
    return timeline[: timeline.index("request 2")] if "request 2" in timeline else timeline


def tool_results(message: BetaMessageParam | None) -> list[Any]:
    if message is None or isinstance(message["content"], str):
        return []
    return [block for block in message["content"] if isinstance(block, dict) and block["type"] == "tool_result"]


def results_sent(test: Setup) -> list[Any]:
    """The tool results the runner sent back for the first reply."""
    return next(results for message in test.requests[1]["messages"] if (results := tool_results(message)))


def label_of(event: dict[str, Any], blocks: dict[int, str]) -> str:
    """Names a stream event, given as JSON, after the block it belongs to, such as `a: content_block_stop`."""
    if event["type"] == "content_block_start":
        block = event["content_block"]
        blocks[event["index"]] = block["id"].removeprefix("toolu_") if block["type"] == "tool_use" else block["type"]
    if event["type"] in ("content_block_start", "content_block_delta", "content_block_stop"):
        return f"{blocks[event['index']]}: {event['type']}"
    if event["type"] == "message_delta":
        return f"message_delta ({event['delta']['stop_reason']})"
    return str(event["type"])


def empty_message() -> dict[str, Any]:
    return {
        "id": "msg_1",
        "type": "message",
        "role": "assistant",
        "model": "claude-haiku-4-5",
        "content": [],
        "stop_reason": None,
        "stop_sequence": None,
        "usage": {"input_tokens": 10, "output_tokens": 0},
    }


def to_events(canned: Reply) -> list[dict[str, Any]]:
    """The reply as the stream events the API sends for it."""
    events: list[dict[str, Any]] = [{"type": "message_start", "message": empty_message()}]
    for index, block in enumerate(canned.blocks):
        start: dict[str, Any] = block
        delta: dict[str, Any] | None = None
        if block["type"] == "tool_use":
            start = {"type": "tool_use", "id": f"toolu_{block['key']}", "name": "lookup", "input": {}}
            delta = {"type": "input_json_delta", "partial_json": block["json"]}
        elif block["type"] == "text":
            start = {"type": "text", "text": ""}
            delta = {"type": "text_delta", "text": block["text"]}
        events.append({"type": "content_block_start", "index": index, "content_block": start})
        if delta is not None:
            events.append({"type": "content_block_delta", "index": index, "delta": delta})
        events.append({"type": "content_block_stop", "index": index})
    events.append(
        {
            "type": "message_delta",
            "delta": {"stop_reason": canned.stop_reason, "stop_sequence": None},
            "usage": {"output_tokens": 20},
        }
    )
    events.append({"type": "message_stop"})
    return events


def to_message(canned: Reply) -> dict[str, Any]:
    """The reply as the message the API sends for it when not streaming."""
    content = [
        {"type": "tool_use", "id": f"toolu_{block['key']}", "name": "lookup", "input": json.loads(block["json"])}
        if block["type"] == "tool_use"
        else block
        for block in canned.blocks
    ]
    return {**empty_message(), "content": content, "stop_reason": canned.stop_reason}


def sse(event: dict[str, Any]) -> bytes:
    return f"event: {event['type']}\ndata: {json.dumps(event)}\n\n".encode()


class EventByEvent(httpx2.SyncByteStream, httpx2.AsyncByteStream):
    """A reply that the server sends one event at a time, as a server still generating would. Each event goes on the
    timeline when it is sent."""

    def __init__(self, canned: Reply, fails_before: str | None) -> None:
        self.timeline: list[str] = []
        """Replaced by the test's timeline once the reply is handed to `setup()`."""

        self._events = to_events(canned)
        self._fails_before = fails_before

    def _send(self) -> Iterator[bytes]:
        blocks: dict[int, str] = {}
        for event in self._events:
            label = label_of(event, blocks)
            if label == self._fails_before:
                self.timeline.append("server fails")
                raise httpx2.ReadError("The connection was lost.")
            self.timeline.append(f"server sends {label}")
            yield sse(event)

    @override
    def __iter__(self) -> Iterator[bytes]:
        yield from self._send()

    @override
    async def __aiter__(self) -> AsyncIterator[bytes]:
        for chunk in self._send():
            yield chunk


def event_by_event(canned: Reply, *, fails_before: str | None = None) -> EventByEvent:
    return EventByEvent(canned, fails_before)


def lookup_tool(
    sync: bool, timeline: list[str], *, lookup: Callable[[str], str] | None = None, log_returns: bool = False
) -> Any:
    """A `lookup` tool that writes to `timeline` when it starts, and returns `value of <key>` unless `lookup` says
    otherwise."""

    def run(key: str) -> str:
        timeline.append(f"lookup({key}) STARTS")
        value = f"value of {key}" if lookup is None else lookup(key)
        if log_returns:
            timeline.append(f"lookup({key}) returns")
        return value

    if sync:

        @beta_tool(name="lookup")
        def sync_lookup(key: str) -> str:
            """Look up a key."""
            return run(key)

        return sync_lookup

    @beta_async_tool(name="lookup")
    async def async_lookup(key: str) -> str:
        """Look up a key."""
        return run(key)

    return async_lookup


class Setup:
    def __init__(self, *, sync: bool, runner: Any, timeline: list[str], requests: list[Any]) -> None:
        self.sync = sync
        self.runner = runner
        self.timeline = timeline
        self.requests = requests
        self._blocks: dict[int, str] = {}

    def label(self, event: Any) -> str:
        """Names a stream event after the block it belongs to, such as `a: content_block_stop`."""
        return label_of(event.to_dict(), self._blocks)

    def see(self, event: Any) -> None:
        """Adds a stream event to the timeline, as the caller saw it."""
        self.timeline.append(self.label(event))


class SetupFactory:
    """Makes a runner whose requests are answered by `replies`, in order, and whose `lookup` tool writes to the
    timeline when it starts. A `Reply` arrives in one piece."""

    def __init__(self, sync: bool, client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter) -> None:
        self._sync = sync
        self._client = client.with_options(max_retries=0) if sync else async_client.with_options(max_retries=0)
        self._respx_mock = respx_mock

    def __call__(
        self,
        replies: list[Reply | EventByEvent],
        *,
        stream: bool = True,
        run_tools_eagerly: bool = True,
        lookup: Callable[[str], str] | None = None,
        log_returns: bool = False,
        messages: list[Any] | None = None,
    ) -> Setup:
        timeline: list[str] = []
        requests: list[Any] = []
        responses = iter(replies)
        for canned in replies:
            if isinstance(canned, EventByEvent):
                canned.timeline = timeline

        def respond(request: httpx2.Request) -> httpx2.Response:
            requests.append(json.loads(request.content))
            if len(requests) > 1:
                timeline.append(f"request {len(requests)}")

            canned = next(responses)
            if not stream:
                assert isinstance(canned, Reply)
                return httpx2.Response(200, json=to_message(canned))
            headers = {"content-type": "text/event-stream"}
            if isinstance(canned, EventByEvent):
                return httpx2.Response(200, stream=canned, headers=headers)
            return httpx2.Response(200, content=b"".join(map(sse, to_events(canned))), headers=headers)

        self._respx_mock.post("/v1/messages").mock(side_effect=respond)

        tool_runner: Any = self._client.beta.messages.tool_runner
        runner = tool_runner(
            **{**PARAMS, "messages": messages or PARAMS["messages"]},
            tools=[lookup_tool(self._sync, timeline, lookup=lookup, log_returns=log_returns)],
            stream=stream,
            **({"run_tools_eagerly": True} if run_tools_eagerly and stream else {}),
        )
        return Setup(sync=self._sync, runner=runner, timeline=timeline, requests=requests)


@pytest.fixture(params=[True, False], ids=["sync", "async"])
def sync(request: pytest.FixtureRequest) -> bool:
    return bool(request.param)


@pytest.fixture
def setup(sync: bool, client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter) -> SetupFactory:
    return SetupFactory(sync, client, async_client, respx_mock)


async def replies_of(runner: Any) -> AsyncIterator[Any]:
    """What the runner yields, whether it is the sync or the async one."""
    if hasattr(runner, "__anext__"):
        async for item in runner:
            yield item
    else:
        for item in runner:
            yield item


async def events_of(stream: Any) -> AsyncIterator[Any]:
    """What the stream yields, whether it is the sync or the async one."""
    if hasattr(stream, "__anext__"):
        async for event in stream:
            yield event
    else:
        for event in stream:
            yield event


async def settled(value: _T | Awaitable[_T]) -> _T:
    """The result of a call on either runner: awaited on the async one."""
    if inspect.isawaitable(value):
        return await value
    return value
