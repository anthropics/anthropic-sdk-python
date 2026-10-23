from __future__ import annotations

import re
import json
from typing import Any, Callable
from contextlib import nullcontext

import httpx2
import pytest
from respx import MockRouter

from anthropic import AnthropicError, AnthropicVertex, AnthropicBedrock, AnthropicFoundry, AnthropicBedrockMantle
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools import beta_tool
from anthropic.types.beta import BetaMessageParam
from anthropic.lib.threads import BetaMessageThread

from .helpers import (
    FOGGY,
    MODEL,
    CREATE,
    FALLBACKS,
    MAX_TOKENS,
    LOOP_BODIES,
    RUNNER_MODES,
    THREADS_BETA,
    FALLBACK_BETA,
    RESPONSE_KINDS,
    THREAD_NOT_FOUND,
    WEATHER_QUESTION,
    INLINE_TOOLS_BETA,
    FALLBACK_ITERATIONS,
    CONTEXT_MANAGEMENT_BETA,
    STRUCTURED_OUTPUTS_BETA,
    NEW_SYSTEM_WITH_ANOTHER_HISTORY,
    Forecast,
    LoopBody,
    user,
    roles,
    lookup,
    marked,
    base_url,
    tool_use,
    assistant,
    id_headers,
    get_weather,
    make_runner,
    tool_result,
    response_ids,
    continue_from,
    request_betas,
    sent_requests,
    request_bodies,
    queue_responses,
    request_threads,
    stream_response,
    message_response,
    tool_change_turns,
    request_helper_tags,
    tool_change_replies,
    unsupported_response,
    two_tool_uses_response,
    assert_sends_conversation,
)

