from __future__ import annotations

import json
import asyncio
from typing import Any, Callable, cast
from contextlib import nullcontext

import httpx2
import pytest
import pydantic
from respx import MockRouter

from anthropic import APIError, AnthropicError, BadRequestError, InternalServerError
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools import beta_async_tool
from anthropic.types.beta import BetaToolParam, BetaMessageParam, BetaTextBlockParam
from anthropic.lib.threads import BetaAsyncMessageThread

from .helpers import (
    MODEL,
    CREATE,
    COMPACTED,
    FALLBACKS,
    LOOP_BODIES,
    RUNNER_MODES,
    THREADS_BETA,
    TURN_METHODS,
    FALLBACK_BETA,
    IN_PLACE_EDITS,
    THREAD_NOT_FOUND,
    WEATHER_QUESTION,
    INLINE_TOOLS_BETA,
    FALLBACK_ITERATIONS,
    ASYNC_RESPONSE_KINDS,
    ANSWERED_TURN_METHODS,
    OWN_CREATE_ONLY_FIELDS,
    CHANGES_DURING_THE_TURN,
    FAILURES_BEFORE_A_REPLY,
    ONE_TURN_CREATE_ONLY_FIELDS,
    NEW_SYSTEM_WITH_ANOTHER_HISTORY,
    CHANGES_OF_ANOTHER_FIELD_DURING_THE_TURN,
    Forecast,
    LoopBody,
    InPlaceEdit,
    user,
    roles,
    marked,
    base_url,
    tool_use,
    unmarked,
    assistant,
    id_headers,
    tool_result,
    async_lookup,
    marked_twice,
    response_ids,
    server_error,
    tool_removal,
    continue_from,
    request_betas,
    sent_requests,
    tool_addition,
    request_bodies,
    queue_responses,
    request_threads,
    message_response,
    async_get_weather,
    make_async_client,
    make_async_runner,
    make_async_thread,
    tool_change_turns,
    compaction_response,
    request_helper_tags,
    tool_change_replies,
    unsupported_response,
    async_stream_response,
    stream_error_response,
    assert_sends_conversation,
    history_with_nested_blocks,
    async_interrupted_stream_response,
)

pytestmark = pytest.mark.respx(base_url=base_url)


