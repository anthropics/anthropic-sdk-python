import json
import logging
from typing import Any, Dict, List, Union
from typing_extensions import Literal, TypeVar

import pytest
from respx import MockRouter
from inline_snapshot import external, snapshot

from anthropic import Anthropic, AsyncAnthropic, beta_tool, beta_async_tool
from anthropic._utils import assert_signatures_in_sync
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools import BetaFunctionToolResultType
from anthropic.lib.tools._beta_runner import BetaToolRunner
from anthropic.types.beta.beta_message import BetaMessage
from anthropic.types.beta.beta_message_param import BetaMessageParam
from anthropic.types.beta.beta_tool_result_block_param import BetaToolResultBlockParam

from ..utils import print_obj
from ...conftest import base_url
from ..snapshots import make_snapshot_request, make_async_snapshot_request, make_stream_snapshot_request

_T = TypeVar("_T")

# all the snapshots in this file are auto-generated from the live API
#
# you can update them with
#
# `ANTHROPIC_LIVE=1 ./scripts/test --inline-snapshot=fix -n0`

snapshots = {
    "basic": {
        "responses": snapshot(
            [
                '{"model": "claude-haiku-4-5-20251001", "id": "msg_0133AjAuLSKXatUZqNkpALPx", "type": "message", "role": "assistant", "content": [{"type": "tool_use", "id": "toolu_01DGiQScbZKPwUBYN79rFUb8", "name": "get_weather", "input": {"location": "San Francisco, CA", "units": "f"}}], "stop_reason": "tool_use", "stop_sequence": null, "usage": {"input_tokens": 656, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 74, "service_tier": "standard"}}',
                '{"model": "claude-haiku-4-5-20251001", "id": "msg_014x2Sxq2p6sewFyUbJp8Mg3", "type": "message", "role": "assistant", "content": [{"type": "text", "text": "The weather in San Francisco, CA is currently **68\\u00b0F** and **Sunny**. It\'s a nice day! \\u2600\\ufe0f"}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 770, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 33, "service_tier": "standard"}}',
            ]
        ),
        "result": snapshot(
            "ParsedBetaMessage(container=None, content=[ParsedBetaTextBlock(citations=None, parsed_output=None, text=\"The weather in San Francisco, CA is currently **68°F** and **Sunny**. It's a nice day! ☀️\", type='text')], context_management=None, id='msg_014x2Sxq2p6sewFyUbJp8Mg3', model='claude-haiku-4-5-20251001', role='assistant', stop_reason='end_turn', stop_sequence=None, type='message', usage=BetaUsage(cache_creation=BetaCacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, cache_read_input_tokens=0, input_tokens=770, output_tokens=33, server_tool_use=None, service_tier='standard'))\n"
        ),
    },
    "custom": {
        "responses": snapshot(
            [
                '{"model": "claude-haiku-4-5-20251001", "id": "msg_01FKEKbzbqHmJv5ozwH7tz99", "type": "message", "role": "assistant", "content": [{"type": "text", "text": "Let me check the weather for San Francisco for you in Celsius."}, {"type": "tool_use", "id": "toolu_01MxFFv4azdWzubHT3dXurMY", "name": "get_weather", "input": {"location": "San Francisco, CA", "units": "c"}}], "stop_reason": "tool_use", "stop_sequence": null, "usage": {"input_tokens": 659, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 88, "service_tier": "standard"}}',
                '{"model": "claude-haiku-4-5-20251001", "id": "msg_01DSPL7PHKQYTe9VAFkHzsA3", "type": "message", "role": "assistant", "content": [{"type": "text", "text": "The weather in San Francisco, CA is currently **20\\u00b0C** and **Sunny**. Nice weather!"}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 787, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 26, "service_tier": "standard"}}',
            ]
        ),
        "result": snapshot(
            "ParsedBetaMessage(container=None, content=[ParsedBetaTextBlock(citations=None, parsed_output=None, text='The weather in San Francisco, CA is currently **20°C** and **Sunny**. Nice weather!', type='text')], context_management=None, id='msg_01DSPL7PHKQYTe9VAFkHzsA3', model='claude-haiku-4-5-20251001', role='assistant', stop_reason='end_turn', stop_sequence=None, type='message', usage=BetaUsage(cache_creation=BetaCacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, cache_read_input_tokens=0, input_tokens=787, output_tokens=26, server_tool_use=None, service_tier='standard'))\n"
        ),
    },
    "streaming": {
        "result": snapshot(
            "ParsedBetaMessage(container=None, content=[ParsedBetaTextBlock(citations=None, parsed_output=None, text='The weather in San Francisco, CA is currently **Sunny** with a temperature of **68°F**.', type='text')], context_management=None, id='msg_01Vm8Ddgc8qm4iuUSKbf6jku', model='claude-haiku-4-5-20251001', role='assistant', stop_reason='end_turn', stop_sequence=None, type='message', usage=BetaUsage(cache_creation=BetaCacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, cache_read_input_tokens=0, input_tokens=781, output_tokens=25, server_tool_use=None, service_tier='standard'))\n"
        )
    },
    "tool_call": {
        "responses": snapshot(
            [
                '{"model": "claude-haiku-4-5-20251001", "id": "msg_01NzLkujbJ7VQgzNHFx76Ab4", "type": "message", "role": "assistant", "content": [{"type": "tool_use", "id": "toolu_01SPe52JjANtJDVJ5yUZj4jz", "name": "get_weather", "input": {"location": "SF", "units": "c"}}], "stop_reason": "tool_use", "stop_sequence": null, "usage": {"input_tokens": 597, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 71, "service_tier": "standard"}}',
                '{"model": "claude-haiku-4-5-20251001", "id": "msg_016bjf5SAczxp28ES4yX7Z7U", "type": "message", "role": "assistant", "content": [{"type": "text", "text": "The weather in SF (San Francisco) is currently **20\\u00b0C** and **sunny**!"}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 705, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 23, "service_tier": "standard"}}',
            ]
        ),
    },
    "tool_call_error": {
        "responses": snapshot(
            [
                '{"model": "claude-haiku-4-5-20251001", "id": "msg_01QhmJFoA3mxD2mxPFnjLHrT", "type": "message", "role": "assistant", "content": [{"type": "tool_use", "id": "toolu_01Do4cDVNxt51EuosKoxdmii", "name": "get_weather", "input": {"location": "San Francisco, CA", "units": "f"}}], "stop_reason": "tool_use", "stop_sequence": null, "usage": {"input_tokens": 656, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 74, "service_tier": "standard"}}',
                '{"model": "claude-haiku-4-5-20251001", "id": "msg_0137FupJYD4A3Mc6jUUxKpU6", "type": "message", "role": "assistant", "content": [{"type": "text", "text": "I apologize, but I encountered an error when trying to fetch the weather for San Francisco. This appears to be a temporary issue with the weather service. Could you please try again in a moment, or let me know if you\'d like me to attempt the lookup again?"}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 760, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 58, "service_tier": "standard"}}',
            ]
        )
    },
}


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
class TestSyncRunTools:
    @pytest.mark.respx(base_url=base_url)
    def test_basic_call_sync(self, client: Anthropic, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch) -> None:
        @beta_tool
        def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
            """Lookup the weather for a given city in either celsius or fahrenheit

            Args:
                location: The city and state, e.g. San Francisco, CA
                units: Unit for the output, either 'c' for celsius or 'f' for fahrenheit
            Returns:
                A dictionary containing the location, temperature, and weather condition.
            """
            return json.dumps(_get_weather(location, units))

        message = make_snapshot_request(
            lambda c: c.beta.messages.tool_runner(
                max_tokens=1024,
                model="claude-haiku-4-5",
                tools=[get_weather],
                messages=[{"role": "user", "content": "What is the weather in SF?"}],
            ).until_done(),
            content_snapshot=snapshots["basic"]["responses"],
            path="/v1/messages",
            mock_client=client,
            respx_mock=respx_mock,
        )

        assert print_obj(message, monkeypatch) == snapshots["basic"]["result"]

    @pytest.mark.respx(base_url=base_url)
    def test_tool_call_error(
        self,
        client: Anthropic,
        respx_mock: MockRouter,
        monkeypatch: pytest.MonkeyPatch,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        called = None

        @beta_tool
        def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
            """Lookup the weather for a given city in either celsius or fahrenheit

            Args:
                location: The city and state, e.g. San Francisco, CA
                units: Unit for the output, either 'c' for celsius or 'f' for fahrenheit
            Returns:
                A dictionary containing the location, temperature, and weather condition.
            """
            nonlocal called

            if called is None:
                called = True
                raise RuntimeError("Unexpected error, try again")
            return json.dumps(_get_weather(location, units))

        def tool_runner(client: Anthropic) -> List[Union[BetaMessageParam, None]]:
            runner = client.beta.messages.tool_runner(
                max_tokens=1024,
                model="claude-haiku-4-5",
                tools=[get_weather],
                messages=[{"role": "user", "content": "What is the weather in SF?"}],
            )

            actual_responses: List[Union[BetaMessageParam, None]] = []
            for _ in runner:
                tool_call_response = runner.generate_tool_call_response()
                if tool_call_response is not None:
                    actual_responses.append(tool_call_response)

            return actual_responses

        with caplog.at_level(logging.ERROR):
            message = make_snapshot_request(
                tool_runner,
                content_snapshot=snapshots["tool_call_error"]["responses"],
                path="/v1/messages",
                mock_client=client,
                respx_mock=respx_mock,
            )

        assert caplog.record_tuples == [
            (
                "anthropic.lib.tools._beta_runner",
                logging.ERROR,
                "Error occurred while calling tool: get_weather",
            ),
        ]
        assert print_obj(message, monkeypatch) == snapshot(
            "[{'role': 'user', 'content': [{'type': 'tool_result', 'tool_use_id': 'toolu_01Do4cDVNxt51EuosKoxdmii', 'content': \"RuntimeError('Unexpected error, try again')\", 'is_error': True}]}]\n"
        )

    @pytest.mark.respx(base_url=base_url)
    def test_custom_message_handling(
        self, client: Anthropic, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        @beta_tool
        def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
            """Lookup the weather for a given city in either celsius or fahrenheit

            Args:
                location: The city and state, e.g. San Francisco, CA
                units: Unit for the output, either 'c' for celsius or 'f' for fahrenheit
            Returns:
                A dictionary containing the location, temperature, and weather condition.
            """
            return json.dumps(_get_weather(location, units))

        def custom_message_handling(client: Anthropic) -> BetaMessage:
            runner = client.beta.messages.tool_runner(
                model="claude-haiku-4-5",
                messages=[{"role": "user", "content": "What's the weather in SF in Celsius?"}],
                tools=[get_weather],
                max_tokens=1024,
            )

            for message in runner:
                # handle only where there is a tool call
                if message.content[0].type == "tool_use":
                    runner.append_messages(
                        BetaMessageParam(
                            role="assistant",
                            content=[
                                BetaToolResultBlockParam(
                                    tool_use_id=message.content[0].id,
                                    content="The weather in San Francisco, CA is currently sunny with a temperature of 20°C.",
                                    type="tool_result",
                                )
                            ],
                        ),
                    )

            return runner.until_done()

        message = make_snapshot_request(
            custom_message_handling,
            content_snapshot=snapshots["custom"]["responses"],
            path="/v1/messages",
            mock_client=client,
            respx_mock=respx_mock,
        )

        assert print_obj(message, monkeypatch) == snapshots["custom"]["result"]

    @pytest.mark.respx(base_url=base_url)
    def test_tool_call_caching(self, client: Anthropic, respx_mock: MockRouter) -> None:
        called = None

        @beta_tool
        def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
            nonlocal called
            """Lookup the weather for a given city in either celsius or fahrenheit

            Args:
                location: The city and state, e.g. San Francisco, CA
                units: Unit for the output, either 'c' for celsius or 'f' for fahrenheit
            Returns:
                A dictionary containing the location, temperature, and weather condition.
            """
            if called is None:
                called = True
                return json.dumps(_get_weather(location, units))
            raise RuntimeError("This tool should not be called again")

        def tool_runner(client: Anthropic) -> None:
            runner = client.beta.messages.tool_runner(
                model="claude-haiku-4-5",
                messages=[{"role": "user", "content": "What's the weather in SF in Celsius?"}],
                tools=[get_weather],
                max_tokens=1024,
            )

            for _ in runner:
                response1 = runner.generate_tool_call_response()
                response2 = runner.generate_tool_call_response()

                if response1 is not None:
                    assert response1 is response2

        make_snapshot_request(
            tool_runner,
            content_snapshot=snapshots["tool_call"]["responses"],
            path="/v1/messages",
            mock_client=client,
            respx_mock=respx_mock,
        )

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_call_sync(
        self, client: Anthropic, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        @beta_tool
        def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
            """Lookup the weather for a given city in either celsius or fahrenheit

            Args:
                location: The city and state, e.g. San Francisco, CA
                units: Unit for the output, either 'c' for celsius or 'f' for fahrenheit
            Returns:
                A dictionary containing the location, temperature, and weather condition.
            """
            return json.dumps(_get_weather(location, units))

        last_response_messsage = make_stream_snapshot_request(
            lambda c: c.beta.messages.tool_runner(
                max_tokens=1024,
                model="claude-haiku-4-5",
                tools=[get_weather],
                messages=[{"role": "user", "content": "What is the weather in SF?"}],
                stream=True,
            ).until_done(),
            content_snapshot=external("hash:cd8d3d185e7a*.json"),
            path="/v1/messages",
            mock_client=client,
            respx_mock=respx_mock,
        )

        assert print_obj(last_response_messsage, monkeypatch) == snapshots["streaming"]["result"]

    @pytest.mark.respx(base_url=base_url)
    def test_max_iterations(self, client: Anthropic, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch) -> None:
        @beta_tool
        def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
            """Lookup the weather for a given city in either celsius or fahrenheit

            Args:
                location: The city and state, e.g. San Francisco, CA
                units: Unit for the output, either 'c' for celsius or 'f' for fahrenheit
            Returns:
                A dictionary containing the location, temperature, and weather condition.
            """
            return json.dumps(_get_weather(location, units))

        def get_weather_answers(client: Anthropic) -> List[Union[BetaMessageParam, None]]:
            runner = client.beta.messages.tool_runner(
                max_tokens=1024,
                model="claude-haiku-4-5",
                tools=[get_weather],
                messages=[
                    {
                        "role": "user",
                        "content": (
                            "What's the weather in San Francisco, New York, London, Tokyo and Paris?"
                            "If you need to use tools, call only one tool at a time. Wait for the tool’s"
                            "response before making another call. Never call multiple tools at once."
                        ),
                    }
                ],
                max_iterations=2,
            )

            answers: List[Union[BetaMessageParam, None]] = []

            for _ in runner:
                answers.append(runner.generate_tool_call_response())

            return answers

        answers = make_snapshot_request(
            get_weather_answers,
            content_snapshot=snapshot(
                [
                    '{"model": "claude-haiku-4-5-20251001", "id": "msg_017GvdrboNn8hipoMJUcK8m6", "type": "message", "role": "assistant", "content": [{"type": "text", "text": "I\'ll get the weather for each of these cities one at a time. Let me start with San Francisco."}, {"type": "tool_use", "id": "toolu_011Q6hjHnpWegJvV1Zn6Cm1h", "name": "get_weather", "input": {"location": "San Francisco, CA", "units": "f"}}], "stop_reason": "tool_use", "stop_sequence": null, "usage": {"input_tokens": 701, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 96, "service_tier": "standard"}}',
                    '{"model": "claude-haiku-4-5-20251001", "id": "msg_01PYFQH4AkK3NBgSpFkWD16q", "type": "message", "role": "assistant", "content": [{"type": "text", "text": "Now let me check New York."}, {"type": "tool_use", "id": "toolu_011QaaAuMeNWTwHjkxcxce1D", "name": "get_weather", "input": {"location": "New York, NY", "units": "f"}}], "stop_reason": "tool_use", "stop_sequence": null, "usage": {"input_tokens": 837, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 81, "service_tier": "standard"}}',
                ]
            ),
            path="/v1/messages",
            mock_client=client,
            respx_mock=respx_mock,
        )

        assert print_obj(answers, monkeypatch) == snapshot(
            "[{'role': 'user', 'content': [{'type': 'tool_result', 'tool_use_id': 'toolu_011Q6hjHnpWegJvV1Zn6Cm1h', 'content': '{\"location\": \"San Francisco, CA\", \"temperature\": \"68\\\\u00b0F\", \"condition\": \"Sunny\"}'}]}, {'role': 'user', 'content': [{'type': 'tool_result', 'tool_use_id': 'toolu_011QaaAuMeNWTwHjkxcxce1D', 'content': '{\"location\": \"New York, NY\", \"temperature\": \"68\\\\u00b0F\", \"condition\": \"Sunny\"}'}]}]\n"
        )

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_call_sync_events(self, client: Anthropic, respx_mock: MockRouter) -> None:
        @beta_tool
        def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
            """Lookup the weather for a given city in either celsius or fahrenheit

            Args:
                location: The city and state, e.g. San Francisco, CA
                units: Unit for the output, either 'c' for celsius or 'f' for fahrenheit
            Returns:
                A dictionary containing the location, temperature, and weather condition.
            """
            return json.dumps(_get_weather(location, units))

        def accumulate_events(client: Anthropic) -> List[str]:
            events: list[str] = []
            runner = client.beta.messages.tool_runner(
                max_tokens=1024,
                model="claude-haiku-4-5",
                tools=[get_weather],
                messages=[{"role": "user", "content": "What is the weather in SF?"}],
                stream=True,
            )

            for stream in runner:
                for event in stream:
                    events.append(event.type)
            return events

        events = make_stream_snapshot_request(
            accumulate_events,
            content_snapshot=external("uuid:9cb114c8-69bd-4111-841b-edee30333afd.json"),
            path="/v1/messages",
            mock_client=client,
            respx_mock=respx_mock,
        )
        assert set(events) == snapshot(
            {
                "content_block_delta",
                "content_block_start",
                "content_block_stop",
                "input_json",
                "message_delta",
                "message_start",
                "message_stop",
                "text",
            }
        )

    @pytest.mark.respx(base_url=base_url)
    def test_compaction_control(
        self, client: Anthropic, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        @beta_tool
        def submit_analysis(summary: str) -> str:  # noqa: ARG001
            """Call this LAST with your final analysis."""
            return "Analysis submitted"

        def tool_runner(client: Anthropic) -> BetaToolRunner[None]:
            runner = client.beta.messages.tool_runner(
                model="claude-sonnet-4-5",
                max_tokens=4000,
                tools=[submit_analysis],
                messages=[
                    {
                        "role": "user",
                        "content": (
                            "Write a detailed 500 word essay about dogs, cats, and birds. "
                            "Call the tool submit_analysis with the information about all three animals. "
                            "Note that you should call it only once at the end of your essay."
                        ),
                    }
                ],
                betas=["structured-outputs-2025-11-13"],
                compaction_control={"enabled": True, "context_token_threshold": 500},
                max_iterations=1,
            )

            next(runner)
            runner.until_done()
            return runner

        with caplog.at_level(logging.INFO, logger="anthropic.lib.tools._beta_runner"):
            runner = make_snapshot_request(
                tool_runner,
                content_snapshot=external("uuid:ab7b2edd-9c2d-4f53-9c04-92bb659b9caa.json"),
                path="/v1/messages",
                mock_client=client,
                respx_mock=respx_mock,
            )

        messages = list(runner._params["messages"])
        assert len(messages) == 1
        assert messages[0]["role"] == "user"

        content = list(messages[0]["content"])[0]
        assert isinstance(content, dict)
        assert content["type"] == "text"
        assert content["text"] == snapshot("""\
<summary>
## 1. Task Overview
The user requests a 500-word essay about dogs, cats, and birds, followed by a single call to the `submit_analysis` tool at the end containing information about all three animals. \n\

**Key constraints:**
- Essay must be detailed and approximately 500 words
- Must cover all three animals: dogs, cats, and birds
- Tool `submit_analysis` must be called exactly once, at the end
- Tool call should contain information about all three animals

## 2. Current State
**Completed:** Nothing has been completed yet.

**Status:** The task has been acknowledged but no essay has been written and no tool has been called.

**Artifacts produced:** None yet.

## 3. Important Discoveries
**Technical requirements:**
- Need to understand the parameters/schema for `submit_analysis` tool (not yet verified)
- Must structure the tool call to include data about all three animal types in a single invocation

**Approach to take:**
- Write a comprehensive 500-word essay discussing dogs, cats, and birds
- Essay should cover characteristics, behaviors, and comparisons between the three
- Extract/organize key information about each animal for the tool call
- Call `submit_analysis` once with consolidated data about all three animals

## 4. Next Steps
1. **Write the 500-word essay** covering:
   - Dogs: characteristics, behavior, relationship with humans
   - Cats: characteristics, behavior, relationship with humans
   - Birds: characteristics, behavior, diversity
   - Comparisons and contrasts between the three
   \n\
2. **Determine the schema for `submit_analysis` tool** - check what parameters it accepts and how to structure data about multiple animals

3. **Call `submit_analysis` once** with information about all three animals in the appropriate format

4. **Verify word count** is approximately 500 words

## 5. Context to Preserve
- User emphasized calling the tool "only once at the end"
- Essay should be "detailed" - not superficial
- The tool call must encompass information about all three animals, not separate calls per animal
- This appears to be a test of following multi-step instructions precisely
</summary>\
""")
        assert caplog.record_tuples == snapshot(
            [
                (
                    "anthropic.lib.tools._beta_runner",
                    20,
                    "Token usage 1615 has exceeded the threshold of 500. Performing compaction.",
                ),
                ("anthropic.lib.tools._beta_runner", 20, "Compaction complete. New token usage: 496"),
            ]
        )


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
async def test_basic_call_async(
    async_client: AsyncAnthropic, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
) -> None:
    @beta_async_tool
    async def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
        """Lookup the weather for a given city in either celsius or fahrenheit

        Args:
            location: The city and state, e.g. San Francisco, CA
            units: Unit for the output, either 'c' for celsius or 'f' for fahrenheit
        Returns:
            A dictionary containing the location, temperature, and weather condition.
        """
        return json.dumps(_get_weather(location, units))

    message = await make_async_snapshot_request(
        lambda c: c.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-3-7",
            tools=[get_weather],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        ).until_done(),
        content_snapshot=snapshots["basic"]["responses"],
        path="/v1/messages",
        mock_client=async_client,
        respx_mock=respx_mock,
    )

    assert print_obj(message, monkeypatch) == snapshots["basic"]["result"]


def _get_weather(location: str, units: Literal["c", "f"]) -> Dict[str, Any]:
    # Simulate a weather API call
    print(f"Fetching weather for {location} in {units}")

    if units == "c":
        return {
            "location": location,
            "temperature": "20°C",
            "condition": "Sunny",
        }
    else:
        return {
            "location": location,
            "temperature": "68°F",
            "condition": "Sunny",
        }


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
def test_tool_runner_method_in_sync(sync: bool, client: Anthropic, async_client: AsyncAnthropic) -> None:
    checking_client: "Anthropic | AsyncAnthropic" = client if sync else async_client

    assert_signatures_in_sync(
        checking_client.beta.messages.create,
        checking_client.beta.messages.tool_runner,
        exclude_params={
            "tools",
            "output_format",
            # TODO
            "stream",
        },
    )