pytestmark = pytest.mark.respx(base_url=base_url)


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
class TestToolRunnerThreading:
    def test_runner_threads_by_default(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock, message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b", "Sunny.")
        )
        runner = make_runner()

        final = runner.until_done()

        created, continued = request_bodies(respx_mock)
        assert (created["thread"], created["messages"]) == (CREATE, [WEATHER_QUESTION])
        assert (continued["thread"], continued["messages"]) == (continue_from("msg_a"), [tool_result("toolu_a")])
        assert "tools" not in continued
        assert request_betas(respx_mock) == [[THREADS_BETA]] * 2
        assert request_helper_tags(respx_mock) == [["BetaToolRunner, message-thread"]] * 2
        assert final.id == "msg_b"

    def test_runner_adds_and_removes_tools_on_the_thread(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, *tool_change_replies())
        added = beta_tool(lookup)
        runner = make_runner(betas=[INLINE_TOOLS_BETA])

        next(runner)
        runner.add_tools(added)
        next(runner)
        runner.remove_tools("get_weather")
        with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
            final = runner.until_done()

        after_msg_a, after_msg_b, after_msg_c = tool_change_turns(added.to_dict())
        assert final.id == "msg_d"
        assert [(body["thread"], body["messages"], body.get("tools")) for body in request_bodies(respx_mock)] == [
            (CREATE, [WEATHER_QUESTION], [beta_tool(get_weather).to_dict()]),
            (continue_from("msg_a"), after_msg_a, None),
            (continue_from("msg_b"), after_msg_b, None),
            (continue_from("msg_c"), after_msg_c, None),
        ]

    def test_runner_with_a_caller_anthropic_beta_header_still_sends_the_threads_beta(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock, message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b", "Sunny.")
        )

        make_runner(extra_headers={"anthropic-beta": CONTEXT_MANAGEMENT_BETA}).until_done()

        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a")]
        assert request_betas(respx_mock) == [[CONTEXT_MANAGEMENT_BETA, THREADS_BETA]] * 2

    @RESPONSE_KINDS
    def test_runner_resumes_a_paused_turn_on_the_thread(
        self, respx_mock: MockRouter, respond: Any, stream: bool
    ) -> None:
        queue_responses(respx_mock, respond("msg_a", "Searching", stop_reason="pause_turn"), respond("msg_b"))
        runner = make_runner(stream=stream)

        final = runner.until_done()

        resumed = request_bodies(respx_mock)[1]
        assert resumed["thread"] == continue_from("msg_a")
        assert resumed["messages"] == []
        assert final.id == "msg_b"

    def test_runner_output_format_sends_the_callers_betas_every_turn(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a"),
            message_response("msg_b", json.dumps({"forecast": "Sunny"})),
        )
        runner = make_runner(output_format=Forecast, betas=[STRUCTURED_OUTPUTS_BETA])

        final = runner.until_done()

        expected = [STRUCTURED_OUTPUTS_BETA, THREADS_BETA]
        assert request_betas(respx_mock) == [expected, expected]
        assert final.parsed_output == Forecast(forecast="Sunny")

    def test_non_streaming_runner_does_not_add_the_structured_outputs_beta(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, message_response("msg_a"))
        runner = make_runner()

        runner.until_done()

        assert request_betas(respx_mock) == [[THREADS_BETA]]

    def test_streaming_runner_does_not_add_the_structured_outputs_beta(self, respx_mock: MockRouter) -> None:
        queue_responses(respx_mock, stream_response("msg_a"))
        runner = make_runner(stream=True)

        runner.until_done()

        assert request_betas(respx_mock) == [[THREADS_BETA]]

    def test_runner_continues_without_a_thread_after_an_unsupported_request(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            unsupported_response("inference_hooks"),
            message_response("msg_b", tool_use_id="toolu_b"),
            message_response("msg_c", "Sunny."),
        )
        runner = make_runner()

        final = runner.until_done()

        assert request_threads(respx_mock) == [CREATE, None, None]
        assert request_helper_tags(respx_mock) == [["BetaToolRunner, message-thread"]] * 3
        assert request_bodies(respx_mock)[2]["messages"] == [
            WEATHER_QUESTION,
            tool_use("toolu_b"),
            tool_result("toolu_b"),
        ]
        assert final.id == "msg_c"

    @RESPONSE_KINDS
    def test_runner_continues_without_a_thread_when_the_thread_is_lost_again_right_after_a_replay(
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
        runner = make_runner(stream=stream)

        final = runner.until_done()

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

    @RESPONSE_KINDS
    def test_runner_goes_on_under_a_new_thread_after_a_reply_from_a_fallback_model(
        self, respx_mock: MockRouter, respond: Any, stream: bool
    ) -> None:
        queue_responses(
            respx_mock,
            respond("msg_a", tool_use_id="toolu_a", iterations=FALLBACK_ITERATIONS),
            respond("msg_b", tool_use_id="toolu_b"),
            respond("msg_c", "Sunny."),
        )
        runner = make_runner(stream=stream, fallbacks=FALLBACKS, betas=[FALLBACK_BETA])

        final = runner.until_done()

        first, created, continued = bodies = request_bodies(respx_mock)
        assert final.id == "msg_c"
        assert [(body["model"], body["fallbacks"]) for body in bodies] == [(MODEL, FALLBACKS)] * 3
        assert [body["thread"] for body in bodies] == [CREATE, CREATE, continue_from("msg_b")]
        assert created["tools"] == first["tools"]
        assert created["messages"] == [WEATHER_QUESTION, tool_use("toolu_a"), tool_result("toolu_a")]
        assert continued["messages"] == [tool_result("toolu_b")]

    def test_runner_with_thread_false_changes_nothing_after_a_reply_from_a_fallback_model(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a", iterations=FALLBACK_ITERATIONS),
            message_response("msg_b", "Sunny."),
        )
        runner = make_runner(thread=False, fallbacks=FALLBACKS, betas=[FALLBACK_BETA])

        runner.until_done()

        second = request_bodies(respx_mock)[1]
        assert (second["model"], second["fallbacks"]) == (MODEL, FALLBACKS)

    def test_runner_with_thread_false_sends_the_full_history_without_a_thread(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock, message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b", "Sunny.")
        )
        runner = make_runner(thread=False)

        runner.until_done()

        assert request_threads(respx_mock) == [None, None]
        assert request_betas(respx_mock) == [[], []]
        assert request_helper_tags(respx_mock) == [["BetaToolRunner"]] * 2
        assert request_bodies(respx_mock)[1]["messages"] == [
            WEATHER_QUESTION,
            tool_use("toolu_a"),
            tool_result("toolu_a"),
        ]

    @pytest.mark.parametrize("thread", [None, False], ids=["threaded", "thread_false"])
    def test_runner_replies_have_the_request_and_workspace_ids_of_their_responses(
        self, respx_mock: MockRouter, thread: bool | None
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a", headers=id_headers("req_a", "wrkspc_a")),
            message_response("msg_b", "Sunny.", headers=id_headers("req_b", "wrkspc_b")),
        )

        replies = list(make_runner(thread=thread))

        assert response_ids(*replies) == [("req_a", "wrkspc_a"), ("req_b", "wrkspc_b")]

    def test_runner_with_thread_false_records_a_refused_turn(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a"),
            message_response("msg_b", "I can't help with that.", stop_reason="refusal"),
        )
        runner = make_runner(thread=False)
        history: list[BetaMessageParam] = []

        final = runner.until_done()
        runner.set_messages_params(lambda params: history.extend(params["messages"]) or params)

        assert final.id == "msg_b"
        assert roles(history) == ["user", "assistant", "user", "assistant"]

    def test_runner_with_thread_false_sends_every_cache_marker_as_given(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock, message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b", "Sunny.")
        )
        runner = make_runner(thread=False, messages=[marked("What is the weather in SF?")])

        runner.until_done()

        assert request_bodies(respx_mock)[1]["messages"] == [
            marked("What is the weather in SF?"),
            tool_use("toolu_a"),
            tool_result("toolu_a"),
        ]

    def test_runner_with_thread_false_reuses_the_container(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a", container="container_a"),
            message_response("msg_b", "Sunny."),
        )
        runner = make_runner(thread=False)

        runner.until_done()

        assert request_bodies(respx_mock)[1]["container"] == "container_a"

    def test_runner_keeps_container_skills_when_adopting_a_container(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a", container="container_a"),
            message_response("msg_b", "Sunny."),
        )
        skills: list[Any] = [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]
        runner = make_runner(container={"skills": skills})

        runner.until_done()

        created, continued = request_bodies(respx_mock)
        assert created["container"] == {"skills": skills}
        assert continued["thread"] == continue_from("msg_a")
        assert continued["container"] == {"skills": skills, "id": "container_a"}

    @LOOP_BODIES
    @RUNNER_MODES
    @RESPONSE_KINDS
    def test_runner_sends_the_history_the_loop_body_leaves(
        self, respx_mock: MockRouter, respond: Any, stream: bool, mode: dict[str, Any], body: LoopBody
    ) -> None:
        queue_responses(respx_mock, respond("msg_a", tool_use_id="toolu_a"), respond("msg_b", "Sunny."))
        locations: list[str] = []

        def get_weather(location: str) -> str:
            locations.append(location)
            return f"Sunny in {location}"

        runner = make_runner(stream=stream, tools=[beta_tool(get_weather)], **mode)

        item: Any = next(runner)
        reply = None if body.reads == "nothing" else item.get_final_message() if stream else item
        tool_response = runner.generate_tool_call_response() if body.reads == "tool_response" else None
        body.change(runner, reply, tool_response)
        final = runner.until_done()

        requests = request_bodies(respx_mock)
        assert len(requests) == 2
        assert_sends_conversation(requests[1], mode, body.conversation)
        assert len(locations) == body.tool_runs
        assert final.id == "msg_b"

    @RUNNER_MODES
    @RESPONSE_KINDS
    def test_runner_leaves_a_raw_tool_call_to_the_result_the_caller_appends(
        self, respx_mock: MockRouter, respond: Any, stream: bool, mode: dict[str, Any]
    ) -> None:
        queue_responses(respx_mock, respond("msg_a", tool_use_id="toolu_a"), respond("msg_b", "Foggy."))
        runner = make_runner(stream=stream, tools=[beta_tool(get_weather).to_dict()], **mode)

        item: Any = next(runner)
        runner.append_messages(item.get_final_message() if stream else item, FOGGY)
        with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
            runner.until_done()

        requests = request_bodies(respx_mock)
        assert len(requests) == 2
        assert_sends_conversation(requests[1], mode, [WEATHER_QUESTION, tool_use("toolu_a"), FOGGY])

    @RUNNER_MODES
    def test_runner_adds_no_result_for_a_call_the_caller_leaves_unanswered(
        self, respx_mock: MockRouter, mode: dict[str, Any]
    ) -> None:
        queue_responses(respx_mock, two_tool_uses_response("msg_a"), message_response("msg_b"))
        runner = make_runner(**mode)

        reply: Any = next(runner)
        runner.append_messages(reply, FOGGY)
        runner.until_done()

        sent = request_bodies(respx_mock)[1]["messages"]
        assert sent[-1] == FOGGY
        assert roles(sent) == (["user", "assistant", "user"] if mode else ["user"])

    @RUNNER_MODES
    def test_runner_gives_set_messages_params_the_history_without_the_reply(
        self, respx_mock: MockRouter, mode: dict[str, Any]
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a"),
            message_response("msg_b", tool_use_id="toolu_b"),
            message_response("msg_c", "Sunny."),
        )
        runner = make_runner(**mode)

        next(runner)
        next(runner)
        runner.set_messages_params(lambda params: {**params, "messages": list(params["messages"])[-2:]})
        runner.until_done()

        assert_sends_conversation(
            request_bodies(respx_mock)[2],
            mode,
            [tool_use("toolu_a"), tool_result("toolu_a"), tool_use("toolu_b"), tool_result("toolu_b")],
        )

    @RUNNER_MODES
    @RESPONSE_KINDS
    def test_runner_still_runs_a_tool_that_set_messages_params_gives_as_a_definition(
        self, respx_mock: MockRouter, respond: Any, stream: bool, mode: dict[str, Any]
    ) -> None:
        queue_responses(respx_mock, respond("msg_a", tool_use_id="toolu_a"), respond("msg_b", "Sunny."))
        tool = beta_tool(get_weather)
        runner = make_runner(stream=stream, tools=[tool], **mode)

        next(runner)
        runner.set_messages_params(lambda params: {**params, "tools": [tool.to_dict()]})
        runner.until_done()

        assert_sends_conversation(
            request_bodies(respx_mock)[1], mode, [WEATHER_QUESTION, tool_use("toolu_a"), tool_result("toolu_a")]
        )

    @RUNNER_MODES
    def test_runner_runs_neither_a_tool_set_messages_params_takes_out_of_tools_nor_one_it_adds(
        self, respx_mock: MockRouter, mode: dict[str, Any]
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a"),
            message_response("msg_b", tool_use_id="toolu_b", tool_name="lookup"),
            message_response("msg_c"),
        )
        locations: list[str] = []

        def get_weather(location: str) -> str:
            locations.append(location)
            return f"Sunny in {location}"

        runner = make_runner(tools=[beta_tool(get_weather)], **mode)

        # With default settings the definitions sent can change only before the first request.
        runner.set_messages_params(lambda params: {**params, "tools": [beta_tool(lookup).to_dict()]})
        with pytest.warns(UserWarning, match="not found in tool runner"):
            runner.until_done()

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

    @RUNNER_MODES
    def test_runner_keeps_the_first_turn_after_append_messages_before_the_loop(
        self, respx_mock: MockRouter, mode: dict[str, Any]
    ) -> None:
        queue_responses(
            respx_mock, message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b", "Sunny.")
        )
        locations: list[str] = []

        def get_weather(location: str) -> str:
            locations.append(location)
            return f"Sunny in {location}"

        runner = make_runner(tools=[beta_tool(get_weather)], **mode)

        runner.append_messages(user("Be concise."))
        runner.until_done()

        first, second = request_bodies(respx_mock)
        turn = [tool_use("toolu_a"), tool_result("toolu_a")]
        assert first["messages"] == [WEATHER_QUESTION, user("Be concise.")]
        assert second.get("thread") == (None if mode else continue_from("msg_a"))
        assert second["messages"] == ([*first["messages"], *turn] if mode else turn[1:])
        assert locations == ["San Francisco"]

    @NEW_SYSTEM_WITH_ANOTHER_HISTORY
    @RUNNER_MODES
    def test_runner_takes_a_new_system_with_another_history_only_when_it_sends_the_whole_history(
        self, respx_mock: MockRouter, mode: dict[str, Any], change: Callable[[Any], None]
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b"))
        locations: list[str] = []

        def get_weather(location: str) -> str:
            locations.append(location)
            return f"Sunny in {location}"

        runner = make_runner(system="Be brief.", tools=[beta_tool(get_weather)], **mode)

        next(runner)
        change(runner)
        with nullcontext() if mode else pytest.raises(AnthropicError, match="Cannot change `system`"):
            runner.until_done()

        sent = ["Be brief.", "Be very brief."] if mode else ["Be brief."]
        assert [body["system"] for body in request_bodies(respx_mock)] == sent
        assert len(locations) == len(sent) - 1

    @RUNNER_MODES
    def test_runner_still_runs_a_tool_from_add_tools_after_set_messages_params(
        self, respx_mock: MockRouter, mode: dict[str, Any]
    ) -> None:
        queue_responses(
            respx_mock,
            message_response("msg_a", tool_use_id="toolu_a"),
            message_response("msg_b", tool_use_id="toolu_b", tool_name="lookup"),
            message_response("msg_c"),
        )
        runner = make_runner(betas=[INLINE_TOOLS_BETA], **mode)

        next(runner)
        runner.add_tools(beta_tool(lookup))
        runner.set_messages_params(lambda params: {**params, "max_tokens": 5})
        runner.until_done()

        assert request_bodies(respx_mock)[2]["messages"][-1] == tool_result(
            "toolu_b", "800,000 people live in San Francisco"
        )

    @RUNNER_MODES
    @RESPONSE_KINDS
    def test_runner_gives_set_messages_params_the_tools_as_definitions(
        self, respx_mock: MockRouter, respond: Any, stream: bool, mode: dict[str, Any]
    ) -> None:
        queue_responses(respx_mock, respond("msg_a", tool_use_id="toolu_a"), respond("msg_b", "Sunny."))
        tool = beta_tool(get_weather)
        runner = make_runner(stream=stream, tools=[tool], **mode)
        seen: list[Any] = []

        def copy_tools(params: Any) -> Any:
            seen.extend(params["tools"])
            return {**params, "tools": [{**tool} for tool in params["tools"]]}

        next(runner)
        runner.set_messages_params(copy_tools)
        runner.until_done()

        assert seen == [tool.to_dict()]
        assert_sends_conversation(
            request_bodies(respx_mock)[1], mode, [WEATHER_QUESTION, tool_use("toolu_a"), tool_result("toolu_a")]
        )

    def test_runner_sends_the_tool_definitions_a_set_messages_params_callback_marks(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b"))
        runner = make_runner(thread=False)

        def mark_tools(params: Any) -> Any:
            return {**params, "tools": [{**tool, "cache_control": {"type": "ephemeral"}} for tool in params["tools"]]}

        next(runner)
        runner.set_messages_params(mark_tools)
        runner.until_done()

        second = request_bodies(respx_mock)[1]
        assert second["tools"] == [{**beta_tool(get_weather).to_dict(), "cache_control": {"type": "ephemeral"}}]
        assert second["messages"][-1] == tool_result("toolu_a")

    @RUNNER_MODES
    @RESPONSE_KINDS
    def test_runner_keeps_the_header_params_that_set_messages_params_leaves_out(
        self, respx_mock: MockRouter, respond: Any, stream: bool, mode: dict[str, Any]
    ) -> None:
        queue_responses(respx_mock, respond("msg_a", tool_use_id="toolu_a"), respond("msg_b", "Sunny."))
        tool = beta_tool(get_weather)
        runner = make_runner(
            stream=stream,
            tools=[tool],
            betas=[CONTEXT_MANAGEMENT_BETA],
            user_profile_id="uprof_a",
            workspace_id="wrkspc_a",
            **mode,
        )

        params: Any = {"model": MODEL, "max_tokens": 2048, "tools": [tool.to_dict()], "messages": [WEATHER_QUESTION]}

        next(runner)
        runner.set_messages_params(params)
        runner.until_done()

        first, second = sent_requests(respx_mock)
        assert json.loads(second.content)["max_tokens"] == 2048
        for header in ("anthropic-beta", "anthropic-user-profile-id", "anthropic-workspace-id"):
            assert second.headers[header] == first.headers[header]
        assert CONTEXT_MANAGEMENT_BETA in request_betas(respx_mock)[1]
        assert second.headers["anthropic-user-profile-id"] == "uprof_a"
        assert second.headers["anthropic-workspace-id"] == "wrkspc_a"

    @RUNNER_MODES
    def test_runner_sends_the_betas_that_set_messages_params_gives(
        self, respx_mock: MockRouter, mode: dict[str, Any]
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b"))
        runner = make_runner(betas=[CONTEXT_MANAGEMENT_BETA], **mode)

        next(runner)
        runner.set_messages_params(lambda params: {**params, "betas": [INLINE_TOOLS_BETA]})
        runner.until_done()

        betas = request_betas(respx_mock)[1]
        assert INLINE_TOOLS_BETA in betas
        assert CONTEXT_MANAGEMENT_BETA not in betas

    @RUNNER_MODES
    @RESPONSE_KINDS
    def test_runner_stops_on_a_tool_use_reply_without_tool_calls_whatever_the_caller_appends(
        self, respx_mock: MockRouter, respond: Any, stream: bool, mode: dict[str, Any]
    ) -> None:
        queue_responses(respx_mock, respond("msg_a", "Which city?", stop_reason="tool_use"))
        runner = make_runner(stream=stream, **mode)

        item: Any = next(runner)
        runner.append_messages(item.get_final_message() if stream else item, user("San Francisco"))
        final = runner.until_done()

        assert final.id == "msg_a"
        assert len(request_bodies(respx_mock)) == 1

    @pytest.mark.parametrize("appends_reply", [True, False], ids=["reply_and_text", "text"])
    @RUNNER_MODES
    @RESPONSE_KINDS
    def test_runner_resumes_a_paused_turn_with_the_history_the_caller_appended_to(
        self, respx_mock: MockRouter, respond: Any, stream: bool, mode: dict[str, Any], appends_reply: bool
    ) -> None:
        queue_responses(respx_mock, respond("msg_a", "Searching", stop_reason="pause_turn"), respond("msg_b"))
        runner = make_runner(stream=stream, **mode)

        item: Any = next(runner)
        if appends_reply:
            runner.append_messages(item.get_final_message() if stream else item)
        runner.append_messages(user("Never mind."))
        runner.until_done()

        resumed = request_bodies(respx_mock)[1]
        if appends_reply and not mode:
            assert (resumed["thread"], resumed["messages"]) == (continue_from("msg_a"), [user("Never mind.")])
        else:
            assert resumed.get("thread") == (None if mode else CREATE)
            assert resumed["messages"] == [
                WEATHER_QUESTION,
                *([assistant("Searching")] if appends_reply else []),
                user("Never mind."),
            ]

    @pytest.mark.parametrize(
        ("question", "thread"),
        [(WEATHER_QUESTION, continue_from("msg_a")), (user("And in Oakland?"), CREATE)],
        ids=["same_history", "rewritten_history"],
    )
    def test_runner_recognizes_the_reply_in_a_history_built_from_the_parsed_message(
        self, respx_mock: MockRouter, question: BetaMessageParam, thread: dict[str, Any]
    ) -> None:
        reply = message_response("msg_a", tool_use_id="toolu_a").json()
        reply["content"] = [{"type": "text", "text": "Let me look."}, *reply["content"]]
        queue_responses(respx_mock, httpx2.Response(200, json=reply), message_response("msg_b"))
        runner = make_runner()
        message = next(runner)

        runner.set_messages_params(
            lambda params: {**params, "messages": [question, {"role": "assistant", "content": message.content}]}
        )
        runner.until_done()

        body = request_bodies(respx_mock)[1]
        assert body["thread"] == thread
        assert roles(body["messages"]) == (["user"] if thread != CREATE else ["user", "assistant", "user"])

    @pytest.mark.respx()
    def test_bedrock_runner_never_threads(self, respx_mock: MockRouter) -> None:
        respx_mock.post(re.compile(r"https://bedrock-runtime\.us-east-1\.amazonaws\.com/model/.*/invoke")).mock(
            side_effect=[message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b", "Sunny.")]
        )
        client = AnthropicBedrock(
            aws_region="us-east-1", aws_access_key="example-access-key", aws_secret_key="example-secret-key"
        )
        runner = client.beta.messages.tool_runner(
            model="anthropic.claude-sonnet-5",
            max_tokens=1024,
            tools=[beta_tool(get_weather)],
            messages=[WEATHER_QUESTION],
        )

        runner.until_done()

        first, second = request_bodies(respx_mock)
        assert request_threads(respx_mock) == [None, None]
        assert "anthropic_beta" not in first and "anthropic_beta" not in second
        assert request_helper_tags(respx_mock) == [["BetaToolRunner"]] * 2

    @pytest.mark.respx(base_url="https://bedrock-mantle.us-east-1.api.aws/anthropic")
    def test_bedrock_mantle_runner_never_threads(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock, message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b", "Sunny.")
        )
        client = AnthropicBedrockMantle(aws_region="us-east-1", api_key="example-api-key")
        runner = client.beta.messages.tool_runner(
            model="claude-sonnet-5",
            max_tokens=1024,
            tools=[beta_tool(get_weather)],
            messages=[WEATHER_QUESTION],
        )

        runner.until_done()

        assert request_threads(respx_mock) == [None, None]
        assert request_helper_tags(respx_mock) == [["BetaToolRunner"]] * 2

    @pytest.mark.parametrize(
        "make_client",
        [
            lambda: AnthropicBedrock(
                aws_region="us-east-1", aws_access_key="example-access-key", aws_secret_key="example-secret-key"
            ),
            lambda: AnthropicBedrockMantle(aws_region="us-east-1", api_key="example-api-key"),
            lambda: AnthropicVertex(region="us-east5", project_id="example-project", access_token="example-token"),
        ],
        ids=["bedrock", "bedrock_mantle", "vertex"],
    )
    def test_thread_raises_on_clients_without_message_threads(self, make_client: Callable[[], Any]) -> None:
        client = make_client()

        with pytest.raises(AnthropicError, match="Message threads are not available on this client"):
            client.beta.messages.thread(model=MODEL, max_tokens=MAX_TOKENS)
        with pytest.raises(AnthropicError, match="Message threads are not available on this client"):
            BetaMessageThread(client, model=MODEL, max_tokens=MAX_TOKENS)  # type: ignore[arg-type]

    @pytest.mark.respx(base_url="https://example-resource.services.ai.azure.com/anthropic")
    def test_foundry_runner_threads_by_default(self, respx_mock: MockRouter) -> None:
        queue_responses(
            respx_mock, message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b", "Sunny.")
        )
        client = AnthropicFoundry(api_key="example-api-key", resource="example-resource")
        runner = client.beta.messages.tool_runner(
            model="claude-sonnet-5",
            max_tokens=1024,
            tools=[beta_tool(get_weather)],
            messages=[WEATHER_QUESTION],
        )

        runner.until_done()

        assert request_threads(respx_mock) == [CREATE, continue_from("msg_a")]