class TestAsyncMessageThread:
    async def test_send_creates_a_thread_then_continues_it(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_async_thread()

        await thread.send(user("Hello"))
        second = await thread.send(user("Again"))

        created, continued = request_bodies(respx_mock)
        assert isinstance(thread, BetaAsyncMessageThread)
        assert (created["thread"], created["messages"]) == (CREATE, [user("Hello")])
        assert (continued["thread"], continued["messages"]) == (continue_from("msg_a"), [user("Again")])
        assert request_betas(respx_mock) == [[THREADS_BETA], [THREADS_BETA]]
        assert thread.previous_message_id == second.id == "msg_b"

    @pytest.mark.parametrize(
        "method",
        [
            "send",
            pytest.param("parse", marks=pytest.mark.skipif(PYDANTIC_V1, reason="parse() is pydantic-v2 only")),
            "stream",
        ],
    )
    async def test_every_request_names_the_thread_in_the_helper_telemetry_header(
        self, respx_mock: MockRouter, method: str
    ) -> None:
        respond = async_stream_response if method == "stream" else message_response
        queue_responses(
            respx_mock,
            respond("msg_a"),
            THREAD_NOT_FOUND,
            respond("msg_c"),
            unsupported_response("inference_hooks"),
            respond("msg_e"),
        )
        thread = make_async_thread(
            extra_headers={"x-stainless-helper": "mine"}, unsupported_request_behavior="continue_unthreaded"
        )

        for text in ("One", "Two", "Three"):
            turn = getattr(thread, method)(user(text))
            if method == "stream":
                async with turn as stream:
                    await stream.until_done()
            else:
                await turn

        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a"), CREATE, continue_from("msg_c"), None]
        assert request_helper_tags(respx_mock) == [["mine, message-thread"]] * 5

    async def test_later_request_options_replace_the_threads_as_a_whole(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"), message_response("msg_c"))
        thread = make_async_thread(extra_headers={"X-Thread": "thread"}, extra_body={"top_k": 5})

        await thread.send(user("Hello"), extra_headers={"X-Turn": "turn"})
        await thread.send(user("Again"))
        thread.update(extra_headers={"X-Update": "update"})
        await thread.send(user("Once more"))

        names = ("X-Thread", "X-Turn", "X-Update")
        assert [tuple(r.headers.get(name) for name in names) for r in sent_requests(respx_mock)] == [
            (None, "turn", None),
            ("thread", None, None),
            (None, None, "update"),
        ]
        assert [body["top_k"] for body in request_bodies(respx_mock)] == [5, 5, 5]

    async def test_send_after_a_paused_reply_continues_from_it_with_no_messages(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock, message_response("msg_a", "Searching", stop_reason="pause_turn"), message_response("msg_b")
        )
        thread = make_async_thread()
        await thread.send(user("Hello"))

        resumed = await thread.send()

        body = request_bodies(respx_mock)[1]
        assert body["thread"] == continue_from("msg_a")
        assert body["messages"] == []
        assert thread.previous_message_id == resumed.id == "msg_b"

    async def test_rejected_previous_message_id_replays_the_full_history_under_a_new_thread(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"), THREAD_NOT_FOUND, message_response("msg_c"))
        thread = make_async_thread()
        await thread.send(user("Hello"))

        second = await thread.send(user("Again"))

        replayed = request_bodies(respx_mock)[2]
        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a"), CREATE]
        assert replayed["messages"] == [user("Hello"), assistant(), user("Again")]
        assert thread.previous_message_id == second.id == "msg_c"

    async def test_fork_and_original_continue_independently(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"), message_response("msg_c"))
        thread = make_async_thread()
        await thread.send(user("Hello"))

        fork = thread.fork()
        await fork.send(user("Fork"))
        await thread.send(user("Original"))

        forked, continued = request_bodies(respx_mock)[1:]
        assert isinstance(fork, BetaAsyncMessageThread)
        assert (forked["thread"], forked["messages"]) == (CREATE, [user("Hello"), assistant(), user("Fork")])
        assert (continued["thread"], continued["messages"]) == (continue_from("msg_a"), [user("Original")])
        assert (thread.previous_message_id, fork.previous_message_id) == ("msg_c", "msg_b")

    @pytest.mark.parametrize(
        "method",
        [
            "send",
            pytest.param("parse", marks=pytest.mark.skipif(PYDANTIC_V1, reason="parse() is pydantic-v2 only")),
            "stream",
        ],
    )
    @pytest.mark.parametrize("forks", [1, 2], ids=["fork", "fork_of_a_fork"])
    async def test_fork_of_a_thread_that_ends_in_a_partial_reply_sends_the_turn_again_without_it(
        self, respx_mock: MockRouter, forks: int, method: str
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            async_stream_response("msg_b", "one two three"),
            async_stream_response("msg_c") if method == "stream" else message_response("msg_c"),
            message_response("msg_d"),
        )
        thread = make_async_thread()
        await thread.send(user("Hello"))
        async with thread.stream(user("Count")) as stream:
            await anext(stream.text_stream)
        messages_after_the_stream = thread.messages

        fork = thread
        for _ in range(forks):
            fork = fork.fork()
        messages_of_the_fork = fork.messages
        await run_turn(fork, method)
        messages_after_the_turn_of_the_fork = thread.messages
        await thread.send()

        forked, original = request_bodies(respx_mock)[2:]
        assert (forked["thread"], forked["messages"]) == (CREATE, [user("Hello"), assistant("Hi!"), user("Count")])
        assert (original["thread"], original["messages"]) == (forked["thread"], forked["messages"])
        assert messages_of_the_fork == messages_after_the_turn_of_the_fork == messages_after_the_stream
        assert (roles(fork.messages), fork.previous_message_id) == (["user", "assistant", "user", "assistant"], "msg_c")

    async def test_fork_of_a_thread_that_ends_in_a_partial_reply_sends_it_ahead_of_a_new_message(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(respx_mock, async_stream_response("msg_a", "one two three"), message_response("msg_b"))
        thread = make_async_thread()
        async with thread.stream(user("Count")) as stream:
            await anext(stream.text_stream)

        await thread.fork().send(user("Just the total"))

        body = request_bodies(respx_mock)[1]
        assert (body["thread"], body["messages"]) == (CREATE, [user("Count"), assistant("one"), user("Just the total")])

    async def test_fork_of_a_thread_that_ends_in_a_whole_reply_sends_the_full_history_with_no_new_message(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_async_thread()
        await thread.send(user("Hello"))

        await thread.fork().send()

        body = request_bodies(respx_mock)[1]
        assert (body["thread"], body["messages"]) == (CREATE, [user("Hello"), assistant()])

    async def test_unsupported_request_raises_by_default_and_keeps_previous_message_id(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"), unsupported_response("inference_hooks"))
        thread = make_async_thread()
        await thread.send(user("Hello"))

        with pytest.raises(BadRequestError):
            await thread.send(user("Again"))

        assert thread.previous_message_id == "msg_a"
        assert roles(thread.messages) == ["user", "assistant"]

    async def test_continue_unthreaded_stops_threading_for_good_after_an_unsupported_request(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            unsupported_response("inference_hooks"),
            message_response("msg_c"),
            message_response("msg_d"),
        )
        thread = make_async_thread(unsupported_request_behavior="continue_unthreaded")
        await thread.send(user("Hello"))

        await thread.send(user("Again"))
        await thread.send(user("Once more"))

        later = request_bodies(respx_mock)[3]
        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a"), None, None]
        assert request_betas(respx_mock)[2:] == [[], []]
        assert roles(later["messages"]) == ["user", "assistant", "user", "assistant", "user"]
        assert thread.previous_message_id is None

    @ANSWERED_TURN_METHODS
    async def test_continue_unthreaded_stops_threading_when_the_thread_is_lost_again_right_after_a_replay(
        self, respx_mock: MockRouter, method: str
    ) -> None:
        respond = async_stream_response if method == "stream" else message_response
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            THREAD_NOT_FOUND,
            message_response("msg_c"),
            THREAD_NOT_FOUND,
            respond("msg_e", "Hi!"),
            message_response("msg_f"),
        )
        thread = make_async_thread(unsupported_request_behavior="continue_unthreaded")
        await thread.send(user("One"))
        await thread.send(user("Two"))

        await run_turn(thread, method, user("Three"))
        await thread.send(user("Four"))

        unthreaded, later = request_bodies(respx_mock)[4:]
        history = [user("One"), assistant(), user("Two"), assistant(), user("Three")]
        assert request_threads(respx_mock) == [
            CREATE,
            continue_from("msg_a"),
            CREATE,
            continue_from("msg_c"),
            None,
            None,
        ]
        assert unthreaded["messages"] == history
        assert later["messages"] == [*history, assistant(), user("Four")]

    async def test_a_thread_lost_again_right_after_a_replay_is_replayed_again_by_default(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            THREAD_NOT_FOUND,
            message_response("msg_c"),
            THREAD_NOT_FOUND,
            message_response("msg_e"),
        )
        thread = make_async_thread()

        for text in ("One", "Two", "Three"):
            await thread.send(user(text))

        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a"), CREATE, continue_from("msg_c"), CREATE]

    async def test_a_thread_built_from_params_keeps_the_unsupported_request_behavior(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            unsupported_response("inference_hooks"),
            message_response("msg_b"),
            unsupported_response("inference_hooks"),
        )
        client = make_async_client()
        unthreaded = make_async_thread(unsupported_request_behavior="continue_unthreaded")

        await client.beta.messages.thread(**unthreaded.params).send(user("Hello"))
        with pytest.raises(BadRequestError):
            await client.beta.messages.thread(**make_async_thread().params).send(user("Hello"))

        assert request_threads(respx_mock) == [CREATE, None, CREATE]
        assert not any("unsupported_request_behavior" in body for body in request_bodies(respx_mock))

    async def test_send_while_another_send_is_in_flight_raises_and_stages_nothing(self, respx_mock: MockRouter) -> None:
        async def respond_slowly(_request: httpx2.Request) -> httpx2.Response:
            await asyncio.sleep(0.05)
            return message_response("msg_a")

        respx_mock.post("/v1/messages").mock(side_effect=respond_slowly)
        thread = make_async_thread()

        in_flight = asyncio.ensure_future(thread.send(user("One")))
        await asyncio.sleep(0)
        with pytest.raises(AnthropicError, match="already in progress"):
            await thread.send(user("Two"))
        await in_flight
        await thread.send(user("Two"))

        assert request_bodies(respx_mock)[1]["messages"] == [user("Two")]
        assert roles(thread.messages) == ["user", "assistant", "user", "assistant"]
        assert (thread.messages[0], thread.messages[2]) == (user("One"), user("Two"))

    async def test_failed_send_lets_the_next_send_run(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, server_error(), message_response("msg_b"))
        thread = make_async_thread()
        with pytest.raises(InternalServerError):
            await thread.send(user("Hello"))

        reply = await thread.send(user("Hello"))

        assert reply.id == "msg_b"

    @TURN_METHODS
    @FAILURES_BEFORE_A_REPLY
    async def test_unrelated_errors_raise_and_the_same_call_again_sends_the_turn_once(
        self, respx_mock: MockRouter, method: str, failure: httpx2.Response | Exception
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"), failure, message_response("msg_c"))
        thread = make_async_thread()
        await thread.send(user("Hello"))
        messages_before = thread.messages

        with pytest.raises(APIError):
            await run_turn(thread, method, user("Again"))
        after_the_error = (thread.messages, thread.previous_message_id)
        await thread.send(user("Again"))

        retried = request_bodies(respx_mock)[2]
        assert (retried["thread"], retried["messages"]) == (continue_from("msg_a"), [user("Again")])
        assert after_the_error == (messages_before, "msg_a")

    async def test_a_cancelled_send_takes_the_turn_back(self, respx_mock: MockRouter) -> None:
        sent = asyncio.Event()

        async def never_respond(_request: httpx2.Request) -> httpx2.Response:
            sent.set()
            await asyncio.sleep(30)
            raise AssertionError("not cancelled")

        queue_responses(respx_mock, message_response("msg_a"))
        thread = make_async_thread()
        await thread.send(user("Hello"))

        respx_mock.post("/v1/messages").mock(side_effect=never_respond)
        in_flight = asyncio.ensure_future(thread.send(user("A long story")))
        await sent.wait()
        in_flight.cancel()
        with pytest.raises(asyncio.CancelledError):
            await in_flight
        queue_responses(respx_mock, message_response("msg_c"))
        await thread.send(user("One word"))

        later = request_bodies(respx_mock)[-1]
        assert (later["thread"], later["messages"]) == (continue_from("msg_a"), [user("One word")])

    async def test_messages_appended_before_a_call_that_fails_stay_staged(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock, message_response("msg_a"), server_error(), server_error(), message_response("msg_d")
        )
        thread = make_async_thread()
        await thread.send(user("Hello"))

        thread.append(user("Appended"))
        with pytest.raises(InternalServerError):
            await thread.send(user("Again"))
        with pytest.raises(InternalServerError):
            await thread.send()
        await thread.send()

        assert [body["messages"] for body in request_bodies(respx_mock)[1:]] == [
            [user("Appended"), user("Again")],
            [user("Appended")],
            [user("Appended")],
        ]

    @ANSWERED_TURN_METHODS
    async def test_a_refused_turn_is_not_recorded_and_the_next_turn_starts_a_new_thread(
        self, respx_mock: MockRouter, method: str
    ) -> None:
        respond = async_stream_response if method == "stream" else message_response
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            respond("msg_b", "I can't help with that.", stop_reason="refusal"),
            message_response("msg_c"),
            message_response("msg_d"),
        )
        thread = make_async_thread(system="You are terse.")
        await thread.send(user("Hello"))
        messages_before = thread.messages

        thread.append(user("Appended"))
        await run_turn(thread, method, user("Refused"))
        after_the_refusal = (thread.messages, thread.previous_message_id)
        await thread.send(user("Rephrased"))
        await thread.send(user("Again"))

        refused, created, continued = request_bodies(respx_mock)[1:]
        assert (refused["thread"], refused["messages"]) == (continue_from("msg_a"), [user("Appended"), user("Refused")])
        assert after_the_refusal == ((*messages_before, user("Appended")), None)
        assert (created["thread"], created["system"]) == (CREATE, "You are terse.")
        assert created["messages"] == [user("Hello"), assistant(), user("Appended"), user("Rephrased")]
        assert (continued["thread"], continued["messages"]) == (continue_from("msg_c"), [user("Again")])

    async def test_a_stream_left_once_it_has_shown_the_refusal_is_not_recorded(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            async_stream_response("msg_b", "I can't help with that.", stop_reason="refusal"),
            message_response("msg_c"),
        )
        thread = make_async_thread(system="You are terse.")
        await thread.send(user("Hello"))
        messages_before = thread.messages

        thread.append(user("Appended"))
        async with thread.stream(user("Refused")) as stream:
            async for event in stream:
                if event.type == "message_delta":
                    break
        after_the_refusal = (thread.messages, thread.previous_message_id)
        await thread.send(user("Rephrased"))

        created = request_bodies(respx_mock)[2]
        assert after_the_refusal == ((*messages_before, user("Appended")), None)
        assert (created["thread"], created["system"]) == (CREATE, "You are terse.")
        assert created["messages"] == [user("Hello"), assistant(), user("Appended"), user("Rephrased")]

    async def test_a_refused_first_turn_keeps_the_seed_and_nothing_the_turn_was_given(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a", stop_reason="refusal"), message_response("msg_b"))
        thread = make_async_thread(messages=[user("Seed"), assistant("Seeded")])

        refused = await thread.send(user("Refused"), system="Be brief.")
        await thread.send(user("Rephrased"))

        created = request_bodies(respx_mock)[1]
        assert (refused.id, refused.stop_reason) == ("msg_a", "refusal")
        assert created["thread"] == CREATE
        assert created["messages"] == [user("Seed"), assistant("Seeded"), user("Rephrased")]
        assert "system" not in created

    @ANSWERED_TURN_METHODS
    async def test_a_replay_drops_the_cache_markers_of_the_recorded_messages(
        self, respx_mock: MockRouter, method: str
    ) -> None:
        respond = async_stream_response if method == "stream" else message_response
        queue_responses(respx_mock, message_response("msg_a"), THREAD_NOT_FOUND, respond("msg_c"))
        given = [marked("Hello"), marked("Again")]
        thread = make_async_thread()
        await thread.send(given[0])

        await run_turn(thread, method, given[1])

        replayed = request_bodies(respx_mock)[2]
        assert (replayed["thread"], replayed["messages"]) == (CREATE, [unmarked("Hello"), assistant(), marked("Again")])
        assert given == [marked("Hello"), marked("Again")]
        assert [message for message in thread.messages if message["role"] == "user"] == given

    async def test_a_replay_drops_nested_cache_markers_and_leaves_free_form_data_alone(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"), THREAD_NOT_FOUND, message_response("msg_c"))
        marker = {"cache_control": {"type": "ephemeral"}}
        given = history_with_nested_blocks(marker)
        thread = make_async_thread(messages=given, betas=[INLINE_TOOLS_BETA])
        await thread.send()

        await thread.send(user("Again"))

        created, _, replayed = request_bodies(respx_mock)
        assert created["messages"] == history_with_nested_blocks(marker)
        assert replayed["messages"] == [*history_with_nested_blocks({}), assistant(), user("Again")]
        assert given == history_with_nested_blocks(marker)
        assert list(thread.messages[: len(given)]) == given

    @pytest.mark.parametrize("new_messages", [[], [marked("Once more")]], ids=["sent_again", "with_a_new_message"])
    async def test_a_turn_that_no_reply_answered_keeps_its_cache_markers(
        self, respx_mock: MockRouter, new_messages: list[BetaMessageParam]
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            async_interrupted_stream_response("msg_b", ""),
            message_response("msg_c"),
        )
        thread = make_async_thread()
        await thread.send(marked("Hello"))
        async with thread.stream(marked_twice("Again")) as stream:
            await stream.until_done()

        await thread.send(*new_messages)

        created = request_bodies(respx_mock)[2]
        assert created["thread"] == CREATE
        assert created["messages"] == [unmarked("Hello"), assistant(), marked_twice("Again"), *new_messages]

    @ANSWERED_TURN_METHODS
    async def test_a_reply_from_a_fallback_model_only_starts_a_new_thread(
        self, respx_mock: MockRouter, method: str
    ) -> None:
        respond = async_stream_response if method == "stream" else message_response
        queue_responses(
            respx_mock,
            respond("msg_a", "Hi!", iterations=FALLBACK_ITERATIONS),
            message_response("msg_b"),
            message_response("msg_c"),
        )
        thread = make_async_thread(fallbacks=FALLBACKS, betas=[FALLBACK_BETA])

        await run_turn(thread, method, user("Hello"))
        params_after_the_reply = thread.params
        await thread.send(user("Again"))
        await thread.send(user("Once more"))

        bodies = request_bodies(respx_mock)
        assert (params_after_the_reply["model"], params_after_the_reply.get("fallbacks")) == (MODEL, FALLBACKS)
        assert [(body["model"], body["fallbacks"]) for body in bodies] == [(MODEL, FALLBACKS)] * 3
        assert [body["thread"] for body in bodies] == [CREATE, CREATE, continue_from("msg_b")]
        assert bodies[1]["messages"] == [user("Hello"), assistant(), user("Again")]
        assert request_betas(respx_mock) == [[FALLBACK_BETA, THREADS_BETA]] * 3

    @TURN_METHODS
    async def test_a_one_turn_system_override_is_refused_and_takes_the_turn_back(
        self, respx_mock: MockRouter, method: str
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_async_thread(system="Be brief.")
        await thread.send(user("Hello"))

        with pytest.raises(AnthropicError, match="Cannot change `system`"):
            await run_turn(thread, method, user("Again"), system="Be verbose.")
        await thread.send(user("Again"))

        continued = request_bodies(respx_mock)[1]
        assert (continued["thread"], continued["messages"]) == (continue_from("msg_a"), [user("Again")])

    @ONE_TURN_CREATE_ONLY_FIELDS
    @pytest.mark.parametrize(
        "method",
        [
            "send",
            pytest.param("parse", marks=pytest.mark.skipif(PYDANTIC_V1, reason="parse() is pydantic-v2 only")),
            "stream",
        ],
    )
    async def test_a_one_turn_system_or_tools_on_the_turn_that_creates_the_thread_stays_with_the_thread(
        self, respx_mock: MockRouter, method: str, override: dict[str, Any]
    ) -> None:
        respond = async_stream_response if method == "stream" else message_response
        queue_responses(respx_mock, respond("msg_a"), message_response("msg_b"))
        thread = make_async_thread()

        await run_turn(thread, method, user("Hello"), **override)
        await thread.send(user("Again"))

        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a")]
        assert {**thread.params, **override} == thread.params

    @ONE_TURN_CREATE_ONLY_FIELDS
    @TURN_METHODS
    async def test_a_one_turn_system_or_tools_on_a_first_turn_that_fails_does_not_stay_with_the_thread(
        self, respx_mock: MockRouter, method: str, override: dict[str, Any]
    ) -> None:
        queue_responses(respx_mock, server_error(), message_response("msg_b"))
        thread = make_async_thread(system="Be kind.")
        params_before = thread.params

        with pytest.raises(InternalServerError):
            await run_turn(thread, method, user("Hello"), **override)
        params_after_the_error = thread.params
        await thread.send(user("Hello"))

        failed, later = request_bodies(respx_mock)
        assert {**failed, **override} == failed
        assert (later["thread"], later["messages"]) == (CREATE, [user("Hello")])
        assert (later["system"], later.get("tools")) == ("Be kind.", None)
        assert params_after_the_error == params_before

    @ONE_TURN_CREATE_ONLY_FIELDS
    @pytest.mark.parametrize("next_turn", [[], [user("Just the total")]], ids=["same_turn_again", "another_message"])
    async def test_a_one_turn_system_or_tools_on_a_first_turn_whose_stream_ends_early_does_not_stay_with_the_thread(
        self, respx_mock: MockRouter, next_turn: list[BetaMessageParam], override: dict[str, Any]
    ) -> None:
        queue_responses(respx_mock, async_stream_response("msg_a", "one two three"), message_response("msg_b"))
        thread = make_async_thread(system="Be kind.")

        async with thread.stream(user("Count"), **override) as stream:
            await anext(stream.text_stream)
        await thread.send(*next_turn)

        later = request_bodies(respx_mock)[1]
        assert (later["thread"], later["system"], later.get("tools")) == (CREATE, "Be kind.", None)

    @CHANGES_DURING_THE_TURN
    async def test_a_change_during_the_turn_that_creates_the_thread_of_what_that_turn_gave_is_refused_on_the_next_turn(
        self, respx_mock: MockRouter, override: dict[str, Any], change: Callable[[BetaAsyncMessageThread[Any]], None]
    ) -> None:
        queue_responses(respx_mock, async_stream_response("msg_a"))
        thread = make_async_thread()

        async with thread.stream(user("Hello"), **override) as stream:
            change(thread)
            await stream.until_done()
        with pytest.raises(AnthropicError, match=f"Cannot change `{next(iter(override))}`"):
            await thread.send(user("Again"))

        assert (respx_mock.calls.call_count, thread.previous_message_id) == (1, "msg_a")

    @OWN_CREATE_ONLY_FIELDS
    @ONE_TURN_CREATE_ONLY_FIELDS
    @CHANGES_OF_ANOTHER_FIELD_DURING_THE_TURN
    async def test_a_change_of_another_field_during_the_turn_that_creates_the_thread_keeps_what_that_turn_gave(
        self,
        respx_mock: MockRouter,
        change: Callable[[BetaAsyncMessageThread[Any]], None],
        override: dict[str, Any],
        own: dict[str, Any],
    ) -> None:
        queue_responses(respx_mock, async_stream_response("msg_a"), message_response("msg_b"))
        thread = make_async_thread(**own)

        async with thread.stream(user("Hello"), **override) as stream:
            change(thread)
            await stream.until_done()
        await thread.send(user("Again"))

        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a")]
        assert request_bodies(respx_mock)[1]["max_tokens"] == 12
        assert {**thread.params, **override} == thread.params

    async def test_a_one_turn_system_on_a_first_turn_that_goes_without_a_thread_is_for_that_turn_only(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock, unsupported_response("inference_hooks"), message_response("msg_b"), message_response("msg_c")
        )
        thread = make_async_thread(unsupported_request_behavior="continue_unthreaded")

        await thread.send(user("Hello"), system="Be brief.")
        await thread.send(user("Again"))

        assert request_threads(respx_mock) == [CREATE, None, None]
        assert [body.get("system") for body in request_bodies(respx_mock)] == ["Be brief.", "Be brief.", None]

    @pytest.mark.skipif(PYDANTIC_V1, reason="structured outputs not supported with pydantic v1")
    async def test_parse_continues_the_thread_and_parses_each_reply(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", json.dumps({"forecast": "Sunny"})),
            message_response("msg_b", json.dumps({"forecast": "Rain"})),
        )
        thread = make_async_thread(output_format=Forecast)

        first = await thread.parse(user("Today?"))
        second = await thread.parse(user("Tomorrow?"), max_tokens=12)

        created, continued = request_bodies(respx_mock)
        assert (first.parsed_output, second.parsed_output) == (Forecast(forecast="Sunny"), Forecast(forecast="Rain"))
        assert created["thread"] == CREATE
        assert created["output_config"]["format"]["type"] == "json_schema"
        assert (continued["thread"], continued["messages"], continued["max_tokens"]) == (
            continue_from("msg_a"),
            [user("Tomorrow?")],
            12,
        )
        assert thread.previous_message_id == second.id

    @pytest.mark.skipif(PYDANTIC_V1, reason="parse() response post-parser is pydantic-v2 only")
    async def test_parsed_reply_has_the_request_and_workspace_ids_of_its_response(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", headers=id_headers("req_a", "wrkspc_a")),
            message_response("msg_b", headers=id_headers("req_b", "wrkspc_b")),
            message_response("msg_c"),
        )
        thread = make_async_thread()

        sent = await thread.send(user("One"))
        parsed = await thread.parse(user("Two"))
        parsed_without_ids = await thread.parse(user("Three"))

        assert response_ids(sent, parsed, parsed_without_ids) == [
            ("req_a", "wrkspc_a"),
            ("req_b", "wrkspc_b"),
            (None, None),
        ]
        assert not parsed.to_dict().keys() & {"_request_id", "_workspace_id"}

    @pytest.mark.skipif(PYDANTIC_V1, reason="structured outputs not supported with pydantic v1")
    async def test_parse_of_a_reply_that_does_not_fit_the_output_format_keeps_the_turn(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a", "Sunny"))
        thread = make_async_thread(output_format=Forecast)

        with pytest.raises(pydantic.ValidationError):
            await thread.parse(user("Today?"))

        assert (roles(thread.messages), thread.previous_message_id) == (["user", "assistant"], "msg_a")

    async def test_stream_records_the_reply_once_it_reaches_message_stop(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, async_stream_response("msg_a"))
        thread = make_async_thread()

        async with thread.stream(user("Hello")) as stream:
            await stream.until_done()
        final = await stream.get_final_message()

        assert final.id == thread.previous_message_id == "msg_a"
        assert roles(thread.messages) == ["user", "assistant"]

    @pytest.mark.parametrize("how", ["break", "close"])
    async def test_a_stream_that_ends_early_records_the_partial_reply_and_starts_a_new_thread(
        self, respx_mock: MockRouter, how: str
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            async_stream_response("msg_b", "one two three"),
            message_response("msg_c"),
        )
        thread = make_async_thread()
        await thread.send(user("Hello"))

        async with thread.stream(user("Count")) as stream:
            await anext(stream.text_stream)
            if how == "close":
                await stream.close()
        previous_message_id_after_stream = thread.previous_message_id
        await thread.send(user("Just the total"))

        later = request_bodies(respx_mock)[2]
        assert previous_message_id_after_stream is None
        assert roles(thread.messages) == ["user", "assistant", "user", "assistant", "user", "assistant"]
        assert thread.messages[3]["content"][0].text == "one"  # type: ignore
        assert (later["thread"], roles(later["messages"])) == (
            CREATE,
            ["user", "assistant", "user", "assistant", "user"],
        )

    @pytest.mark.parametrize("error", [httpx2.ReadError, None], ids=["events_fail", "events_run_out"])
    async def test_a_stream_whose_events_fail_or_run_out_early_frees_the_thread_at_once(
        self, respx_mock: MockRouter, error: type[httpx2.TransportError] | None
    ) -> None:
        queue_responses(
            respx_mock,
            async_interrupted_stream_response("msg_a", "one", error=error),
            message_response("msg_b"),
        )
        thread = make_async_thread()

        async with thread.stream(user("Count")) as stream:
            with pytest.raises(error) if error else nullcontext():
                await stream.until_done()
            await thread.send(user("Just the total"))

        later = request_bodies(respx_mock)[1]
        assert (later["thread"], later["messages"]) == (
            CREATE,
            [user("Count"), assistant("one"), user("Just the total")],
        )
        assert roles(thread.messages) == ["user", "assistant", "user", "assistant"]
        assert thread.previous_message_id == "msg_b"

    async def test_a_stream_read_to_message_stop_frees_the_thread_at_once(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, async_stream_response("msg_a"), message_response("msg_b"))
        thread = make_async_thread()

        async with thread.stream(user("Hello")) as stream:
            await stream.until_done()
            previous_message_id_inside_the_block = thread.previous_message_id
            await thread.send(user("Again"))

        assert previous_message_id_inside_the_block == "msg_a"
        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a")]
        assert request_bodies(respx_mock)[1]["messages"] == [user("Again")]
        assert thread.previous_message_id == "msg_b"

    @pytest.mark.parametrize("how", ["leave", "close", "error_event"])
    async def test_a_stream_that_ends_before_message_start_takes_the_turn_back(
        self, respx_mock: MockRouter, how: str
    ) -> None:
        streamed = stream_error_response() if how == "error_event" else async_stream_response("msg_b")
        queue_responses(respx_mock, message_response("msg_a"), streamed, message_response("msg_c"))
        thread = make_async_thread()
        await thread.send(user("Hello"))

        with pytest.raises(APIError) if how == "error_event" else nullcontext():
            async with thread.stream(user("Count")) as stream:
                if how == "close":
                    await stream.close()
                elif how == "error_event":
                    await stream.until_done()
        await thread.send(user("Count"))

        retried = request_bodies(respx_mock)[2]
        assert (retried["thread"], retried["messages"]) == (continue_from("msg_a"), [user("Count")])

    async def test_send_with_no_messages_still_sends_a_partial_turn_again_after_a_call_that_failed(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            async_stream_response("msg_b", "one two three"),
            server_error(),
            message_response("msg_d"),
        )
        thread = make_async_thread()
        await thread.send(user("Hello"))
        async with thread.stream(user("Count")) as stream:
            await anext(stream.text_stream)
        messages_after_the_stream = thread.messages

        with pytest.raises(InternalServerError):
            await thread.send(user("Just the total"))
        messages_after_the_error = thread.messages
        await thread.send()

        retried = request_bodies(respx_mock)[3]
        assert (retried["thread"], retried["messages"]) == (CREATE, [user("Hello"), assistant("Hi!"), user("Count")])
        assert messages_after_the_error == messages_after_the_stream

    async def test_a_tool_removal_appended_by_hand_is_sent_on_the_continue_as_given(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        noop: BetaToolParam = {"name": "noop", "input_schema": {"type": "object", "properties": {}}}
        thread = make_async_thread(tools=[noop], betas=[INLINE_TOOLS_BETA])
        await thread.send(user("Hello"))

        thread.append(tool_removal("noop"))
        await thread.send(user("Again"))

        continued = request_bodies(respx_mock)[1]
        assert (continued["thread"], continued.get("tools")) == (continue_from("msg_a"), None)
        assert continued["messages"] == [tool_removal("noop"), user("Again")]

    @IN_PLACE_EDITS
    async def test_system_or_a_tool_edited_in_place_is_refused_and_a_thread_from_the_params_takes_the_edit(
        self, respx_mock: MockRouter, field: str, edit: InPlaceEdit
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        system: list[BetaTextBlockParam] = [{"type": "text", "text": "Be brief."}]
        tool: BetaToolParam = {"name": "noop", "input_schema": {"type": "object", "properties": {}}}
        thread = make_async_thread(system=system, tools=[tool])
        await thread.send(user("Hello"))

        edit(system, tool)
        with pytest.raises(AnthropicError, match=f"Cannot change `{field}` on a thread"):
            await thread.send(user("Again"))
        assert respx_mock.calls.call_count == 1
        await make_async_client().beta.messages.thread(**thread.params).send(user("Again"))

        recreated = request_bodies(respx_mock)[1]
        assert (recreated["thread"], roles(recreated["messages"])) == (CREATE, ["user", "assistant", "user"])
        assert (recreated["system"], recreated["tools"]) == (system, [tool])

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    async def test_runner_given_no_betas_sends_the_threads_beta_and_no_other(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"))
        runner = make_async_runner()

        await runner.until_done()

        assert request_betas(respx_mock) == [[THREADS_BETA]]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    async def test_runner_threads_by_default(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock, message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b", "Sunny.")
        )
        runner = make_async_runner()

        final = await runner.until_done()

        continued = request_bodies(respx_mock)[1]
        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a")]
        assert continued["messages"] == [tool_result("toolu_a")]
        assert request_helper_tags(respx_mock) == [["BetaToolRunner, message-thread"]] * 2
        assert final.id == "msg_b"

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    async def test_runner_adds_and_removes_tools_on_the_thread(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, *tool_change_replies())
        added = beta_async_tool(async_lookup, name="lookup")
        runner = make_async_runner(betas=[INLINE_TOOLS_BETA])

        await anext(runner)
        runner.add_tools(added)
        await anext(runner)
        runner.remove_tools("get_weather")
        with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
            final = await runner.until_done()

        after_msg_a, after_msg_b, after_msg_c = tool_change_turns(added.to_dict())
        assert final.id == "msg_d"
        assert [(body["thread"], body["messages"], body.get("tools")) for body in request_bodies(respx_mock)] == [
            (CREATE, [WEATHER_QUESTION], [beta_async_tool(async_get_weather, name="get_weather").to_dict()]),
            (continue_from("msg_a"), after_msg_a, None),
            (continue_from("msg_b"), after_msg_b, None),
            (continue_from("msg_c"), after_msg_c, None),
        ]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    async def test_runner_with_thread_false_sends_no_thread(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"))

        await make_async_runner(thread=False).until_done()

        assert (request_threads(respx_mock), request_betas(respx_mock)) == ([None], [[]])
        assert request_helper_tags(respx_mock) == [["BetaToolRunner"]]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    @pytest.mark.parametrize("thread", [None, False], ids=["threaded", "thread_false"])
    async def test_runner_replies_have_the_request_and_workspace_ids_of_their_responses(
        self, respx_mock: MockRouter, thread: bool | None
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a", headers=id_headers("req_a", "wrkspc_a")),
            message_response("msg_b", "Sunny.", headers=id_headers("req_b", "wrkspc_b")),
        )

        replies = [reply async for reply in make_async_runner(thread=thread)]

        assert response_ids(*replies) == [("req_a", "wrkspc_a"), ("req_b", "wrkspc_b")]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    @pytest.mark.parametrize("thread", [CREATE, continue_from("msg_a")], ids=["create", "continue"])
    async def test_runner_refuses_a_thread_value(self, respx_mock: MockRouter, thread: Any) -> None:
        queue_responses(respx_mock, message_response("msg_a"))
        runner = make_async_runner()

        with pytest.raises(TypeError, match="`thread` cannot be set in the params of a tool runner"):
            make_async_runner(thread=thread)
        with pytest.raises(TypeError, match="`thread` cannot be set in the params of a tool runner"):
            runner.set_messages_params(lambda params: {**params, "thread": thread})
        await runner.until_done()

        assert request_threads(respx_mock) == [CREATE]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    async def test_runner_over_an_existing_thread_continues_it(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            message_response("msg_b", tool_use_id="toolu_b"),
            message_response("msg_c", "Sunny."),
        )
        thread = make_async_thread(tools=[beta_async_tool(async_get_weather, name="get_weather")])
        await thread.send(user("Hello"))
        thread.append(WEATHER_QUESTION)

        final = await thread.tool_runner().until_done()

        assert thread.previous_message_id == final.id == "msg_c"
        assert roles(thread.messages) == ["user", "assistant", "user", "assistant", "user", "assistant"]
        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a"), continue_from("msg_b")]
        assert request_helper_tags(respx_mock) == [["message-thread"], *[["BetaToolRunner, message-thread"]] * 2]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    async def test_runner_over_an_existing_thread_adds_and_removes_tools_on_it(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_0"), *tool_change_replies(), message_response("msg_e"))
        added = beta_async_tool(async_lookup, name="lookup")
        thread = make_async_thread(
            tools=[beta_async_tool(async_get_weather, name="get_weather")], betas=[INLINE_TOOLS_BETA]
        )
        await thread.send(user("Hello"))
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner()

        await anext(runner)
        runner.add_tools(added)
        await anext(runner)
        runner.remove_tools("get_weather")
        with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
            await runner.until_done()
        await thread.send(user("Thanks"))

        bodies = request_bodies(respx_mock)
        assert [body["thread"] for body in bodies] == [
            CREATE,
            *map(continue_from, ("msg_0", "msg_a", "msg_b", "msg_c", "msg_d")),
        ]
        assert ["tools" in body for body in bodies] == [True, False, False, False, False, False]
        assert [body["messages"] for body in bodies[1:]] == [
            [WEATHER_QUESTION],
            *tool_change_turns(added.to_dict()),
            [user("Thanks")],
        ]
        assert [message for message in thread.messages if message["role"] == "system"] == [
            tool_addition(added.to_dict()),
            tool_removal("get_weather"),
        ]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    @pytest.mark.parametrize(
        ("headers", "sent"),
        [(None, ("thread", None)), ({"X-Run": "run"}, (None, "run"))],
        ids=["none_given", "headers_given"],
    )
    async def test_runner_request_options_replace_the_threads_for_its_turns_only(
        self, respx_mock: MockRouter, headers: dict[str, str] | None, sent: tuple[str | None, str | None]
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a"),
            message_response("msg_b", "Sunny."),
            message_response("msg_c"),
        )
        thread = make_async_thread(
            tools=[beta_async_tool(async_get_weather, name="get_weather")], extra_headers={"X-Thread": "thread"}
        )
        thread.append(WEATHER_QUESTION)

        await thread.tool_runner(extra_headers=headers).until_done()
        await thread.send(user("Thanks"))

        requests = sent_requests(respx_mock)
        assert [(r.headers.get("X-Thread"), r.headers.get("X-Run")) for r in requests] == [sent, sent, ("thread", None)]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    @pytest.mark.parametrize(
        "dropped", [None, ["container"]], ids=["params_left_alone", "params_set_without_the_container"]
    )
    async def test_runner_that_stops_at_its_limit_leaves_the_tool_results_and_the_container_on_the_thread(
        self, respx_mock: MockRouter, dropped: list[str] | None
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a", container="container_a"),
            message_response("msg_b"),
        )
        thread = make_async_thread(tools=[beta_async_tool(async_get_weather, name="get_weather")])
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner(max_iterations=1)

        await anext(runner)
        if dropped is not None:
            runner.set_messages_params(lambda params: cast(Any, {k: v for k, v in params.items() if k not in dropped}))
        await runner.until_done()
        await thread.send(user("Thanks"))

        continued = request_bodies(respx_mock)[1]
        assert (continued["thread"], continued.get("container")) == (continue_from("msg_a"), "container_a")
        assert continued["messages"] == [tool_result("toolu_a"), user("Thanks")]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    @ASYNC_RESPONSE_KINDS
    async def test_runner_ends_on_a_refused_turn_and_leaves_its_tool_results_staged(
        self, respx_mock: MockRouter, respond: Any, stream: bool
    ) -> None:
        queue_responses(
            respx_mock,
            respond("msg_a", tool_use_id="toolu_a"),
            respond("msg_b", "I can't help with that.", stop_reason="refusal"),
            message_response("msg_c"),
        )
        thread = make_async_thread(tools=[beta_async_tool(async_get_weather, name="get_weather")])
        thread.append(WEATHER_QUESTION)

        final = await thread.tool_runner(stream=stream).until_done()
        await thread.send(user("Never mind"))

        refused, created = request_bodies(respx_mock)[1:]
        assert (final.id, final.stop_reason) == ("msg_b", "refusal")
        assert (refused["thread"], refused["messages"]) == (continue_from("msg_a"), [tool_result("toolu_a")])
        assert created["thread"] == CREATE
        assert created["messages"] == [
            WEATHER_QUESTION,
            tool_use("toolu_a"),
            tool_result("toolu_a"),
            user("Never mind"),
        ]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    @ASYNC_RESPONSE_KINDS
    async def test_runner_continues_without_a_thread_when_the_thread_is_lost_again_right_after_a_replay(
        self, respx_mock: MockRouter, respond: Any, stream: bool
    ) -> None:
        queue_responses(
            respx_mock,
            respond("msg_a", tool_use_id="toolu_a"),
            THREAD_NOT_FOUND,
            respond("msg_c", tool_use_id="toolu_c"),
            THREAD_NOT_FOUND,
            respond("msg_e", tool_use_id="toolu_e"),
            respond("msg_f", "Sunny."),
        )
        runner = make_async_runner(stream=stream)

        final = await runner.until_done()

        history = [
            WEATHER_QUESTION,
            tool_use("toolu_a"),
            tool_result("toolu_a"),
            tool_use("toolu_c"),
            tool_result("toolu_c"),
        ]
        assert final.id == "msg_f"
        assert request_threads(respx_mock) == [
            CREATE,
            continue_from("msg_a"),
            CREATE,
            continue_from("msg_c"),
            None,
            None,
        ]
        assert [body["messages"] for body in request_bodies(respx_mock)[4:]] == [
            history,
            [*history, tool_use("toolu_e"), tool_result("toolu_e")],
        ]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    @ASYNC_RESPONSE_KINDS
    async def test_runner_goes_on_under_a_new_thread_after_a_reply_from_a_fallback_model(
        self, respx_mock: MockRouter, respond: Any, stream: bool
    ) -> None:
        queue_responses(
            respx_mock,
            respond("msg_a", tool_use_id="toolu_a", iterations=FALLBACK_ITERATIONS),
            respond("msg_b", tool_use_id="toolu_b"),
            respond("msg_c", "Sunny."),
        )
        runner = make_async_runner(stream=stream, fallbacks=FALLBACKS, betas=[FALLBACK_BETA])

        final = await runner.until_done()

        first, created, continued = bodies = request_bodies(respx_mock)
        assert final.id == "msg_c"
        assert [(body["model"], body["fallbacks"]) for body in bodies] == [(MODEL, FALLBACKS)] * 3
        assert [body["thread"] for body in bodies] == [CREATE, CREATE, continue_from("msg_b")]
        assert created["tools"] == first["tools"]
        assert created["messages"] == [WEATHER_QUESTION, tool_use("toolu_a"), tool_result("toolu_a")]
        assert continued["messages"] == [tool_result("toolu_b")]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    async def test_runner_over_a_typed_thread_parses_the_final_message(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a"),
            message_response("msg_b", json.dumps({"forecast": "Sunny"})),
        )
        thread = make_async_thread(
            tools=[beta_async_tool(async_get_weather, name="get_weather")], output_format=Forecast
        )
        thread.append(WEATHER_QUESTION)

        final = await thread.tool_runner().until_done()

        assert final.parsed_output == Forecast(forecast="Sunny")
        assert thread.previous_message_id == final.id == "msg_b"

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    async def test_streaming_runner_set_messages_params_replaces_the_history_mid_loop(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock, async_stream_response("msg_a", tool_use_id="toolu_a"), async_stream_response("msg_b", "Sunny.")
        )
        thread = make_async_thread(tools=[beta_async_tool(async_get_weather, name="get_weather")])
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner(stream=True)

        await anext(runner)
        runner.set_messages_params(lambda params: {**params, "messages": [user("Start over: Oakland?")]})
        await runner.until_done()

        replaced = request_bodies(respx_mock)[1]
        assert replaced["thread"] == CREATE
        assert replaced["messages"] == [user("Start over: Oakland?"), tool_use("toolu_a"), tool_result("toolu_a")]
        assert roles(thread.messages) == ["user", "assistant", "user", "assistant"]
        assert thread.previous_message_id == "msg_b"

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    async def test_fork_during_a_turn_has_the_history_that_set_messages_params_replaced_the_threads_with(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock, message_response("msg_a"), async_stream_response("msg_b", "Sunny."), message_response("msg_c")
        )
        thread = make_async_thread(tools=[beta_async_tool(async_get_weather, name="get_weather")])
        await thread.send(user("Hello"))
        runner = thread.tool_runner()

        async with thread.stream(WEATHER_QUESTION):
            runner.set_messages_params(lambda params: {**params, "messages": [user("Start over: Oakland?")]})
            await thread.fork().send()

        forked = request_bodies(respx_mock)[2]
        assert (forked["thread"], forked["messages"]) == (CREATE, [user("Start over: Oakland?")])

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    async def test_streaming_runner_whose_stream_fails_leaves_the_thread_free(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            async_interrupted_stream_response("msg_a", "Let me", error=httpx2.ReadError),
            message_response("msg_b"),
        )
        thread = make_async_thread(tools=[beta_async_tool(async_get_weather, name="get_weather")])
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner(stream=True)
        with pytest.raises(httpx2.ReadError):
            async for stream in runner:
                await stream.until_done()

        await thread.send(user("Are you there?"))

        later = request_bodies(respx_mock)[1]
        assert (later["thread"], later["messages"]) == (
            CREATE,
            [WEATHER_QUESTION, assistant("Let me"), user("Are you there?")],
        )
        assert thread.previous_message_id == "msg_b"

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    async def test_runner_adds_tool_results_ahead_of_messages_appended_to_the_thread_mid_loop(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock, message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b", "Sunny.")
        )
        thread = make_async_thread(tools=[beta_async_tool(async_get_weather, name="get_weather")])
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner()

        await anext(runner)
        thread.append(user("In one word."))
        await runner.until_done()

        continued = request_bodies(respx_mock)[1]
        assert continued["thread"] == continue_from("msg_a")
        assert continued["messages"] == [tool_result("toolu_a"), user("In one word.")]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    @LOOP_BODIES
    @RUNNER_MODES
    @ASYNC_RESPONSE_KINDS
    async def test_runner_sends_the_history_the_loop_body_leaves(
        self, respx_mock: MockRouter, respond: Any, stream: bool, mode: dict[str, Any], body: LoopBody
    ) -> None:
        queue_responses(respx_mock, respond("msg_a", tool_use_id="toolu_a"), respond("msg_b", "Sunny."))
        locations: list[str] = []

        async def get_weather(location: str) -> str:
            locations.append(location)
            return f"Sunny in {location}"

        runner = make_async_runner(stream=stream, tools=[beta_async_tool(get_weather)], **mode)

        item: Any = await anext(runner)
        reply = None if body.reads == "nothing" else await item.get_final_message() if stream else item
        tool_response = await runner.generate_tool_call_response() if body.reads == "tool_response" else None
        body.change(runner, reply, tool_response)
        final = await runner.until_done()

        requests = request_bodies(respx_mock)
        assert len(requests) == 2
        assert_sends_conversation(requests[1], mode, body.conversation)
        assert len(locations) == body.tool_runs
        assert final.id == "msg_b"

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    @RUNNER_MODES
    @ASYNC_RESPONSE_KINDS
    async def test_runner_still_runs_a_tool_that_set_messages_params_gives_as_a_definition(
        self, respx_mock: MockRouter, respond: Any, stream: bool, mode: dict[str, Any]
    ) -> None:
        queue_responses(respx_mock, respond("msg_a", tool_use_id="toolu_a"), respond("msg_b", "Sunny."))
        tool = beta_async_tool(async_get_weather, name="get_weather")
        runner = make_async_runner(stream=stream, tools=[tool], **mode)

        await anext(runner)
        runner.set_messages_params(lambda params: {**params, "tools": [tool.to_dict()]})
        await runner.until_done()

        assert_sends_conversation(
            request_bodies(respx_mock)[1], mode, [WEATHER_QUESTION, tool_use("toolu_a"), tool_result("toolu_a")]
        )

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    @RUNNER_MODES
    async def test_runner_runs_neither_a_tool_set_messages_params_takes_out_of_tools_nor_one_it_adds(
        self, respx_mock: MockRouter, mode: dict[str, Any]
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a"),
            message_response("msg_b", tool_use_id="toolu_b", tool_name="lookup"),
            message_response("msg_c"),
        )
        locations: list[str] = []

        async def get_weather(location: str) -> str:
            locations.append(location)
            return f"Sunny in {location}"

        runner = make_async_runner(tools=[beta_async_tool(get_weather)], **mode)
        added = beta_async_tool(async_lookup, name="lookup").to_dict()

        # With default settings the definitions sent can change only before the first request.
        runner.set_messages_params(lambda params: {**params, "tools": [added]})
        with pytest.warns(UserWarning, match="not found in tool runner"):
            await runner.until_done()

        first, second, third = request_bodies(respx_mock)
        assert locations == []
        assert [tool["name"] for tool in first["tools"]] == ["lookup"]
        for request, tool_use_id, name in ((second, "toolu_a", "get_weather"), (third, "toolu_b", "lookup")):
            assert request["messages"][-1]["content"] == [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": f"Error: Tool '{name}' not found",
                    "is_error": True,
                }
            ]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    async def test_set_messages_params_leaves_the_tools_of_the_thread_to_a_later_runner(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            message_response("msg_b", tool_use_id="toolu_b"),
            message_response("msg_c"),
        )
        tool = beta_async_tool(async_get_weather, name="get_weather")
        thread = make_async_thread(tools=[tool], messages=[WEATHER_QUESTION])

        runner = thread.tool_runner()
        runner.set_messages_params(lambda params: {**params, "max_tokens": 12})
        await runner.until_done()
        thread.append(user("And now?"))
        await thread.tool_runner().until_done()

        assert thread.params.get("tools") == [tool]
        assert request_bodies(respx_mock)[2]["messages"] == [tool_result("toolu_b")]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    @RUNNER_MODES
    async def test_runner_keeps_the_first_turn_after_append_messages_before_the_loop(
        self, respx_mock: MockRouter, mode: dict[str, Any]
    ) -> None:
        queue_responses(
            respx_mock, message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b", "Sunny.")
        )
        locations: list[str] = []

        async def get_weather(location: str) -> str:
            locations.append(location)
            return f"Sunny in {location}"

        runner = make_async_runner(tools=[beta_async_tool(get_weather)], **mode)

        runner.append_messages(user("Be concise."))
        await runner.until_done()

        first, second = request_bodies(respx_mock)
        turn = [tool_use("toolu_a"), tool_result("toolu_a")]
        assert first["messages"] == [WEATHER_QUESTION, user("Be concise.")]
        assert second.get("thread") == (None if mode else continue_from("msg_a"))
        assert second["messages"] == ([*first["messages"], *turn] if mode else turn[1:])
        assert locations == ["San Francisco"]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    @NEW_SYSTEM_WITH_ANOTHER_HISTORY
    @RUNNER_MODES
    async def test_runner_takes_a_new_system_with_another_history_only_when_it_sends_the_whole_history(
        self, respx_mock: MockRouter, mode: dict[str, Any], change: Callable[[Any], None]
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b"))
        locations: list[str] = []

        async def get_weather(location: str) -> str:
            locations.append(location)
            return f"Sunny in {location}"

        runner = make_async_runner(system="Be brief.", tools=[beta_async_tool(get_weather)], **mode)

        await anext(runner)
        change(runner)
        with nullcontext() if mode else pytest.raises(AnthropicError, match="Cannot change `system`"):
            await runner.until_done()

        sent = ["Be brief.", "Be very brief."] if mode else ["Be brief."]
        assert [body["system"] for body in request_bodies(respx_mock)] == sent
        assert len(locations) == len(sent) - 1

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    @RUNNER_MODES
    @ASYNC_RESPONSE_KINDS
    async def test_runner_gives_set_messages_params_the_tools_as_definitions(
        self, respx_mock: MockRouter, respond: Any, stream: bool, mode: dict[str, Any]
    ) -> None:
        queue_responses(respx_mock, respond("msg_a", tool_use_id="toolu_a"), respond("msg_b", "Sunny."))
        tool = beta_async_tool(async_get_weather, name="get_weather")
        runner = make_async_runner(stream=stream, tools=[tool], **mode)
        seen: list[Any] = []

        def copy_tools(params: Any) -> Any:
            seen.extend(params["tools"])
            return {**params, "tools": [{**tool} for tool in params["tools"]]}

        await anext(runner)
        runner.set_messages_params(copy_tools)
        await runner.until_done()

        assert seen == [tool.to_dict()]
        assert_sends_conversation(
            request_bodies(respx_mock)[1], mode, [WEATHER_QUESTION, tool_use("toolu_a"), tool_result("toolu_a")]
        )

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    @RUNNER_MODES
    @ASYNC_RESPONSE_KINDS
    async def test_runner_keeps_the_header_params_that_set_messages_params_leaves_out(
        self, respx_mock: MockRouter, respond: Any, stream: bool, mode: dict[str, Any]
    ) -> None:
        queue_responses(respx_mock, respond("msg_a", tool_use_id="toolu_a"), respond("msg_b", "Sunny."))
        tool = beta_async_tool(async_get_weather, name="get_weather")
        runner = make_async_runner(
            stream=stream,
            tools=[tool],
            betas=[INLINE_TOOLS_BETA],
            user_profile_id="uprof_a",
            workspace_id="wrkspc_a",
            **mode,
        )

        params: Any = {"model": MODEL, "max_tokens": 2048, "tools": [tool.to_dict()], "messages": [WEATHER_QUESTION]}

        await anext(runner)
        runner.set_messages_params(params)
        await runner.until_done()

        first, second = sent_requests(respx_mock)
        assert json.loads(second.content)["max_tokens"] == 2048
        assert INLINE_TOOLS_BETA in request_betas(respx_mock)[1]
        for header in ("anthropic-beta", "anthropic-user-profile-id", "anthropic-workspace-id"):
            assert second.headers[header] == first.headers[header]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    @RUNNER_MODES
    @ASYNC_RESPONSE_KINDS
    async def test_runner_stops_on_a_tool_use_reply_without_tool_calls_whatever_the_caller_appends(
        self, respx_mock: MockRouter, respond: Any, stream: bool, mode: dict[str, Any]
    ) -> None:
        queue_responses(respx_mock, respond("msg_a", "Which city?", stop_reason="tool_use"))
        runner = make_async_runner(stream=stream, **mode)

        item: Any = await anext(runner)
        runner.append_messages(await item.get_final_message() if stream else item, user("San Francisco"))
        final = await runner.until_done()

        assert final.id == "msg_a"
        assert len(request_bodies(respx_mock)) == 1

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    @RUNNER_MODES
    @ASYNC_RESPONSE_KINDS
    async def test_runner_resumes_a_paused_turn_with_the_history_the_caller_appended_to(
        self, respx_mock: MockRouter, respond: Any, stream: bool, mode: dict[str, Any]
    ) -> None:
        queue_responses(respx_mock, respond("msg_a", "Searching", stop_reason="pause_turn"), respond("msg_b"))
        runner = make_async_runner(stream=stream, **mode)

        await anext(runner)
        runner.append_messages(user("Never mind."))
        await runner.until_done()

        resumed = request_bodies(respx_mock)[1]
        assert resumed.get("thread") == (None if mode else CREATE)
        assert resumed["messages"] == [WEATHER_QUESTION, user("Never mind.")]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    async def test_runner_refuses_a_changed_system_before_it_runs_a_tool(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a", tool_use_id="toolu_a"))
        locations: list[str] = []

        async def record_location(location: str) -> str:
            locations.append(location)
            return "Sunny"

        runner = make_async_runner(system="Be brief.", tools=[beta_async_tool(record_location, name="get_weather")])

        await anext(runner)
        runner.set_messages_params(lambda params: {**params, "system": "Be very brief."})
        with pytest.raises(AnthropicError, match="Cannot change `system`"):
            await runner.until_done()

        assert locations == []
        assert respx_mock.calls.call_count == 1

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    async def test_runner_stops_threading_after_a_compaction_request_that_cannot_be_threaded(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a"),
            unsupported_response("context_management"),
            compaction_response("msg_b"),
            message_response("msg_c", "Sunny."),
        )
        runner = make_async_runner(betas=["compact-2026-09-04"])

        await anext(runner)
        runner.compact_before_next_turn()
        await runner.until_done()

        assert request_threads(respx_mock) == [CREATE, CREATE, None, None]
        assert request_bodies(respx_mock)[3]["messages"] == [COMPACTED]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    async def test_runner_keeps_a_message_appended_to_the_thread_while_it_compacts(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a"),
            compaction_response("msg_b"),
            message_response("msg_c", "Sunny."),
        )
        thread = make_async_thread(
            tools=[beta_async_tool(async_get_weather, name="get_weather")], betas=["compact-2026-09-04"]
        )
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner()

        await anext(runner)
        runner.compact_before_next_turn()
        assert (await anext(runner)).stop_reason == "compaction"
        with pytest.raises(ValueError, match="being compacted"):
            runner.append_messages(user("In two words."))
        thread.append(user("In one word."))
        await runner.until_done()

        assert request_bodies(respx_mock)[2]["messages"] == [COMPACTED, user("In one word.")]
        assert thread.messages[1] == user("In one word.")
        assert roles(thread.messages) == ["assistant", "user", "assistant"]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    async def test_runner_keeps_a_message_appended_to_the_thread_while_it_compacts_after_the_final_turn(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", "Sunny."),
            compaction_response("msg_b"),
            message_response("msg_c", "Sunny."),
        )
        thread = make_async_thread(
            tools=[beta_async_tool(async_get_weather, name="get_weather")], betas=["compact-2026-09-04"]
        )
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner()

        await anext(runner)
        runner.compact_before_next_turn()
        assert (await anext(runner)).stop_reason == "compaction"
        thread.append(user("In one word."))
        await runner.until_done()
        messages_after_the_runner, requests_of_the_runner = thread.messages, respx_mock.calls.call_count
        await thread.send()

        assert requests_of_the_runner == 2
        assert messages_after_the_runner[1:] == (user("In one word."),)
        assert request_bodies(respx_mock)[2]["messages"] == [COMPACTED, user("In one word.")]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    async def test_runner_sends_the_compaction_once_when_it_is_appended_to_the_thread_again(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a"),
            compaction_response("msg_b"),
            message_response("msg_c", "Sunny."),
        )
        thread = make_async_thread(
            tools=[beta_async_tool(async_get_weather, name="get_weather")], betas=["compact-2026-09-04"]
        )
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner()

        await anext(runner)
        runner.compact_before_next_turn()
        thread.append(await anext(runner), user("In one word."))
        await runner.until_done()

        assert request_bodies(respx_mock)[2]["messages"] == [COMPACTED, user("In one word.")]
        assert roles(thread.messages) == ["assistant", "user", "assistant"]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    @pytest.mark.parametrize("ending", ["block_left_early", "events_run_out"])
    async def test_runner_compacts_a_thread_that_ends_in_a_partial_reply_without_that_reply(
        self, respx_mock: MockRouter, ending: str
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            async_stream_response("msg_b", "one two three")
            if ending == "block_left_early"
            else async_interrupted_stream_response("msg_b", "one"),
            compaction_response("msg_c"),
            message_response("msg_d", "Three."),
        )
        thread = make_async_thread(
            tools=[beta_async_tool(async_get_weather, name="get_weather")], betas=["compact-2026-09-04"]
        )
        await thread.send(user("Hello"))
        async with thread.stream(user("Count")) as stream:
            if ending == "block_left_early":
                await anext(stream.text_stream)
            else:
                await stream.until_done()
        messages_after_the_stream = thread.messages
        runner = thread.tool_runner()

        runner.compact_before_next_turn()
        await runner.until_done()

        compaction, later = request_bodies(respx_mock)[2:]
        assert roles(messages_after_the_stream) == ["user", "assistant", "user", "assistant"]
        assert compaction["compaction"] == {"type": "summarize"}
        assert (compaction["thread"], compaction["messages"]) == (CREATE, [user("Hello"), assistant(), user("Count")])
        assert (later["thread"], later["messages"]) == (CREATE, [COMPACTED])
        assert roles(thread.messages) == ["assistant", "assistant"]

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    async def test_runner_takes_other_params_after_a_message_is_appended_to_the_thread_while_it_compacts(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a"),
            compaction_response("msg_b"),
            message_response("msg_c", "Sunny."),
        )
        thread = make_async_thread(
            tools=[beta_async_tool(async_get_weather, name="get_weather")], betas=["compact-2026-09-04"]
        )
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner()

        await anext(runner)
        runner.compact_before_next_turn()
        assert (await anext(runner)).stop_reason == "compaction"
        thread.append(user("In one word."))
        runner.set_messages_params(lambda params: {**params, "max_tokens": 12})
        with pytest.raises(ValueError, match="being compacted"):
            runner.set_messages_params(lambda params: {**params, "messages": [user("Hello")]})
        await runner.until_done()

        later = request_bodies(respx_mock)[2]
        assert (later["max_tokens"], later["messages"]) == (12, [COMPACTED, user("In one word.")])

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    @ASYNC_RESPONSE_KINDS
    async def test_runner_sends_a_message_appended_to_the_thread_while_a_turn_is_paused_with_the_resume(
        self, respx_mock: MockRouter, respond: Any, stream: bool
    ) -> None:
        queue_responses(respx_mock, respond("msg_a", "Searching", stop_reason="pause_turn"), server_error())
        thread = make_async_thread(tools=[beta_async_tool(async_get_weather, name="get_weather")])
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner(stream=stream)

        await anext(runner)
        thread.append(user("In one word."))
        with pytest.raises(InternalServerError):
            await runner.until_done()

        resumed = request_bodies(respx_mock)[1]
        assert (resumed["thread"], resumed["messages"]) == (continue_from("msg_a"), [user("In one word.")])
        assert thread.messages[2:] == (user("In one word."),)


async def run_turn(
    thread: BetaAsyncMessageThread[Any], method: str, *messages: BetaMessageParam, **overrides: Any
) -> None:
    """Call `send()`, `parse()` or `stream()`, and read a stream to its end."""
    turn = getattr(thread, method)(*messages, **overrides)
    if method == "stream":
        async with turn as stream:
            await stream.until_done()
    else:
        await turn
