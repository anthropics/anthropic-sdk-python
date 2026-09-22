import os
import json
import logging
from copy import copy
from typing import Any, Dict, List, Type, Union, cast
from collections.abc import Callable
from typing_extensions import Literal, get_args

import httpx2
import pytest
import pydantic
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
from anthropic.types.beta.beta_tool_param import BetaToolParam
from anthropic.types.beta.beta_stop_reason import BetaStopReason
from anthropic.types.beta.beta_message_param import BetaMessageParam
from anthropic.types.beta.beta_fallback_param import BetaFallbackParam
from anthropic.types.beta.beta_tool_choice_param import BetaToolChoiceParam
from anthropic.types.beta.beta_content_block_param import BetaContentBlockParam
from anthropic.types.beta.beta_output_config_param import BetaOutputConfigParam
from anthropic.types.beta.beta_tool_result_block_param import BetaToolResultBlockParam
from anthropic.types.beta.beta_json_output_format_param import BetaJSONOutputFormatParam
from anthropic.types.beta.beta_web_search_tool_20250305_param import BetaWebSearchTool20250305Param
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
def test_tool_addition_by_value_re_enables_removed_tool_sync(respx_mock: MockRouter) -> None:
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
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "tool_addition",
                            "tool": {"type": "tool_definition", "definition": get_weather.to_dict()},
                        }
                    ],
                },
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


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_tool_removal_in_echoed_compaction_turn_routes_call_down_unknown_tool_path_sync(
    respx_mock: MockRouter,
) -> None:
    # The compaction block comes from the server, so the runner holds it as a response model, not a dict.
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            httpx2.Response(
                200,
                json={
                    "id": "msg_compaction",
                    "type": "message",
                    "role": "assistant",
                    "model": "claude-haiku-4-5",
                    "content": [
                        {
                            "type": "compaction",
                            "content": "Earlier turns, summarized.",
                            "encrypted_content": None,
                            "tool_changes": [
                                {"type": "tool_removal", "tool": {"type": "tool_reference", "name": "get_weather"}}
                            ],
                        }
                    ],
                    "stop_reason": "compaction",
                    "stop_sequence": None,
                    "usage": {"input_tokens": 1, "output_tokens": 1},
                },
            ),
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
        with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
            results = _run_sync_tool_use(
                client,
                tools=[get_weather],
                messages=[{"role": "user", "content": "What is the weather in SF?"}],
            )

    assert weather_called is False
    assert results == [_not_found_result("toolu_change")]
    echoed = _sent_request_bodies(respx_mock)[1]["messages"][1]
    assert echoed["content"][0]["tool_changes"] == [
        {"type": "tool_removal", "tool": {"type": "tool_reference", "name": "get_weather"}}
    ]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_tool_removal_in_compaction_tool_changes_routes_call_down_unknown_tool_path_sync(
    respx_mock: MockRouter,
) -> None:
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
        with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
            results = _run_sync_tool_use(
                client,
                tools=[get_weather],
                messages=[
                    {
                        "role": "assistant",
                        "content": [
                            {
                                "type": "compaction",
                                "content": "Earlier turns, summarized.",
                                "tool_changes": [
                                    {"type": "tool_removal", "tool": {"type": "tool_reference", "name": "get_weather"}}
                                ],
                            }
                        ],
                    },
                    {"role": "user", "content": "What is the weather in SF?"},
                ],
            )

    assert weather_called is False
    assert results == [_not_found_result("toolu_change")]


_ToolChangeScript = dict[str, Callable[[Any], None]]
"""What to do with the runner while handling the message with a given id."""

_WEB_SEARCH: BetaWebSearchTool20250305Param = {"type": "web_search_20250305", "name": "web_search", "max_uses": 3}

_sync_and_async = pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])


def _recording_tool(sync: bool, name: str, calls: list[str], label: str | None = None) -> Any:
    """A tool taking no input that appends `label` (its name by default) to `calls` when it runs."""
    label = label or name

    def run() -> BetaFunctionToolResultType:
        calls.append(label)
        return f"{label} ran"

    async def run_async() -> BetaFunctionToolResultType:
        return run()

    if sync:
        return beta_tool(run, name=name, description=f"Run {name}.")
    return beta_async_tool(run_async, name=name, description=f"Run {name}.")


