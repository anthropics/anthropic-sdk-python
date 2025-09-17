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
# `ANTHROPIC_LIVE=1 pytest --inline-snapshot=fix -p no:xdist -o addopts=""`

snapshots = {
    "basic": {
        "responses": snapshot(
            [
                '{"id": "msg_011VcyTSZL4mKtyjRLHBuqA5", "type": "message", "role": "assistant", "model": "claude-3-5-sonnet-20241022", "content": [{"type": "text", "text": "I\'ll help you check the weather in San Francisco. I\'ll use the get_weather function, and I\'ll show you the temperature in both Celsius and Fahrenheit for completeness."}, {"type": "tool_use", "id": "toolu_013nheddwxiFJt4C4Q8eGUXJ", "name": "get_weather", "input": {"location": "San Francisco, CA", "units": "c"}}, {"type": "tool_use", "id": "toolu_01Vg4JstpLEp3JiQadw9aTU1", "name": "get_weather", "input": {"location": "San Francisco, CA", "units": "f"}}], "stop_reason": "tool_use", "stop_sequence": null, "usage": {"input_tokens": 473, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 169, "service_tier": "standard"}}',
                '{"id": "msg_0151Rxp5cbUKiA6TJbEoG1U1", "type": "message", "role": "assistant", "model": "claude-3-5-sonnet-20241022", "content": [{"type": "text", "text": "The weather in San Francisco is currently sunny with a temperature of 20\\u00b0C (68\\u00b0F)."}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 760, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 25, "service_tier": "standard"}}',
            ]
        ),
        "result": snapshot(
            """\
BetaMessage(
    container=None,
    content=[
        BetaTextBlock(
            citations=None,
            text='The weather in San Francisco is currently sunny with a temperature of 20°C (68°F).',
            type='text'
        )
    ],
    id='msg_0151Rxp5cbUKiA6TJbEoG1U1',
    model='claude-3-5-sonnet-20241022',
    role='assistant',
    stop_reason='end_turn',
    stop_sequence=None,
    type='message',
    usage=BetaUsage(
        cache_creation=BetaCacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0),
        cache_creation_input_tokens=0,
        cache_read_input_tokens=0,
        input_tokens=760,
        output_tokens=25,
        server_tool_use=None,
        service_tier='standard'
    )
)
"""
        ),
    },
    "custom": {
        "responses": snapshot(
            [
                '{"id": "msg_01Xabmr29SxRofCJKx6dShd1", "type": "message", "role": "assistant", "model": "claude-3-5-sonnet-20241022", "content": [{"type": "text", "text": "I\'ll help you check the weather in San Francisco. Since you want it in Celsius, I\'ll use \'c\' for the units."}, {"type": "tool_use", "id": "toolu_01TndJ8oicsz1CBQvnKa6XYM", "name": "get_weather", "input": {"location": "San Francisco, CA", "units": "c"}}], "stop_reason": "tool_use", "stop_sequence": null, "usage": {"input_tokens": 476, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 104, "service_tier": "standard"}}',
                '{"id": "msg_01JyRBYxoqpZHJh5tanTRPqU", "type": "message", "role": "assistant", "model": "claude-3-5-sonnet-20241022", "content": [{"type": "text", "text": "The weather in San Francisco is currently 20\\u00b0C and it\'s Sunny."}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 619, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 21, "service_tier": "standard"}}',
            ]
        ),
        "result": snapshot("""\
BetaMessage(
    container=None,
    content=[
        BetaTextBlock(
            citations=None,
            text="The weather in San Francisco is currently 20°C and it's Sunny.",
            type='text'
        )
    ],
    id='msg_01JyRBYxoqpZHJh5tanTRPqU',
    model='claude-3-5-sonnet-20241022',
    role='assistant',
    stop_reason='end_turn',
    stop_sequence=None,
    type='message',
    usage=BetaUsage(
        cache_creation=BetaCacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0),
        cache_creation_input_tokens=0,
        cache_read_input_tokens=0,
        input_tokens=619,
        output_tokens=21,
        server_tool_use=None,
        service_tier='standard'
    )
)
"""),
    },
    "streaming": {
        "result": snapshot("""\
BetaMessage(
    container=None,
    content=[
        BetaTextBlock(citations=None, text='The weather in San Francisco is currently 68°F and sunny.', type='text')
    ],
    id='msg_01FtWrpBLsm99NpQCoFrhuf9',
    model='claude-3-5-sonnet-20241022',
    role='assistant',
    stop_reason='end_turn',
    stop_sequence=None,
    type='message',
    usage=BetaUsage(
        cache_creation=BetaCacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0),
        cache_creation_input_tokens=0,
        cache_read_input_tokens=0,
        input_tokens=605,
        output_tokens=18,
        server_tool_use=None,
        service_tier='standard'
    )
)
""")
    },
    "tool_call": {
        "responses": snapshot(
            [
                '{"id": "msg_01N73bKQGcVyRtRFmYKS3nF7", "type": "message", "role": "assistant", "model": "claude-3-5-sonnet-20241022", "content": [{"type": "text", "text": "I\'ll help you check the weather in San Francisco using Celsius units."}, {"type": "tool_use", "id": "toolu_01KBWEMjDHXQMrtG3Mb4ifsr", "name": "get_weather", "input": {"location": "SF", "units": "c"}}], "stop_reason": "tool_use", "stop_sequence": null, "usage": {"input_tokens": 414, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 86, "service_tier": "standard"}}',
                '{"id": "msg_01LYmChWYohv9p2EbNojAQUD", "type": "message", "role": "assistant", "model": "claude-3-5-sonnet-20241022", "content": [{"type": "text", "text": "The weather in San Francisco is currently 20\\u00b0C and it\'s sunny."}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 536, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 20, "service_tier": "standard"}}',
            ]
        ),
    },
    "tool_call_error": {
        "responses": snapshot(
            [
                '{"id": "msg_014RTukBtZkatJqx6AQNJmz5", "type": "message", "role": "assistant", "model": "claude-3-5-sonnet-20241022", "content": [{"type": "text", "text": "I\'ll help you check the weather in San Francisco. Since the temperature unit wasn\'t specified, I\'ll show it in both Celsius and Fahrenheit."}, {"type": "tool_use", "id": "toolu_01Eqm7dFsQRKLFSSecctffe1", "name": "get_weather", "input": {"location": "San Francisco, CA", "units": "c"}}, {"type": "tool_use", "id": "toolu_01E7AD7aA4uR7cRk3kWs4oxa", "name": "get_weather", "input": {"location": "San Francisco, CA", "units": "f"}}], "stop_reason": "tool_use", "stop_sequence": null, "usage": {"input_tokens": 473, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 162, "service_tier": "standard"}}',
                '{"id": "msg_011W15YiUj9QAvCEQ1gDYCKB", "type": "message", "role": "assistant", "model": "claude-3-5-sonnet-20241022", "content": [{"type": "text", "text": "The weather in San Francisco, CA is currently sunny with a temperature of 68\\u00b0F (the Celsius reading encountered an error, but you can see the Fahrenheit temperature)."}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 735, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 41, "service_tier": "standard"}}',
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
                model="claude-3-5-sonnet-latest",
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
                model="claude-3-5-sonnet-latest",
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
        assert print_obj(message, monkeypatch) == snapshot("""\
[
    {
        'role': 'user',
        'content': [
            {
                'type': 'tool_result',
                'tool_use_id': 'toolu_01Eqm7dFsQRKLFSSecctffe1',
                'content': "RuntimeError('Unexpected error, try again')",
                'is_error': True
            },
            {
                'type': 'tool_result',
                'tool_use_id': 'toolu_01E7AD7aA4uR7cRk3kWs4oxa',
                'content': '{"location": "San Francisco, CA", "temperature": "68\\\\u00b0F", "condition": "Sunny"}'
            }
        ]
    }
]
""")

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
                model="claude-3-5-sonnet-latest",
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
                model="claude-3-5-sonnet-latest",
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
                model="claude-3-5-sonnet-latest",
                tools=[get_weather],
                messages=[{"role": "user", "content": "What is the weather in SF?"}],
                stream=True,
            ).until_done(),
            content_snapshot=snapshot(external("uuid:e2140c0f-07db-47ee-b86b-c2ec476866d5.json")),
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
                model="claude-3-5-sonnet-latest",
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
            content_snapshot=snapshot(external("uuid:d105e140-a30c-4d6b-91df-257247da3623.json")),
            path="/v1/messages",
            mock_client=client,
            respx_mock=respx_mock,
        )

        assert print_obj(answers, monkeypatch) == snapshot("""\
[
    {
        'role': 'user',
        'content': [
            {
                'type': 'tool_result',
                'tool_use_id': 'toolu_01PeNQ4nbMcyDpCGiuKSfkMM',
                'content': '{"location": "San Francisco, CA", "temperature": "20\\\\u00b0C", "condition": "Sunny"}'
            }
        ]
    },
    {
        'role': 'user',
        'content': [
            {
                'type': 'tool_result',
                'tool_use_id': 'toolu_01WcZvizPr9EybXFMyGXRxYA',
                'content': '{"location": "New York, NY", "temperature": "20\\\\u00b0C", "condition": "Sunny"}'
            }
        ]
    }
]
""")

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
                model="claude-3-5-sonnet-latest",
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
            content_snapshot=snapshot(external("uuid:9cb114c8-69bd-4111-841b-edee30333afd.json")),
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
            model="claude-3-5-sonnet-latest",
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
def test_parse_method_in_sync(sync: bool, client: Anthropic, async_client: AsyncAnthropic) -> None:
    checking_client: "Anthropic | AsyncAnthropic" = client if sync else async_client

    assert_signatures_in_sync(
        checking_client.beta.messages.create,
        checking_client.beta.messages.tool_runner,
        exclude_params={
            "tools",
            # TODO
            "stream",
        },
    )
