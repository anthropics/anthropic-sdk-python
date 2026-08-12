from __future__ import annotations

import os
from typing import Any, Set, TypeVar, Iterator, cast

import httpx
import pytest
from respx import MockRouter

from anthropic import Stream, Anthropic, AsyncStream, AsyncAnthropic
from anthropic._utils import assert_signatures_in_sync
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.streaming import InputJsonEvent, ParsedMessageStreamEvent
from anthropic.types.message import Message
from anthropic.resources.messages import DEPRECATED_MODELS
from anthropic.lib.streaming._messages import TRACKS_TOOL_INPUT

from .helpers import get_response, to_async_iter

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
api_key = "my-anthropic-api-key"

sync_client = Anthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True)
async_client = AsyncAnthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True)

_T = TypeVar("_T")

# the accumulator must wrap the raw parser error with context and echo the offending JSON
INVALID_TOOL_JSON_ERROR = (
    r"^Unable to parse tool parameter JSON from model\. Please retry your request or adjust your prompt\. "
    r'Error: .+\. JSON: \{"location": "Paris", "unit": celsius\}$'
)


def assert_basic_response(events: list[ParsedMessageStreamEvent[None]], message: Message) -> None:
    assert message.id == "msg_4QpJur2dWWDjF6C758FbBw5vm12BaVipnK"
    assert message.model == "claude-3-opus-latest"
    assert message.role == "assistant"
    assert message.stop_reason == "end_turn"
    assert message.stop_sequence is None
    assert message.type == "message"
    assert len(message.content) == 1

    content = message.content[0]
    assert content.type == "text"
    assert content.text == "Hello there!"
    # accumulated blocks must serialize like a non-streaming response: keys the API didn't send stay unset
    assert content.to_dict() == {"type": "text", "text": "Hello there!"}

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


def assert_tool_use_response(events: list[ParsedMessageStreamEvent[None]], message: Message) -> None:
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


def assert_server_tool_use_response(events: list[ParsedMessageStreamEvent[None]], message: Message) -> None:
    assert [e.type for e in events] == [
        "message_start",
        "content_block_start",
        *["content_block_delta", "input_json"] * 6,
        "content_block_stop",
        "content_block_start",
        "content_block_stop",
        "content_block_start",
        "content_block_delta",
        "citation",
        "content_block_delta",
        "text",
        "content_block_delta",
        "text",
        "content_block_stop",
        "message_delta",
    ]

    server_tool_use = message.content[0]
    assert server_tool_use.type == "server_tool_use"
    assert server_tool_use.input == {"query": "anthropic claude release notes"}

    # input_json events must fire for server_tool_use blocks, not just client tool_use
    input_json_events = [e for e in events if isinstance(e, InputJsonEvent)]
    assert [e.partial_json for e in input_json_events] == [
        "",
        '{"query": "',
        "anthropic cl",
        "aude re",
        "lease notes",
        '"}',
    ]
    assert input_json_events[-1].snapshot == {"query": "anthropic claude release notes"}


def get_tool_use_response_without_caller() -> Iterator[bytes]:
    return (line.replace(b'"caller":{"type":"direct"},', b"") for line in get_response("tool_use_response.txt"))


def assert_tool_use_caller_unset(message: Message) -> None:
    tool_use = message.content[1]
    assert tool_use.type == "tool_use"
    assert tool_use.input == {"location": "Paris"}
    assert tool_use.caller is None
    # an omitted `caller` must stay unset so it doesn't round-trip as `"caller": null`, which the API rejects
    assert "caller" not in tool_use.model_fields_set
    assert "caller" not in tool_use.to_dict()


def assert_refusal_response(message: Message) -> None:
    assert message.stop_reason == "refusal"
    assert message.stop_details is not None
    assert message.stop_details.type == "refusal"
    assert message.stop_details.category == "cyber"
    assert message.stop_details.explanation == "This request was refused due to policy."


def assert_message_delta_fields_response(message: Message) -> None:
    # every field the final `message_delta` carried must land on the accumulated message
    assert message.container is not None
    assert message.container.id == "container_01AbCdEfGh"
    assert message.usage.output_tokens == 8
    assert message.usage.input_tokens == 40
    assert message.usage.cache_creation_input_tokens == 12
    assert message.usage.cache_read_input_tokens == 7
    assert message.usage.output_tokens_details is not None
    assert message.usage.output_tokens_details.thinking_tokens == 3
    assert message.usage.server_tool_use is not None
    assert message.usage.server_tool_use.web_search_requests == 1
    # never re-sent on `message_delta`, so these must survive from `message_start`
    assert message.usage.service_tier == "standard"
    assert message.usage.cache_creation is not None
    assert message.usage.cache_creation.ephemeral_5m_input_tokens == 10


