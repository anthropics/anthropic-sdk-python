from __future__ import annotations

import os
from typing import Any, Set, TypeVar, cast

import httpx
import pytest
from respx import MockRouter

from anthropic import Stream, Anthropic, AsyncStream, AsyncAnthropic
from anthropic._utils import assert_signatures_in_sync
from anthropic._compat import PYDANTIC_V1
from anthropic.lib.streaming import ParsedMessageStreamEvent
from anthropic.types.message import Message
from anthropic.resources.messages import DEPRECATED_MODELS
from anthropic.lib.streaming._messages import TRACKS_TOOL_INPUT

from .helpers import get_response, to_async_iter

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
api_key = "my-anthropic-api-key"

sync_client = Anthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True)
async_client = AsyncAnthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True)

_T = TypeVar("_T")


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


def assert_refusal_response(message: Message) -> None:
    assert message.stop_reason == "refusal"
    assert message.stop_details is not None
    assert message.stop_details.type == "refusal"
    assert message.stop_details.category == "cyber"
    assert message.stop_details.explanation == "This request was refused due to policy."


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


# Regression tests for https://github.com/anthropics/anthropic-sdk-python/issues/1325
#
# ParsedContentBlock was missing 5 of 6 server tool result types. When blocks like
# CodeExecutionToolResultBlock arrived as content_block_start events during streaming,
# construct_type() failed discriminated union parsing and silently dropped them from
# current_snapshot.content, so get_final_message().content was missing server tool results.


class TestServerToolResultBlocks:
    @pytest.mark.respx(base_url=base_url)
    def test_server_tool_result_blocks_not_dropped(self, respx_mock: MockRouter) -> None:
        """
        Sync: server tool result blocks (web_search_tool_result, code_execution_tool_result)
        must appear in get_final_message().content when streamed concurrently with client tools.
        """
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=get_response("server_tool_result_response.txt"))
        )

        with sync_client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": "search the web and run code"}],
            model="claude-sonnet-4-20250514",
        ) as stream:
            events = [event for event in stream]
            final_message = stream.get_final_message()

        block_types = [b.type for b in final_message.content]

        assert len(final_message.content) == 4, (
            f"Expected 4 content blocks, got {len(final_message.content)}. "
            f"Types present: {block_types}. "
            f"server tool result blocks are being silently dropped."
        )
        assert final_message.content[0].type == "server_tool_use"
        assert final_message.content[1].type == "tool_use"
        assert final_message.content[2].type == "web_search_tool_result"
        assert final_message.content[3].type == "code_execution_tool_result"

        # All 4 content_block_start events must have been yielded to the caller
        block_start_events = [e for e in events if e.type == "content_block_start"]
        assert len(block_start_events) == 4, (
            f"Expected 4 content_block_start events, got {len(block_start_events)}"
        )

    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_async_server_tool_result_blocks_not_dropped(self, respx_mock: MockRouter) -> None:
        """
        Async: same regression test as above for the async streaming path.
        """
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=to_async_iter(get_response("server_tool_result_response.txt")))
        )

        async with async_client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": "search the web and run code"}],
            model="claude-sonnet-4-20250514",
        ) as stream:
            events = [event async for event in stream]
            final_message = await stream.get_final_message()

        block_types = [b.type for b in final_message.content]

        assert len(final_message.content) == 4, (
            f"Expected 4 content blocks, got {len(final_message.content)}. "
            f"Types present: {block_types}. "
            f"server tool result blocks are being silently dropped."
        )
        assert final_message.content[0].type == "server_tool_use"
        assert final_message.content[1].type == "tool_use"
        assert final_message.content[2].type == "web_search_tool_result"
        assert final_message.content[3].type == "code_execution_tool_result"

        block_start_events = [e for e in events if e.type == "content_block_start"]
        assert len(block_start_events) == 4, (
            f"Expected 4 content_block_start events, got {len(block_start_events)}"
        )
