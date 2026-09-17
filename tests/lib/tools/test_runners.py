import os
import json
import logging
from typing import Any, Dict, List, Union, cast
from typing_extensions import Literal, get_args

import httpx2
import pytest
from respx import MockRouter
from inline_snapshot import external, snapshot

from anthropic import Anthropic, AsyncAnthropic, InternalServerError, beta_tool, beta_async_tool
from anthropic._types import Omit, omit
from anthropic._utils import assert_signatures_in_sync
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.tools import BetaFunctionTool, BetaAsyncFunctionTool, BetaFunctionToolResultType
from anthropic.lib.tools._beta_runner import (
    _STOP_REASON_STEPS,
    BetaToolRunner,
    BetaAsyncToolRunner,
    _determine_next_step_from_stop_reason,
)
from anthropic.types.anthropic_beta_param import AnthropicBetaParam
from anthropic.types.beta.beta_stop_reason import BetaStopReason
from anthropic.types.beta.beta_message_param import BetaMessageParam
from anthropic.types.beta.beta_content_block_param import BetaContentBlockParam
from anthropic.types.beta.beta_tool_result_block_param import BetaToolResultBlockParam
from anthropic.types.beta.beta_context_management_config_param import BetaContextManagementConfigParam
from anthropic.types.beta.beta_tool_change_tool_reference_param import BetaToolChangeToolReferenceParam

from ..utils import print_obj

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

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
    diagnostics=None,
    id='msg_01BZsMQjer9AFLgmdRKJ8NcA',
    input_transformations=None,
    model='claude-haiku-4-5-20251001',
    role='assistant',
    stop_details=None,
    stop_reason='end_turn',
    stop_sequence=None,
    type='message',
    usage=BetaUsage(
        cache_creation=BetaCacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0),
        cache_creation_input_tokens=0,
        cache_read_input_tokens=0,
        fallback_credit=None,
        inference_geo='not_available',
        input_tokens=770,
        iterations=None,
        output_tokens=25,
        output_tokens_details=None,
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
            "ParsedBetaMessage(container=None, content=[ParsedBetaTextBlock(citations=None, parsed_output=None, text='The weather in San Francisco, CA is currently **20°C** and **Sunny**. Nice weather!', type='text')], context_management=None, id='msg_01DSPL7PHKQYTe9VAFkHzsA3', model='claude-haiku-4-5-20251001', role='assistant', stop_details=None, stop_reason='end_turn', stop_sequence=None, type='message', usage=BetaUsage(cache_creation=BetaCacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, cache_read_input_tokens=0, inference_geo=None, input_tokens=787, iterations=None, output_tokens=26, server_tool_use=None, service_tier='standard', speed=None))\n"
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
    diagnostics=None,
    id='msg_0158JyopQTFaomteeJoDpS5q',
    input_transformations=None,
    model='claude-haiku-4-5-20251001',
    role='assistant',
    stop_details=None,
    stop_reason='end_turn',
    stop_sequence=None,
    type='message',
    usage=BetaUsage(
        cache_creation=BetaCacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0),
        cache_creation_input_tokens=0,
        cache_read_input_tokens=0,
        fallback_credit=None,
        inference_geo='not_available',
        input_tokens=770,
        iterations=None,
        output_tokens=27,
        output_tokens_details=None,
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

    @pytest.mark.parametrize(
        "http_snapshot",
        [
            cast(Any, external("uuid:092be1de-d3f8-4c22-a4ea-a7ad54689836.json")),
        ],
    )
    def test_programmatic_tool_call(self, snapshot_client: Anthropic) -> None:
        @beta_tool(allowed_callers=["code_execution_20260120"])
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
            model="claude-opus-4-5",
            tools=[get_weather],
            messages=[{"role": "user", "content": "What is the weather in SF, NY, and London in Celsius?"}],
        )

        first_response = next(runner)

        # one more iteration so runner can process the tool call response and update its params with the container info
        next(runner)

        assert first_response.container is not None
        container_id = first_response.container.id
        assert "container" in runner._params
        assert runner._params["container"] is not None
        assert container_id == runner._params["container"]


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


def _refusal_with_tool_use() -> httpx2.Response:
    return httpx2.Response(
        200,
        json={
            "id": "msg_refusal",
            "type": "message",
            "role": "assistant",
            "model": "claude-haiku-4-5",
            "content": [
                {
                    "type": "tool_use",
                    "id": "toolu_refusal",
                    "name": "get_weather",
                    "input": {"location": "San Francisco, CA", "units": "f"},
                }
            ],
            "stop_reason": "refusal",
            "stop_sequence": None,
            "usage": {"input_tokens": 1, "output_tokens": 1},
        },
    )


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_refusal_ends_runner_without_executing_tools_sync(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=[_refusal_with_tool_use()])

    called = False

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
        called = True
        return json.dumps(_get_weather(location, units))

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        )
        message = runner.until_done()

    assert message.stop_reason == "refusal"
    assert called is False
    assert len(respx_mock.calls) == 1


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
async def test_refusal_ends_runner_without_executing_tools_async(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=[_refusal_with_tool_use()])

    called = False

    @beta_async_tool
    async def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
        """Lookup the weather for a given city in either celsius or fahrenheit

        Args:
            location: The city and state, e.g. San Francisco, CA
            units: Unit for the output, either 'c' for celsius or 'f' for fahrenheit
        Returns:
            A dictionary containing the location, temperature, and weather condition.
        """
        nonlocal called
        called = True
        return json.dumps(_get_weather(location, units))

    async with AsyncAnthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        )
        message = await runner.until_done()

    assert message.stop_reason == "refusal"
    assert called is False
    assert len(respx_mock.calls) == 1


def _paused_server_tool_use() -> httpx2.Response:
    return httpx2.Response(
        200,
        json={
            "id": "msg_paused",
            "type": "message",
            "role": "assistant",
            "model": "claude-haiku-4-5",
            "content": [
                {
                    "type": "server_tool_use",
                    "id": "srvtoolu_paused",
                    "name": "web_search",
                    "input": {"query": "weather in SF"},
                }
            ],
            "stop_reason": "pause_turn",
            "stop_sequence": None,
            "usage": {"input_tokens": 1, "output_tokens": 1},
        },
    )


