from __future__ import annotations

import re
import json
from typing import Any, Callable

import httpx2
import pytest
from respx import MockRouter

from anthropic import AnthropicError, AnthropicVertex, AnthropicBedrock, AnthropicFoundry, AnthropicBedrockMantle
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools import beta_tool
from anthropic.types.beta import BetaMessageParam
from anthropic.lib.threads import BetaMessageThread

from .helpers import (
    MODEL,
    CREATE,
    FALLBACKS,
    MAX_TOKENS,
    THREADS_BETA,
    FALLBACK_BETA,
    RESPONSE_KINDS,
    THREAD_NOT_FOUND,
    WEATHER_QUESTION,
    INLINE_TOOLS_BETA,
    FALLBACK_ITERATIONS,
    CONTEXT_MANAGEMENT_BETA,
    STRUCTURED_OUTPUTS_BETA,
    Forecast,
    user,
    roles,
    lookup,
    marked,
    base_url,
    tool_use,
    id_headers,
    get_weather,
    make_runner,
    tool_result,
    response_ids,
    continue_from,
    request_betas,
    request_bodies,
    queue_responses,
    request_threads,
    stream_response,
    message_response,
    tool_change_turns,
    request_helper_tags,
    tool_change_replies,
    unsupported_response,
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

    def test_runner_set_messages_params_with_the_callers_own_history_continues_the_thread(
        self, respx_mock: MockRouter
    ) -> None:
        queue_responses(respx_mock, message_response("msg_a", tool_use_id="toolu_a"), message_response("msg_b"))
        history = [user("A"), user("B")]
        runner = make_runner(messages=history)
        reply = next(runner)

        runner.set_messages_params(
            lambda params: {
                **params,
                "messages": [*history, {"role": "assistant", "content": reply.content}, user("C")],
            }
        )
        runner.until_done()

        continued = request_bodies(respx_mock)[1]
        assert continued["thread"] == continue_from("msg_a")
        assert continued["messages"] == [tool_result("toolu_a"), user("C")]

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