def _calls_tool(name: str, tool_use_id: str) -> httpx2.Response:
    return _tool_use_response(name, tool_use_id, input={})


def _ran_result(tool_use_id: str, label: str) -> BetaMessageParam:
    return {"role": "user", "content": [{"type": "tool_result", "tool_use_id": tool_use_id, "content": f"{label} ran"}]}


def _tool_changes_message(*blocks: Any) -> BetaMessageParam:
    return {"role": "system", "content": list(blocks)}


def _addition(definition: Any) -> BetaContentBlockParam:
    return {"type": "tool_addition", "tool": {"type": "tool_definition", "definition": definition}}


async def _run_with_tool_changes(
    client: Anthropic | AsyncAnthropic,
    *,
    tools: list[Any],
    script: _ToolChangeScript,
    before_first_request: Callable[[Any], None] | None = None,
    max_iterations: int | Omit = omit,
    messages: list[BetaMessageParam] | None = None,
    stream: bool = False,
) -> None:
    """Drive a tool runner to the end, running `script[message.id]` while each message is being handled."""
    runner: Any = client.beta.messages.tool_runner(
        max_tokens=1024,
        model="claude-haiku-4-5",
        tools=tools,
        messages=messages or [{"role": "user", "content": "What time is it, and what is the weather in SF?"}],
        max_iterations=max_iterations,
        stream=stream,
    )
    if before_first_request is not None:
        before_first_request(runner)
    if isinstance(client, Anthropic):
        for item in runner:
            message = item.get_final_message() if stream else item
            script.get(message.id, _leave_tools_alone)(runner)
    else:
        async for item in runner:
            message = await item.get_final_message() if stream else item
            script.get(message.id, _leave_tools_alone)(runner)


def _leave_tools_alone(runner: Any) -> None:
    pass


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@_sync_and_async
@pytest.mark.respx(base_url=base_url)
async def test_add_tools_sends_the_definition_with_the_next_request(
    sync: bool, client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _calls_tool("get_time", "toolu_time"),
            _calls_tool("get_weather", "toolu_weather"),
            _end_turn_response(),
        ]
    )
    calls: list[str] = []
    get_time = _recording_tool(sync, "get_time", calls)
    get_weather = _recording_tool(sync, "get_weather", calls)

    await _run_with_tool_changes(
        client if sync else async_client,
        tools=[get_time],
        script={"msg_toolu_time": lambda runner: runner.add_tools(get_weather)},
    )

    assert calls == ["get_time", "get_weather"]
    requests = _sent_request_bodies(respx_mock)
    assert [request["tools"] for request in requests] == [[get_time.to_dict()]] * 3
    assert requests[1]["messages"][-2:] == [
        _ran_result("toolu_time", "get_time"),
        _tool_changes_message(_addition(get_weather.to_dict())),
    ]
    assert requests[2]["messages"][-1] == _ran_result("toolu_weather", "get_weather")
    betas = [call.request.headers.get("anthropic-beta", "") for call in cast("list[Any]", respx_mock.calls)]
    assert all("inline-tools-2026-09-15" not in header for header in betas)


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@_sync_and_async
@pytest.mark.respx(base_url=base_url)
async def test_tool_changes_made_before_the_first_request_follow_a_trailing_assistant_message(
    sync: bool, client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[_calls_tool("get_weather", "toolu_weather"), _end_turn_response()]
    )
    calls: list[str] = []
    get_weather = _recording_tool(sync, "get_weather", calls)

    await _run_with_tool_changes(
        client if sync else async_client,
        tools=[],
        script={},
        messages=[cast(BetaMessageParam, _COMPACTION_ASSISTANT_TURN)],
        before_first_request=lambda runner: runner.add_tools(get_weather),
    )

    assert calls == ["get_weather"]
    assert _sent_request_bodies(respx_mock)[0]["messages"] == [
        _COMPACTION_ASSISTANT_TURN,
        _tool_changes_message(_addition(get_weather.to_dict())),
    ]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.parametrize("remove_by", ["tool", "name"])