_PAUSED_ASSISTANT_TURN = {
    "role": "assistant",
    "content": [
        {"type": "server_tool_use", "id": "srvtoolu_paused", "name": "web_search", "input": {"query": "weather in SF"}}
    ],
}


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_pause_turn_resumes_runner_sync(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=[_paused_server_tool_use(), _end_turn_response()])

    @beta_tool
    def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
        """Lookup the weather for a given city.

        Args:
            location: The city and state, e.g. San Francisco, CA
            units: Unit for the output, either 'c' for celsius or 'f' for fahrenheit
        """
        return json.dumps(_get_weather(location, units))

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        message = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather, {"type": "web_search_20250305", "name": "web_search"}],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        ).until_done()

    assert message.stop_reason == "end_turn"
    assert len(respx_mock.calls) == 2
    assert json.loads(respx_mock.calls.last.request.content)["messages"][-1] == _PAUSED_ASSISTANT_TURN


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
async def test_pause_turn_resumes_runner_async(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=[_paused_server_tool_use(), _end_turn_response()])

    @beta_async_tool
    async def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
        """Lookup the weather for a given city.

        Args:
            location: The city and state, e.g. San Francisco, CA
            units: Unit for the output, either 'c' for celsius or 'f' for fahrenheit
        """
        return json.dumps(_get_weather(location, units))

    async with AsyncAnthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        message = await client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather, {"type": "web_search_20250305", "name": "web_search"}],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        ).until_done()

    assert message.stop_reason == "end_turn"
    assert len(respx_mock.calls) == 2
    assert json.loads(respx_mock.calls.last.request.content)["messages"][-1] == _PAUSED_ASSISTANT_TURN


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_pause_turn_respects_max_iterations_sync(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=[_paused_server_tool_use() for _ in range(5)])

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        message = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
            max_iterations=3,
        ).until_done()

    assert message.stop_reason == "pause_turn"
    assert len(respx_mock.calls) == 3


def test_every_stop_reason_is_classified() -> None:
    # A newly generated stop reason must be mapped to a step before this passes.
    assert set(get_args(BetaStopReason)) == set(_STOP_REASON_STEPS)

    expected: Dict[BetaStopReason, str] = {
        "tool_use": "run_tools",
        "pause_turn": "resume",
        "compaction": "resume",
        "end_turn": "stop",
        "stop_sequence": "stop",
        "max_tokens": "stop",
        "model_context_window_exceeded": "stop",
        "refusal": "stop",
    }
    assert {
        stop_reason: _determine_next_step_from_stop_reason(stop_reason) for stop_reason in get_args(BetaStopReason)
    } == expected
    assert _determine_next_step_from_stop_reason(None) == "stop"
    assert _determine_next_step_from_stop_reason(cast(Any, "some_future_reason")) == "stop"


def _compaction_response() -> httpx2.Response:
    return httpx2.Response(
        200,
        json={
            "id": "msg_compaction",
            "type": "message",
            "role": "assistant",
            "model": "claude-haiku-4-5",
            "content": [{"type": "compaction", "content": "Summary of the conversation so far."}],
            "stop_reason": "compaction",
            "stop_sequence": None,
            "usage": {"input_tokens": 1, "output_tokens": 1},
        },
    )


_COMPACTION_ASSISTANT_TURN = {
    "role": "assistant",
    "content": [{"type": "compaction", "content": "Summary of the conversation so far."}],
}


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_compaction_resumes_runner_sync(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=[_compaction_response(), _end_turn_response()])

    @beta_tool
    def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
        """Lookup the weather for a given city.

        Args:
            location: The city and state, e.g. San Francisco, CA
            units: Unit for the output, either 'c' for celsius or 'f' for fahrenheit
        """
        return json.dumps(_get_weather(location, units))

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        message = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        ).until_done()

    assert message.stop_reason == "end_turn"
    assert len(respx_mock.calls) == 2
    assert json.loads(respx_mock.calls.last.request.content)["messages"][-1] == _COMPACTION_ASSISTANT_TURN


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
async def test_compaction_resumes_runner_async(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=[_compaction_response(), _end_turn_response()])

    @beta_async_tool
    async def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
        """Lookup the weather for a given city.

        Args:
            location: The city and state, e.g. San Francisco, CA
            units: Unit for the output, either 'c' for celsius or 'f' for fahrenheit
        """
        return json.dumps(_get_weather(location, units))

    async with AsyncAnthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        message = await client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        ).until_done()

    assert message.stop_reason == "end_turn"
    assert len(respx_mock.calls) == 2
    assert json.loads(respx_mock.calls.last.request.content)["messages"][-1] == _COMPACTION_ASSISTANT_TURN


def _max_tokens_with_tool_use() -> httpx2.Response:
    return httpx2.Response(
        200,
        json={
            "id": "msg_max_tokens",
            "type": "message",
            "role": "assistant",
            "model": "claude-haiku-4-5",
            "content": [
                {
                    "type": "tool_use",
                    "id": "toolu_max_tokens",
                    "name": "get_weather",
                    "input": {"location": "San Francisco, CA", "units": "f"},
                }
            ],
            "stop_reason": "max_tokens",
            "stop_sequence": None,
            "usage": {"input_tokens": 1, "output_tokens": 1},
        },
    )


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_max_tokens_ends_runner_without_executing_tools_sync(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=[_max_tokens_with_tool_use()])

    called = False

    @beta_tool
    def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
        """Lookup the weather for a given city.

        Args:
            location: The city and state, e.g. San Francisco, CA
            units: Unit for the output, either 'c' for celsius or 'f' for fahrenheit
        """
        nonlocal called
        called = True
        return json.dumps(_get_weather(location, units))

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        message = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        ).until_done()

    assert message.stop_reason == "max_tokens"
    assert called is False
    assert len(respx_mock.calls) == 1


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
async def test_max_tokens_ends_runner_without_executing_tools_async(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=[_max_tokens_with_tool_use()])

    called = False

    @beta_async_tool
    async def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
        """Lookup the weather for a given city.

        Args:
            location: The city and state, e.g. San Francisco, CA
            units: Unit for the output, either 'c' for celsius or 'f' for fahrenheit
        """
        nonlocal called
        called = True
        return json.dumps(_get_weather(location, units))

    async with AsyncAnthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        message = await client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        ).until_done()

    assert message.stop_reason == "max_tokens"
    assert called is False
    assert len(respx_mock.calls) == 1