def assert_message_delta_omitted_usage_response(message: Message) -> None:
    # the delta omitted every optional usage key, so the `message_start` values stand
    assert message.usage.output_tokens == 8
    assert message.usage.input_tokens == 25
    assert message.usage.cache_creation_input_tokens == 10
    assert message.usage.cache_read_input_tokens == 5
    assert message.usage.service_tier == "priority"
    assert message.usage.cache_creation is not None
    assert message.usage.cache_creation.ephemeral_5m_input_tokens == 10
    assert message.container is None


class TestSyncMessages:
    @pytest.mark.respx(base_url=base_url)
    def test_basic_response(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=get_response("basic_response.txt"))
        )

        with sync_client.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-3-opus-latest",
        ) as stream:
            with pytest.warns(DeprecationWarning):
                assert isinstance(cast(Any, stream), Stream)

            assert_basic_response([event for event in stream], stream.get_final_message())

    @pytest.mark.respx(base_url=base_url)
    def test_context_manager(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=get_response("basic_response.txt"))
        )

        with sync_client.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-3-opus-latest",
        ) as stream:
            assert not stream.response.is_closed

        # response should be closed even if the body isn't read
        assert stream.response.is_closed

    @pytest.mark.respx(base_url=base_url)
    def test_deprecated_model_warning_stream(self, respx_mock: MockRouter) -> None:
        for deprecated_model in DEPRECATED_MODELS:
            respx_mock.post("/v1/messages").mock(
                return_value=httpx.Response(200, content=get_response("basic_response.txt"))
            )

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
            return_value=httpx.Response(200, content=get_response("tool_use_response.txt"))
        )

        with sync_client.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-sonnet-4-5",
        ) as stream:
            with pytest.warns(DeprecationWarning):
                assert isinstance(cast(Any, stream), Stream)

            assert_tool_use_response([event for event in stream], stream.get_final_message())

    @pytest.mark.respx(base_url=base_url)
    def test_server_tool_use(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=get_response("server_tool_use_response.txt"))
        )

        with sync_client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Say hello there!"}],
            model="claude-sonnet-4-5",
        ) as stream:
            assert_server_tool_use_response([event for event in stream], stream.get_final_message())

    @pytest.mark.respx(base_url=base_url)
    def test_tool_use_invalid_json(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=get_response("tool_use_invalid_json_response.txt"))
        )

        with pytest.raises(ValueError, match=INVALID_TOOL_JSON_ERROR):
            with sync_client.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": "What's the weather in Paris?"}],
                model="claude-sonnet-4-5",
            ) as stream:
                stream.until_done()

    @pytest.mark.respx(base_url=base_url)
    def test_tool_use_caller_omitted(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=get_tool_use_response_without_caller())
        )

        with sync_client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": "What is the weather in Paris?"}],
            model="claude-sonnet-4-5",
        ) as stream:
            assert_tool_use_caller_unset(stream.get_final_message())

    @pytest.mark.respx(base_url=base_url)
    def test_refusal_stop_details_propagated(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=get_response("refusal_response.txt"))
        )

        with sync_client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Say hello there!"}],
            model="claude-opus-4-7",
        ) as stream:
            assert_refusal_response(stream.get_final_message())

    @pytest.mark.respx(base_url=base_url)
    def test_message_delta_fields_propagated(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=get_response("message_delta_fields_response.txt"))
        )

        with sync_client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Say hello there!"}],
            model="claude-sonnet-4-5",
        ) as stream:
            assert_message_delta_fields_response(stream.get_final_message())

    @pytest.mark.respx(base_url=base_url)
    def test_message_delta_omitted_usage_keeps_message_start(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=get_response("message_delta_omitted_usage_response.txt"))
        )

        with sync_client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Say hello there!"}],
            model="claude-sonnet-4-5",
        ) as stream:
            assert_message_delta_omitted_usage_response(stream.get_final_message())

    @pytest.mark.respx(base_url=base_url)
    @pytest.mark.filterwarnings("error")
    def test_message_stop_event_serialization(self, respx_mock: MockRouter) -> None:
        # trailing blank line terminates the final `message_stop` SSE so it is dispatched
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=iter([*get_response("basic_response.txt"), b"\n"]))
        )

        with sync_client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Say hello there!"}],
            model="claude-opus-4-7",
        ) as stream:
            stop_event = [event for event in stream][-1]

        assert stop_event.type == "message_stop"
        assert stop_event.message.content[0].type == "text"
        # must not emit `PydanticSerializationUnexpectedValue` warnings
        stop_event.model_dump()
        stop_event.model_dump_json()