@_sync_and_async
@pytest.mark.respx(base_url=base_url)
async def test_remove_tools_stops_a_call_already_in_the_turn(
    sync: bool, remove_by: str, client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[_calls_tool("get_weather", "toolu_weather"), _end_turn_response()]
    )
    calls: list[str] = []
    get_weather = _recording_tool(sync, "get_weather", calls)
    removed = get_weather if remove_by == "tool" else "get_weather"

    with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
        await _run_with_tool_changes(
            client if sync else async_client,
            tools=[get_weather],
            script={"msg_toolu_weather": lambda runner: runner.remove_tools(removed)},
        )

    assert calls == []
    requests = _sent_request_bodies(respx_mock)
    assert [request["tools"] for request in requests] == [[get_weather.to_dict()]] * 2
    assert requests[1]["messages"][-2:] == [
        _not_found_result("toolu_weather"),
        _tool_changes_message(_tool_reference_block("tool_removal", "get_weather")),
    ]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.parametrize("removed", ["starting_tool", "tool_added_in_the_same_turn"])
@_sync_and_async
@pytest.mark.respx(base_url=base_url)
async def test_a_removed_tool_stays_removed_when_its_removal_block_leaves_the_history(
    sync: bool, removed: str, client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _calls_tool("get_time", "toolu_time"),
            _calls_tool("get_time", "toolu_time_again"),
            _calls_tool("get_weather", "toolu_weather"),
            _end_turn_response(),
        ]
    )
    calls: list[str] = []
    get_time = _recording_tool(sync, "get_time", calls)
    get_weather = _recording_tool(sync, "get_weather", calls)

    def remove_weather(runner: Any) -> None:
        if removed == "tool_added_in_the_same_turn":
            runner.add_tools(get_weather)
        runner.remove_tools(get_weather)

    def keep_first_message(params: Any) -> Any:
        return {**params, "messages": list(params["messages"])[:1]}

    with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
        await _run_with_tool_changes(
            client if sync else async_client,
            tools=[get_weather, get_time] if removed == "starting_tool" else [get_time],
            script={
                "msg_toolu_time": remove_weather,
                "msg_toolu_time_again": lambda runner: runner.set_messages_params(keep_first_message),
            },
        )

    assert calls == ["get_time", "get_time"]
    requests = _sent_request_bodies(respx_mock)
    # Nothing left in the conversation removes get_weather.
    assert [message["role"] for message in requests[2]["messages"]] == ["user", "assistant", "user"]
    assert requests[3]["messages"][-1] == _not_found_result("toolu_weather")


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.parametrize("order", ["add_then_remove", "remove_then_add"])
@_sync_and_async
@pytest.mark.respx(base_url=base_url)
async def test_tool_changes_in_one_turn_are_sent_together_in_call_order(
    sync: bool, order: str, client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _calls_tool("get_time", "toolu_time"),
            _calls_tool("get_weather", "toolu_weather"),
            _end_turn_response(),
        ]
    )
    calls: list[str] = []
    get_time = _recording_tool(sync, "get_time", calls)
    get_weather = _recording_tool(sync, "get_weather", calls)
    addition = _addition(get_weather.to_dict())
    removal = _tool_reference_block("tool_removal", "get_weather")

    def add_then_remove(runner: Any) -> None:
        runner.add_tools(get_weather)
        runner.remove_tools(get_weather)

    def remove_then_add(runner: Any) -> None:
        runner.remove_tools(get_weather)
        runner.add_tools(get_weather)

    if order == "add_then_remove":
        with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
            await _run_with_tool_changes(
                client if sync else async_client, tools=[get_time], script={"msg_toolu_time": add_then_remove}
            )
        expected_changes, expected_calls = [addition, removal], ["get_time"]
    else:
        await _run_with_tool_changes(
            client if sync else async_client, tools=[get_weather, get_time], script={"msg_toolu_time": remove_then_add}
        )
        expected_changes, expected_calls = [removal, addition], ["get_time", "get_weather"]

    assert calls == expected_calls
    assert _sent_request_bodies(respx_mock)[1]["messages"][-2:] == [
        _ran_result("toolu_time", "get_time"),
        _tool_changes_message(*expected_changes),
    ]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@_sync_and_async
