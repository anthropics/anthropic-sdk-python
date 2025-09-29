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
                '{"id": "msg_01Lf1uRSXq1sB9df6EigSkXA", "type": "message", "role": "assistant", "model": "claude-3-5-sonnet-20241022", "content": [{"type": "text", "text": "I\'ll help you check the weather in San Francisco. I\'ll use the get_weather function, and I\'ll show you the temperature in both Celsius and Fahrenheit for completeness."}, {"type": "tool_use", "id": "toolu_013bzsyqF4LyvJj6CF5gYCEn", "name": "get_weather", "input": {"location": "San Francisco, CA", "units": "c"}}, {"type": "tool_use", "id": "toolu_01Ugb5BSmDUth8vbdkUsNYrs", "name": "get_weather", "input": {"location": "San Francisco, CA", "units": "f"}}], "stop_reason": "tool_use", "stop_sequence": null, "usage": {"input_tokens": 473, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 169, "service_tier": "standard"}}',
                '{"id": "msg_01SUujjdE6BMF3CYWCTR4vHF", "type": "message", "role": "assistant", "model": "claude-3-5-sonnet-20241022", "content": [{"type": "text", "text": "The weather in San Francisco is currently sunny with a temperature of 20\\u00b0C (68\\u00b0F)."}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 760, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 25, "service_tier": "standard"}}',
            ]
        ),
        "result": snapshot("""\
BetaMessage(
    container=None,
    content=[
        BetaTextBlock(
            citations=None,
            text='The weather in San Francisco is currently sunny with a temperature of 20°C (68°F).',
            type='text'
        )
    ],
    context_management=None,
    id='msg_01SUujjdE6BMF3CYWCTR4vHF',
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
"""),
    },
    "custom": {
        "responses": snapshot(
            [
                '{"id": "msg_01QebvpjSMHnjRVYDQpthDCM", "type": "message", "role": "assistant", "model": "claude-3-5-sonnet-20241022", "content": [{"type": "text", "text": "I\'ll help you check the weather in San Francisco using the get_weather function. Since you want it in Celsius, I\'ll use \'c\' for the units."}, {"type": "tool_use", "id": "toolu_01W8QFaZz5X8w6UezBfvJaHG", "name": "get_weather", "input": {"location": "San Francisco, CA", "units": "c"}}], "stop_reason": "tool_use", "stop_sequence": null, "usage": {"input_tokens": 476, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 110, "service_tier": "standard"}}',
                '{"id": "msg_01GQD2QBjkCMtD8rEfbF7J7y", "type": "message", "role": "assistant", "model": "claude-3-5-sonnet-20241022", "content": [{"type": "text", "text": "The weather in San Francisco is currently 20\\u00b0C and it\'s sunny."}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 625, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 20, "service_tier": "standard"}}',
            ]
        ),
        "result": snapshot("""\
BetaMessage(
    container=None,
    content=[
        BetaTextBlock(
            citations=None,
            text="The weather in San Francisco is currently 20°C and it's sunny.",
            type='text'
        )
    ],
    context_management=None,
    id='msg_01GQD2QBjkCMtD8rEfbF7J7y',
    model='claude-3-5-sonnet-20241022',
    role='assistant',
    stop_reason='end_turn',
    stop_sequence=None,
    type='message',
    usage=BetaUsage(
        cache_creation=BetaCacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0),
        cache_creation_input_tokens=0,
        cache_read_input_tokens=0,
        input_tokens=625,
        output_tokens=20,
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
    context_management=None,
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
                '{"id": "msg_01CcxTJKA7URvATmjs9yemNw", "type": "message", "role": "assistant", "model": "claude-3-5-sonnet-20241022", "content": [{"type": "text", "text": "I\'ll help you check the weather in San Francisco using Celsius units."}, {"type": "tool_use", "id": "toolu_01X4rAg6afq9WTkdXDwNdo9g", "name": "get_weather", "input": {"location": "SF", "units": "c"}}], "stop_reason": "tool_use", "stop_sequence": null, "usage": {"input_tokens": 414, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 86, "service_tier": "standard"}}',
                '{"id": "msg_01Hswpqi8rjN9k6Erfof4NML", "type": "message", "role": "assistant", "model": "claude-3-5-sonnet-20241022", "content": [{"type": "text", "text": "The weather in San Francisco is currently 20\\u00b0C and it\'s sunny."}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 536, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 20, "service_tier": "standard"}}',
            ]
        ),
    },
    "tool_call_error": {
        "responses": snapshot(
            [
                '{"id": "msg_01UCU1h4ayreA2Ridzbpk5ut", "type": "message", "role": "assistant", "model": "claude-3-5-sonnet-20241022", "content": [{"type": "text", "text": "I\'ll help you check the weather in San Francisco. Since the location format should include the state, I\'ll use \\"San Francisco, CA\\". I\'ll provide the temperature in both Celsius and Fahrenheit for completeness."}, {"type": "tool_use", "id": "toolu_01ECouLXJaT6yocMNDstufPc", "name": "get_weather", "input": {"location": "San Francisco, CA", "units": "c"}}, {"type": "tool_use", "id": "toolu_01FHQTcVXvPoLL3bzxsAUtJJ", "name": "get_weather", "input": {"location": "San Francisco, CA", "units": "f"}}], "stop_reason": "tool_use", "stop_sequence": null, "usage": {"input_tokens": 473, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 176, "service_tier": "standard"}}',
                '{"id": "msg_01PYwhqAdduuZYymTokQ4JQU", "type": "message", "role": "assistant", "model": "claude-3-5-sonnet-20241022", "content": [{"type": "text", "text": "The weather in San Francisco, CA is currently sunny with a temperature of 68\\u00b0F."}], "stop_reason": "end_turn", "stop_sequence": null, "usage": {"input_tokens": 749, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0}, "output_tokens": 23, "service_tier": "standard"}}',
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
                'tool_use_id': 'toolu_01ECouLXJaT6yocMNDstufPc',
                'content': "RuntimeError('Unexpected error, try again')",
                'is_error': True
            },
            {
                'type': 'tool_result',
                'tool_use_id': 'toolu_01FHQTcVXvPoLL3bzxsAUtJJ',
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
            content_snapshot=snapshot(external("uuid:ef758469-6fa6-454c-b2e6-19d0b450a8c5.json")),
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
                'tool_use_id': 'toolu_01GiQJzt5d2ThB4fSUsRCSML',
                'content': '{"location": "San Francisco, CA", "temperature": "68\\\\u00b0F", "condition": "Sunny"}'
            }
        ]
    },
    {
        'role': 'user',
        'content': [
            {
                'type': 'tool_result',
                'tool_use_id': 'toolu_015yzRQ92SwYGz5Veoq7A3P7',
                'content': '{"location": "New York, NY", "temperature": "68\\\\u00b0F", "condition": "Sunny"}'
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