def _tool_use_response(tool_name: str, tool_use_id: str, input: Union[Dict[str, Any], None] = None) -> httpx2.Response:
    return httpx2.Response(
        200,
        json={
            "id": f"msg_{tool_use_id}",
            "type": "message",
            "role": "assistant",
            "model": "claude-haiku-4-5",
            "content": [
                {
                    "type": "tool_use",
                    "id": tool_use_id,
                    "name": tool_name,
                    "input": input if input is not None else {"location": "San Francisco, CA", "units": "f"},
                }
            ],
            "stop_reason": "tool_use",
            "stop_sequence": None,
            "usage": {"input_tokens": 1, "output_tokens": 1},
        },
    )


def _end_turn_response() -> httpx2.Response:
    return httpx2.Response(
        200,
        json={
            "id": "msg_end_turn",
            "type": "message",
            "role": "assistant",
            "model": "claude-haiku-4-5",
            "content": [{"type": "text", "text": "Done."}],
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {"input_tokens": 1, "output_tokens": 1},
        },
    )


def _tool_reference_block(kind: Literal["tool_removal", "tool_addition"], name: str) -> BetaContentBlockParam:
    tool: BetaToolChangeToolReferenceParam = {"type": "tool_reference", "name": name}
    if kind == "tool_removal":
        return {"type": "tool_removal", "tool": tool}
    return {"type": "tool_addition", "tool": tool}


def _run_sync_tool_use(
    client: Anthropic,
    *,
    tools: List[Any],
    messages: List[BetaMessageParam],
) -> List[BetaMessageParam]:
    """Drive a tool runner over `messages` and collect the tool_result
    messages it generated."""
    runner = client.beta.messages.tool_runner(
        max_tokens=1024,
        model="claude-haiku-4-5",
        tools=tools,
        messages=messages,
    )
    responses: List[BetaMessageParam] = []
    for _ in runner:
        response = runner.generate_tool_call_response()
        if response is not None:
            responses.append(response)
    return responses


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_tool_removal_routes_call_down_unknown_tool_path_sync(respx_mock: MockRouter) -> None:
    # First runner: `get_weather` is registered but withdrawn mid-conversation via `tool_removal`.
    # Second runner: `get_weather` was never declared at all. The model calls it in both;
    # the resulting tool_result must be identical.
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _tool_use_response("get_weather", "toolu_change"),
            _end_turn_response(),
            _tool_use_response("get_weather", "toolu_change"),
            _end_turn_response(),
        ]
    )

    weather_called = False

    @beta_tool
    def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
        """Lookup the weather for a given city."""
        nonlocal weather_called
        weather_called = True
        return json.dumps(_get_weather(location, units))

    @beta_tool
    def get_time(timezone: str) -> BetaFunctionToolResultType:
        """Lookup the current time in a timezone."""
        return timezone

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
            removed_results = _run_sync_tool_use(
                client,
                tools=[get_weather],
                messages=[
                    {"role": "user", "content": "What is the weather in SF?"},
                    {"role": "system", "content": [_tool_reference_block("tool_removal", "get_weather")]},
                ],
            )
        with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
            never_defined_results = _run_sync_tool_use(
                client,
                tools=[get_time],
                messages=[{"role": "user", "content": "What is the weather in SF?"}],
            )

    assert weather_called is False
    assert (
        removed_results
        == never_defined_results
        == [
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": "toolu_change",
                        "content": "Error: Tool 'get_weather' not found",
                        "is_error": True,
                    }
                ],
            }
        ]
    )


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_tool_addition_re_enables_removed_tool_sync(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _tool_use_response("get_weather", "toolu_change"),
            _end_turn_response(),
        ]
    )

    weather_called = False

    @beta_tool
    def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
        """Lookup the weather for a given city."""
        nonlocal weather_called
        weather_called = True
        return json.dumps(_get_weather(location, units))

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        results = _run_sync_tool_use(
            client,
            tools=[get_weather],
            messages=[
                {"role": "user", "content": "What is the weather in SF?"},
                {"role": "system", "content": [_tool_reference_block("tool_removal", "get_weather")]},
                {"role": "system", "content": [_tool_reference_block("tool_addition", "get_weather")]},
            ],
        )

    assert weather_called is True
    assert results == [
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_change",
                    "content": json.dumps(_get_weather("San Francisco, CA", "f")),
                }
            ],
        }
    ]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
async def test_tool_removal_routes_call_down_unknown_tool_path_async(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _tool_use_response("get_weather", "toolu_change"),
            _end_turn_response(),
        ]
    )

    weather_called = False

    @beta_async_tool
    async def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
        """Lookup the weather for a given city."""
        nonlocal weather_called
        weather_called = True
        return json.dumps(_get_weather(location, units))

    async with AsyncAnthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather],
            messages=[
                {"role": "user", "content": "What is the weather in SF?"},
                {"role": "system", "content": [_tool_reference_block("tool_removal", "get_weather")]},
            ],
        )
        results: List[BetaMessageParam] = []
        with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
            async for _ in runner:
                response = await runner.generate_tool_call_response()
                if response is not None:
                    results.append(response)

    assert weather_called is False
    assert results == [
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_change",
                    "content": "Error: Tool 'get_weather' not found",
                    "is_error": True,
                }
            ],
        }
    ]


