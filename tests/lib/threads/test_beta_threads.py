from __future__ import annotations

import gc
import json
import asyncio
import inspect
import logging
import operator
from typing import Any, Callable
from functools import reduce
from contextlib import nullcontext
from typing_extensions import get_args, get_type_hints

import httpx2
import pytest
import pydantic
from respx import MockRouter

from anthropic import (
    APIError,
    Anthropic,
    AnthropicError,
    AsyncAnthropic,
    BadRequestError,
    InternalServerError,
    omit,
)
from anthropic._types import Omit
from anthropic._utils import is_required_type, assert_signatures_in_sync
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools import beta_tool
from anthropic.types.beta import (
    BetaToolParam,
    BetaMessageParam,
    ThreadSendParams,
    BetaTextBlockParam,
    ThreadCreateParams,
)
from anthropic.lib.threads import BetaMessageThread, BetaAsyncMessageThread
from anthropic.types.beta.message_create_params import MessageCreateParamsBase

from .helpers import (
    MODEL,
    CREATE,
    FALLBACKS,
    MAX_TOKENS,
    CLIENT_KINDS,
    THREADS_BETA,
    TURN_METHODS,
    FALLBACK_BETA,
    IN_PLACE_EDITS,
    THREADS_LOGGER,
    THREAD_NOT_FOUND,
    WEATHER_QUESTION,
    ALREADY_CONTINUED,
    INLINE_TOOLS_BETA,
    CONTINUE_IN_FLIGHT,
    FALLBACK_ITERATIONS,
    FINGERPRINT_MISMATCH,
    ANSWERED_TURN_METHODS,
    OWN_CREATE_ONLY_FIELDS,
    CHANGES_DURING_THE_TURN,
    CONTEXT_MANAGEMENT_BETA,
    FAILURES_BEFORE_A_REPLY,
    ALREADY_CONTINUED_MESSAGE,
    ONE_TURN_CREATE_ONLY_FIELDS,
    CHANGES_OF_ANOTHER_FIELD_DURING_THE_TURN,
    Forecast,
    InPlaceEdit,
    user,
    roles,
    marked,
    base_url,
    unmarked,
    assistant,
    id_headers,
    get_weather,
    make_client,
    make_thread,
    thread_logs,
    marked_twice,
    response_ids,
    server_error,
    tool_removal,
    continue_from,
    request_betas,
    sent_requests,
    fallback_reply,
    request_bodies,
    queue_responses,
    request_threads,
    stream_response,
    message_response,
    fallback_response,
    api_error_response,
    request_helper_tags,
    unsupported_response,
    stream_error_response,
    history_with_nested_blocks,
    interrupted_stream_response,
    partial_tool_use_stream_response,
)

pytestmark = pytest.mark.respx(base_url=base_url)