@pytest.mark.respx(base_url=base_url)
async def test_add_tools_replaces_a_tool_of_the_same_name_straight_away(
    sync: bool, client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _calls_tool("get_weather", "toolu_weather"),
            _calls_tool("get_weather", "toolu_weather_again"),
            _end_turn_response(),
        ]
    )
    calls: list[str] = []
    old_get_weather = _recording_tool(sync, "get_weather", calls, label="old get_weather")
    new_get_weather = _recording_tool(sync, "get_weather", calls, label="new get_weather")

    await _run_with_tool_changes(
        client if sync else async_client,
        tools=[old_get_weather],
        script={"msg_toolu_weather": lambda runner: runner.add_tools(new_get_weather)},
    )

    # Even the call the model made before the swap ran the new function.
    assert calls == ["new get_weather", "new get_weather"]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@_sync_and_async
@pytest.mark.respx(base_url=base_url)
async def test_a_call_already_in_the_turn_gets_the_input_error_of_the_tool_added_under_its_name(
    sync: bool, client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[_calls_tool("get_weather", "toolu_weather"), _end_turn_response()]
    )
    calls: list[str] = []
    old_get_weather = _recording_tool(sync, "get_weather", calls)

    def get_weather(city: str) -> str:
        calls.append(city)
        return f"Raining in {city}"

    async def get_weather_async(city: str) -> str:
        return get_weather(city)

    description = "Lookup the weather for a given city."
    new_get_weather: Any = (
        beta_tool(get_weather, description=description)
        if sync
        else beta_async_tool(get_weather_async, name="get_weather", description=description)
    )

    await _run_with_tool_changes(
        client if sync else async_client,
        tools=[old_get_weather],
        script={"msg_toolu_weather": lambda runner: runner.add_tools(new_get_weather)},
    )

    assert calls == []
    assert _sent_request_bodies(respx_mock)[1]["messages"][-2:] == [
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_weather",
                    "content": "ValueError('Invalid arguments for function get_weather')",
                    "is_error": True,
                }
            ],
        },
        _tool_changes_message(_addition(new_get_weather.to_dict())),
    ]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@_sync_and_async
@pytest.mark.respx(base_url=base_url)
async def test_a_removed_tool_added_back_while_handling_a_call_to_it_is_run(
    sync: bool, client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _calls_tool("get_time", "toolu_time"),
            _calls_tool("get_weather", "toolu_weather"),
            _end_turn_response(),
        ]
    )
    calls: list[str] = []
    get_time = _recording_tool(sync, "get_time", calls)
    get_weather = _recording_tool(sync, "get_weather", calls)

    await _run_with_tool_changes(
        client if sync else async_client,
        tools=[get_time, get_weather],
        script={
            "msg_toolu_time": lambda runner: runner.remove_tools(get_weather),
            "msg_toolu_weather": lambda runner: runner.add_tools(get_weather),
        },
    )

    assert calls == ["get_time", "get_weather"]
    requests = _sent_request_bodies(respx_mock)
    # The removal is in the history when the model calls the tool anyway.
    assert requests[1]["messages"][-1] == _tool_changes_message(_tool_reference_block("tool_removal", "get_weather"))
    assert requests[2]["messages"][-2:] == [
        _ran_result("toolu_weather", "get_weather"),
        _tool_changes_message(_addition(get_weather.to_dict())),
    ]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@_sync_and_async