def _not_found_result(tool_use_id: str) -> BetaMessageParam:
    return {
        "role": "user",
        "content": [
            {
                "type": "tool_result",
                "tool_use_id": tool_use_id,
                "content": "Error: Tool 'get_weather' not found",
                "is_error": True,
            }
        ],
    }


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_tool_removal_via_append_messages_between_turns_sync(respx_mock: MockRouter) -> None:
    # The removal is not in the initial params: it is appended while iterating, on the
    # turn *before* the model calls the withdrawn tool.
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _tool_use_response("get_time", "toolu_time", input={"timezone": "UTC"}),
            _tool_use_response("get_weather", "toolu_weather"),
            _end_turn_response(),
        ]
    )

    weather_called = False

    @beta_tool
    def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
        """Lookup the weather for a given city."""
        nonlocal weather_called
        weather_called = True
        return json.dumps(_get_weather(location, units))

    @beta_tool
    def get_time(timezone: str) -> BetaFunctionToolResultType:
        """Lookup the current time in a timezone."""
        return f"12:00 {timezone}"

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather, get_time],
            messages=[{"role": "user", "content": "What time is it, and what is the weather in SF?"}],
        )
        results: List[BetaMessageParam] = []
        with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
            for message in runner:
                if any(block.type == "tool_use" and block.name == "get_time" for block in message.content):
                    # Withdraw get_weather during turn 1; the model calls it on turn 2.
                    runner.append_messages(
                        {"role": "system", "content": [_tool_reference_block("tool_removal", "get_weather")]}
                    )
                response = runner.generate_tool_call_response()
                if response is not None:
                    results.append(response)

    assert weather_called is False
    assert results == [
        {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "toolu_time", "content": "12:00 UTC"}]},
        _not_found_result("toolu_weather"),
    ]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_tool_removal_via_append_messages_same_turn_sync(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _tool_use_response("get_weather", "toolu_weather"),
            _end_turn_response(),
        ]
    )

    weather_called = False

    @beta_tool
    def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
        """Lookup the weather for a given city."""
        nonlocal weather_called
        weather_called = True
        return json.dumps(_get_weather(location, units))

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        )
        results: List[BetaMessageParam] = []
        with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
            for message in runner:
                if any(block.type == "tool_use" for block in message.content):
                    # The tool_use is already in `message`, but the runner has not dispatched it yet:
                    # the loop body runs before dispatch, so a removal appended here still applies.
                    runner.append_messages(
                        {"role": "system", "content": [_tool_reference_block("tool_removal", "get_weather")]}
                    )
                response = runner.generate_tool_call_response()
                if response is not None:
                    results.append(response)

    assert weather_called is False
    assert results == [_not_found_result("toolu_weather")]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_tool_removal_via_set_messages_params_sync(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _tool_use_response("get_time", "toolu_time", input={"timezone": "UTC"}),
            _tool_use_response("get_weather", "toolu_weather"),
            _end_turn_response(),
        ]
    )

    weather_called = False

    @beta_tool
    def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
        """Lookup the weather for a given city."""
        nonlocal weather_called
        weather_called = True
        return json.dumps(_get_weather(location, units))

    @beta_tool
    def get_time(timezone: str) -> BetaFunctionToolResultType:
        """Lookup the current time in a timezone."""
        return f"12:00 {timezone}"

    replacement_history: List[BetaMessageParam] = [
        {"role": "user", "content": "What time is it, and what is the weather in SF?"},
        {"role": "system", "content": [_tool_reference_block("tool_removal", "get_weather")]},
    ]

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather, get_time],
            messages=[{"role": "user", "content": "What time is it, and what is the weather in SF?"}],
        )
        results: List[BetaMessageParam] = []
        with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
            for message in runner:
                if any(block.type == "tool_use" and block.name == "get_time" for block in message.content):
                    # Replace the history wholesale with one carrying the removal.
                    runner.set_messages_params(lambda params: {**params, "messages": list(replacement_history)})
                response = runner.generate_tool_call_response()
                if response is not None:
                    results.append(response)

    assert weather_called is False
    assert results == [
        {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "toolu_time", "content": "12:00 UTC"}]},
        _not_found_result("toolu_weather"),
    ]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_tool_addition_via_append_messages_re_enables_removed_tool_sync(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _tool_use_response("get_weather", "toolu_weather"),
            _end_turn_response(),
        ]
    )

    weather_called = False

    @beta_tool
    def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
        """Lookup the weather for a given city."""
        nonlocal weather_called
        weather_called = True
        return json.dumps(_get_weather(location, units))

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather],
            messages=[
                {"role": "user", "content": "What is the weather in SF?"},
                {"role": "system", "content": [_tool_reference_block("tool_removal", "get_weather")]},
            ],
        )
        results: List[BetaMessageParam] = []
        for message in runner:
            if any(block.type == "tool_use" for block in message.content):
                # Re-add the withdrawn tool before dispatch: it must execute normally again.
                runner.append_messages(
                    {"role": "system", "content": [_tool_reference_block("tool_addition", "get_weather")]}
                )
            response = runner.generate_tool_call_response()
            if response is not None:
                results.append(response)

    assert weather_called is True
    assert results == [
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_weather",
                    "content": json.dumps(_get_weather("San Francisco, CA", "f")),
                }
            ],
        }
    ]


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
            # a tool runner can't take it: every request of the loop would compact again
            "compaction",
        },
    )


def _sent_request_bodies(respx_mock: MockRouter) -> List[Any]:
    return [json.loads(call.request.content) for call in cast("List[Any]", respx_mock.calls)]


def _compacted_response() -> httpx2.Response:
    return httpx2.Response(
        200,
        json={
            "id": "msg_compacted",
            "type": "message",
            "role": "assistant",
            "model": "claude-haiku-4-5",
            "content": [{"type": "compaction", "content": "Summary so far.", "signature": "sig_01"}],
            "stop_reason": "compaction",
            "stop_sequence": None,
            "usage": {"input_tokens": 1, "output_tokens": 1},
        },
    )


def _compaction_block_alone() -> List[Any]:
    return [
        {"role": "assistant", "content": [{"type": "compaction", "content": "Summary so far.", "signature": "sig_01"}]}
    ]


_COMPACTION_RESPONSE_CONTENT_WITH_AN_UNMODELLED_BLOCK: List[Dict[str, Any]] = [
    {"type": "compaction", "content": "Summary so far.", "signature": "sig_01"},
    {"type": "mcp_tool_listing", "mcp_server_name": "docs", "tools": []},
]


def _compacted_response_with_an_unmodelled_block() -> httpx2.Response:
    body = _compacted_response().json()
    body["content"] = _COMPACTION_RESPONSE_CONTENT_WITH_AN_UNMODELLED_BLOCK
    return httpx2.Response(200, json=body)


_FINAL_ASSISTANT_TURN = {"role": "assistant", "content": [{"type": "text", "text": "Done."}]}


def _response_without_a_summary(content: List[Any], stop_reason: str) -> httpx2.Response:
    body = _compacted_response().json()
    return httpx2.Response(200, json={**body, "content": content, "stop_reason": stop_reason})


