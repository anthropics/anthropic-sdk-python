from __future__ import annotations

import os
import inspect
from typing import Any, Set, TypeVar, cast
from typing_extensions import Iterator, AsyncIterator

import httpx
import pytest
from respx import MockRouter

from anthropic import Stream, Anthropic, AsyncStream, AsyncAnthropic
from anthropic._compat import PYDANTIC_V2
from anthropic.lib.streaming import MessageStreamEvent
from anthropic.types.message import Message
from anthropic.resources.messages import DEPRECATED_MODELS
from anthropic.lib.streaming._messages import TRACKS_TOOL_INPUT

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
api_key = "my-anthropic-api-key"

sync_client = Anthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True)
async_client = AsyncAnthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True)

_T = TypeVar("_T")

# copied from the real API
stream_example = """
event: message_start
data: {"type":"message_start","message":{"id":"msg_4QpJur2dWWDjF6C758FbBw5vm12BaVipnK","type":"message","role":"assistant","content":[],"model":"claude-3-opus-20240229","stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":11,"output_tokens":1}}}

event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}}

event: ping
data: {"type": "ping"}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"Hello"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" there"}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"!"}}

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"end_turn","stop_sequence":null},"usage":{"output_tokens":6}}

event: message_stop
data: {"type":"message_stop"}
"""


streaming_with_tool_use_example = """
event: message_start
data: {"type":"message_start","message":{"id":"msg_019Q1hrJbZG26Fb9BQhrkHEr","type":"message","role":"assistant","model":"claude-sonnet-4-20250514","content":[],"stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":377,"cache_creation_input_tokens":0,"cache_read_input_tokens":0,"output_tokens":1,"service_tier":"standard"}}     }

event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}            }

event: ping
data: {"type": "ping"}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"I"}    }

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"'ll check the current weather in Paris for you."}           }

event: content_block_stop
data: {"type":"content_block_stop","index":0             }

event: content_block_start
data: {"type":"content_block_start","index":1,"content_block":{"type":"tool_use","id":"toolu_01NRLabsLyVHZPKxbKvkfSMn","name":"get_weather","input":{}}             }

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":""}   }

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"{\\"locati"}               }

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"on\\": \\"P"}              }

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"ar"}    }

event: content_block_delta
data: {"type":"content_block_delta","index":1,"delta":{"type":"input_json_delta","partial_json":"is\\"}"}               }

event: content_block_stop
data: {"type":"content_block_stop","index":1           }

event: message_delta
data: {"type":"message_delta","delta":{"stop_reason":"tool_use","stop_sequence":null},"usage":{"output_tokens":65}   }

event: message_stop
data: {"type":"message_stop"       }
"""


def basic_response() -> Iterator[bytes]:
    for line in stream_example.splitlines():
        yield line.encode() + b"\n"


def streaming_with_tool_use_example_response() -> Iterator[bytes]:
    for line in streaming_with_tool_use_example.splitlines():
        yield line.encode() + b"\n"


async def to_async_iter(iter: Iterator[_T]) -> AsyncIterator[_T]:
    for event in iter:
        yield event


def assert_basic_response(events: list[MessageStreamEvent], message: Message) -> None:
    assert message.id == "msg_4QpJur2dWWDjF6C758FbBw5vm12BaVipnK"
    assert message.model == "claude-3-opus-20240229"
    assert message.role == "assistant"
    assert message.stop_reason == "end_turn"
    assert message.stop_sequence is None
    assert message.type == "message"
    assert len(message.content) == 1

    content = message.content[0]
    assert content.type == "text"
    assert content.text == "Hello there!"

    assert [e.type for e in events] == [
        "message_start",
        "content_block_start",
        "content_block_delta",
        "text",
        "content_block_delta",
        "text",
        "content_block_delta",
        "text",
        "content_block_stop",
        "message_delta",
    ]


def assert_tool_use_response(events: list[MessageStreamEvent], message: Message) -> None:
    assert message.id == "msg_019Q1hrJbZG26Fb9BQhrkHEr"
    assert message.model == "claude-sonnet-4-20250514"
    assert message.role == "assistant"
    assert message.stop_reason == "tool_use"
    assert message.stop_sequence is None
    assert message.type == "message"
    assert len(message.content) == 2

    content = message.content[0]
    assert content.type == "text"
    assert content.text == "I'll check the current weather in Paris for you."

    tool_use = message.content[1]
    assert tool_use.type == "tool_use"
    assert tool_use.id == "toolu_01NRLabsLyVHZPKxbKvkfSMn"
    assert tool_use.name == "get_weather"
    assert tool_use.input == {
        "location": "Paris",
    }

    assert message.usage.input_tokens == 377
    assert message.usage.output_tokens == 65
    assert message.usage.cache_creation_input_tokens == 0
    assert message.usage.cache_read_input_tokens == 0
    assert message.usage.service_tier == "standard"
    assert message.usage.server_tool_use == None

    print(f"Events: {[e.type for e in events]}")

    assert [e.type for e in events] == [
        "message_start",
        "content_block_start",
        "content_block_delta",
        "text",
        "content_block_delta",
        "text",
        "content_block_stop",
        "content_block_start",
        "content_block_delta",
        "input_json",
        "content_block_delta",
        "input_json",
        "content_block_delta",
        "input_json",
        "content_block_delta",
        "input_json",
        "content_block_delta",
        "input_json",
        "content_block_stop",
        "message_delta",
    ]