XLSX_SKILL = {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
NOOP_TOOL: BetaToolParam = {
    "name": "noop",
    "description": "Does nothing.",
    "input_schema": {"type": "object", "properties": {}},
}


class TestMessageThread:
    def test_first_send_creates_a_thread_with_the_seed_and_the_new_messages(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"))
        thread = make_thread(messages=[user("Seed"), assistant("Seeded")])

        reply = thread.send(user("Hello"))

        body = request_bodies(respx_mock)[0]
        assert body["thread"] == CREATE
        assert body["messages"] == [user("Seed"), assistant("Seeded"), user("Hello")]
        assert thread.previous_message_id == reply.id == "msg_a"

    def test_next_send_continues_the_thread_with_only_the_new_messages(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_thread()

        thread.send(user("Hello"))
        second = thread.send(user("Again"))

        body = request_bodies(respx_mock)[1]
        assert body["thread"] == continue_from("msg_a")
        assert body["messages"] == [user("Again")]
        assert thread.previous_message_id == second.id == "msg_b"
        assert roles(thread.messages) == ["user", "assistant", "user", "assistant"]

    def test_continue_omits_the_system_and_tools_the_server_holds(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_thread(model="claude-sonnet-5", system="You are terse.", tools=[NOOP_TOOL])

        thread.send(user("Hello"))
        thread.send(user("Again"))

        created, continued = request_bodies(respx_mock)
        assert (created["system"], created["tools"]) == ("You are terse.", [NOOP_TOOL])
        assert continued["model"] == "claude-sonnet-5"
        assert "system" not in continued and "tools" not in continued

    def test_replay_after_a_continue_sends_system_and_tools_again(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), THREAD_NOT_FOUND, message_response("msg_c"))
        thread = make_thread(system="You are terse.", tools=[NOOP_TOOL])
        thread.send(user("Hello"))

        thread.send(user("Again"))

        replayed = request_bodies(respx_mock)[2]
        assert (replayed["thread"], replayed["system"], replayed["tools"]) == (CREATE, "You are terse.", [NOOP_TOOL])

    def test_send_overrides_apply_to_that_turn_only(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_thread(max_tokens=1024)

        thread.send(user("Hello"), max_tokens=12, speed="fast")
        thread.send(user("Again"))

        overridden, later = request_bodies(respx_mock)
        assert (overridden["max_tokens"], overridden["speed"]) == (12, "fast")
        assert later["max_tokens"] == 1024
        assert "speed" not in later

    @pytest.mark.parametrize(
        ("betas", "expected"),
        [
            ([], [THREADS_BETA]),
            ([CONTEXT_MANAGEMENT_BETA], [CONTEXT_MANAGEMENT_BETA, THREADS_BETA]),
            ([CONTEXT_MANAGEMENT_BETA, THREADS_BETA], [CONTEXT_MANAGEMENT_BETA, THREADS_BETA]),
        ],
        ids=["no_betas", "another_beta", "threads_beta_already_set"],
    )
    def test_every_turn_sends_the_threads_beta_once_after_the_callers_betas(
        self, respx_mock: MockRouter, betas: list[Any], expected: list[str]
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_thread(betas=betas)

        thread.send(user("Hello"))
        thread.send(user("Again"))

        assert request_betas(respx_mock) == [expected, expected]

    @pytest.mark.parametrize(
        "header",
        [CONTEXT_MANAGEMENT_BETA, f"{CONTEXT_MANAGEMENT_BETA}, {THREADS_BETA}"],
        ids=["another_beta", "threads_beta_already_set"],
    )
    def test_caller_anthropic_beta_header_gains_the_threads_beta_once(
        self, respx_mock: MockRouter, header: str
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_thread(extra_headers={"Anthropic-Beta": header})

        thread.send(user("Hello"))
        thread.send(user("Again"), extra_headers={"anthropic-beta": header})

        expected = [CONTEXT_MANAGEMENT_BETA, THREADS_BETA]
        assert [[beta.strip() for beta in betas] for betas in request_betas(respx_mock)] == [expected, expected]

    def test_caller_anthropic_beta_header_is_left_alone_once_unthreaded(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, unsupported_response("inference_hooks"), message_response("msg_b"))
        thread = make_thread(
            extra_headers={"anthropic-beta": CONTEXT_MANAGEMENT_BETA},
            unsupported_request_behavior="continue_unthreaded",
        )

        thread.send(user("Hello"))

        assert request_betas(respx_mock) == [[CONTEXT_MANAGEMENT_BETA, THREADS_BETA], [CONTEXT_MANAGEMENT_BETA]]

    @pytest.mark.parametrize(
        "method",
        [
            "send",
            pytest.param("parse", marks=pytest.mark.skipif(PYDANTIC_V1, reason="parse() is pydantic-v2 only")),
            "stream",
        ],
    )
    def test_every_request_names_the_thread_in_the_helper_telemetry_header(
        self, respx_mock: MockRouter, method: str
    ) -> None:
        respond = stream_response if method == "stream" else message_response
        queue_responses(
            respx_mock,
            respond("msg_a"),
            THREAD_NOT_FOUND,
            respond("msg_c"),
            unsupported_response("inference_hooks"),
            respond("msg_e"),
        )
        thread = make_thread(unsupported_request_behavior="continue_unthreaded")

        for text in ("One", "Two", "Three"):
            turn = getattr(thread, method)(user(text))
            if method == "stream":
                with turn as stream:
                    stream.until_done()

        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a"), CREATE, continue_from("msg_c"), None]
        assert request_helper_tags(respx_mock) == [["message-thread"]] * 5

    def test_no_request_option_drops_or_repeats_the_helper_tag(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, *(message_response(id) for id in ("msg_a", "msg_b", "msg_c", "msg_d")))
        thread = make_thread(extra_headers={"X-Stainless-Helper": "mine"})

        thread.send(user("One"))
        thread.send(user("Two"), extra_headers={})
        thread.send(user("Three"), extra_headers={"x-stainless-helper": "message-thread, mine"})
        thread.update(extra_headers={"x-stainless-helper": omit})
        thread.send(user("Four"))

        assert request_helper_tags(respx_mock) == [
            ["mine, message-thread"],
            ["message-thread"],
            ["message-thread, mine"],
            ["message-thread"],
        ]
        assert "message-thread" not in repr(thread.params)

    def test_consecutive_user_messages_are_sent_as_they_were_appended(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"))
        thread = make_thread()

        thread.append(user("part one"))
        thread.append({"role": "user", "content": [{"type": "text", "text": "part two"}]})
        thread.send()

        assert request_bodies(respx_mock)[0]["messages"] == [
            user("part one"),
            {"role": "user", "content": [{"type": "text", "text": "part two"}]},
        ]

    def test_send_with_nothing_staged_goes_out(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_thread()
        thread.send(user("Hello"))

        thread.send()

        body = request_bodies(respx_mock)[1]
        assert (body["thread"], body["messages"]) == (continue_from("msg_a"), [])

    def test_send_after_a_paused_reply_continues_from_it_with_no_messages(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock, message_response("msg_a", "Searching", stop_reason="pause_turn"), message_response("msg_b")
        )
        thread = make_thread()
        thread.send(user("Hello"))

        resumed = thread.send()

        body = request_bodies(respx_mock)[1]
        assert body["thread"] == continue_from("msg_a")
        assert body["messages"] == []
        assert thread.previous_message_id == resumed.id == "msg_b"

    def test_a_turn_that_pauses_twice_continues_from_the_second_pause_with_no_messages(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", "Searching", stop_reason="pause_turn"),
            message_response("msg_b", "Still searching", stop_reason="pause_turn"),
            message_response("msg_c"),
        )
        thread = make_thread()
        thread.send(user("Hello"))
        thread.send()

        thread.send()

        body = request_bodies(respx_mock)[2]
        assert body["thread"] == continue_from("msg_b")
        assert body["messages"] == []
        assert roles(thread.messages) == ["user", "assistant", "assistant", "assistant"]

    def test_send_after_a_resumed_turn_finishes_continues_from_its_last_reply(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", "Searching", stop_reason="pause_turn"),
            message_response("msg_b"),
            message_response("msg_c"),
        )
        thread = make_thread()
        thread.send(user("Hello"))
        thread.send()

        thread.send(user("Again"))

        body = request_bodies(respx_mock)[2]
        assert body["thread"] == continue_from("msg_b")
        assert body["messages"] == [user("Again")]

    def test_user_message_after_a_paused_reply_is_sent_alone_and_the_400_is_raised(
        self, respx_mock: MockRouter
    ) -> None:
        unexecuted = api_error_response(400, "invalid_request_error", "messages.0: `server_tool_use` was not executed")
        queue_responses(respx_mock, message_response("msg_a", "Searching", stop_reason="pause_turn"), unexecuted)
        thread = make_thread()
        thread.send(user("Hello"))

        with pytest.raises(BadRequestError):
            thread.send(user("Never mind"))

        body = request_bodies(respx_mock)[1]
        assert body["thread"] == continue_from("msg_a")
        assert body["messages"] == [user("Never mind")]

    def test_resume_stream_that_ends_before_any_content_keeps_the_paused_reply_resumable(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", "Searching", stop_reason="pause_turn"),
            stream_response("msg_b", "found it"),
            message_response("msg_c"),
        )
        thread = make_thread()
        thread.send(user("Hello"))

        with thread.stream() as stream:
            assert next(iter(stream)).type == "message_start"
        thread.send()

        retried = request_bodies(respx_mock)[2]
        assert (retried["thread"], retried["messages"]) == (CREATE, [user("Hello"), assistant("Searching")])
        assert thread.previous_message_id == "msg_c"

    def test_resume_that_finds_the_thread_gone_replays_the_history_ending_in_the_paused_reply(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", "Searching", stop_reason="pause_turn"),
            THREAD_NOT_FOUND,
            message_response("msg_c"),
        )
        thread = make_thread()
        thread.send(user("Hello"))

        thread.send()

        replayed = request_bodies(respx_mock)[2]
        assert replayed["thread"] == CREATE
        assert replayed["messages"] == [user("Hello"), assistant("Searching")]

    @pytest.mark.parametrize(
        ("rejection", "reason"),
        [
            (THREAD_NOT_FOUND, "thread_not_found"),
            (ALREADY_CONTINUED, "thread_already_continued"),
            (CONTINUE_IN_FLIGHT, "thread_continue_in_flight"),
        ],
        ids=["thread_not_found", "thread_already_continued", "thread_continue_in_flight"],
    )
    def test_rejected_previous_message_id_replays_the_full_history_under_a_new_thread(
        self, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture, rejection: httpx2.Response, reason: str
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"), rejection, message_response("msg_c"))
        caplog.set_level(logging.INFO, logger=THREADS_LOGGER)
        thread = make_thread()

        thread.send(user("Hello"))
        second = thread.send(user("Again"))

        rejected, replayed = request_bodies(respx_mock)[1:]
        assert (rejected["thread"], rejected["messages"]) == (continue_from("msg_a"), [user("Again")])
        assert (replayed["thread"], replayed["messages"]) == (CREATE, [user("Hello"), assistant(), user("Again")])
        assert thread.previous_message_id == second.id == "msg_c"
        assert (
            logging.INFO,
            f"Replaying the full message history under a new thread: reason={reason} previous_message_id=msg_a",
        ) in thread_logs(caplog)

    @pytest.mark.parametrize(
        "rejection",
        [FINGERPRINT_MISMATCH, api_error_response(400, "invalid_request_error", ALREADY_CONTINUED_MESSAGE)],
        ids=["fingerprint_mismatch", "already_continued_without_error_code"],
    )
    def test_other_thread_rejections_raise_and_keep_previous_message_id(
        self, respx_mock: MockRouter, rejection: httpx2.Response
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"), rejection)
        thread = make_thread()
        thread.send(user("Hello"))

        with pytest.raises(BadRequestError):
            thread.send(user("Again"))

        assert respx_mock.calls.call_count == 2
        assert thread.previous_message_id == "msg_a"
        assert roles(thread.messages) == ["user", "assistant"]

    def test_unsupported_request_raises_by_default_and_keeps_previous_message_id(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock, message_response("msg_a"), unsupported_response("fallbacks"), message_response("msg_c")
        )
        thread = make_thread()
        thread.send(user("Hello"))

        with pytest.raises(BadRequestError):
            thread.send(user("Again"), fallbacks=FALLBACKS)
        thread.send(user("Again"))

        retried = request_bodies(respx_mock)[2]
        assert respx_mock.calls.call_count == 3
        assert (retried["thread"], retried["messages"]) == (continue_from("msg_a"), [user("Again")])
        assert "fallbacks" not in retried
        assert thread.previous_message_id == "msg_c"

    def test_continue_unthreaded_stops_threading_after_an_unsupported_request_that_lists_no_feature(
        self, respx_mock: MockRouter
    ) -> None:
        rejection = api_error_response(
            400, "invalid_request_error", "Cannot be used with `thread`.", error_code="thread_unsupported_request"
        )
        queue_responses(respx_mock, rejection, message_response("msg_a"))
        thread = make_thread(unsupported_request_behavior="continue_unthreaded")

        thread.send(user("Hello"))

        assert request_threads(respx_mock) == [CREATE, None]

    @pytest.mark.parametrize(
        "unsupported",
        [["fallbacks"], ["inference_hooks"], ["fallbacks", "thinking"], ["something_new"]],
        ids=["fallbacks", "inference_hooks", "fallbacks_and_thinking", "unknown_feature"],
    )
    def test_continue_unthreaded_stops_threading_for_good_after_an_unsupported_request(
        self, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture, unsupported: list[str]
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            unsupported_response(*unsupported),
            message_response("msg_c"),
            message_response("msg_d"),
        )
        caplog.set_level(logging.INFO, logger=THREADS_LOGGER)
        thread = make_thread(unsupported_request_behavior="continue_unthreaded")
        thread.send(user("Hello"))

        thread.send(user("Again"))
        thread.send(user("Once more"))

        rejected, unthreaded, later = request_bodies(respx_mock)[1:]
        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a"), None, None]
        assert request_betas(respx_mock)[2:] == [[], []]
        assert rejected["messages"] == [user("Again")]
        assert unthreaded["messages"] == [user("Hello"), assistant(), user("Again")]
        assert roles(later["messages"]) == ["user", "assistant", "user", "assistant", "user"]
        assert thread.previous_message_id is None
        assert (
            logging.INFO,
            f"The server cannot thread this request; continuing without a thread: unsupported={','.join(unsupported)}",
        ) in thread_logs(caplog)

    def test_continue_unthreaded_replay_that_is_unsupported_goes_without_a_thread(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            THREAD_NOT_FOUND,
            unsupported_response("fallbacks"),
            message_response("msg_d"),
            message_response("msg_e"),
        )
        thread = make_thread(unsupported_request_behavior="continue_unthreaded")
        thread.send(user("Hello"))

        thread.send(user("Again"), fallbacks=FALLBACKS)
        thread.send(user("Once more"))

        unthreaded, later = request_bodies(respx_mock)[3:]
        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a"), CREATE, None, None]
        assert roles(unthreaded["messages"]) == ["user", "assistant", "user"]
        assert roles(later["messages"]) == ["user", "assistant", "user", "assistant", "user"]
        assert thread.previous_message_id is None

    @ANSWERED_TURN_METHODS
    def test_continue_unthreaded_stops_threading_when_the_thread_is_lost_again_right_after_a_replay(
        self, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture, method: str
    ) -> None:
        respond = stream_response if method == "stream" else message_response
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            THREAD_NOT_FOUND,
            message_response("msg_c"),
            THREAD_NOT_FOUND,
            respond("msg_e", "Hi!"),
            message_response("msg_f"),
        )
        caplog.set_level(logging.INFO, logger=THREADS_LOGGER)
        thread = make_thread(system="You are terse.", unsupported_request_behavior="continue_unthreaded")
        thread.send(user("One"))
        thread.send(user("Two"))

        run_turn(thread, method, user("Three"))
        thread.send(user("Four"))

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
        assert (unthreaded["messages"], unthreaded["system"]) == (history, "You are terse.")
        assert later["messages"] == [*history, assistant(), user("Four")]
        assert request_betas(respx_mock)[4:] == [[], []]
        assert thread.previous_message_id is None
        assert (
            logging.INFO,
            "The server lost the thread again right after a replay; continuing without a thread: "
            "previous_message_id=msg_c",
        ) in thread_logs(caplog)

    def test_continue_unthreaded_counts_the_create_after_a_replay_that_failed_as_the_replay(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            THREAD_NOT_FOUND,
            server_error(),
            message_response("msg_d"),
            THREAD_NOT_FOUND,
            message_response("msg_f"),
        )
        thread = make_thread(unsupported_request_behavior="continue_unthreaded")
        thread.send(user("One"))
        with pytest.raises(InternalServerError):
            thread.send(user("Two"))

        thread.send(user("Two"))
        thread.send(user("Three"))

        assert request_threads(respx_mock) == [
            CREATE,
            continue_from("msg_a"),
            CREATE,
            CREATE,
            continue_from("msg_d"),
            None,
        ]

    def test_a_thread_lost_again_right_after_a_replay_is_replayed_again_by_default(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            THREAD_NOT_FOUND,
            message_response("msg_c"),
            THREAD_NOT_FOUND,
            message_response("msg_e"),
            message_response("msg_f"),
        )
        thread = make_thread()

        for text in ("One", "Two", "Three", "Four"):
            thread.send(user(text))

        assert request_threads(respx_mock) == [
            CREATE,
            continue_from("msg_a"),
            CREATE,
            continue_from("msg_c"),
            CREATE,
            continue_from("msg_e"),
        ]

    def test_continue_unthreaded_replays_a_thread_that_is_lost_after_a_continue_that_succeeded(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            THREAD_NOT_FOUND,
            message_response("msg_c"),
            message_response("msg_d"),
            THREAD_NOT_FOUND,
            message_response("msg_f"),
        )
        thread = make_thread(unsupported_request_behavior="continue_unthreaded")

        for text in ("One", "Two", "Three", "Four"):
            thread.send(user(text))

        assert request_threads(respx_mock) == [
            CREATE,
            continue_from("msg_a"),
            CREATE,
            continue_from("msg_c"),
            continue_from("msg_d"),
            CREATE,
        ]

    @pytest.mark.parametrize(
        ("first", "second"),
        [
            (ALREADY_CONTINUED, THREAD_NOT_FOUND),
            (THREAD_NOT_FOUND, ALREADY_CONTINUED),
            (THREAD_NOT_FOUND, CONTINUE_IN_FLIGHT),
        ],
        ids=["already_continued_first", "already_continued_second", "continue_in_flight_second"],
    )
    def test_continue_unthreaded_keeps_threading_unless_both_rejections_are_thread_not_found(
        self, respx_mock: MockRouter, first: httpx2.Response, second: httpx2.Response
    ) -> None:
        queue_responses(
            respx_mock, message_response("msg_a"), first, message_response("msg_c"), second, message_response("msg_e")
        )
        thread = make_thread(unsupported_request_behavior="continue_unthreaded")

        for text in ("One", "Two", "Three"):
            thread.send(user(text))

        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a"), CREATE, continue_from("msg_c"), CREATE]

    def test_continue_unthreaded_stream_stops_threading_for_good_after_an_unsupported_request(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            unsupported_response("fallbacks"),
            stream_response("msg_c", "Fallback"),
            message_response("msg_d"),
        )
        thread = make_thread(unsupported_request_behavior="continue_unthreaded")
        thread.send(user("Hello"))

        with thread.stream(user("Again"), fallbacks=FALLBACKS) as stream:
            streamed = stream.get_final_message()
        thread.send(user("Once more"))

        unthreaded, later = request_bodies(respx_mock)[2:]
        assert streamed.id == "msg_c"
        assert unthreaded["stream"] is True
        assert "thread" not in unthreaded
        assert "thread" not in later
        assert roles(later["messages"]) == ["user", "assistant", "user", "assistant", "user"]
        assert thread.previous_message_id is None

    @TURN_METHODS
    @FAILURES_BEFORE_A_REPLY
    def test_unrelated_errors_raise_and_the_same_call_again_sends_the_turn_once(
        self, respx_mock: MockRouter, method: str, failure: httpx2.Response | Exception
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"), failure, message_response("msg_c"))
        thread = make_thread()
        thread.send(user("Hello"))
        messages_before = thread.messages

        with pytest.raises(APIError):
            run_turn(thread, method, user("Again"))
        after_the_error = (thread.messages, thread.previous_message_id)
        thread.send(user("Again"))

        retried = request_bodies(respx_mock)[2]
        assert (retried["thread"], retried["messages"]) == (continue_from("msg_a"), [user("Again")])
        assert after_the_error == (messages_before, "msg_a")

    def test_turn_that_failed_is_not_sent_with_the_next_turn(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), server_error(), message_response("msg_c"))
        thread = make_thread()
        thread.send(user("Hello"))
        with pytest.raises(InternalServerError):
            thread.send(user("Again"))

        thread.send(user("Never mind"))

        body = request_bodies(respx_mock)[2]
        assert body["thread"] == continue_from("msg_a")
        assert body["messages"] == [user("Never mind")]
        assert thread.previous_message_id == "msg_c"

    def test_messages_appended_before_a_call_that_fails_stay_staged(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock, message_response("msg_a"), server_error(), server_error(), message_response("msg_d")
        )
        thread = make_thread()
        thread.send(user("Hello"))

        thread.append(user("Appended"))
        with pytest.raises(InternalServerError):
            thread.send(user("Again"))
        with pytest.raises(InternalServerError):
            thread.send()
        thread.send()

        assert [body["messages"] for body in request_bodies(respx_mock)[1:]] == [
            [user("Appended"), user("Again")],
            [user("Appended")],
            [user("Appended")],
        ]

    def test_failed_replay_clears_previous_message_id(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), THREAD_NOT_FOUND, server_error())
        thread = make_thread()
        thread.send(user("Hello"))

        with pytest.raises(InternalServerError):
            thread.send(user("Again"))

        assert respx_mock.calls.call_count == 3
        assert thread.previous_message_id is None

    def test_turn_after_a_failed_replay_creates_a_thread_with_the_full_history(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock, message_response("msg_a"), THREAD_NOT_FOUND, server_error(), message_response("msg_d")
        )
        thread = make_thread()
        thread.send(user("Hello"))
        with pytest.raises(InternalServerError):
            thread.send(user("Again"))

        thread.send(user("Again"))

        body = request_bodies(respx_mock)[3]
        assert (body["thread"], body["messages"]) == (CREATE, [user("Hello"), assistant(), user("Again")])
        assert thread.previous_message_id == "msg_d"

    @ANSWERED_TURN_METHODS
    def test_a_refused_turn_is_not_recorded_and_the_next_turn_starts_a_new_thread(
        self, respx_mock: MockRouter, method: str
    ) -> None:
        respond = stream_response if method == "stream" else message_response
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            respond("msg_b", "I can't help with that.", stop_reason="refusal"),
            message_response("msg_c"),
            message_response("msg_d"),
        )
        thread = make_thread(system="You are terse.", tools=[NOOP_TOOL])
        thread.send(user("Hello"))
        messages_before = thread.messages

        run_turn(thread, method, user("Refused"))
        after_the_refusal = (thread.messages, thread.previous_message_id)
        thread.send(user("Rephrased"))
        thread.send(user("Again"))

        refused, created, continued = request_bodies(respx_mock)[1:]
        assert (refused["thread"], refused["messages"]) == (continue_from("msg_a"), [user("Refused")])
        assert after_the_refusal == (messages_before, None)
        assert (created["thread"], created["system"], created["tools"]) == (CREATE, "You are terse.", [NOOP_TOOL])
        assert created["messages"] == [user("Hello"), assistant(), user("Rephrased")]
        assert (continued["thread"], continued["messages"]) == (continue_from("msg_c"), [user("Again")])

    def test_a_stream_left_once_it_has_shown_the_refusal_is_not_recorded(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            stream_response("msg_b", "I can't help with that.", stop_reason="refusal"),
            message_response("msg_c"),
        )
        thread = make_thread(system="You are terse.")
        thread.send(user("Hello"))
        messages_before = thread.messages

        thread.append(user("Appended"))
        with thread.stream(user("Refused")) as stream:
            for event in stream:
                if event.type == "message_delta":
                    break
        after_the_refusal = (thread.messages, thread.previous_message_id)
        thread.send(user("Rephrased"))

        created = request_bodies(respx_mock)[2]
        assert after_the_refusal == ((*messages_before, user("Appended")), None)
        assert (created["thread"], created["system"]) == (CREATE, "You are terse.")
        assert created["messages"] == [user("Hello"), assistant(), user("Appended"), user("Rephrased")]

    def test_a_refused_reply_reaches_the_caller_as_it_came(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", "I can't help with that.", stop_reason="refusal"),
            stream_response("msg_b", "I can't help with that.", stop_reason="refusal"),
        )
        thread = make_thread()

        sent = thread.send(user("Refused"))
        with thread.stream(user("Refused")) as stream:
            events = [event.type for event in stream]
            streamed = stream.get_final_message()

        for reply, id in ((sent, "msg_a"), (streamed, "msg_b")):
            assert (reply.id, reply.stop_reason) == (id, "refusal")
            assert [block.text for block in reply.content if block.type == "text"] == ["I can't help with that."]
        assert events[-1] == "message_stop"

    def test_a_refused_first_turn_keeps_the_seed_and_nothing_the_turn_was_given(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a", stop_reason="refusal"), message_response("msg_b"))
        thread = make_thread(messages=[user("Seed"), assistant("Seeded")])

        thread.send(user("Refused"), system="Be brief.", tools=[NOOP_TOOL])
        thread.send(user("Rephrased"))

        created = request_bodies(respx_mock)[1]
        assert created["thread"] == CREATE
        assert created["messages"] == [user("Seed"), assistant("Seeded"), user("Rephrased")]
        assert "system" not in created and "tools" not in created

    def test_messages_appended_before_a_refused_turn_stay_staged(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            message_response("msg_b", stop_reason="refusal"),
            message_response("msg_c"),
        )
        thread = make_thread()
        thread.send(user("Hello"))

        thread.append(user("Appended"))
        thread.send(user("Refused"))
        thread.send(user("Rephrased"))

        created = request_bodies(respx_mock)[2]
        assert created["thread"] == CREATE
        assert created["messages"] == [user("Hello"), assistant(), user("Appended"), user("Rephrased")]

    def test_a_refused_turn_is_not_recorded_once_unthreaded_either(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            unsupported_response("fallbacks"),
            message_response("msg_a"),
            message_response("msg_b", stop_reason="refusal"),
            message_response("msg_c"),
        )
        thread = make_thread(unsupported_request_behavior="continue_unthreaded")
        thread.send(user("Hello"))

        thread.send(user("Refused"))
        thread.send(user("Rephrased"))

        assert request_threads(respx_mock) == [CREATE, None, None, None]
        assert request_bodies(respx_mock)[3]["messages"] == [user("Hello"), assistant(), user("Rephrased")]

    def test_a_replay_drops_the_cache_markers_of_the_recorded_messages(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            *(message_response(f"msg_{turn}") for turn in range(5)),
            THREAD_NOT_FOUND,
            message_response("msg_5"),
        )
        given = [marked(f"Turn {turn}") for turn in range(6)]
        thread = make_thread()
        for message in given[:5]:
            thread.send(message)

        thread.send(given[5])

        *sent_first, rejected, replayed = request_bodies(respx_mock)
        assert [body["messages"] for body in (*sent_first, rejected)] == [[marked(f"Turn {turn}")] for turn in range(6)]
        assert replayed["thread"] == CREATE
        assert replayed["messages"] == [
            *(message for turn in range(5) for message in (unmarked(f"Turn {turn}"), assistant())),
            marked("Turn 5"),
        ]
        assert given == [marked(f"Turn {turn}") for turn in range(6)]
        assert [message for message in thread.messages if message["role"] == "user"] == given
        assert [message for message in thread.params["messages"] if message["role"] == "user"] == given

    def test_the_first_turn_sends_the_cache_markers_of_the_seed_as_given(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"))
        thread = make_thread(messages=[marked("Seed"), assistant("Seeded")])
        thread.append(marked("Appended"))

        thread.send(marked("Hello"))

        assert request_bodies(respx_mock)[0]["messages"] == [
            marked("Seed"),
            assistant("Seeded"),
            marked("Appended"),
            marked("Hello"),
        ]

    @pytest.mark.parametrize("new_messages", [[], [marked("Once more")]], ids=["sent_again", "with_a_new_message"])
    def test_a_turn_that_no_reply_answered_keeps_its_cache_markers(
        self, respx_mock: MockRouter, new_messages: list[BetaMessageParam]
    ) -> None:
        queue_responses(
            respx_mock, message_response("msg_a"), interrupted_stream_response("msg_b", ""), message_response("msg_c")
        )
        thread = make_thread()
        thread.send(marked("Hello"))
        with thread.stream(marked_twice("Again")) as stream:
            stream.until_done()

        thread.send(*new_messages)

        created = request_bodies(respx_mock)[2]
        assert created["thread"] == CREATE
        assert created["messages"] == [unmarked("Hello"), assistant(), marked_twice("Again"), *new_messages]

    def test_a_replay_drops_nested_cache_markers_and_leaves_free_form_data_alone(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), THREAD_NOT_FOUND, message_response("msg_c"))
        marker = {"cache_control": {"type": "ephemeral"}}
        given = history_with_nested_blocks(marker)
        thread = make_thread(messages=given, betas=[INLINE_TOOLS_BETA])
        thread.send()

        thread.send(user("Again"))

        created, _, replayed = request_bodies(respx_mock)
        assert created["messages"] == history_with_nested_blocks(marker)
        assert replayed["messages"] == [*history_with_nested_blocks({}), assistant(), user("Again")]
        assert given == history_with_nested_blocks(marker)
        assert list(thread.messages[: len(given)]) == given

    def test_a_replay_keeps_the_cache_markers_outside_the_messages(self, respx_mock: MockRouter) -> None:
        marker = {"type": "ephemeral"}
        fields: dict[str, Any] = {
            "system": [{"type": "text", "text": "You are terse.", "cache_control": marker}],
            "tools": [{**NOOP_TOOL, "cache_control": marker}],
            "cache_control": marker,
        }
        queue_responses(respx_mock, message_response("msg_a"), THREAD_NOT_FOUND, message_response("msg_c"))
        thread = make_thread(**fields)
        thread.send(user("Hello"))

        thread.send(user("Again"))

        replayed = request_bodies(respx_mock)[2]
        assert {field: replayed[field] for field in fields} == fields

    def test_every_turn_drops_the_cache_markers_of_the_recorded_messages_once_unthreaded(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            unsupported_response("fallbacks"),
            message_response("msg_a"),
            message_response("msg_b"),
            message_response("msg_c"),
        )
        thread = make_thread(unsupported_request_behavior="continue_unthreaded")

        for text in ("One", "Two", "Three"):
            thread.send(marked(text))

        assert [body["messages"] for body in request_bodies(respx_mock)[1:]] == [
            [marked("One")],
            [unmarked("One"), assistant(), marked("Two")],
            [unmarked("One"), assistant(), unmarked("Two"), assistant(), marked("Three")],
        ]

    def test_the_first_turn_of_a_fork_drops_the_cache_markers_of_the_recorded_messages(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_thread()
        thread.send(marked("Hello"))
        thread.append(marked("Appended"))

        thread.fork().send(marked("Again"))

        created = request_bodies(respx_mock)[1]
        assert created["thread"] == CREATE
        assert created["messages"] == [unmarked("Hello"), assistant(), marked("Appended"), marked("Again")]

    def test_the_turn_after_a_refused_one_drops_the_cache_markers_of_the_recorded_messages(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            message_response("msg_b", stop_reason="refusal"),
            message_response("msg_c"),
        )
        thread = make_thread()
        thread.send(marked("Hello"))
        thread.send(marked("Refused"))

        thread.send(marked("Rephrased"))

        assert request_bodies(respx_mock)[2]["messages"] == [unmarked("Hello"), assistant(), marked("Rephrased")]

    def test_a_reply_from_a_fallback_model_only_starts_a_new_thread(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            fallback_response("msg_a"),
            fallback_response("msg_b"),
            message_response("msg_c"),
            message_response("msg_d"),
        )
        thread = make_thread(system="You are terse.", fallbacks=FALLBACKS, betas=[FALLBACK_BETA])

        thread.send(user("Hello"))
        params_after_the_reply = thread.params
        thread.send(user("Again"))
        thread.send(user("Once more"))
        thread.send(user("One last time"))

        bodies = request_bodies(respx_mock)
        history = [user("Hello"), fallback_reply(), user("Again")]
        assert (params_after_the_reply["model"], params_after_the_reply.get("fallbacks")) == (MODEL, FALLBACKS)
        assert [(body["model"], body["fallbacks"]) for body in bodies] == [(MODEL, FALLBACKS)] * 4
        assert [body["thread"] for body in bodies] == [CREATE, CREATE, CREATE, continue_from("msg_c")]
        assert [body.get("system") for body in bodies] == ["You are terse."] * 3 + [None]
        assert [body["messages"] for body in bodies[1:]] == [
            history,
            [*history, fallback_reply(), user("Once more")],
            [user("One last time")],
        ]
        assert request_betas(respx_mock) == [[FALLBACK_BETA, THREADS_BETA]] * 4

    @ANSWERED_TURN_METHODS
    def test_a_reply_from_a_fallback_model_on_a_continue_starts_a_new_thread(
        self, respx_mock: MockRouter, method: str
    ) -> None:
        respond = stream_response if method == "stream" else message_response
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            respond("msg_b", "Hi!", iterations=FALLBACK_ITERATIONS),
            message_response("msg_c"),
        )
        thread = make_thread(fallbacks="default", betas=[FALLBACK_BETA])
        thread.send(user("Hello"))

        run_turn(thread, method, user("Again"))
        thread.send(user("Once more"))

        continued, created = request_bodies(respx_mock)[1:]
        assert (continued["thread"], continued["model"], continued["fallbacks"]) == (
            continue_from("msg_a"),
            MODEL,
            "default",
        )
        assert (created["thread"], created["model"], created["fallbacks"]) == (CREATE, MODEL, "default")
        assert created["messages"] == [user("Hello"), assistant(), user("Again"), assistant(), user("Once more")]

    def test_a_thread_started_after_a_reply_from_a_fallback_model_replaces_no_lost_thread(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            fallback_response("msg_a"),
            message_response("msg_b"),
            THREAD_NOT_FOUND,
            message_response("msg_d"),
        )
        thread = make_thread(
            fallbacks=FALLBACKS, betas=[FALLBACK_BETA], unsupported_request_behavior="continue_unthreaded"
        )

        for text in ("Hello", "Again", "Once more"):
            thread.send(user(text))

        assert request_threads(respx_mock) == [CREATE, CREATE, continue_from("msg_b"), CREATE]

    def test_a_refused_reply_from_a_fallback_model_is_not_recorded(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", stop_reason="refusal", iterations=FALLBACK_ITERATIONS),
            message_response("msg_b"),
        )
        thread = make_thread(fallbacks=FALLBACKS, betas=[FALLBACK_BETA])

        thread.send(user("Refused"))
        thread.send(user("Rephrased"))

        created = request_bodies(respx_mock)[1]
        assert (created["thread"], created["model"], created["fallbacks"]) == (CREATE, MODEL, FALLBACKS)
        assert created["messages"] == [user("Rephrased")]

    def test_a_reply_from_the_requested_model_is_continued(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock, message_response("msg_a", iterations=FALLBACK_ITERATIONS[:1]), message_response("msg_b")
        )
        thread = make_thread(fallbacks=FALLBACKS, betas=[FALLBACK_BETA])

        thread.send(user("Hello"))
        thread.send(user("Again"))

        continued = request_bodies(respx_mock)[1]
        assert (continued["thread"], continued["model"], continued["fallbacks"]) == (
            continue_from("msg_a"),
            MODEL,
            FALLBACKS,
        )

    def test_a_reply_from_a_fallback_model_changes_nothing_once_unthreaded(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            unsupported_response("fallbacks"),
            message_response("msg_a", iterations=FALLBACK_ITERATIONS),
            message_response("msg_b"),
        )
        thread = make_thread(
            fallbacks=FALLBACKS, betas=[FALLBACK_BETA], unsupported_request_behavior="continue_unthreaded"
        )

        thread.send(user("Hello"))
        thread.send(user("Again"))

        later = request_bodies(respx_mock)[2]
        assert "thread" not in later
        assert (later["model"], later["fallbacks"], thread.params["model"]) == (MODEL, FALLBACKS, MODEL)

    def test_a_stop_reason_this_version_does_not_know_is_recorded(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a", stop_reason="something_new"), message_response("msg_b"))
        client = Anthropic(base_url=base_url, api_key="my-anthropic-api-key", max_retries=0)
        thread = client.beta.messages.thread(model=MODEL, max_tokens=MAX_TOKENS)

        thread.send(user("Hello"))
        thread.send(user("Again"))

        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a")]

    @pytest.mark.parametrize(
        ("fields", "expected"),
        [
            ({}, "container_a"),
            ({"container": {"skills": [XLSX_SKILL]}}, {"skills": [XLSX_SKILL], "id": "container_a"}),
            ({"container": "container_mine"}, "container_mine"),
        ],
        ids=["no_container", "container_skills_without_an_id", "caller_container_id"],
    )
    def test_later_turns_run_in_the_container_of_the_last_reply(
        self, respx_mock: MockRouter, fields: dict[str, Any], expected: Any
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a", container="container_a"), message_response("msg_b"))
        thread = make_thread(**fields)

        thread.send(user("Hello"))
        thread.send(user("Again"))

        assert request_bodies(respx_mock)[1]["container"] == expected

    def test_update_changes_the_fields_of_later_turns_without_a_request(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_thread()
        thread.send(user("Hello"))

        thread.update(max_tokens=77, stop_sequences=["END"])
        requests_after_update = respx_mock.calls.call_count
        thread.send(user("Again"))

        body = request_bodies(respx_mock)[1]
        assert requests_after_update == 1
        assert (body["max_tokens"], body["stop_sequences"]) == (77, ["END"])
        assert (body["thread"], body["messages"]) == (continue_from("msg_a"), [user("Again")])

    def test_send_overrides_take_precedence_over_update(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_thread()
        thread.update(max_tokens=77)

        thread.send(user("Hello"), max_tokens=12)
        thread.send(user("Again"))

        overridden, later = request_bodies(respx_mock)
        assert (overridden["max_tokens"], later["max_tokens"]) == (12, 77)

    def test_update_request_options_apply_to_later_turns(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_thread()
        thread.send(user("Hello"))

        thread.update(extra_body={"top_k": 5}, extra_headers={"X-Trace": "abc"})
        thread.send(user("Again"))

        before, after = request_bodies(respx_mock)
        assert "top_k" not in before
        assert after["top_k"] == 5
        assert sent_requests(respx_mock)[1].headers["X-Trace"] == "abc"

    def test_update_replaces_each_request_option_it_is_given_as_a_whole(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"))
        thread = make_thread(
            extra_headers={"X-Thread": "thread"}, extra_query={"thread": "1"}, extra_body={"top_k": 5}, timeout=12
        )

        thread.update(extra_headers={"X-Update": "update"}, extra_query={"update": "1"})
        thread.send(user("Hello"))

        request = sent_requests(respx_mock)[0]
        assert (request.headers.get("X-Thread"), request.headers.get("X-Update")) == (None, "update")
        assert (request.url.params.get("thread"), request.url.params.get("update")) == (None, "1")
        assert (request_bodies(respx_mock)[0]["top_k"], request.extensions["timeout"]["read"]) == (5, 12)

    def test_send_request_options_replace_the_threads_for_that_turn_only(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_thread(extra_headers={"X-Thread": "thread"}, extra_query={"thread": "1"}, extra_body={"top_k": 5})

        thread.send(user("Hello"), extra_headers={"X-Turn": "turn"}, extra_query={"turn": "1"})
        thread.send(user("Again"))

        requests = sent_requests(respx_mock)
        assert [(r.headers.get("X-Thread"), r.headers.get("X-Turn")) for r in requests] == [
            (None, "turn"),
            ("thread", None),
        ]
        assert [(r.url.params.get("thread"), r.url.params.get("turn")) for r in requests] == [(None, "1"), ("1", None)]
        assert [body["top_k"] for body in request_bodies(respx_mock)] == [5, 5]

    def test_an_empty_request_option_clears_the_threads(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"))
        thread = make_thread(extra_headers={"X-Thread": "thread"}, extra_query={"thread": "1"}, extra_body={"top_k": 5})

        thread.send(user("Hello"), extra_headers={}, extra_query={}, extra_body={})

        request = sent_requests(respx_mock)[0]
        assert "X-Thread" not in request.headers and "thread" not in request.url.params
        assert "top_k" not in request_bodies(respx_mock)[0]

    def test_params_is_the_whole_conversation_as_thread_arguments(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"))
        thread = make_thread(system="Be brief.", betas=["context-management-2025-06-27"])
        thread.send(user("Hello"))
        thread.update(max_tokens=2048)
        thread.append(user("Again"))

        params = thread.params

        assert (params["model"], params["max_tokens"], params.get("system"), params.get("betas")) == (
            MODEL,
            2048,
            "Be brief.",
            ["context-management-2025-06-27"],
        )
        assert roles(params["messages"]) == ["user", "assistant", "user"]
        assert "output_format" not in params and "thread" not in params
        assert thread.params is not params and thread.params["messages"] is not params["messages"]

    def test_a_thread_built_from_params_replays_the_conversation(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        client = make_client()
        thread = client.beta.messages.thread(model=MODEL, max_tokens=1024, system="Be brief.")
        thread.send(user("Hello"))

        params = thread.params
        params["messages"] = params["messages"][:1]
        rewound = client.beta.messages.thread(**params)
        rewound.send()

        body = request_bodies(respx_mock)[1]
        assert (body["thread"], body["system"], body["messages"]) == (CREATE, "Be brief.", [user("Hello")])

    def test_a_thread_built_from_params_keeps_the_unsupported_request_behavior(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            unsupported_response("inference_hooks"),
            message_response("msg_b"),
            unsupported_response("inference_hooks"),
        )
        client = make_client()
        unthreaded = make_thread(unsupported_request_behavior="continue_unthreaded")

        client.beta.messages.thread(**unthreaded.params).send(user("Hello"))
        with pytest.raises(BadRequestError):
            client.beta.messages.thread(**make_thread().params).send(user("Hello"))

        assert request_threads(respx_mock) == [CREATE, None, CREATE]
        assert not any("unsupported_request_behavior" in body for body in request_bodies(respx_mock))

    @pytest.mark.skipif(PYDANTIC_V1, reason="structured outputs not supported with pydantic v1")
    def test_params_includes_the_output_format(self) -> None:
        thread = make_client().beta.messages.thread(model=MODEL, max_tokens=1024, output_format=Forecast)

        assert thread.params.get("output_format") is Forecast

    def test_fork_returns_a_thread_with_no_previous_message_id_without_a_request(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"))
        thread = make_thread()
        thread.send(user("Hello"))

        fork = thread.fork()

        assert isinstance(fork, BetaMessageThread)
        assert fork.previous_message_id is None
        assert fork.messages == thread.messages
        assert respx_mock.calls.call_count == 1

    def test_fork_creates_a_thread_with_the_full_history_and_the_same_fields(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_thread(max_tokens=1024, system="You are terse.", extra_headers={"X-Trace": "abc"})
        thread.send(user("Hello"))

        thread.fork().send(user("Fork"))

        body = request_bodies(respx_mock)[1]
        assert (body["thread"], body["messages"]) == (CREATE, [user("Hello"), assistant(), user("Fork")])
        assert (body["system"], body["max_tokens"]) == ("You are terse.", 1024)
        assert sent_requests(respx_mock)[1].headers["X-Trace"] == "abc"
        assert request_betas(respx_mock)[1] == [THREADS_BETA]

    def test_fork_keeps_the_unsupported_request_behavior(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, unsupported_response("inference_hooks"), message_response("msg_b"))
        thread = make_thread(unsupported_request_behavior="continue_unthreaded")

        fork = thread.fork()
        fork.send(user("Hello"))

        assert request_threads(respx_mock) == [CREATE, None]
        assert fork.previous_message_id is None

    def test_fork_and_original_continue_independently(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"), message_response("msg_c"))
        thread = make_thread()
        thread.send(user("Hello"))
        fork = thread.fork()

        fork.send(user("Fork"))
        thread.send(user("Original"))

        body = request_bodies(respx_mock)[2]
        assert (body["thread"], body["messages"]) == (continue_from("msg_a"), [user("Original")])
        assert (thread.previous_message_id, fork.previous_message_id) == ("msg_c", "msg_b")
        assert (thread.messages[2], fork.messages[2]) == (user("Original"), user("Fork"))
        assert roles(thread.messages) == roles(fork.messages) == ["user", "assistant", "user", "assistant"]

    @pytest.mark.parametrize(
        "method",
        [
            "send",
            pytest.param("parse", marks=pytest.mark.skipif(PYDANTIC_V1, reason="parse() is pydantic-v2 only")),
            "stream",
        ],
    )
    @pytest.mark.parametrize("forks", [1, 2], ids=["fork", "fork_of_a_fork"])
    def test_fork_of_a_thread_that_ends_in_a_partial_reply_sends_the_turn_again_without_it(
        self, respx_mock: MockRouter, forks: int, method: str
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            stream_response("msg_b", "one two three"),
            stream_response("msg_c") if method == "stream" else message_response("msg_c"),
            message_response("msg_d"),
        )
        thread = make_thread()
        thread.send(user("Hello"))
        with thread.stream(user("Count")) as stream:
            next(stream.text_stream)
        messages_after_the_stream = thread.messages

        fork = thread
        for _ in range(forks):
            fork = fork.fork()
        messages_of_the_fork = fork.messages
        run_turn(fork, method)
        messages_after_the_turn_of_the_fork = thread.messages
        thread.send()

        forked, original = request_bodies(respx_mock)[2:]
        assert (forked["thread"], forked["messages"]) == (CREATE, [user("Hello"), assistant("Hi!"), user("Count")])
        assert (original["thread"], original["messages"]) == (forked["thread"], forked["messages"])
        assert messages_of_the_fork == messages_after_the_turn_of_the_fork == messages_after_the_stream
        assert (roles(fork.messages), fork.previous_message_id) == (["user", "assistant", "user", "assistant"], "msg_c")

    def test_fork_of_a_thread_that_ends_in_a_partial_reply_sends_it_ahead_of_a_new_message(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(respx_mock, stream_response("msg_a", "one two three"), message_response("msg_b"))
        thread = make_thread()
        with thread.stream(user("Count")) as stream:
            next(stream.text_stream)

        thread.fork().send(user("Just the total"))

        body = request_bodies(respx_mock)[1]
        assert (body["thread"], body["messages"]) == (CREATE, [user("Count"), assistant("one"), user("Just the total")])

    def test_fork_of_a_thread_that_ends_in_a_whole_reply_sends_the_full_history_with_no_new_message(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_thread()
        thread.send(user("Hello"))

        thread.fork().send()

        body = request_bodies(respx_mock)[1]
        assert (body["thread"], body["messages"]) == (CREATE, [user("Hello"), assistant()])

    @pytest.mark.parametrize(
        "fields",
        [
            pytest.param(
                {"output_format": Forecast},
                marks=pytest.mark.skipif(PYDANTIC_V1, reason="structured outputs not supported with pydantic v1"),
            ),
            {"output_config": {"format": {"type": "json_schema", "schema": {"type": "object"}}}},
        ],
        ids=["output_format", "output_config_format"],
    )
    def test_output_format_adds_no_beta_beyond_the_threads_beta(
        self, respx_mock: MockRouter, fields: dict[str, Any]
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"))
        thread = make_thread(**fields)

        thread.send(user("Hello"))

        assert request_betas(respx_mock) == [[THREADS_BETA]]

    @pytest.mark.parametrize(
        "fields",
        [
            pytest.param(
                {"output_format": Forecast, "output_config": {"effort": "low"}},
                marks=pytest.mark.skipif(PYDANTIC_V1, reason="structured outputs not supported with pydantic v1"),
            ),
            {"output_config": {"format": {"type": "json_schema", "schema": {"type": "object"}}}},
        ],
        ids=["output_format", "output_config_format"],
    )
    def test_every_turn_and_a_thread_built_from_params_send_the_output_config_given_at_creation(
        self, respx_mock: MockRouter, fields: dict[str, Any]
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"), message_response("msg_c"))
        thread = make_thread(**fields)

        thread.send(user("Hello"))
        thread.send(user("Again"))
        make_client().beta.messages.thread(**thread.params).send(user("Once more"))

        created, continued, rebuilt = request_bodies(respx_mock)
        assert created["output_config"]["format"]["type"] == "json_schema"
        assert created["output_config"] == continued["output_config"] == rebuilt["output_config"]

    @pytest.mark.skipif(PYDANTIC_V1, reason="structured outputs not supported with pydantic v1")
    def test_thread_rejects_both_output_format_and_output_config_format(self) -> None:
        with pytest.raises(AnthropicError, match="output_config.format"):
            make_thread(
                output_format=Forecast, output_config={"format": {"type": "json_schema", "schema": {"type": "object"}}}
            )

    def test_output_format_rejects_a_schema_dict(self) -> None:
        schema = {"type": "json_schema", "schema": {"type": "object"}}

        with pytest.raises(TypeError, match="output_config"):
            make_thread(output_format=schema)

    @pytest.mark.skipif(PYDANTIC_V1, reason="structured outputs not supported with pydantic v1")
    def test_parse_continues_the_thread_and_parses_each_reply(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", json.dumps({"forecast": "Sunny"})),
            message_response("msg_b", json.dumps({"forecast": "Rain"})),
        )
        thread = make_thread(output_format=Forecast)

        first = thread.parse(user("Today?"))
        second = thread.parse(user("Tomorrow?"), max_tokens=12)

        created, continued = request_bodies(respx_mock)
        assert (first.parsed_output, second.parsed_output) == (Forecast(forecast="Sunny"), Forecast(forecast="Rain"))
        assert created["thread"] == CREATE
        assert created["output_config"]["format"]["type"] == "json_schema"
        assert continued["thread"] == continue_from("msg_a")
        assert (continued["messages"], continued["max_tokens"]) == ([user("Tomorrow?")], 12)
        assert thread.previous_message_id == second.id
        assert roles(thread.messages) == ["user", "assistant", "user", "assistant"]

    @pytest.mark.skipif(PYDANTIC_V1, reason="parse() response post-parser is pydantic-v2 only")
    def test_parse_without_output_format_returns_no_parsed_output(self, respx_mock: MockRouter) -> None:
        text = json.dumps({"forecast": "Sunny"})
        queue_responses(respx_mock, message_response("msg_a", text))
        thread = make_thread()

        message = thread.parse(user("Today?"))

        assert message.parsed_output is None
        assert message.content[0].type == "text"
        assert message.content[0].text == text
        assert "output_config" not in request_bodies(respx_mock)[0]
        assert thread.previous_message_id == "msg_a"

    @pytest.mark.skipif(PYDANTIC_V1, reason="parse() response post-parser is pydantic-v2 only")
    def test_parsed_reply_has_the_request_and_workspace_ids_of_its_response(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", headers=id_headers("req_a", "wrkspc_a")),
            message_response("msg_b", headers=id_headers("req_b", "wrkspc_b")),
            message_response("msg_c"),
        )
        thread = make_thread()

        sent = thread.send(user("One"))
        parsed = thread.parse(user("Two"))
        parsed_without_ids = thread.parse(user("Three"))

        assert response_ids(sent, parsed, parsed_without_ids) == [
            ("req_a", "wrkspc_a"),
            ("req_b", "wrkspc_b"),
            (None, None),
        ]
        assert not parsed.to_dict().keys() & {"_request_id", "_workspace_id"}

    @pytest.mark.skipif(PYDANTIC_V1, reason="structured outputs not supported with pydantic v1")
    def test_parse_of_a_reply_that_does_not_fit_the_output_format_keeps_the_turn(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a", "Sunny"))
        thread = make_thread(output_format=Forecast)

        with pytest.raises(pydantic.ValidationError):
            thread.parse(user("Today?"))

        assert (roles(thread.messages), thread.previous_message_id) == (["user", "assistant"], "msg_a")

    def test_send_while_streaming_raises_and_stages_nothing(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, stream_response("msg_a"), message_response("msg_b"))
        thread = make_thread()

        with thread.stream(user("Hello")) as stream:
            with pytest.raises(AnthropicError, match="already in progress"):
                thread.send(user("Interrupting"))
            stream.until_done()
        thread.send(user("Now"))

        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a")]
        assert request_bodies(respx_mock)[1]["messages"] == [user("Now")]
        assert thread.previous_message_id == "msg_b"

    def test_failed_send_lets_the_next_send_run(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, server_error(), message_response("msg_b"))
        thread = make_thread()
        with pytest.raises(InternalServerError):
            thread.send(user("Hello"))

        reply = thread.send(user("Hello"))

        assert reply.id == "msg_b"

    def test_stream_records_the_reply_once_it_reaches_message_stop(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, stream_response("msg_a"))
        thread = make_thread()

        with thread.stream(user("Hello")) as stream:
            stream.until_done()

        body = request_bodies(respx_mock)[0]
        assert (body["stream"], body["thread"]) == (True, CREATE)
        assert stream.get_final_message().id == thread.previous_message_id == "msg_a"
        assert roles(thread.messages) == ["user", "assistant"]

    def test_stream_that_finds_the_thread_gone_replays_inside_the_same_stream(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), THREAD_NOT_FOUND, stream_response("msg_c", "one two"))
        thread = make_thread()
        thread.send(user("Hello"))

        with thread.stream(user("Count")) as stream:
            text = "".join(stream.text_stream)

        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a"), CREATE]
        assert text == "one two"
        assert stream.get_final_message().id == thread.previous_message_id == "msg_c"

    def test_stream_error_takes_the_turn_back(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), server_error())
        thread = make_thread()
        thread.send(user("Hello"))

        with pytest.raises(InternalServerError):
            with thread.stream(user("Count")) as stream:
                stream.until_done()

        assert thread.previous_message_id == "msg_a"
        assert roles(thread.messages) == ["user", "assistant"]

    @pytest.mark.parametrize("how", ["leave", "close", "error_event"])
    def test_a_stream_that_ends_before_message_start_takes_the_turn_back(
        self, respx_mock: MockRouter, how: str
    ) -> None:
        streamed = stream_error_response() if how == "error_event" else stream_response("msg_b")
        queue_responses(respx_mock, message_response("msg_a"), streamed, message_response("msg_c"))
        thread = make_thread()
        thread.send(user("Hello"))

        with pytest.raises(APIError) if how == "error_event" else nullcontext():
            with thread.stream(user("Count")) as stream:
                if how == "close":
                    stream.close()
                elif how == "error_event":
                    stream.until_done()
        thread.send(user("Count"))

        retried = request_bodies(respx_mock)[2]
        assert (retried["thread"], retried["messages"]) == (continue_from("msg_a"), [user("Count")])

    def test_a_stream_that_is_never_entered_stages_nothing(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"))
        thread = make_thread()

        thread.stream(user("Never sent"))
        thread.send(user("Hello"))

        assert request_bodies(respx_mock)[0]["messages"] == [user("Hello")]

    def test_messages_appended_during_a_turn_are_staged_once_it_finishes(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, stream_response("msg_a"), message_response("msg_b"))
        thread = make_thread()

        with thread.stream(user("Hello")) as stream:
            thread.append(user("While you were out"))
            messages_during_the_turn = thread.messages
            stream.until_done()
        thread.send()

        assert messages_during_the_turn == (user("Hello"), user("While you were out"))
        assert request_bodies(respx_mock)[1]["messages"] == [user("While you were out")]
        assert roles(thread.messages) == ["user", "assistant", "user", "assistant"]

    @pytest.mark.parametrize("how", ["break", "close"])
    def test_a_stream_that_ends_early_records_the_partial_reply_and_starts_a_new_thread(
        self, respx_mock: MockRouter, how: str, caplog: pytest.LogCaptureFixture
    ) -> None:
        queue_responses(
            respx_mock, message_response("msg_a"), stream_response("msg_b", "one two three"), message_response("msg_c")
        )
        thread = make_thread()
        thread.send(user("Hello"))

        with caplog.at_level(logging.INFO, logger=THREADS_LOGGER):
            with thread.stream(user("Count")) as stream:
                next(stream.text_stream)
                if how == "close":
                    stream.close()
        previous_message_id_after_stream = thread.previous_message_id
        history_after_stream = list(thread.messages)
        thread.send(user("Just the total"))

        later = request_bodies(respx_mock)[2]
        assert previous_message_id_after_stream is None
        assert roles(history_after_stream) == ["user", "assistant", "user", "assistant"]
        assert history_after_stream[-1]["content"][0].text == "one"  # type: ignore
        assert (
            logging.INFO,
            "Replaying the full message history under a new thread: "
            "reason=stream_ended_before_message_stop previous_message_id=msg_a",
        ) in thread_logs(caplog)
        assert (later["thread"], roles(later["messages"])) == (
            CREATE,
            ["user", "assistant", "user", "assistant", "user"],
        )
        assert later["messages"][3] == assistant("one")
        assert thread.previous_message_id == "msg_c"

    def test_an_exception_inside_the_stream_block_records_the_partial_reply(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), stream_response("msg_b", "one two"))
        thread = make_thread()
        thread.send(user("Hello"))

        with pytest.raises(KeyError):
            with thread.stream(user("Count")) as stream:
                next(stream.text_stream)
                raise KeyError("boom")

        assert (roles(thread.messages), thread.previous_message_id) == (
            ["user", "assistant", "user", "assistant"],
            None,
        )

    def test_send_with_no_messages_after_a_partial_reply_sends_the_turn_again_without_it(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock, message_response("msg_a"), stream_response("msg_b", "one two three"), message_response("msg_c")
        )
        thread = make_thread()
        thread.send(user("Hello"))
        with thread.stream(user("Count")) as stream:
            next(stream.text_stream)

        reply = thread.send()

        retried = request_bodies(respx_mock)[2]
        assert (retried["thread"], retried["messages"]) == (CREATE, [user("Hello"), assistant("Hi!"), user("Count")])
        assert roles(thread.messages) == ["user", "assistant", "user", "assistant"]
        assert thread.previous_message_id == reply.id == "msg_c"

    def test_send_with_no_messages_still_sends_a_partial_turn_again_after_a_call_that_failed(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            stream_response("msg_b", "one two three"),
            server_error(),
            message_response("msg_d"),
        )
        thread = make_thread()
        thread.send(user("Hello"))
        with thread.stream(user("Count")) as stream:
            next(stream.text_stream)
        messages_after_the_stream = thread.messages

        with pytest.raises(InternalServerError):
            thread.send(user("Just the total"))
        messages_after_the_error = thread.messages
        thread.send()

        retried = request_bodies(respx_mock)[3]
        assert (retried["thread"], retried["messages"]) == (CREATE, [user("Hello"), assistant("Hi!"), user("Count")])
        assert messages_after_the_error == messages_after_the_stream

    def test_a_stream_that_ends_after_message_delta_is_still_a_partial_turn(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            stream_response("msg_b", tool_use_id="toolu_b", message_stop=False),
            message_response("msg_c"),
        )
        thread = make_thread()
        thread.send(user("Hello"))
        with thread.stream(user("Weather?")) as stream:
            stream.until_done()
        after_stream = (roles(thread.messages), thread.previous_message_id)

        thread.send()

        retried = request_bodies(respx_mock)[2]
        assert after_stream == (["user", "assistant", "user", "assistant"], None)
        assert (retried["thread"], retried["messages"]) == (CREATE, [user("Hello"), assistant("Hi!"), user("Weather?")])
        assert thread.previous_message_id == "msg_c"

    def test_resume_stream_that_ends_mid_text_keeps_the_paused_reply_resumable(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", "Searching", stop_reason="pause_turn"),
            stream_response("msg_b", "found it"),
            message_response("msg_c"),
        )
        thread = make_thread()
        thread.send(user("Hello"))
        with thread.stream() as stream:
            next(stream.text_stream)

        thread.send()

        retried = request_bodies(respx_mock)[2]
        assert (retried["thread"], retried["messages"]) == (CREATE, [user("Hello"), assistant("Searching")])
        assert thread.previous_message_id == "msg_c"

    def test_a_partial_reply_keeps_finished_blocks_and_drops_an_unfinished_tool_call(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            partial_tool_use_stream_response("msg_b", "Let me check.", tool_use_id="toolu_b"),
        )
        thread = make_thread()
        thread.send(user("Hello"))

        with thread.stream(user("What's the weather in SF?")) as stream:
            for event in stream:
                if event.type == "content_block_delta" and event.delta.type == "input_json_delta":
                    break

        assert [block.type for block in thread.messages[-1]["content"]] == ["text"]  # type: ignore
        assert thread.messages[-1]["content"][0].text == "Let me check."  # type: ignore
        assert thread.previous_message_id is None

    @pytest.mark.parametrize("error", [httpx2.ReadError, None], ids=["events_fail", "events_run_out"])
    def test_a_stream_whose_events_fail_or_run_out_early_frees_the_thread_at_once(
        self, respx_mock: MockRouter, error: type[httpx2.TransportError] | None
    ) -> None:
        queue_responses(
            respx_mock,
            interrupted_stream_response("msg_a", "one", error=error),
            message_response("msg_b"),
        )
        thread = make_thread()

        with thread.stream(user("Count")) as stream:
            with pytest.raises(error) if error else nullcontext():
                stream.until_done()
            thread.send(user("Just the total"))

        later = request_bodies(respx_mock)[1]
        assert (later["thread"], later["messages"]) == (
            CREATE,
            [user("Count"), assistant("one"), user("Just the total")],
        )
        assert roles(thread.messages) == ["user", "assistant", "user", "assistant"]
        assert thread.previous_message_id == "msg_b"

    def test_a_stream_read_to_message_stop_frees_the_thread_at_once(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, stream_response("msg_a"), message_response("msg_b"))
        thread = make_thread()

        with thread.stream(user("Hello")) as stream:
            stream.until_done()
            previous_message_id_inside_the_block = thread.previous_message_id
            thread.send(user("Again"))

        assert previous_message_id_inside_the_block == "msg_a"
        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a")]
        assert request_bodies(respx_mock)[1]["messages"] == [user("Again")]
        assert thread.previous_message_id == "msg_b"

    @pytest.mark.parametrize("first_block", ["reads_to_message_stop", "leaves_early", "reads_nothing"])
    def test_a_stream_manager_entered_again_streams_another_turn_and_frees_the_thread(
        self, respx_mock: MockRouter, first_block: str
    ) -> None:
        queue_responses(respx_mock, stream_response("msg_a"), stream_response("msg_b"), message_response("msg_c"))
        thread = make_thread()
        manager = thread.stream(user("Hello"))

        with manager as stream:
            if first_block == "reads_to_message_stop":
                stream.until_done()
            elif first_block == "leaves_early":
                next(stream.text_stream)
        with manager as stream:
            gc.collect()  # The first stream is out of reach by now, so this finalizes what is left of it.
            stream.until_done()
        previous_message_id_after_the_second_block = thread.previous_message_id
        thread.send(user("Again"))

        later = request_bodies(respx_mock)[2]
        assert previous_message_id_after_the_second_block == "msg_b"
        assert (later["thread"], later["messages"]) == (continue_from("msg_b"), [user("Again")])

    def test_a_stream_that_ends_before_any_content_stores_the_turn_and_send_repeats_it(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock, message_response("msg_a"), stream_response("msg_b", "one two"), message_response("msg_c")
        )
        thread = make_thread()
        thread.send(user("Hello"))

        with thread.stream(user("Count")) as stream:
            assert next(iter(stream)).type == "message_start"
        after_stream = (roles(thread.messages), thread.previous_message_id)
        thread.send()

        retried = request_bodies(respx_mock)[2]
        assert after_stream == (["user", "assistant", "user"], None)
        assert (retried["thread"], retried["messages"]) == (CREATE, [user("Hello"), assistant("Hi!"), user("Count")])

    @CLIENT_KINDS
    def test_the_constructor_takes_the_arguments_of_thread(
        self, make_client: Callable[[], Anthropic | AsyncAnthropic]
    ) -> None:
        client = make_client()
        thread = inspect.signature(client.beta.messages.thread).parameters

        thread_class = BetaMessageThread if isinstance(client, Anthropic) else BetaAsyncMessageThread
        constructor = inspect.signature(thread_class.__init__).parameters
        assert [*constructor][2:] == [*thread] and constructor["client"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
        assert_signatures_in_sync(client.beta.messages.thread, thread_class.__init__, exclude_params={"client"})

    @CLIENT_KINDS
    @pytest.mark.parametrize("method", ["send", "parse", "stream", "update", "tool_runner"])
    def test_a_thread_value_from_the_caller_is_refused(
        self, make_client: Callable[[], Anthropic | AsyncAnthropic], method: str
    ) -> None:
        client: Any = make_client()
        thread = client.beta.messages.thread(model=MODEL, max_tokens=MAX_TOKENS)

        with pytest.raises(TypeError, match="unexpected keyword argument 'thread'"):
            finish(getattr(thread, method)(thread=CREATE))
        with pytest.raises(TypeError, match="unexpected keyword argument 'thread'"):
            client.beta.messages.thread(**thread.params, thread=CREATE)

    @CLIENT_KINDS
    @pytest.mark.parametrize("method", ["send", "parse", "stream", "update"])
    @pytest.mark.parametrize("field", ["output_config", "output_format"])
    def test_the_output_format_is_given_only_when_the_thread_is_created(
        self, make_client: Callable[[], Anthropic | AsyncAnthropic], method: str, field: str
    ) -> None:
        thread = make_client().beta.messages.thread(model=MODEL, max_tokens=MAX_TOKENS)

        with pytest.raises(TypeError, match=f"unexpected keyword argument '{field}'"):
            finish(getattr(thread, method)(**{field: None}))

    @CLIENT_KINDS
    @pytest.mark.parametrize("field", ["max_tokens", "model"])
    def test_thread_requires_the_fields_create_requires(
        self, make_client: Callable[[], Anthropic | AsyncAnthropic], field: str
    ) -> None:
        client: Any = make_client()
        fields = {"max_tokens": MAX_TOKENS, "model": MODEL}
        del fields[field]

        with pytest.raises(TypeError, match=f"missing 1 required keyword-only argument: '{field}'"):
            client.beta.messages.thread(**fields)

    def test_a_field_given_as_omit_is_left_out(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"))
        thread = make_client().beta.messages.thread(
            model=MODEL, max_tokens=MAX_TOKENS, system=omit, metadata={"user_id": "thread"}
        )
        stop_sequences: list[str] = []

        thread.send(user("Hello"), metadata=omit, stop_sequences=stop_sequences if stop_sequences else omit)

        body = request_bodies(respx_mock)[0]
        assert "system" not in body and "stop_sequences" not in body
        assert body["metadata"] == {"user_id": "thread"}

    def test_constructor_starts_the_same_thread_as_the_factory(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = BetaMessageThread(
            make_client(), model=MODEL, max_tokens=64, system="Be brief.", messages=[user("Hello")]
        )

        thread.send()
        thread.send(user("Again"))

        first, second = request_bodies(respx_mock)
        assert (first["thread"], first["system"], first["messages"]) == (CREATE, "Be brief.", [user("Hello")])
        assert (second["thread"], second["messages"]) == (continue_from("msg_a"), [user("Again")])

    def test_thread_without_messages_starts_empty(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"))
        thread = make_thread()

        thread.send(user("Hello"))

        assert thread.messages[0] == user("Hello")
        assert request_bodies(respx_mock)[0]["messages"] == [user("Hello")]

    @CLIENT_KINDS
    def test_send_parse_and_stream_take_the_arguments_of_update(
        self, make_client: Callable[[], Anthropic | AsyncAnthropic]
    ) -> None:
        client = make_client()
        thread = client.beta.messages.thread(model=MODEL, max_tokens=MAX_TOKENS)

        assert_signatures_in_sync(thread.send, thread.parse)
        assert_signatures_in_sync(thread.send, thread.stream)
        assert list(inspect.signature(thread.send).parameters) == [
            "messages",
            *inspect.signature(thread.update).parameters,
        ]

    def test_thread_params_types_hold_the_fields_of_create(self) -> None:
        create_types = get_type_hints(MessageCreateParamsBase, include_extras=True)
        arguments_of_their_own = {"messages", "thread", "tools"}
        given_at_creation_only = {"output_config"}
        out_of_date = (
            "`MessageCreateParamsBase` changed: make the same change in `src/anthropic/types/beta/thread_create_params.py` "
            "and `src/anthropic/types/beta/thread_send_params.py`, which are copies of it"
        )

        unchanged_types = {field: create_types[field] for field in create_types.keys() - arguments_of_their_own}
        required = {field for field, hint in unchanged_types.items() if is_required_type(hint)}
        thread_types = {field: hint for field, hint in unchanged_types.items() if field not in required}
        turn_types = {
            field: get_args(hint)[0] if field in required else hint
            for field, hint in unchanged_types.items()
            if field not in given_at_creation_only
        }
        assert without_omit(get_type_hints(ThreadCreateParams, include_extras=True)) == thread_types, out_of_date
        assert without_omit(get_type_hints(ThreadSendParams, include_extras=True)) == turn_types, out_of_date
        thread = inspect.signature(make_client().beta.messages.thread).parameters
        assert required == {name for name, parameter in thread.items() if parameter.default is parameter.empty} - {
            "params"
        }, "`create()` requires other fields than `thread()` and the thread constructors spell out"

    def test_a_changed_pinned_field_is_sent_on_continue_for_the_server_to_reject(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_thread(tool_choice={"type": "auto"})
        thread.send(user("Hello"))

        thread.send(user("Again"), tool_choice={"type": "none"})

        body = request_bodies(respx_mock)[1]
        assert (body["thread"], body["tool_choice"]) == (continue_from("msg_a"), {"type": "none"})

    @pytest.mark.parametrize(
        "change",
        [{"system": "Be very brief."}, {"tools": [NOOP_TOOL]}],
        ids=["system", "tools"],
    )
    def test_changing_system_or_tools_is_refused_and_a_thread_from_the_params_takes_the_change(
        self, respx_mock: MockRouter, change: dict[str, Any]
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_thread(system="Be brief.")
        thread.send(user("Hello"))

        thread.update(**change)
        with pytest.raises(AnthropicError, match="Cannot change") as refusal:
            thread.send(user("Again"))
        assert ("send `tool_addition` or `tool_removal` blocks" in str(refusal.value)) == ("tools" in change)
        assert str(refusal.value).endswith("blocks in a `system` message.") == ("tools" in change)
        assert respx_mock.calls.call_count == 1
        make_client().beta.messages.thread(**thread.params).send(user("Again"))

        recreated = request_bodies(respx_mock)[1]
        assert recreated["thread"] == CREATE
        assert [m["role"] for m in recreated["messages"]] == ["user", "assistant", "user"]
        assert all(recreated[field] == value for field, value in change.items())

    def test_a_tools_list_edited_in_place_is_sent_on_the_create_and_refused_on_a_continue(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"))
        other_tool: BetaToolParam = {**NOOP_TOOL, "name": "other"}
        tools = [NOOP_TOOL]
        thread = make_thread(tools=tools)

        tools.append(other_tool)
        thread.send(user("Hello"))
        tools.remove(other_tool)
        with pytest.raises(AnthropicError, match="Cannot change `tools`"):
            thread.send(user("Again"))

        assert [body["tools"] for body in request_bodies(respx_mock)] == [[NOOP_TOOL, other_tool]]

    @IN_PLACE_EDITS
    def test_system_or_a_tool_edited_in_place_is_refused_and_a_thread_from_the_params_takes_the_edit(
        self, respx_mock: MockRouter, field: str, edit: InPlaceEdit
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        system: list[BetaTextBlockParam] = [{"type": "text", "text": "Be brief."}]
        tool: BetaToolParam = {**NOOP_TOOL}
        thread = make_thread(system=system, tools=[tool])
        thread.send(user("Hello"))

        edit(system, tool)
        with pytest.raises(AnthropicError, match=f"Cannot change `{field}` on a thread"):
            thread.send(user("Again"))
        assert respx_mock.calls.call_count == 1
        make_client().beta.messages.thread(**thread.params).send(user("Again"))

        recreated = request_bodies(respx_mock)[1]
        assert (recreated["thread"], roles(recreated["messages"])) == (CREATE, ["user", "assistant", "user"])
        assert (recreated["system"], recreated["tools"]) == (system, [tool])

    def test_an_equal_copy_of_system_and_tools_continues_the_thread(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_thread(system=[{"type": "text", "text": "Be brief."}], tools=[NOOP_TOOL])
        thread.send(user("Hello"))

        thread.send(user("Again"), system=({"type": "text", "text": "Be brief."},), tools=({**NOOP_TOOL},))

        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a")]

    def test_a_tool_removal_appended_by_hand_is_sent_on_the_continue_as_given(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_thread(tools=[NOOP_TOOL], betas=[INLINE_TOOLS_BETA])
        thread.send(user("Hello"))

        thread.append(tool_removal("noop"))
        thread.send(user("Again"))

        continued = request_bodies(respx_mock)[1]
        assert (continued["thread"], continued.get("tools")) == (continue_from("msg_a"), None)
        assert continued["messages"] == [tool_removal("noop"), user("Again")]

    @pytest.mark.parametrize(
        ("override", "kept"),
        [({"system": "Be brief."}, {"system": "Be brief."}), ({"tools": (NOOP_TOOL,)}, {"tools": [NOOP_TOOL]})],
        ids=["system", "tools"],
    )
    @pytest.mark.parametrize(
        "method",
        [
            "send",
            pytest.param("parse", marks=pytest.mark.skipif(PYDANTIC_V1, reason="parse() is pydantic-v2 only")),
            "stream",
        ],
    )
    def test_a_one_turn_system_or_tools_on_the_turn_that_creates_the_thread_stays_with_the_thread(
        self, respx_mock: MockRouter, method: str, override: dict[str, Any], kept: dict[str, Any]
    ) -> None:
        respond = stream_response if method == "stream" else message_response
        queue_responses(respx_mock, respond("msg_a"), message_response("msg_b"))
        thread = make_thread()

        run_turn(thread, method, user("Hello"), **override)
        thread.send(user("Again"))

        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a")]
        assert {**thread.params, **kept} == thread.params

    @ONE_TURN_CREATE_ONLY_FIELDS
    @TURN_METHODS
    def test_a_one_turn_system_or_tools_on_a_first_turn_that_fails_does_not_stay_with_the_thread(
        self, respx_mock: MockRouter, method: str, override: dict[str, Any]
    ) -> None:
        queue_responses(respx_mock, server_error(), message_response("msg_b"))
        thread = make_thread(system="Be kind.")
        params_before = thread.params

        with pytest.raises(InternalServerError):
            run_turn(thread, method, user("Hello"), **override)
        params_after_the_error = thread.params
        thread.send(user("Hello"))

        failed, later = request_bodies(respx_mock)
        assert {**failed, **override} == failed
        assert (later["thread"], later["messages"]) == (CREATE, [user("Hello")])
        assert (later["system"], later.get("tools")) == ("Be kind.", None)
        assert params_after_the_error == params_before

    @ONE_TURN_CREATE_ONLY_FIELDS
    @pytest.mark.parametrize("next_turn", [[], [user("Just the total")]], ids=["same_turn_again", "another_message"])
    def test_a_one_turn_system_or_tools_on_a_first_turn_whose_stream_ends_early_does_not_stay_with_the_thread(
        self, respx_mock: MockRouter, next_turn: list[BetaMessageParam], override: dict[str, Any]
    ) -> None:
        queue_responses(respx_mock, stream_response("msg_a", "one two three"), message_response("msg_b"))
        thread = make_thread(system="Be kind.")

        with thread.stream(user("Count"), **override) as stream:
            next(stream.text_stream)
        thread.send(*next_turn)

        later = request_bodies(respx_mock)[1]
        assert (later["thread"], later["system"], later.get("tools")) == (CREATE, "Be kind.", None)

    @CHANGES_DURING_THE_TURN
    def test_a_change_during_the_turn_that_creates_the_thread_of_what_that_turn_gave_is_refused_on_the_next_turn(
        self, respx_mock: MockRouter, override: dict[str, Any], change: Callable[[BetaMessageThread[Any]], None]
    ) -> None:
        queue_responses(respx_mock, stream_response("msg_a"))
        thread = make_thread()

        with thread.stream(user("Hello"), **override) as stream:
            change(thread)
            stream.until_done()
        with pytest.raises(AnthropicError, match=f"Cannot change `{next(iter(override))}`"):
            thread.send(user("Again"))

        assert (respx_mock.calls.call_count, thread.previous_message_id) == (1, "msg_a")

    @OWN_CREATE_ONLY_FIELDS
    @ONE_TURN_CREATE_ONLY_FIELDS
    @CHANGES_OF_ANOTHER_FIELD_DURING_THE_TURN
    def test_a_change_of_another_field_during_the_turn_that_creates_the_thread_keeps_what_that_turn_gave(
        self,
        respx_mock: MockRouter,
        change: Callable[[BetaMessageThread[Any]], None],
        override: dict[str, Any],
        own: dict[str, Any],
    ) -> None:
        queue_responses(respx_mock, stream_response("msg_a"), message_response("msg_b"))
        thread = make_thread(**own)

        with thread.stream(user("Hello"), **override) as stream:
            change(thread)
            stream.until_done()
        thread.send(user("Again"))

        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a")]
        assert request_bodies(respx_mock)[1]["max_tokens"] == 12
        assert {**thread.params, **override} == thread.params

    def test_a_one_turn_system_on_a_first_turn_that_goes_without_a_thread_is_for_that_turn_only(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock, unsupported_response("inference_hooks"), message_response("msg_b"), message_response("msg_c")
        )
        thread = make_thread(unsupported_request_behavior="continue_unthreaded")

        thread.send(user("Hello"), system="Be brief.")
        thread.send(user("Again"))

        assert request_threads(respx_mock) == [CREATE, None, None]
        assert [body.get("system") for body in request_bodies(respx_mock)] == ["Be brief.", "Be brief.", None]

    @TURN_METHODS
    def test_a_one_turn_system_override_is_refused_and_takes_the_turn_back(
        self, respx_mock: MockRouter, method: str
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a"), message_response("msg_b"))
        thread = make_thread(system="Be brief.")
        thread.send(user("Hello"))

        with pytest.raises(AnthropicError, match="Cannot change `system`"):
            run_turn(thread, method, user("Again"), system="Be verbose.")
        thread.send(user("Again"))

        continued = request_bodies(respx_mock)[1]
        assert (continued["thread"], continued["messages"]) == (continue_from("msg_a"), [user("Again")])

    @pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
    def test_update_tools_replaces_the_runnable_tools(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock, message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b", "Sunny.")
        )
        thread = make_thread()

        thread.update(tools=[beta_tool(get_weather)])
        thread.append(WEATHER_QUESTION)
        final = thread.tool_runner().until_done()

        first, second = request_bodies(respx_mock)
        assert [tool["name"] for tool in first["tools"]] == ["get_weather"]
        assert second["messages"][0]["content"][0]["type"] == "tool_result"
        assert final.id == "msg_b"


def without_omit(hints: dict[str, Any]) -> dict[str, Any]:
    """`hints` with the `| Omit` that every optional field of a thread params type adds to the type `create()` gives it."""
    assert all(Omit in get_args(hint) for hint in hints.values())
    return {
        field: reduce(operator.or_, (member for member in get_args(hint) if member is not Omit))
        for field, hint in hints.items()
    }


def run_turn(thread: BetaMessageThread[Any], method: str, *messages: BetaMessageParam, **overrides: Any) -> None:
    """Call `send()`, `parse()` or `stream()`, and read a stream to its end."""
    turn = getattr(thread, method)(*messages, **overrides)
    if method == "stream":
        with turn as stream:
            stream.until_done()


def finish(result: object) -> None:
    """Await `result` if it is the coroutine of an async thread's `send()` or `parse()`, which runs nothing until then."""
    if inspect.iscoroutine(result):
        asyncio.run(result)