def _sync_weather_tool() -> BetaFunctionTool[Any]:
    @beta_tool
    def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
        """Lookup the weather for a given city."""
        return json.dumps(_get_weather(location, units))

    return get_weather


def _async_weather_tool() -> BetaAsyncFunctionTool[Any]:
    @beta_async_tool
    async def get_weather(location: str, units: Literal["c", "f"]) -> BetaFunctionToolResultType:
        """Lookup the weather for a given city."""
        return json.dumps(_get_weather(location, units))

    return get_weather


def _sync_compact_runner(
    client: Anthropic,
    *,
    betas: Union[List[AnthropicBetaParam], Omit] = omit,
    context_management: Union[BetaContextManagementConfigParam, Omit] = omit,
    max_iterations: Union[int, Omit] = omit,
) -> BetaToolRunner[None]:
    return client.beta.messages.tool_runner(
        max_tokens=1024,
        model="claude-haiku-4-5",
        tools=[_sync_weather_tool()],
        messages=[{"role": "user", "content": "What is the weather in SF?"}],
        betas=betas,
        context_management=context_management,
        max_iterations=max_iterations,
    )


def _async_compact_runner(
    client: AsyncAnthropic,
    *,
    context_management: Union[BetaContextManagementConfigParam, Omit] = omit,
    max_iterations: Union[int, Omit] = omit,
) -> BetaAsyncToolRunner[None]:
    return client.beta.messages.tool_runner(
        max_tokens=1024,
        model="claude-haiku-4-5",
        tools=[_async_weather_tool()],
        messages=[{"role": "user", "content": "What is the weather in SF?"}],
        context_management=context_management,
        max_iterations=max_iterations,
    )


def _current_messages(runner: Union[BetaToolRunner[None], BetaAsyncToolRunner[None]]) -> List[Any]:
    seen: List[Any] = []

    def read(params: Any) -> Any:
        seen.append(params["messages"])
        return params

    runner.set_messages_params(read)
    return [
        message
        if isinstance(message["content"], str)
        else {**message, "content": [block.to_dict() for block in message["content"]]}
        for message in seen[0]
    ]


# `parse()` serializes the response it was given, and pydantic warns about a block type it doesn't know.
@pytest.mark.filterwarnings("ignore:Pydantic serializer warnings:UserWarning")
@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_compact_before_next_turn_is_sent_after_the_tools_run_sync(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _tool_use_response("get_weather", "toolu_1"),
            _compacted_response_with_an_unmodelled_block(),
            _end_turn_response(),
        ]
    )

    # Strict response validation would reject the block type this SDK version doesn't model.
    with Anthropic(base_url=base_url, api_key="my-anthropic-api-key", max_retries=0) as client:
        runner = _sync_compact_runner(
            client,
            betas=["compact-2026-09-04"],
            context_management={"edits": [{"type": "clear_tool_uses_20250919"}]},
            # The compaction request is not a model turn, so both real turns still fit.
            max_iterations=2,
        )
        yielded: List[Any] = []
        for message in runner:
            yielded.append(message)
            if message.stop_reason == "tool_use":
                runner.compact_before_next_turn({"type": "summarize", "instructions": "Keep the city."})

    assert [message.stop_reason for message in yielded] == ["tool_use", "compaction", "end_turn"]
    assert yielded[1].content[0].content == "Summary so far."

    first, compaction, after = _sent_request_bodies(respx_mock)
    assert compaction["compaction"] == {"type": "summarize", "instructions": "Keep the city."}
    assert "context_management" not in compaction
    assert compaction["messages"] == [
        {"role": "user", "content": "What is the weather in SF?"},
        {
            "role": "assistant",
            "content": [
                {
                    "type": "tool_use",
                    "id": "toolu_1",
                    "name": "get_weather",
                    "input": {"location": "San Francisco, CA", "units": "f"},
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_1",
                    "content": json.dumps(_get_weather("San Francisco, CA", "f")),
                }
            ],
        },
    ]

    # The response goes back as it came, blocks this SDK version doesn't model included.
    assert after["messages"] == [
        {"role": "assistant", "content": _COMPACTION_RESPONSE_CONTENT_WITH_AN_UNMODELLED_BLOCK}
    ]
    assert "compaction" not in after
    assert after["context_management"] == first["context_management"]
    # The beta is the caller's to pass; the runner sends what it was given and nothing more.
    assert [call.request.headers.get("anthropic-beta") for call in cast("List[Any]", respx_mock.calls)] == [
        "compact-2026-09-04"
    ] * 3