@pytest.mark.respx(base_url=base_url)
async def test_a_raw_definition_is_sent_as_given_and_never_run(
    sync: bool, client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _calls_tool("get_time", "toolu_time"),
            _calls_tool("get_weather", "toolu_weather"),
            _end_turn_response(),
        ]
    )
    calls: list[str] = []
    get_time = _recording_tool(sync, "get_time", calls)
    get_weather = _recording_tool(sync, "get_weather", calls)
    web_search = copy(_WEB_SEARCH)
    raw_get_weather: BetaToolParam = {
        "name": "get_weather",
        "description": "Lookup the weather for a given city.",
        "input_schema": {"type": "object", "properties": {}},
    }

    def add_raw_definitions(runner: Any) -> None:
        runner.add_tools(web_search, raw_get_weather)
        # The runner keeps its own copy, so a later edit doesn't change what is sent.
        web_search["max_uses"] = 10

    with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
        await _run_with_tool_changes(
            client if sync else async_client,
            tools=[get_time, get_weather],
            script={"msg_toolu_time": add_raw_definitions},
        )

    # The raw definition took over the name of the function tool, so the function is not run.
    assert calls == ["get_time"]
    requests = _sent_request_bodies(respx_mock)
    assert requests[1]["messages"][-1] == _tool_changes_message(_addition(_WEB_SEARCH), _addition(raw_get_weather))
    assert requests[2]["messages"][-1] == _not_found_result("toolu_weather")


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@_sync_and_async
@pytest.mark.respx(base_url=base_url)
async def test_tool_changes_made_during_a_paused_turn_are_sent_one_request_later(
    sync: bool, client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _paused_server_tool_use(),
            _calls_tool("get_weather", "toolu_weather"),
            _calls_tool("get_time", "toolu_time"),
            _end_turn_response(),
        ]
    )
    calls: list[str] = []
    get_time = _recording_tool(sync, "get_time", calls)
    get_weather = _recording_tool(sync, "get_weather", calls)

    def swap_tools(runner: Any) -> None:
        runner.remove_tools(get_weather)
        runner.add_tools(get_time)

    with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
        await _run_with_tool_changes(
            client if sync else async_client, tools=[get_weather, _WEB_SEARCH], script={"msg_paused": swap_tools}
        )

    assert calls == ["get_time"]
    requests = _sent_request_bodies(respx_mock)
    # The paused turn is sent back as it came; it has to stay last to be continued.
    assert requests[1]["messages"][1:] == [_PAUSED_ASSISTANT_TURN]
    assert requests[2]["messages"][-2:] == [
        _not_found_result("toolu_weather"),
        _tool_changes_message(_tool_reference_block("tool_removal", "get_weather"), _addition(get_time.to_dict())),
    ]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@_sync_and_async
@pytest.mark.respx(base_url=base_url)
async def test_tool_changes_go_out_with_the_compaction_request_and_follow_its_response(
    sync: bool, client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _calls_tool("get_time", "toolu_time"),
            _compacted_response(),
            _calls_tool("get_forecast", "toolu_forecast"),
            _calls_tool("get_weather", "toolu_weather"),
            _end_turn_response(),
        ]
    )
    calls: list[str] = []
    get_time = _recording_tool(sync, "get_time", calls)
    get_weather = _recording_tool(sync, "get_weather", calls)
    get_forecast = _recording_tool(sync, "get_forecast", calls)

    def add_weather_and_compact(runner: Any) -> None:
        runner.add_tools(get_weather)
        runner.compact_before_next_turn()

    await _run_with_tool_changes(
        client if sync else async_client,
        tools=[get_time],
        script={
            "msg_toolu_time": add_weather_and_compact,
            "msg_compacted": lambda runner: runner.add_tools(get_forecast),
        },
    )

    # A tool added before the compaction is still run after it.
    assert calls == ["get_time", "get_forecast", "get_weather"]
    _, compaction, after, _, _ = _sent_request_bodies(respx_mock)
    assert compaction["compaction"] == {"type": "summarize"}
    assert compaction["messages"][-2:] == [
        _ran_result("toolu_time", "get_time"),
        _tool_changes_message(_addition(get_weather.to_dict())),
    ]
    assert after["messages"] == [*_compaction_block_alone(), _tool_changes_message(_addition(get_forecast.to_dict()))]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@_sync_and_async
