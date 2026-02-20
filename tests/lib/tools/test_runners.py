import json
import logging
from typing import Any, Dict, List, Union, cast
from typing_extensions import Literal

import pytest
from inline_snapshot import external, snapshot

from anthropic import Anthropic, AsyncAnthropic, beta_tool, beta_async_tool
from anthropic._utils import assert_signatures_in_sync
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools import BetaFunctionToolResultType
from anthropic.types.beta.beta_message_param import BetaMessageParam
from anthropic.types.beta.beta_tool_result_block_param import BetaToolResultBlockParam

from ..utils import print_obj

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
            """\
ParsedBetaMessage(
    container=None,
    content=[
        ParsedBetaTextBlock(
            citations=None,
            parsed_output=None,
            text='The weather in San Francisco, CA is currently **Sunny** with a temperature of **68°F**.',
            type='text'
        )
    ],
    context_management=None,
    id='msg_01BZsMQjer9AFLgmdRKJ8NcA',
    model='claude-haiku-4-5-20251001',
    role='assistant',
    stop_reason='end_turn',
    stop_sequence=None,
    type='message',
    usage=BetaUsage(
        cache_creation=BetaCacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0),
        cache_creation_input_tokens=0,
        cache_read_input_tokens=0,
        inference_geo='not_available',
        input_tokens=770,
        iterations=None,
        output_tokens=25,
        server_tool_use=None,
        service_tier='standard',
        speed=None
    )
)
"""
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
            "ParsedBetaMessage(container=None, content=[ParsedBetaTextBlock(citations=None, parsed_output=None, text='The weather in San Francisco, CA is currently **20°C** and **Sunny**. Nice weather!', type='text')], context_management=None, id='msg_01DSPL7PHKQYTe9VAFkHzsA3', model='claude-haiku-4-5-20251001', role='assistant', stop_reason='end_turn', stop_sequence=None, type='message', usage=BetaUsage(cache_creation=BetaCacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, cache_read_input_tokens=0, inference_geo=None, input_tokens=787, iterations=None, output_tokens=26, server_tool_use=None, service_tier='standard', speed=None))\n"
        ),
    },
    "streaming": {
        "result": snapshot(
            """\
ParsedBetaMessage(
    container=None,
    content=[
        ParsedBetaTextBlock(
            citations=None,
            parsed_output=None,
            text="The weather in San Francisco, CA is currently **68°F and Sunny**. It's a nice day!",
            type='text'
        )
    ],
    context_management=None,
    id='msg_0158JyopQTFaomteeJoDpS5q',
    model='claude-haiku-4-5-20251001',
    role='assistant',
    stop_reason='end_turn',
    stop_sequence=None,
    type='message',
    usage=BetaUsage(
        cache_creation=BetaCacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0),
        cache_creation_input_tokens=0,
        cache_read_input_tokens=0,
        inference_geo='not_available',
        input_tokens=770,
        iterations=None,
        output_tokens=27,
        server_tool_use=None,
        service_tier='standard',
        speed=None
    )
)
"""
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
    @pytest.mark.parametrize(
        "http_snapshot",
        [
            cast(Any, external("uuid:b38bbf6c-9a76-40ca-b09d-7a3911776e0f.json")),
        ],
    )
    def test_basic_call_sync(self, snapshot_client: Anthropic) -> None:
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

        message = snapshot_client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        ).until_done()

        assert print_obj(message) == snapshots["basic"]["result"]

    @pytest.mark.parametrize(
        "http_snapshot",
        [
            cast(Any, external("uuid:10e53c1d-51be-4c64-b5bf-99adb3fa4719.json")),
        ],
    )
    def test_tool_call_error(
        self,
        snapshot_client: Anthropic,
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

        runner = snapshot_client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        )

        actual_responses: List[Union[BetaMessageParam, None]] = []
        with caplog.at_level(logging.ERROR):
            for _ in runner:
                tool_call_response = runner.generate_tool_call_response()
                if tool_call_response is not None:
                    actual_responses.append(tool_call_response)

        message = actual_responses

        assert caplog.record_tuples == [
            (
                "anthropic.lib.tools._beta_runner",
                logging.ERROR,
                "Error occurred while calling tool: get_weather",
            ),
        ]
        assert print_obj(message) == snapshot(
            """\
[
    {
        'role': 'user',
        'content': [
            {
                'type': 'tool_result',
                'tool_use_id': 'toolu_01A9HHF5Ezy3oBrKmSgfASm9',
                'content': "RuntimeError('Unexpected error, try again')",
                'is_error': True
            }
        ]
    }
]
"""
        )

    @pytest.mark.parametrize(
        "http_snapshot",
        [
            cast(Any, external("uuid:f59a9391-643b-422c-96dc-1f28bc7ea4d7.json")),
        ],
    )
    # TODO: fix the append_messages method
    @pytest.mark.xfail(reason="bug in append messages")
    def test_custom_message_handling(self, snapshot_client: Anthropic) -> None:
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

        runner = snapshot_client.beta.messages.tool_runner(
            model="claude-haiku-4-5",
            messages=[{"role": "user", "content": "What's the weather in SF in Celsius?"}],
            tools=[get_weather],
            max_tokens=1024,
        )

        for message_iter in runner:
            if message_iter.content[0].type == "tool_use":
                runner.append_messages(
                    BetaMessageParam(
                        role="user",
                        content=[
                            BetaToolResultBlockParam(
                                tool_use_id=message_iter.content[0].id,
                                content="The weather in San Francisco, CA is currently sunny with a temperature of 20°C.",
                                type="tool_result",
                            )
                        ],
                    ),
                )

        message = runner.until_done()

        assert print_obj(message) == snapshots["custom"]["result"]

    @pytest.mark.parametrize(
        "http_snapshot",
        [
            cast(Any, external("uuid:a8ac789b-f856-48cd-9ff3-d5f36799e432.json")),
        ],
    )
    def test_tool_call_caching(self, snapshot_client: Anthropic) -> None:
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

        runner = snapshot_client.beta.messages.tool_runner(
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

    @pytest.mark.parametrize(
        "http_snapshot",
        [
            cast(Any, external("uuid:771c64ff-a0af-4cd9-8080-a5a539da7cb9.json")),
        ],
    )
    def test_streaming_call_sync(self, snapshot_client: Anthropic) -> None:
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

        last_response_messsage = snapshot_client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
            stream=True,
        ).until_done()

        assert print_obj(last_response_messsage) == snapshots["streaming"]["result"]

    @pytest.mark.parametrize(
        "http_snapshot",
        [
            cast(Any, external("uuid:e075a6c2-de4d-4125-9709-f0e178058190.json")),
        ],
    )
    def test_max_iterations(self, snapshot_client: Anthropic) -> None:
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

        runner = snapshot_client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather],
            messages=[
                {
                    "role": "user",
                    "content": (
                        "What's the weather in San Francisco, New York, London, Tokyo and Paris?"
                        "If you need to use tools, call only one tool at a time. Wait for the tool's"
                        "response before making another call. Never call multiple tools at once."
                    ),
                }
            ],
            max_iterations=2,
        )

        answers: List[Union[BetaMessageParam, None]] = []

        for _ in runner:
            answers.append(runner.generate_tool_call_response())

        assert print_obj(answers) == snapshot(
            """\
[
    {
        'role': 'user',
        'content': [
            {
                'type': 'tool_result',
                'tool_use_id': 'toolu_01LRanfq6DmHn1yDTB4d1SAh',
                'content': '{"location": "San Francisco, CA", "temperature": "68\\\\u00b0F", "condition": "Sunny"}'
            }
        ]
    },
    {
        'role': 'user',
        'content': [
            {
                'type': 'tool_result',
                'tool_use_id': 'toolu_01RWdcDdE8NAFDgZ8F9Xk2K7',
                'content': '{"location": "New York, NY", "temperature": "68\\\\u00b0F", "condition": "Sunny"}'
            }
        ]
    }
]
"""
        )

    @pytest.mark.parametrize(
        "http_snapshot",
        [
            cast(Any, external("uuid:555fb399-a54c-455b-9ac5-2c9673f18e12.json")),
        ],
    )
    def test_streaming_call_sync_events(self, snapshot_client: Anthropic) -> None:
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

        events: list[str] = []
        runner = snapshot_client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
            stream=True,
        )

        for stream in runner:
            for event in stream:
                events.append(event.type)

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

    @pytest.mark.parametrize(
        "http_snapshot",
        [
            cast(Any, external("uuid:956fa2fe-8752-4f7c-8f9a-33735e62b898.json")),
        ],
    )
    def test_compaction_control(self, snapshot_client: Anthropic, caplog: pytest.LogCaptureFixture) -> None:
        @beta_tool
        def submit_analysis(summary: str) -> str:  # noqa: ARG001
            """Call this LAST with your final analysis."""
            return "Analysis submitted"

        runner = snapshot_client.beta.messages.tool_runner(
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
            betas=["structured-outputs-2025-12-15"],
            compaction_control={"enabled": True, "context_token_threshold": 500},
            max_iterations=1,
        )

        with caplog.at_level(logging.INFO, logger="anthropic.lib.tools._beta_runner"):
            next(runner)
            runner.until_done()

        messages = list(runner._params["messages"])
        assert len(messages) == 1
        assert messages[0]["role"] == "user"

        content = list(messages[0]["content"])[0]
        assert isinstance(content, dict)
        assert content["type"] == "text"
        assert content["text"] == snapshot("""\
<summary>
## Task Overview
The user requests a detailed 500-word essay about dogs, cats, and birds, followed by a single call to the `submit_analysis` tool at the end containing information about all three animals. \n\

**Key Requirements:**
- Essay must be 500 words in length
- Cover dogs, cats, and birds
- Call `submit_analysis` tool only once at the completion
- The tool call should contain information about all three animals

## Current State
**Status:** Not started - no work has been completed yet.

**Completed:**
- None

**Artifacts Produced:**
- None

## Important Discoveries
**Unknown Information:**
- The exact structure/parameters expected by the `submit_analysis` tool (need to determine what format the tool accepts)
- Whether the tool requires specific data fields for each animal or free-form text
- The level of detail expected in the analysis (scientific, casual, comparative, etc.)

**Assumptions to Verify:**
- The essay should likely compare/contrast the three animals as pets or discuss their characteristics
- The `submit_analysis` tool probably accepts structured data about the animals

## Next Steps
1. **Write the 500-word essay** covering:
   - Dogs (characteristics, behavior, role as pets)
   - Cats (characteristics, behavior, role as pets)
   - Birds (characteristics, behavior, role as pets)
   - Potentially comparative elements between the three

2. **Determine the `submit_analysis` tool structure** - check what parameters it accepts

3. **Call `submit_analysis` once** with comprehensive information about all three animals in the appropriate format

4. **Verify word count** is approximately 500 words before submitting

## Context to Preserve
- User emphasized calling the tool "only once at the end" - this is a specific constraint to respect
- The tool should contain information about "all three animals" - comprehensive coverage required
- Essay should be "detailed" - suggests substantive content rather than superficial treatment

## Priority
High priority on understanding the `submit_analysis` tool parameters before writing the essay, as the content may need to be structured to align with tool requirements.
</summary>\
""")
        assert caplog.record_tuples == snapshot(
            [
                (
                    "anthropic.lib.tools._beta_runner",
                    20,
                    "Token usage 1612 has exceeded the threshold of 500. Performing compaction.",
                ),
                ("anthropic.lib.tools._beta_runner", 20, "Compaction complete. New token usage: 486"),
            ]
        )

    @pytest.mark.parametrize("snapshot_client", [False], indirect=True)
    @pytest.mark.parametrize(
        "http_snapshot",
        [
            cast(Any, external("uuid:32da0815-2270-4d29-87be-3b5b63ab42e2.json")),
        ],
    )
    def test_server_side_tool(
        self,
        snapshot_client: Anthropic,
    ) -> None:
        runner = snapshot_client.beta.messages.tool_runner(
            model="claude-haiku-4-5",
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
            tools=[
                {
                    "type": "web_search_20250305",
                    "name": "web_search",
                }
            ],
            max_tokens=1024,
        )

        message = next(runner)

        content_types = [content.type for content in message.content]

        assert "server_tool_use" in content_types
        assert "web_search_tool_result" in content_types


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.parametrize(
    "http_snapshot",
    [
        cast(Any, external("uuid:64fe7974-681a-4023-9848-b32ba39c8664.json")),
    ],
)
async def test_basic_call_async(async_snapshot_client: AsyncAnthropic) -> None:
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

    await async_snapshot_client.beta.messages.tool_runner(
        max_tokens=1024,
        model="claude-haiku-4-5",
        tools=[get_weather],
        messages=[{"role": "user", "content": "What is the weather in SF?"}],
    ).until_done()


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