@pytest.mark.filterwarnings("ignore:Pydantic serializer warnings:UserWarning")
@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
async def test_compact_before_next_turn_is_sent_after_the_tools_run_async(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _tool_use_response("get_weather", "toolu_1"),
            _compacted_response_with_an_unmodelled_block(),
            _end_turn_response(),
        ]
    )

    async with AsyncAnthropic(base_url=base_url, api_key="my-anthropic-api-key", max_retries=0) as client:
        runner = _async_compact_runner(
            client,
            context_management={"edits": [{"type": "clear_tool_uses_20250919"}]},
            max_iterations=2,
        )
        stop_reasons: List[Any] = []
        async for message in runner:
            stop_reasons.append(message.stop_reason)
            if message.stop_reason == "tool_use":
                runner.compact_before_next_turn()

    assert stop_reasons == ["tool_use", "compaction", "end_turn"]
    first, compaction, after = _sent_request_bodies(respx_mock)
    assert compaction["compaction"] == {"type": "summarize"}
    assert "context_management" not in compaction
    assert [message["role"] for message in compaction["messages"]] == ["user", "assistant", "user"]
    assert compaction["messages"][-1]["content"][0]["type"] == "tool_result"
    assert after["messages"] == [
        {"role": "assistant", "content": _COMPACTION_RESPONSE_CONTENT_WITH_AN_UNMODELLED_BLOCK}
    ]
    assert "compaction" not in after
    assert after["context_management"] == first["context_management"]
    assert all(
        "compact-2026-09-04" not in call.request.headers.get("anthropic-beta", "")
        for call in cast("List[Any]", respx_mock.calls)
    )


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_compact_before_next_turn_on_the_final_turn_is_sent_before_stopping_sync(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=[_end_turn_response(), _compacted_response()])

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        # The final answer is also the last iteration allowed; the compaction still goes out.
        runner = _sync_compact_runner(client, max_iterations=1)
        stop_reasons: List[Any] = []
        for message in runner:
            stop_reasons.append(message.stop_reason)
            if message.stop_reason == "end_turn":
                runner.compact_before_next_turn()

    assert stop_reasons == ["end_turn", "compaction"]
    _, compaction = _sent_request_bodies(respx_mock)
    assert compaction["compaction"] == {"type": "summarize"}
    assert compaction["messages"] == [{"role": "user", "content": "What is the weather in SF?"}, _FINAL_ASSISTANT_TURN]
    assert _current_messages(runner) == _compaction_block_alone()


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
async def test_compact_before_next_turn_on_the_final_turn_is_sent_before_stopping_async(
    respx_mock: MockRouter,
) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=[_end_turn_response(), _compacted_response()])

    async with AsyncAnthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = _async_compact_runner(client, max_iterations=1)
        stop_reasons: List[Any] = []
        async for message in runner:
            stop_reasons.append(message.stop_reason)
            if message.stop_reason == "end_turn":
                runner.compact_before_next_turn()

    assert stop_reasons == ["end_turn", "compaction"]
    _, compaction = _sent_request_bodies(respx_mock)
    assert compaction["compaction"] == {"type": "summarize"}
    assert compaction["messages"] == [{"role": "user", "content": "What is the weather in SF?"}, _FINAL_ASSISTANT_TURN]
    assert _current_messages(runner) == _compaction_block_alone()


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_pending_compaction_is_skipped_on_a_final_turn_with_unrun_tool_calls_sync(
    respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=[_max_tokens_with_tool_use()])

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = _sync_compact_runner(client)
        stop_reasons: List[Any] = []
        with caplog.at_level(logging.WARNING, logger="anthropic.lib.tools._beta_runner"):
            for message in runner:
                stop_reasons.append(message.stop_reason)
                runner.compact_before_next_turn()

    assert stop_reasons == ["max_tokens"]
    assert len(respx_mock.calls) == 1
    assert _current_messages(runner) == [{"role": "user", "content": "What is the weather in SF?"}]
    assert "pending compaction was skipped" in caplog.text


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
async def test_pending_compaction_is_skipped_on_a_final_turn_with_unrun_tool_calls_async(
    respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=[_max_tokens_with_tool_use()])

    async with AsyncAnthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = _async_compact_runner(client)
        stop_reasons: List[Any] = []
        with caplog.at_level(logging.WARNING, logger="anthropic.lib.tools._beta_runner"):
            async for message in runner:
                stop_reasons.append(message.stop_reason)
                runner.compact_before_next_turn()

    assert stop_reasons == ["max_tokens"]
    assert len(respx_mock.calls) == 1
    assert _current_messages(runner) == [{"role": "user", "content": "What is the weather in SF?"}]
    assert "pending compaction was skipped" in caplog.text


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_compact_before_next_turn_waits_out_a_paused_turn_sync(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _paused_server_tool_use(),
            _tool_use_response("get_weather", "toolu_1"),
            _compacted_response(),
            _end_turn_response(),
        ]
    )

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = _sync_compact_runner(client)
        for message in runner:
            if message.stop_reason == "pause_turn":
                runner.compact_before_next_turn()

    _, resumed, compaction, after = _sent_request_bodies(respx_mock)
    assert "compaction" not in resumed
    assert resumed["messages"][-1] == _PAUSED_ASSISTANT_TURN
    assert compaction["compaction"] == {"type": "summarize"}
    assert compaction["messages"][-1]["content"][0]["type"] == "tool_result"
    assert after["messages"] == _compaction_block_alone()


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
async def test_compact_before_next_turn_waits_out_a_paused_turn_async(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _paused_server_tool_use(),
            _tool_use_response("get_weather", "toolu_1"),
            _compacted_response(),
            _end_turn_response(),
        ]
    )

    async with AsyncAnthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = _async_compact_runner(client)
        async for message in runner:
            if message.stop_reason == "pause_turn":
                runner.compact_before_next_turn()

    _, resumed, compaction, after = _sent_request_bodies(respx_mock)
    assert "compaction" not in resumed
    assert resumed["messages"][-1] == _PAUSED_ASSISTANT_TURN
    assert compaction["compaction"] == {"type": "summarize"}
    assert compaction["messages"][-1]["content"][0]["type"] == "tool_result"
    assert after["messages"] == _compaction_block_alone()


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_compact_before_next_turn_before_the_first_iteration_is_the_first_request_sync(
    respx_mock: MockRouter,
) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=[_compacted_response(), _end_turn_response()])

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = _sync_compact_runner(client)
        # An edit made before the compaction request is part of what gets summarized.
        runner.append_messages({"role": "user", "content": "And in NYC?"})
        runner.compact_before_next_turn()
        final = runner.until_done()

    assert final.stop_reason == "end_turn"
    compaction, after = _sent_request_bodies(respx_mock)
    assert compaction["compaction"] == {"type": "summarize"}
    assert [message["content"] for message in compaction["messages"]] == ["What is the weather in SF?", "And in NYC?"]
    assert after["messages"] == _compaction_block_alone()


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
async def test_compact_before_next_turn_before_the_first_iteration_is_the_first_request_async(
    respx_mock: MockRouter,
) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=[_compacted_response(), _end_turn_response()])

    async with AsyncAnthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = _async_compact_runner(client)
        runner.append_messages({"role": "user", "content": "And in NYC?"})
        runner.compact_before_next_turn()
        final = await runner.until_done()

    assert final.stop_reason == "end_turn"
    compaction, after = _sent_request_bodies(respx_mock)
    assert compaction["compaction"] == {"type": "summarize"}
    assert [message["content"] for message in compaction["messages"]] == ["What is the weather in SF?", "And in NYC?"]
    assert after["messages"] == _compaction_block_alone()


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_compact_before_next_turn_again_replaces_the_pending_compaction_sync(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _tool_use_response("get_weather", "toolu_1"),
            _compacted_response(),
            _end_turn_response(),
        ]
    )

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = _sync_compact_runner(client)
        for message in runner:
            if message.stop_reason == "tool_use":
                runner.compact_before_next_turn({"type": "summarize", "instructions": "Keep the city."})
                runner.compact_before_next_turn({"type": "summarize", "instructions": "Keep the units."})

    requests = _sent_request_bodies(respx_mock)
    assert [request.get("compaction") for request in requests] == [
        None,
        {"type": "summarize", "instructions": "Keep the units."},
        None,
    ]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_compact_before_next_turn_on_the_compaction_response_is_ignored_sync(respx_mock: MockRouter) -> None:
    # A fourth request would exhaust the mocked responses and fail the test.
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _tool_use_response("get_weather", "toolu_1"),
            _compacted_response(),
            _end_turn_response(),
        ]
    )

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        edits: List[Any] = []
        runner = _sync_compact_runner(client, context_management={"edits": edits})
        stop_reasons: List[Any] = []
        for message in runner:
            stop_reasons.append(message.stop_reason)
            if message.stop_reason == "compaction":
                # A call that is going to be ignored doesn't raise over a compaction edit either.
                edits.append({"type": "compact_20260112"})
            if message.stop_reason != "end_turn":
                runner.compact_before_next_turn()

    assert stop_reasons == ["tool_use", "compaction", "end_turn"]
    assert [request.get("compaction") for request in _sent_request_bodies(respx_mock)] == [
        None,
        {"type": "summarize"},
        None,
    ]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_a_tool_removed_in_the_history_stays_removed_after_compaction_sync(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _compacted_response(),
            _tool_use_response("get_weather", "toolu_1", input={}),
            _end_turn_response(),
        ]
    )
    calls: List[str] = []

    @beta_tool
    def get_weather() -> BetaFunctionToolResultType:
        """Lookup the weather."""
        calls.append("get_weather")
        return "sunny"

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        )
        runner.append_messages({"role": "system", "content": [_tool_reference_block("tool_removal", "get_weather")]})
        runner.compact_before_next_turn()
        with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
            runner.until_done()

    assert calls == []
    assert _sent_request_bodies(respx_mock)[2]["messages"][-1] == _not_found_result("toolu_1")


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
async def test_a_tool_removed_in_the_history_stays_removed_after_compaction_async(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _compacted_response(),
            _tool_use_response("get_weather", "toolu_1", input={}),
            _end_turn_response(),
        ]
    )
    calls: List[str] = []

    @beta_async_tool
    async def get_weather() -> BetaFunctionToolResultType:
        """Lookup the weather."""
        calls.append("get_weather")
        return "sunny"

    async with AsyncAnthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[get_weather],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        )
        runner.append_messages({"role": "system", "content": [_tool_reference_block("tool_removal", "get_weather")]})
        runner.compact_before_next_turn()
        with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
            await runner.until_done()

    assert calls == []
    assert _sent_request_bodies(respx_mock)[2]["messages"][-1] == _not_found_result("toolu_1")


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_pending_compaction_is_skipped_when_max_iterations_ends_the_run_sync(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=[_tool_use_response("get_weather", "toolu_1")])

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = _sync_compact_runner(client, max_iterations=1)
        for _ in runner:
            runner.compact_before_next_turn()

    assert len(respx_mock.calls) == 1


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.parametrize(
    "content, stop_reason",
    [([{"type": "compaction", "content": None}], "compaction"), ([], "max_tokens")],
    ids=["block without content", "no block"],
)
@pytest.mark.respx(base_url=base_url)
def test_compaction_without_a_summary_keeps_the_history_and_warns_sync(
    respx_mock: MockRouter, caplog: pytest.LogCaptureFixture, content: List[Any], stop_reason: str
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _response_without_a_summary(content, stop_reason),
            _tool_use_response("get_weather", "toolu_1"),
            _end_turn_response(),
        ]
    )

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = _sync_compact_runner(client)
        runner.append_messages({"role": "user", "content": "And in NYC?"})
        runner.compact_before_next_turn()
        yielded = 0
        with caplog.at_level(logging.WARNING, logger="anthropic.lib.tools._beta_runner"):
            for _ in runner:
                yielded += 1
                # This call is made on the compaction response, so it is ignored: no retry is sent.
                if yielded == 1:
                    runner.compact_before_next_turn()

    compaction, after, last = _sent_request_bodies(respx_mock)
    assert after["messages"] == compaction["messages"]
    assert "compaction" not in after
    # The edit made before the compaction request doesn't keep the turn that follows out of the history.
    assert [message["role"] for message in last["messages"]] == ["user", "user", "assistant", "user"]
    assert "Compaction produced no summary" in caplog.text


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_until_done_returns_the_final_turn_after_a_compaction_without_a_summary_sync(
    respx_mock: MockRouter,
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[_end_turn_response(), _response_without_a_summary([], "max_tokens")]
    )

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = _sync_compact_runner(client)
        stop_reasons: List[Any] = []
        for message in runner:
            stop_reasons.append(message.stop_reason)
            runner.compact_before_next_turn()
        final = runner.until_done()

    assert stop_reasons == ["end_turn", "max_tokens"]
    assert final.stop_reason == "end_turn"


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
async def test_until_done_returns_the_final_turn_after_a_compaction_without_a_summary_async(
    respx_mock: MockRouter,
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[_end_turn_response(), _response_without_a_summary([], "max_tokens")]
    )

    async with AsyncAnthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = _async_compact_runner(client)
        stop_reasons: List[Any] = []
        async for message in runner:
            stop_reasons.append(message.stop_reason)
            runner.compact_before_next_turn()
        final = await runner.until_done()

    assert stop_reasons == ["end_turn", "max_tokens"]
    assert final.stop_reason == "end_turn"


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_messages_cannot_be_replaced_while_compacting_sync(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _tool_use_response("get_weather", "toolu_1"),
            _compacted_response(),
            _end_turn_response(),
        ]
    )

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = _sync_compact_runner(client)
        for message in runner:
            if message.stop_reason == "tool_use":
                runner.compact_before_next_turn()
            elif message.stop_reason == "compaction":
                with pytest.raises(ValueError, match="Message params can't be changed"):
                    runner.append_messages({"role": "user", "content": "And in NYC?"})
                with pytest.raises(ValueError, match="while the conversation is being compacted"):
                    runner.set_messages_params(lambda params: {**params, "messages": []})
                # Other params can still change, and the change is kept after the history is replaced.
                runner.set_messages_params(lambda params: {**params, "max_tokens": 2048})

    after = _sent_request_bodies(respx_mock)[2]
    assert after["messages"] == _compaction_block_alone()
    assert after["max_tokens"] == 2048


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_failed_compaction_request_is_not_retried_and_frees_the_messages_sync(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[_tool_use_response("get_weather", "toolu_1"), httpx2.Response(500, json={"type": "error"})]
    )

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = _sync_compact_runner(client)
        with pytest.raises(InternalServerError):
            for _ in runner:
                runner.compact_before_next_turn()

        runner.append_messages({"role": "user", "content": "And in NYC?"})
        assert list(runner) == []

    assert [request.get("compaction") for request in _sent_request_bodies(respx_mock)] == [None, {"type": "summarize"}]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
