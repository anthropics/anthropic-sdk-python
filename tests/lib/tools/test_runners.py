import json
import logging
from typing import Any, Dict, List, Union, cast
from typing_extensions import Literal, TypeVar

import pytest
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

_T = TypeVar("_T")

# all the snapshots in this file are auto-generated from the live API,
# you can update them with
# `./scripts/test --inline-snapshot=fix -n0 --http-record`


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
class TestSyncRunTools:
    @pytest.mark.parametrize(
        "http_snapshot",
        [cast(Any, external("uuid:ad005e89-f72b-4f0e-941a-9ec3473c1bc8.json"))],
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

        assert print_obj(message) == snapshot(
            """\
ParsedBetaMessage(
    container=None,
    content=[
        ParsedBetaTextBlock(
            citations=None,
            parsed_output=None,
            text='The weather in San Francisco is currently **68°F and Sunny**. Great day to be out and about!',
            type='text'
        )
    ],
    context_management=None,
    id='msg_01FvTMNojoLmBYw4KxJXB27y',
    model='claude-haiku-4-5-20251001',
    role='assistant',
    stop_reason='end_turn',
    stop_sequence=None,
    type='message',
    usage=BetaUsage(
        cache_creation=BetaCacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0),
        cache_creation_input_tokens=0,
        cache_read_input_tokens=0,
        input_tokens=770,
        output_tokens=27,
        server_tool_use=None,
        service_tier='standard'
    )
)
"""
        )

    @pytest.mark.parametrize(
        "http_snapshot",
        [
            cast(Any, external("uuid:6cd089e9-1c08-40a5-851d-c272b3f1c248.json")),
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

        def tool_runner(client: Anthropic) -> List[Union[BetaMessageParam, None]]:
            runner = client.beta.messages.tool_runner(
                max_tokens=1024,
                model="claude-3-5-haiku-latest",
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
            message = tool_runner(snapshot_client)
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
                'tool_use_id': 'toolu_01Not8sU7rvvvixVRigDz1ee',
                'content': "RuntimeError('Unexpected error, try again')",
                'is_error': True
            }
        ]
    },
    {
        'role': 'user',
        'content': [
            {
                'type': 'tool_result',
                'tool_use_id': 'toolu_01LJTxn5gThzGiq5MgRfbogp',
                'content': '{"location": "San Francisco, CA", "temperature": "68\\\\u00b0F", "condition": "Sunny"}'
            }
        ]
    }
]
"""
        )

    @pytest.mark.parametrize(
        "http_snapshot",
        [cast(Any, external("uuid:f1c3350a-cdb1-4508-a208-18544b825a9e.json"))],
    )
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
                        message,
                        BetaMessageParam(
                            role="user",
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

        message = custom_message_handling(snapshot_client)
        assert print_obj(message) == snapshot(
            """\
ParsedBetaMessage(
    container=None,
    content=[
        ParsedBetaTextBlock(
            citations=None,
            parsed_output=None,
            text='The weather in San Francisco, CA is currently **sunny** with a temperature of **20°C**.',
            type='text'
        )
    ],
    context_management=None,
    id='msg_01K4waJ1jAaJvWS9uatX5ANU',
    model='claude-haiku-4-5-20251001',
    role='assistant',
    stop_reason='end_turn',
    stop_sequence=None,
    type='message',
    usage=BetaUsage(
        cache_creation=BetaCacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0),
        cache_creation_input_tokens=0,
        cache_read_input_tokens=0,
        input_tokens=763,
        output_tokens=24,
        server_tool_use=None,
        service_tier='standard'
    )
)
"""
        )

    @pytest.mark.parametrize(
        "http_snapshot",
        [cast(Any, external("uuid:6401445a-5758-4777-9778-3008bae873ec.json"))],
    )
    def test_tool_call_caching(
        self,
        snapshot_client: Anthropic,
    ) -> None:
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

        tool_runner(snapshot_client)

    @pytest.mark.parametrize(
        "http_snapshot",
        [cast(Any, external("uuid:ff848716-2309-477f-8e90-39877809aaad.json"))],
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

        last_response_messsage = (
            snapshot_client.beta.messages.tool_runner(
                max_tokens=1024,
                model="claude-haiku-4-5",
                tools=[get_weather],
                messages=[{"role": "user", "content": "What is the weather in SF?"}],
                stream=True,
            ).until_done(),
        )

        assert print_obj(last_response_messsage) == snapshot(
            """\
