from __future__ import annotations

import json
from typing import Any, cast

import httpx2
import pytest
from respx import MockRouter

from anthropic import AnthropicError, BadRequestError, InternalServerError
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools import beta_tool
from anthropic.types.beta import BetaToolParam

from .helpers import (
    MODEL,
    CREATE,
    COMPACTED,
    MAX_TOKENS,
    THREADS_BETA,
    RESPONSE_KINDS,
    WEATHER_QUESTION,
    INLINE_TOOLS_BETA,
    Forecast,
    user,
    roles,
    lookup,
    base_url,
    tool_use,
    assistant,
    get_weather,
    make_client,
    make_runner,
    make_thread,
    tool_result,
    server_error,
    tool_removal,
    continue_from,
    request_betas,
    sent_requests,
    tool_addition,
    request_bodies,
    queue_responses,
    request_threads,
    stream_response,
    message_response,
    tool_change_turns,
    compaction_response,
    request_helper_tags,
    tool_change_replies,
    unsupported_response,
    interrupted_stream_response,
)

pytestmark = pytest.mark.respx(base_url=base_url)


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
class TestThreadToolRunner:
    @RESPONSE_KINDS
    def test_runner_over_a_typed_thread_parses_the_final_message(
        self, respx_mock: MockRouter, respond: Any, stream: bool
    ) -> None:
        queue_responses(
            respx_mock, respond("msg_a", tool_use_id="toolu_a"), respond("msg_b", json.dumps({"forecast": "Sunny"}))
        )
        thread = make_thread(tools=[beta_tool(get_weather)], output_format=Forecast)
        thread.append(WEATHER_QUESTION)

        final = thread.tool_runner(stream=stream).until_done()

        assert final.parsed_output == Forecast(forecast="Sunny")
        assert thread.previous_message_id == final.id == "msg_b"

    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_runner_over_a_default_thread_raises_on_an_unsupported_request(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, unsupported_response("inference_hooks"), message_response("msg_b", "Sunny."))
        thread = make_thread(tools=[beta_tool(get_weather)])
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner()

        with pytest.raises(BadRequestError):
            runner.until_done()

        assert request_threads(respx_mock) == [CREATE]

    def test_runner_over_a_continue_unthreaded_thread_continues_without_a_thread(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, unsupported_response("inference_hooks"), message_response("msg_b", "Sunny."))
        thread = make_thread(tools=[beta_tool(get_weather)], unsupported_request_behavior="continue_unthreaded")
        thread.append(WEATHER_QUESTION)

        final = thread.tool_runner().until_done()

        assert request_threads(respx_mock) == [CREATE, None]
        assert final.id == "msg_b"

    @RESPONSE_KINDS
    def test_runner_continues_the_thread_in_the_adopted_container(
        self, respx_mock: MockRouter, respond: Any, stream: bool
    ) -> None:
        queue_responses(
            respx_mock, respond("msg_a", tool_use_id="toolu_a", container="container_a"), respond("msg_b", "Sunny.")
        )
        thread = make_thread(tools=[beta_tool(get_weather)])
        thread.append(WEATHER_QUESTION)

        final = thread.tool_runner(stream=stream).until_done()

        created, continued = request_bodies(respx_mock)
        assert "container" not in created
        assert continued["container"] == "container_a"
        assert (continued["thread"], continued["messages"]) == (continue_from("msg_a"), [tool_result("toolu_a")])
        assert thread.previous_message_id == final.id == "msg_b"

    @RESPONSE_KINDS
    @pytest.mark.parametrize(
        ("headers", "sent"),
        [(None, ("thread", None)), ({"X-Run": "run"}, (None, "run"))],
        ids=["none_given", "headers_given"],
    )
    def test_runner_request_options_replace_the_threads_for_its_turns_only(
        self,
        respx_mock: MockRouter,
        respond: Any,
        stream: bool,
        headers: dict[str, str] | None,
        sent: tuple[str | None, str | None],
    ) -> None:
        queue_responses(
            respx_mock, respond("msg_a", tool_use_id="toolu_a"), respond("msg_b", "Sunny."), message_response("msg_c")
        )
        thread = make_thread(tools=[beta_tool(get_weather)], extra_headers={"X-Thread": "thread"})
        thread.append(WEATHER_QUESTION)

        thread.tool_runner(stream=stream, extra_headers=headers).until_done()
        thread.send(user("Thanks"))

        requests = sent_requests(respx_mock)
        assert [(r.headers.get("X-Thread"), r.headers.get("X-Run")) for r in requests] == [sent, sent, ("thread", None)]

    def test_streaming_runner_set_messages_params_adds_ahead_of_the_in_flight_reply(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(respx_mock, stream_response("msg_a", tool_use_id="toolu_a"), stream_response("msg_b", "Sunny."))
        thread = make_thread(tools=[beta_tool(get_weather)])
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner(stream=True)

        next(runner)
        runner.set_messages_params(lambda params: {**params, "messages": [*params["messages"], user("One word.")]})
        runner.until_done()

        rewritten = request_bodies(respx_mock)[1]
        assert rewritten["thread"] == CREATE
        assert rewritten["messages"] == [
            WEATHER_QUESTION,
            user("One word."),
            tool_use("toolu_a"),
            tool_result("toolu_a"),
        ]
        assert roles(thread.messages) == ["user", "user", "assistant", "user", "assistant"]
        assert thread.previous_message_id == "msg_b"

    def test_params_returns_the_runnable_tools_as_given(self) -> None:
        weather = beta_tool(get_weather)
        raw_tool: BetaToolParam = {
            "name": "noop",
            "description": "Does nothing.",
            "input_schema": {"type": "object", "properties": {}},
        }
        thread = make_thread(tools=[weather, raw_tool])

        assert thread.params.get("tools") == [weather, raw_tool]
        assert make_client().beta.messages.thread(**thread.params).params.get("tools") == [weather, raw_tool]

    def test_set_messages_params_leaves_the_tools_of_the_thread_to_a_later_runner(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            message_response("msg_b", tool_use_id="toolu_b"),
            message_response("msg_c"),
        )
        tool = beta_tool(get_weather)
        thread = make_thread(tools=[tool], messages=[WEATHER_QUESTION])

        runner = thread.tool_runner()
        runner.set_messages_params(lambda params: {**params, "max_tokens": 12})
        runner.until_done()
        thread.append(user("And now?"))
        thread.tool_runner().until_done()

        assert thread.params.get("tools") == [tool]
        assert request_bodies(respx_mock)[2]["messages"] == [tool_result("toolu_b")]

    def test_set_messages_params_hands_out_request_params_only(self) -> None:
        runner = make_thread(tools=[beta_tool(get_weather)]).tool_runner()
        handed_out: list[str] = []

        runner.set_messages_params(lambda params: handed_out.extend(params) or params)

        assert sorted(handed_out) == ["max_tokens", "messages", "model", "tools"]

    def test_set_messages_params_with_some_fields_drops_the_others(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"))
        runner = make_client().beta.messages.tool_runner(
            model=MODEL, max_tokens=1024, system="Be brief.", tools=[beta_tool(get_weather)], messages=[user("Hello")]
        )

        runner.set_messages_params(
            lambda params: {"model": params["model"], "max_tokens": 2048, "messages": params["messages"]}  # type: ignore
        )
        runner.until_done()

        body = request_bodies(respx_mock)[0]
        assert body["max_tokens"] == 2048
        assert "system" not in body and "tools" not in body

    @RESPONSE_KINDS
    def test_runner_set_messages_params_replaces_the_history_mid_loop(
        self, respx_mock: MockRouter, respond: Any, stream: bool
    ) -> None:
        queue_responses(respx_mock, respond("msg_a", tool_use_id="toolu_a"), respond("msg_b", "Sunny."))
        thread = make_thread(tools=[beta_tool(get_weather)])
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner(stream=stream)

        next(runner)
        runner.set_messages_params(lambda params: {**params, "messages": [user("Start over: Oakland?")]})
        runner.until_done()

        replaced = request_bodies(respx_mock)[1]
        assert replaced["thread"] == CREATE
        assert replaced["messages"] == [user("Start over: Oakland?"), tool_use("toolu_a"), tool_result("toolu_a")]
        assert roles(thread.messages) == ["user", "assistant", "user", "assistant"]
        assert thread.previous_message_id == "msg_b"

    def test_fork_during_a_turn_has_the_history_that_set_messages_params_replaced_the_threads_with(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock, message_response("msg_a"), stream_response("msg_b", "Sunny."), message_response("msg_c")
        )
        thread = make_thread(tools=[beta_tool(get_weather)])
        thread.send(user("Hello"))
        runner = thread.tool_runner()

        with thread.stream(WEATHER_QUESTION):
            runner.set_messages_params(lambda params: {**params, "messages": [user("Start over: Oakland?")]})
            thread.fork().send()

        forked = request_bodies(respx_mock)[2]
        assert (forked["thread"], forked["messages"]) == (CREATE, [user("Start over: Oakland?")])

    def test_set_messages_params_without_tools_still_runs_the_call_the_reply_made(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock, message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b", "Sunny.")
        )
        runner = make_runner(thread=False)

        next(runner)
        runner.set_messages_params(
            lambda params: {"model": params["model"], "max_tokens": 1024, "messages": params["messages"]}  # type: ignore
        )
        runner.until_done()

        body = request_bodies(respx_mock)[1]
        assert "tools" not in body
        assert body["messages"] == [WEATHER_QUESTION, tool_use("toolu_a"), tool_result("toolu_a")]

    def test_runner_refuses_a_changed_system_before_it_runs_a_tool(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a", tool_use_id="toolu_a"))
        locations: list[str] = []

        def record_location(location: str) -> str:
            locations.append(location)
            return "Sunny"

        runner = make_runner(system="Be brief.", tools=[beta_tool(record_location, name="get_weather")])

        next(runner)
        runner.set_messages_params(lambda params: {**params, "system": "Be very brief."})
        with pytest.raises(AnthropicError, match="Cannot change `system`"):
            runner.until_done()

        assert locations == []
        assert respx_mock.calls.call_count == 1

    def test_runner_stops_threading_after_a_compaction_request_that_cannot_be_threaded(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a"),
            unsupported_response("context_management"),
            compaction_response("msg_b"),
            message_response("msg_c", "Sunny."),
        )
        runner = make_runner(betas=["compact-2026-09-04"])

        next(runner)
        runner.compact_before_next_turn()
        runner.until_done()

        _, rejected, compaction, later = request_bodies(respx_mock)
        assert request_threads(respx_mock) == [CREATE, CREATE, None, None]
        assert rejected["messages"] == compaction["messages"]
        assert later["messages"] == [COMPACTED]

    def test_runner_keeps_a_message_appended_to_the_thread_while_it_compacts(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a"),
            compaction_response("msg_b"),
            message_response("msg_c", "Sunny."),
        )
        thread = make_thread(tools=[beta_tool(get_weather)], betas=["compact-2026-09-04"])
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner()

        next(runner)
        runner.compact_before_next_turn()
        assert next(runner).stop_reason == "compaction"
        with pytest.raises(ValueError, match="being compacted"):
            runner.append_messages(user("In two words."))
        thread.append(user("In one word."))
        runner.until_done()

        assert request_bodies(respx_mock)[2]["messages"] == [COMPACTED, user("In one word.")]
        assert thread.messages[1] == user("In one word.")
        assert roles(thread.messages) == ["assistant", "user", "assistant"]

    def test_runner_keeps_a_message_appended_to_the_thread_while_it_compacts_after_the_final_turn(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", "Sunny."),
            compaction_response("msg_b"),
            message_response("msg_c", "Sunny."),
        )
        thread = make_thread(tools=[beta_tool(get_weather)], betas=["compact-2026-09-04"])
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner()

        next(runner)
        runner.compact_before_next_turn()
        assert next(runner).stop_reason == "compaction"
        thread.append(user("In one word."))
        runner.until_done()
        messages_after_the_runner, requests_of_the_runner = thread.messages, respx_mock.calls.call_count
        thread.send()

        assert requests_of_the_runner == 2
        assert messages_after_the_runner[1:] == (user("In one word."),)
        assert request_bodies(respx_mock)[2]["messages"] == [COMPACTED, user("In one word.")]

    def test_runner_sends_the_compaction_once_when_it_is_appended_to_the_thread_again(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a"),
            compaction_response("msg_b"),
            message_response("msg_c", "Sunny."),
        )
        thread = make_thread(tools=[beta_tool(get_weather)], betas=["compact-2026-09-04"])
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner()

        next(runner)
        runner.compact_before_next_turn()
        thread.append(next(runner), user("In one word."))
        runner.until_done()

        assert request_bodies(respx_mock)[2]["messages"] == [COMPACTED, user("In one word.")]
        assert roles(thread.messages) == ["assistant", "user", "assistant"]

    @pytest.mark.parametrize("ending", ["block_left_early", "events_run_out"])
    def test_runner_compacts_a_thread_that_ends_in_a_partial_reply_without_that_reply(
        self, respx_mock: MockRouter, ending: str
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            stream_response("msg_b", "one two three")
            if ending == "block_left_early"
            else interrupted_stream_response("msg_b", "one"),
            compaction_response("msg_c"),
            message_response("msg_d", "Three."),
        )
        thread = make_thread(tools=[beta_tool(get_weather)], betas=["compact-2026-09-04"])
        thread.send(user("Hello"))
        with thread.stream(user("Count")) as stream:
            if ending == "block_left_early":
                next(stream.text_stream)
            else:
                stream.until_done()
        messages_after_the_stream = thread.messages
        runner = thread.tool_runner()

        runner.compact_before_next_turn()
        runner.until_done()

        compaction, later = request_bodies(respx_mock)[2:]
        assert roles(messages_after_the_stream) == ["user", "assistant", "user", "assistant"]
        assert compaction["compaction"] == {"type": "summarize"}
        assert (compaction["thread"], compaction["messages"]) == (CREATE, [user("Hello"), assistant(), user("Count")])
        assert (later["thread"], later["messages"]) == (CREATE, [COMPACTED])
        assert roles(thread.messages) == ["assistant", "assistant"]

    def test_runner_takes_other_params_after_a_message_is_appended_to_the_thread_while_it_compacts(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a"),
            compaction_response("msg_b"),
            message_response("msg_c", "Sunny."),
        )
        thread = make_thread(tools=[beta_tool(get_weather)], betas=["compact-2026-09-04"])
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner()

        next(runner)
        runner.compact_before_next_turn()
        assert next(runner).stop_reason == "compaction"
        thread.append(user("In one word."))
        runner.set_messages_params(lambda params: {**params, "max_tokens": 12})
        with pytest.raises(ValueError, match="being compacted"):
            runner.set_messages_params(lambda params: {**params, "messages": [user("Hello")]})
        runner.until_done()

        later = request_bodies(respx_mock)[2]
        assert (later["max_tokens"], later["messages"]) == (12, [COMPACTED, user("In one word.")])

    @RESPONSE_KINDS
    def test_runner_adds_tool_results_ahead_of_messages_appended_to_the_thread_mid_loop(
        self, respx_mock: MockRouter, respond: Any, stream: bool
    ) -> None:
        queue_responses(respx_mock, respond("msg_a", tool_use_id="toolu_a"), respond("msg_b", "Sunny."))
        thread = make_thread(tools=[beta_tool(get_weather)])
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner(stream=stream)

        next(runner)
        thread.append(user("In one word."))
        runner.until_done()

        continued = request_bodies(respx_mock)[1]
        assert continued["thread"] == continue_from("msg_a")
        assert continued["messages"] == [tool_result("toolu_a"), user("In one word.")]
        assert roles(thread.messages) == ["user", "assistant", "user", "user", "assistant"]

    def test_runner_on_a_thread_whose_stream_ended_early_sends_that_turn_again(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock, message_response("msg_a"), stream_response("msg_b", "one two three"), message_response("msg_c")
        )
        thread = make_thread(tools=[beta_tool(get_weather)])
        thread.send(user("Hello"))
        with thread.stream(user("Count")) as stream:
            next(stream.text_stream)

        final = thread.tool_runner().until_done()

        retried = request_bodies(respx_mock)[2]
        assert (retried["thread"], retried["messages"]) == (CREATE, [user("Hello"), assistant("Hi!"), user("Count")])
        assert roles(thread.messages) == ["user", "assistant", "user", "assistant"]
        assert thread.previous_message_id == final.id == "msg_c"

    def test_streaming_runner_whose_stream_fails_leaves_the_thread_free(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            interrupted_stream_response("msg_a", "Let me", error=httpx2.ReadError),
            message_response("msg_b"),
        )
        thread = make_thread(tools=[beta_tool(get_weather)])
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner(stream=True)
        with pytest.raises(httpx2.ReadError):
            for stream in runner:
                stream.until_done()

        thread.send(user("Are you there?"))

        later = request_bodies(respx_mock)[1]
        assert (later["thread"], later["messages"]) == (
            CREATE,
            [WEATHER_QUESTION, assistant("Let me"), user("Are you there?")],
        )
        assert thread.previous_message_id == "msg_b"

    def test_runner_sends_a_message_appended_to_the_thread_during_a_yield(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", "Which city?", stop_reason="tool_use"),
            message_response("msg_b", "Sunny."),
        )
        thread = make_thread(tools=[beta_tool(get_weather)])
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner()

        first = next(runner)
        thread.append(user("San Francisco"))
        final = runner.until_done()

        assert (first.id, final.id) == ("msg_a", "msg_b")
        assert request_bodies(respx_mock)[1]["messages"] == [user("San Francisco")]

    @RESPONSE_KINDS
    def test_runner_sends_a_message_appended_to_the_thread_while_a_turn_is_paused_with_the_resume(
        self, respx_mock: MockRouter, respond: Any, stream: bool
    ) -> None:
        queue_responses(respx_mock, respond("msg_a", "Searching", stop_reason="pause_turn"), server_error())
        thread = make_thread(tools=[beta_tool(get_weather)])
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner(stream=stream)

        next(runner)
        thread.append(user("In one word."))
        with pytest.raises(InternalServerError):
            runner.until_done()

        resumed = request_bodies(respx_mock)[1]
        assert (resumed["thread"], resumed["messages"]) == (continue_from("msg_a"), [user("In one word.")])
        assert thread.messages[2:] == (user("In one word."),)

    def test_runner_set_messages_params_trimmed_history_keeps_one_copy_of_the_reply(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            message_response("msg_b", tool_use_id="toolu_b"),
            message_response("msg_c", "Sunny."),
        )
        thread = make_thread(tools=[beta_tool(get_weather)])
        thread.send(user("Hello"))
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner()

        next(runner)
        runner.set_messages_params(lambda params: {**params, "messages": list(params["messages"])[2:]})
        runner.until_done()

        trimmed = request_bodies(respx_mock)[2]
        assert trimmed["thread"] == CREATE
        assert trimmed["messages"] == [WEATHER_QUESTION, tool_use("toolu_b"), tool_result("toolu_b")]
        assert thread.previous_message_id == "msg_c"

    def test_streaming_runner_keeps_messages_appended_after_a_mid_loop_rewrite(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, stream_response("msg_a", tool_use_id="toolu_a"), stream_response("msg_b", "Sunny."))
        thread = make_thread(tools=[beta_tool(get_weather)])
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner(stream=True)

        next(runner)
        runner.set_messages_params(lambda params: {**params, "messages": [user("Start over: Oakland?")]})
        runner.append_messages(user("Also Berkeley."))
        runner.until_done()

        rewritten = request_bodies(respx_mock)[1]
        assert rewritten["thread"] == CREATE
        assert rewritten["messages"] == [user("Start over: Oakland?"), user("Also Berkeley.")]
        assert roles(thread.messages) == ["user", "user", "assistant"]
        assert thread.previous_message_id == "msg_b"

    def test_runner_over_an_existing_thread_continues_it(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a"),
            message_response("msg_b", tool_use_id="toolu_b"),
            message_response("msg_c", "Sunny."),
            message_response("msg_d"),
        )
        thread = make_thread(tools=[beta_tool(get_weather)])
        thread.send(user("Hello"))
        thread.append(WEATHER_QUESTION)

        final = thread.tool_runner().until_done()
        messages_after_the_runner = roles(thread.messages)
        thread.send(user("Thanks"))

        assert final.id == "msg_c"
        assert messages_after_the_runner == ["user", "assistant", "user", "assistant", "user", "assistant"]
        assert request_threads(respx_mock) == [
            CREATE,
            continue_from("msg_a"),
            continue_from("msg_b"),
            continue_from("msg_c"),
        ]
        assert request_betas(respx_mock) == [[THREADS_BETA]] * 4
        assert request_helper_tags(respx_mock) == [
            ["message-thread"],
            ["BetaToolRunner, message-thread"],
            ["BetaToolRunner, message-thread"],
            ["message-thread"],
        ]

    def test_runner_over_an_existing_thread_adds_and_removes_tools_on_it(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_0"), *tool_change_replies(), message_response("msg_e"))
        added = beta_tool(lookup)
        thread = make_thread(tools=[beta_tool(get_weather)], betas=[INLINE_TOOLS_BETA])
        thread.send(user("Hello"))
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner()

        next(runner)
        runner.add_tools(added)
        next(runner)
        runner.remove_tools("get_weather")
        with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
            runner.until_done()
        thread.send(user("Thanks"))

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

    @RESPONSE_KINDS
    @pytest.mark.parametrize(
        "dropped",
        [None, [], ["container"]],
        ids=["params_left_alone", "params_set_again", "params_set_without_the_container"],
    )
    def test_runner_that_stops_at_its_limit_leaves_the_tool_results_and_the_container_on_the_thread(
        self, respx_mock: MockRouter, respond: Any, stream: bool, dropped: list[str] | None
    ) -> None:
        queue_responses(
            respx_mock, respond("msg_a", tool_use_id="toolu_a", container="container_a"), message_response("msg_b")
        )
        thread = make_thread(tools=[beta_tool(get_weather)])
        thread.append(WEATHER_QUESTION)
        runner = thread.tool_runner(stream=stream, max_iterations=1)

        next(runner)
        if dropped is not None:
            runner.set_messages_params(lambda params: cast(Any, {k: v for k, v in params.items() if k not in dropped}))
        runner.until_done()
        thread.send(user("Thanks"))

        continued = request_bodies(respx_mock)[1]
        assert (continued["thread"], continued.get("container")) == (continue_from("msg_a"), "container_a")
        assert continued["messages"] == [tool_result("toolu_a"), user("Thanks")]

    @RESPONSE_KINDS
    def test_runner_ends_on_a_refused_turn_and_leaves_its_tool_results_staged(
        self, respx_mock: MockRouter, respond: Any, stream: bool
    ) -> None:
        queue_responses(
            respx_mock,
            respond("msg_a", tool_use_id="toolu_a"),
            respond("msg_b", "I can't help with that.", stop_reason="refusal"),
            message_response("msg_c"),
        )
        thread = make_thread(tools=[beta_tool(get_weather)])
        thread.append(WEATHER_QUESTION)

        final = thread.tool_runner(stream=stream).until_done()
        thread.send(user("Never mind"))

        refused, created = request_bodies(respx_mock)[1:]
        assert (final.id, final.stop_reason) == ("msg_b", "refusal")
        assert (refused["thread"], refused["messages"]) == (continue_from("msg_a"), [tool_result("toolu_a")])
        assert (created["thread"], created["tools"]) == (CREATE, [beta_tool(get_weather).to_dict()])
        assert created["messages"] == [
            WEATHER_QUESTION,
            tool_use("toolu_a"),
            tool_result("toolu_a"),
            user("Never mind"),
        ]

    def test_runner_over_a_fork_calls_the_original_tools(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock, message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b", "Sunny.")
        )
        thread = make_thread(tools=[beta_tool(get_weather)])
        fork = thread.fork()
        fork.append(WEATHER_QUESTION)

        final = fork.tool_runner().until_done()

        created, continued = request_bodies(respx_mock)
        assert final.id == "msg_b"
        assert created["tools"] == [beta_tool(get_weather).to_dict()]
        assert (continued["thread"], continued["messages"]) == (continue_from("msg_a"), [tool_result("toolu_a")])
        assert (thread.messages, thread.previous_message_id) == ((), None)

    @pytest.mark.parametrize("thread", [CREATE, continue_from("msg_a")], ids=["create", "continue"])
    def test_runner_refuses_a_thread_value_when_it_is_created(self, respx_mock: MockRouter, thread: Any) -> None:
        with pytest.raises(TypeError, match="`thread` cannot be set in the params of a tool runner"):
            make_runner(thread=thread)

        assert respx_mock.calls.call_count == 0

    @pytest.mark.parametrize("thread", [CREATE, continue_from("msg_a")], ids=["create", "continue"])
    def test_runner_refuses_a_thread_value_in_set_messages_params(self, respx_mock: MockRouter, thread: Any) -> None:
        queue_responses(
            respx_mock, message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b", "Sunny.")
        )
        runner = make_runner()
        next(runner)

        with pytest.raises(TypeError, match="`thread` cannot be set in the params of a tool runner"):
            runner.set_messages_params(lambda params: {**params, "max_tokens": 12, "thread": thread})
        runner.until_done()

        continued = request_bodies(respx_mock)[1]
        assert (continued["thread"], continued["max_tokens"]) == (continue_from("msg_a"), MAX_TOKENS)

    def test_runner_with_thread_none_threads_as_by_default(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"))

        make_runner(thread=None).until_done()

        assert request_threads(respx_mock) == [CREATE]