async def test_failed_compaction_request_is_not_retried_and_frees_the_messages_async(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[_tool_use_response("get_weather", "toolu_1"), httpx2.Response(500, json={"type": "error"})]
    )

    async with AsyncAnthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = _async_compact_runner(client)
        with pytest.raises(InternalServerError):
            async for _ in runner:
                runner.compact_before_next_turn()

        runner.append_messages({"role": "user", "content": "And in NYC?"})
        assert [message async for message in runner] == []

    assert [request.get("compaction") for request in _sent_request_bodies(respx_mock)] == [None, {"type": "summarize"}]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
def test_compaction_param_is_refused_on_a_tool_runner() -> None:
    refusal = (
        "`compaction` cannot be set on a tool runner: every request in the loop would compact again. "
        "Call `runner.compact_before_next_turn()` when the conversation should be compacted instead."
    )
    with Anthropic(base_url=base_url, api_key="my-anthropic-api-key") as client:
        runner = _sync_compact_runner(client)
        with pytest.raises(ValueError) as from_setter:
            runner.set_messages_params(lambda params: {**params, "compaction": {"type": "summarize"}})
        with pytest.raises(ValueError) as from_constructor:
            BetaToolRunner(
                params={
                    "max_tokens": 1024,
                    "model": "claude-haiku-4-5",
                    "messages": [{"role": "user", "content": "What is the weather in SF?"}],
                    "compaction": {"type": "summarize"},
                    "output_format": type(None),
                },
                options={},
                tools=[_sync_weather_tool()],
                client=client,
            )

    assert str(from_setter.value) == str(from_constructor.value) == refusal


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
def test_compact_before_next_turn_is_refused_beside_a_compaction_edit() -> None:
    with Anthropic(base_url=base_url, api_key="my-anthropic-api-key") as client:
        runner = _sync_compact_runner(client, context_management={"edits": [{"type": "compact_20260112"}]})
        with pytest.raises(ValueError, match="has a compaction edit"):
            runner.compact_before_next_turn()

        edits: List[Any] = []
        runner = _sync_compact_runner(client, context_management={"edits": edits})
        runner.compact_before_next_turn()
        with pytest.raises(ValueError, match="has a compaction edit"):
            runner.set_messages_params(
                lambda params: {**params, "context_management": {"edits": [{"type": "compact_20260112"}]}}
            )
        # An edit made in place never reaches the setter, so the refusal comes when the request would be sent.
        edits.append({"type": "compact_20260112"})
        with pytest.raises(ValueError, match="has a compaction edit"):
            next(runner)