(
    ParsedBetaMessage(
        container=None,
        content=[
            ParsedBetaTextBlock(
                citations=None,
                parsed_output=None,
                text='The weather in San Francisco, CA is currently **68°F and Sunny** ☀️',
                type='text'
            )
        ],
        context_management=None,
        id='msg_01ERB2ekevEhTbZtAuM2HjmS',
        model='claude-haiku-4-5-20251001',
        role='assistant',
        stop_reason='end_turn',
        stop_sequence=None,
        type='message',
        usage=BetaUsage(
            cache_creation=BetaCacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0),
            cache_creation_input_tokens=0,
            cache_read_input_tokens=0,
            input_tokens=770,
            output_tokens=24,
            server_tool_use=None,
            service_tier='standard'
        )
    ),
)
"""
        )

    @pytest.mark.parametrize(
        "http_snapshot",
        [cast(Any, external("uuid:4a71c9f9-6191-4820-b1a1-89f3bb179078.json"))],
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

        answers = get_weather_answers(snapshot_client)

        assert print_obj(answers) == snapshot(
            """\
[
    {
        'role': 'user',
        'content': [
            {
                'type': 'tool_result',
                'tool_use_id': 'toolu_01FpmqujJtkj11RDCJySJWUH',
                'content': '{"location": "San Francisco, CA", "temperature": "68\\\\u00b0F", "condition": "Sunny"}'
            }
        ]
    },
    {
        'role': 'user',
        'content': [
            {
                'type': 'tool_result',
                'tool_use_id': 'toolu_017cDHUBfAhBDseR2vW7axod',
                'content': '{"location": "New York, NY", "temperature": "68\\\\u00b0F", "condition": "Sunny"}'
            }
        ]
    }
]
"""
        )

    @pytest.mark.parametrize(
        "http_snapshot",
        [cast(Any, external("uuid:f27add0c-5771-4452-8ed9-996f5d74ef77.json"))],
    )
    def test_streaming_call_sync_events(
        self,
        snapshot_client: Anthropic,
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

        events = accumulate_events(snapshot_client)
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
        [cast(Any, external("uuid:e4c374b8-ae08-48f3-96e5-9d28066820b0.json"))],
    )
    def test_compaction_control(self, snapshot_client: Anthropic, caplog: pytest.LogCaptureFixture) -> None:
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
            runner = tool_runner(snapshot_client)

        messages = list(runner._params["messages"])
        assert len(messages) == 1
        assert messages[0]["role"] == "user"

        content = list(messages[0]["content"])[0]
        assert isinstance(content, dict)
        assert content["type"] == "text"
        assert content["text"] == snapshot("""\
<summary>
## 1. Task Overview
The user has requested:
- Write a detailed 500-word essay about dogs, cats, and birds
- Call the tool `submit_analysis` ONCE at the end with information about all three animals
- The tool should contain compiled information from the essay about all three animal types

Success criteria:
- Essay must be approximately 500 words
- Must cover all three animals (dogs, cats, birds)
- Must be detailed
- Single tool call at the very end containing analysis/information about all three animals

## 2. Current State
**Completed:** Nothing has been completed yet.

**Files/Outputs:** None created.

**Status:** Task not started. No essay has been written, and no tool has been called.

## 3. Important Discoveries
No technical constraints have been uncovered yet, as work hasn't begun.

**Key requirements identified:**
- Need to understand the `submit_analysis` tool parameters (what fields it accepts)
- The tool call should synthesize information about all three animals from the essay
- Only ONE tool call should be made, despite covering three different animals

## 4. Next Steps
**Immediate actions required:**

1. **Write the 500-word essay** covering:
   - Dogs (characteristics, behavior, role as pets, etc.)
   - Cats (characteristics, behavior, role as pets, etc.)
   - Birds (characteristics, behavior, role as pets, etc.)
   - Ensure balanced coverage of all three animals
   - Aim for approximately 500 words total

2. **Call `submit_analysis` tool once** after completing the essay:
   - Structure the tool call to include information about all three animals
   - Likely format: summarize key points about each animal type
   - May need to check tool schema to understand expected parameters

**Priority:** Write essay first, then make single tool call.

**Blockers/Questions:** \n\
- Need to determine exact parameters for `submit_analysis` tool when ready to call it

## 5. Context to Preserve
- User specifically emphasized calling the tool "only once at the end"
- Essay should be "detailed" - aim for substantive content, not superficial
- All three animals must be covered adequately
- Word count target: approximately 500 words
</summary>\
""")
        assert caplog.record_tuples == snapshot(
            [
                (
                    "anthropic.lib.tools._beta_runner",
                    20,
                    "Token usage 1663 has exceeded the threshold of 500. Performing compaction.",
                ),
                ("anthropic.lib.tools._beta_runner", 20, "Compaction complete. New token usage: 518"),
            ]
        )

    @pytest.mark.parametrize("http_snapshot", [cast(Any, external("uuid:6f763c87-ecb6-4217-8f6f-32db8e84a6be.json"))])
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
        cast(Any, external("uuid:c4061e82-ea59-4756-9549-71a35da24499.json")),
    ],
)
async def test_basic_call_async(
    async_snapshot_client: AsyncAnthropic,
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