class TestAsyncMessages:
    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_basic_response(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=to_async_iter(get_response("basic_response.txt")))
        )

        async with async_client.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-3-opus-latest",
        ) as stream:
            with pytest.warns(DeprecationWarning):
                assert isinstance(cast(Any, stream), AsyncStream)

            assert_basic_response([event async for event in stream], await stream.get_final_message())

    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_context_manager(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=to_async_iter(get_response("basic_response.txt")))
        )

        async with async_client.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-3-opus-latest",
        ) as stream:
            assert not stream.response.is_closed

        # response should be closed even if the body isn't read
        assert stream.response.is_closed

    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_deprecated_model_warning_stream(self, respx_mock: MockRouter) -> None:
        for deprecated_model in DEPRECATED_MODELS:
            respx_mock.post("/v1/messages").mock(
                return_value=httpx.Response(200, content=to_async_iter(get_response("basic_response.txt")))
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
            return_value=httpx.Response(200, content=to_async_iter(get_response("tool_use_response.txt")))
        )

        async with async_client.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-sonnet-4-5",
        ) as stream:
            with pytest.warns(DeprecationWarning):
                assert isinstance(cast(Any, stream), AsyncStream)

            assert_tool_use_response([event async for event in stream], await stream.get_final_message())

    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_server_tool_use(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=to_async_iter(get_response("server_tool_use_response.txt")))
        )

        async with async_client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Say hello there!"}],
            model="claude-sonnet-4-5",
        ) as stream:
            assert_server_tool_use_response([event async for event in stream], await stream.get_final_message())

    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_tool_use_invalid_json(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=to_async_iter(get_response("tool_use_invalid_json_response.txt")))
        )

        with pytest.raises(ValueError, match=INVALID_TOOL_JSON_ERROR):
            async with async_client.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": "What's the weather in Paris?"}],
                model="claude-sonnet-4-5",
            ) as stream:
                await stream.until_done()

    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_tool_use_caller_omitted(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=to_async_iter(get_tool_use_response_without_caller()))
        )

        async with async_client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": "What is the weather in Paris?"}],
            model="claude-sonnet-4-5",
        ) as stream:
            assert_tool_use_caller_unset(await stream.get_final_message())

    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_refusal_stop_details_propagated(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=to_async_iter(get_response("refusal_response.txt")))
        )

        async with async_client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Say hello there!"}],
            model="claude-opus-4-7",
        ) as stream:
            assert_refusal_response(await stream.get_final_message())

    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_message_delta_fields_propagated(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=to_async_iter(get_response("message_delta_fields_response.txt")))
        )

        async with async_client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Say hello there!"}],
            model="claude-sonnet-4-5",
        ) as stream:
            assert_message_delta_fields_response(await stream.get_final_message())

    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_message_delta_omitted_usage_keeps_message_start(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                200, content=to_async_iter(get_response("message_delta_omitted_usage_response.txt"))
            )
        )

        async with async_client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Say hello there!"}],
            model="claude-sonnet-4-5",
        ) as stream:
            assert_message_delta_omitted_usage_response(await stream.get_final_message())

    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    @pytest.mark.filterwarnings("error")
    async def test_message_stop_event_serialization(self, respx_mock: MockRouter) -> None:
        # trailing blank line terminates the final `message_stop` SSE so it is dispatched
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=to_async_iter(iter([*get_response("basic_response.txt"), b"\n"])))
        )

        async with async_client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Say hello there!"}],
            model="claude-opus-4-7",
        ) as stream:
            stop_event = [event async for event in stream][-1]

        assert stop_event.type == "message_stop"
        assert stop_event.message.content[0].type == "text"
        # must not emit `PydanticSerializationUnexpectedValue` warnings
        stop_event.model_dump()
        stop_event.model_dump_json()


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
def test_stream_method_definition_in_sync(sync: bool) -> None:
    client: Anthropic | AsyncAnthropic = sync_client if sync else async_client
    assert_signatures_in_sync(
        client.messages.create,
        client.messages.stream,
        exclude_params={"stream"},
    )


# go through all the ContentBlock types to make sure the type alias is up to date
# with any type that has an input property of type object
@pytest.mark.skipif(PYDANTIC_V1, reason="only applicable in pydantic v2")
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