@pytest.mark.respx(base_url=base_url)
async def test_a_removed_tool_added_back_while_handling_the_compaction_response_is_run(
    sync: bool, client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _calls_tool("get_time", "toolu_time"),
            _compacted_response(),
            _calls_tool("get_weather", "toolu_weather"),
            _end_turn_response(),
        ]
    )
    calls: list[str] = []
    get_time = _recording_tool(sync, "get_time", calls)
    get_weather = _recording_tool(sync, "get_weather", calls)

    def remove_weather_and_compact(runner: Any) -> None:
        runner.remove_tools(get_weather)
        runner.compact_before_next_turn()

    await _run_with_tool_changes(
        client if sync else async_client,
        tools=[get_time, get_weather],
        script={
            "msg_toolu_time": remove_weather_and_compact,
            "msg_compacted": lambda runner: runner.add_tools(get_weather),
        },
    )

    assert calls == ["get_time", "get_weather"]
    _, compaction, after, _ = _sent_request_bodies(respx_mock)
    assert compaction["messages"][-1] == _tool_changes_message(_tool_reference_block("tool_removal", "get_weather"))
    assert after["messages"] == [*_compaction_block_alone(), _tool_changes_message(_addition(get_weather.to_dict()))]


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.parametrize("ended_by", ["end_turn", "max_iterations"])
@_sync_and_async
@pytest.mark.respx(base_url=base_url)
async def test_tool_changes_pending_when_the_run_ends_are_not_sent(
    sync: bool, ended_by: str, client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    calls: list[str] = []
    get_time = _recording_tool(sync, "get_time", calls)
    get_weather = _recording_tool(sync, "get_weather", calls)

    def swap_tools(runner: Any) -> None:
        runner.add_tools(get_time)
        runner.remove_tools(get_weather)

    if ended_by == "end_turn":
        respx_mock.post("/v1/messages").mock(side_effect=[_end_turn_response()])
        await _run_with_tool_changes(
            client if sync else async_client, tools=[get_weather], script={"msg_end_turn": swap_tools}
        )
    else:
        respx_mock.post("/v1/messages").mock(side_effect=[_calls_tool("get_weather", "toolu_weather")])
        with pytest.warns(UserWarning, match="Tool 'get_weather' not found in tool runner"):
            await _run_with_tool_changes(
                client if sync else async_client,
                tools=[get_weather],
                script={"msg_toolu_weather": swap_tools},
                max_iterations=1,
            )

    assert calls == []
    assert len(_sent_request_bodies(respx_mock)) == 1


@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@_sync_and_async
@pytest.mark.respx(base_url=base_url)
async def test_tool_changes_when_streaming(
    sync: bool, client: Anthropic, async_client: AsyncAnthropic, respx_mock: MockRouter
) -> None:
    respx_mock.post("/v1/messages").mock(
        side_effect=[
            _sse_message(
                {"type": "tool_use", "id": "toolu_time", "name": "get_time", "input": {}},
                "tool_use",
                {"type": "input_json_delta", "partial_json": "{}"},
            ),
            _sse_message({"type": "text", "text": ""}, "end_turn", {"type": "text_delta", "text": "Done."}),
        ]
    )
    calls: list[str] = []
    get_time = _recording_tool(sync, "get_time", calls)
    get_weather = _recording_tool(sync, "get_weather", calls)

    await _run_with_tool_changes(
        client if sync else async_client,
        tools=[get_time],
        # Every streamed message has this id, so the final turn adds the tool again; that change is never sent.
        script={"msg_streamed": lambda runner: runner.add_tools(get_weather)},
        stream=True,
    )

    assert calls == ["get_time"]
    requests = _sent_request_bodies(respx_mock)
    assert [request["stream"] for request in requests] == [True] * 2
    assert requests[1]["messages"][-2:] == [
        _ran_result("toolu_time", "get_time"),
        _tool_changes_message(_addition(get_weather.to_dict())),
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


class _Forecast(pydantic.BaseModel):
    summary: str


_FORECAST_FORMAT: BetaJSONOutputFormatParam = {
    "type": "json_schema",
    "schema": {
        "type": "object",
        "properties": {"summary": {"type": "string"}},
        "required": ["summary"],
        "additionalProperties": False,
    },
}

_REPLY_PARAMS_CASES = pytest.mark.parametrize(
    "tool_choice, output_format, output_config, fallbacks, tool_choice_on_compaction",
    [
        pytest.param(
            {"type": "tool", "name": "get_weather"},
            _Forecast,
            {"effort": "low"},
            omit,
            None,
            id="forced tool and output_format",
        ),
        pytest.param(
            {"type": "any"},
            omit,
            {"effort": "low", "format": _FORECAST_FORMAT},
            omit,
            None,
            id="any tool and output_config.format",
        ),
        pytest.param(
            {"type": "auto"},
            omit,
            {"effort": "low", "format": _FORECAST_FORMAT},
            omit,
            {"type": "auto"},
            id="auto tool_choice stays",
        ),
        pytest.param(
            {"type": "auto"},
            omit,
            {"effort": "low", "format": _FORECAST_FORMAT},
            [
                {"model": "claude-sonnet-4-5", "output_config": {"effort": "medium", "format": _FORECAST_FORMAT}},
                {"model": "claude-opus-4-5", "max_tokens": 512},
            ],
            {"type": "auto"},
            id="fallback output_config.format",
        ),
    ],
)


def _compaction_then_forecast_responses() -> List[httpx2.Response]:
    forecast = {**_end_turn_response().json(), "content": [{"type": "text", "text": '{"summary": "Sunny"}'}]}
    return [_compacted_response(), httpx2.Response(200, json=forecast)]


def _assert_reply_params_are_left_off_the_compaction_request_only(
    respx_mock: MockRouter,
    tool_choice: BetaToolChoiceParam,
    fallbacks: Union[List[BetaFallbackParam], Omit],
    tool_choice_on_compaction: Union[BetaToolChoiceParam, None],
) -> None:
    compaction, after = _sent_request_bodies(respx_mock)
    assert compaction["compaction"] == {"type": "summarize"}
    assert "stop_sequences" not in compaction
    assert "output_format" not in compaction
    assert compaction["output_config"] == {"effort": "low"}
    assert compaction.get("tool_choice") == tool_choice_on_compaction
    if isinstance(fallbacks, Omit):
        assert "fallbacks" not in compaction
    else:
        assert compaction["fallbacks"] == [
            {"model": "claude-sonnet-4-5", "output_config": {"effort": "medium"}},
            {"model": "claude-opus-4-5", "max_tokens": 512},
        ]
        assert after["fallbacks"] == fallbacks
    for kept in ("max_tokens", "system", "tools"):
        assert compaction[kept] == after[kept]
    assert compaction["system"] == "Be brief."
    assert [tool["name"] for tool in compaction["tools"]] == ["get_weather"]

    assert after["stop_sequences"] == ["STOP"]
    assert after["tool_choice"] == tool_choice
    assert after["output_config"]["effort"] == "low"
    assert after["output_config"]["format"]["type"] == "json_schema"
    assert [call.request.headers.get("anthropic-beta") for call in cast("List[Any]", respx_mock.calls)] == [
        "compact-2026-09-04"
    ] * 2


@_REPLY_PARAMS_CASES
@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
def test_compaction_request_leaves_off_reply_params_sync(
    respx_mock: MockRouter,
    tool_choice: BetaToolChoiceParam,
    output_format: Union[Type[_Forecast], Omit],
    output_config: BetaOutputConfigParam,
    fallbacks: Union[List[BetaFallbackParam], Omit],
    tool_choice_on_compaction: Union[BetaToolChoiceParam, None],
) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=_compaction_then_forecast_responses())

    with Anthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            system="Be brief.",
            tools=[_sync_weather_tool()],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
            betas=["compact-2026-09-04"],
            stop_sequences=["STOP"],
            tool_choice=tool_choice,
            output_format=output_format,
            output_config=output_config,
            fallbacks=fallbacks,
        )
        runner.compact_before_next_turn()
        runner.until_done()

    _assert_reply_params_are_left_off_the_compaction_request_only(
        respx_mock, tool_choice, fallbacks, tool_choice_on_compaction
    )