def _sse_message(content_block: Dict[str, Any], stop_reason: str, *deltas: Dict[str, Any]) -> httpx2.Response:
    events: List[Dict[str, Any]] = [
        {
            "type": "message_start",
            "message": {
                "id": "msg_streamed",
                "type": "message",
                "role": "assistant",
                "model": "claude-haiku-4-5",
                "content": [],
                "stop_reason": None,
                "stop_sequence": None,
                "usage": {"input_tokens": 1, "output_tokens": 1},
            },
        },
        {"type": "content_block_start", "index": 0, "content_block": content_block},
        *({"type": "content_block_delta", "index": 0, "delta": delta} for delta in deltas),
        {"type": "content_block_stop", "index": 0},
        {
            "type": "message_delta",
            "delta": {"stop_reason": stop_reason, "stop_sequence": None},
            "usage": {"output_tokens": 1},
        },
        {"type": "message_stop"},
    ]
    body = "".join(f"event: {event['type']}\ndata: {json.dumps(event)}\n\n" for event in events)
    return httpx2.Response(200, content=body.encode(), headers={"content-type": "text/event-stream"})


def _streamed_responses() -> List[httpx2.Response]:
    return [
        _sse_message(
            {"type": "tool_use", "id": "toolu_1", "name": "get_weather", "input": {}},
            "tool_use",
            {"type": "input_json_delta", "partial_json": '{"location": "SF", "units": "f"}'},
        ),
        # A compaction block arrives whole on the start event; there is no delta for it.
        _sse_message({"type": "compaction", "content": "Summary so far.", "signature": "sig_01"}, "compaction"),
        _sse_message({"type": "text", "text": ""}, "end_turn", {"type": "text_delta", "text": "Done."}),
    ]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_compact_before_next_turn_when_streaming_sync(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=_streamed_responses())

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[_sync_weather_tool()],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
            stream=True,
        )
        stop_reasons: List[Any] = []
        for stream in runner:
            stop_reasons.append(stream.get_final_message().stop_reason)
            if stop_reasons[-1] == "tool_use":
                runner.compact_before_next_turn()

    assert stop_reasons == ["tool_use", "compaction", "end_turn"]
    _, compaction, after = _sent_request_bodies(respx_mock)
    assert compaction["compaction"] == {"type": "summarize"}
    assert compaction["stream"] is True
    assert after["messages"] == _compaction_block_alone()


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
async def test_compact_before_next_turn_when_streaming_async(respx_mock: MockRouter) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=_streamed_responses())

    async with AsyncAnthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            tools=[_async_weather_tool()],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
            stream=True,
        )
        stop_reasons: List[Any] = []
        async for stream in runner:
            stop_reasons.append((await stream.get_final_message()).stop_reason)
            if stop_reasons[-1] == "tool_use":
                runner.compact_before_next_turn()

    assert stop_reasons == ["tool_use", "compaction", "end_turn"]
    _, compaction, after = _sent_request_bodies(respx_mock)
    assert compaction["compaction"] == {"type": "summarize"}
    assert compaction["stream"] is True
    assert after["messages"] == _compaction_block_alone()