class TestSyncMessages:
    @pytest.mark.respx(base_url=base_url)
    def test_basic_response(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, content=basic_response()))

        with sync_client.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-3-opus-20240229",
        ) as stream:
            with pytest.warns(DeprecationWarning):
                assert isinstance(cast(Any, stream), Stream)

            assert_basic_response([event for event in stream], stream.get_final_message())

    @pytest.mark.respx(base_url=base_url)
    def test_context_manager(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, content=basic_response()))

        with sync_client.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-3-opus-20240229",
        ) as stream:
            assert not stream.response.is_closed

        # response should be closed even if the body isn't read
        assert stream.response.is_closed

    @pytest.mark.respx(base_url=base_url)
    def test_deprecated_model_warning_stream(self, respx_mock: MockRouter) -> None:
        for deprecated_model in DEPRECATED_MODELS:
            respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, content=basic_response()))

            with pytest.warns(DeprecationWarning, match=f"The model '{deprecated_model}' is deprecated"):
                with sync_client.messages.stream(
                    max_tokens=1024,
                    messages=[{"role": "user", "content": "Hello"}],
                    model=deprecated_model,
                ) as stream:
                    # Consume the stream to ensure the warning is triggered
                    stream.until_done()

    @pytest.mark.respx(base_url=base_url)
    def test_tool_use(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=streaming_with_tool_use_example_response())
        )

        with sync_client.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-sonnet-4-20250514",
        ) as stream:
            with pytest.warns(DeprecationWarning):
                assert isinstance(cast(Any, stream), Stream)

            assert_tool_use_response([event for event in stream], stream.get_final_message())


class TestAsyncMessages:
    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_basic_response(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, content=to_async_iter(basic_response())))

        async with async_client.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-3-opus-20240229",
        ) as stream:
            with pytest.warns(DeprecationWarning):
                assert isinstance(cast(Any, stream), AsyncStream)

            assert_basic_response([event async for event in stream], await stream.get_final_message())

    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_context_manager(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, content=to_async_iter(basic_response())))

        async with async_client.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-3-opus-20240229",
        ) as stream:
            assert not stream.response.is_closed

        # response should be closed even if the body isn't read
        assert stream.response.is_closed

    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_deprecated_model_warning_stream(self, respx_mock: MockRouter) -> None:
        for deprecated_model in DEPRECATED_MODELS:
            respx_mock.post("/v1/messages").mock(
                return_value=httpx.Response(200, content=to_async_iter(basic_response()))
            )

            with pytest.warns(DeprecationWarning, match=f"The model '{deprecated_model}' is deprecated"):
                async with async_client.messages.stream(
                    max_tokens=1024,
                    messages=[{"role": "user", "content": "Hello"}],
                    model=deprecated_model,
                ) as stream:
                    # Consume the stream to ensure the warning is triggered
                    await stream.get_final_message()

    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_tool_use(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=to_async_iter(streaming_with_tool_use_example_response()))
        )

        async with async_client.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-sonnet-4-20250514",
        ) as stream:
            with pytest.warns(DeprecationWarning):
                assert isinstance(cast(Any, stream), AsyncStream)

            assert_tool_use_response([event async for event in stream], await stream.get_final_message())


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
def test_stream_method_definition_in_sync(sync: bool) -> None:
    client: Anthropic | AsyncAnthropic = sync_client if sync else async_client

    sig = inspect.signature(client.messages.stream)
    generated_sig = inspect.signature(client.messages.create)

    errors: list[str] = []

    for name, generated_param in generated_sig.parameters.items():
        if name == "stream":
            # intentionally excluded
            continue

        custom_param = sig.parameters.get(name)
        if not custom_param:
            errors.append(f"the `{name}` param is missing")
            continue

        if custom_param.annotation != generated_param.annotation:
            errors.append(
                f"types for the `{name}` param are do not match; generated={repr(generated_param.annotation)} custom={repr(custom_param.annotation)}"
            )
            continue

    if errors:
        raise AssertionError(
            f"{len(errors)} errors encountered with the {'sync' if sync else 'async'} client `messages.stream()` method:\n\n"
            + "\n\n".join(errors)
        )


# go through all the ContentBlock types to make sure the type alias is up to date
# with any type that has an input property of type object
@pytest.mark.skipif(not PYDANTIC_V2, reason='only applicable in pydantic v2')
def test_tracks_tool_input_type_alias_is_up_to_date() -> None:
    from typing import get_args

    from pydantic import BaseModel

    from anthropic.types.content_block import ContentBlock

    # Get the content block union type
    content_block_union = get_args(ContentBlock)[0]

    # Get all types from ContentBlock union
    content_block_types = get_args(content_block_union)

    # Types that should have an input property
    types_with_input: Set[Any] = set()

    # Check each type to see if it has an input property in its model_fields
    for block_type in content_block_types:
        if issubclass(block_type, BaseModel) and "input" in block_type.model_fields:
            types_with_input.add(block_type)

    # Get the types included in TRACKS_TOOL_INPUT
    tracked_types = TRACKS_TOOL_INPUT

    # Make sure all types with input are tracked
    for block_type in types_with_input:
        assert block_type in tracked_types, (
            f"ContentBlock type {block_type.__name__} has an input property, "
            f"but is not included in TRACKS_TOOL_INPUT. You probably need to update the TRACKS_TOOL_INPUT type alias."
        )