@_REPLY_PARAMS_CASES
@pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")
@pytest.mark.respx(base_url=base_url)
async def test_compaction_request_leaves_off_reply_params_async(
    respx_mock: MockRouter,
    tool_choice: BetaToolChoiceParam,
    output_format: Union[Type[_Forecast], Omit],
    output_config: BetaOutputConfigParam,
    fallbacks: Union[List[BetaFallbackParam], Omit],
    tool_choice_on_compaction: Union[BetaToolChoiceParam, None],
) -> None:
    respx_mock.post("/v1/messages").mock(side_effect=_compaction_then_forecast_responses())

    async with AsyncAnthropic(
        base_url=base_url, api_key="my-anthropic-api-key", _strict_response_validation=True, max_retries=0
    ) as client:
        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-haiku-4-5",
            system="Be brief.",
            tools=[_async_weather_tool()],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
            betas=["compact-2026-09-04"],
            stop_sequences=["STOP"],
            tool_choice=tool_choice,
            output_format=output_format,
            output_config=output_config,
            fallbacks=fallbacks,
        )
        runner.compact_before_next_turn()
        await runner.until_done()

    _assert_reply_params_are_left_off_the_compaction_request_only(
        respx_mock, tool_choice, fallbacks, tool_choice_on_compaction
    )


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
