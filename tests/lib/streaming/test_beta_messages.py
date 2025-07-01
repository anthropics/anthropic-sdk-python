from __future__ import annotations

import os
import json
import inspect
from typing import Any, Set, Dict, TypeVar, cast
from unittest import TestCase

import httpx
import pytest
from respx import MockRouter

from anthropic import Anthropic, AsyncAnthropic
from anthropic._compat import PYDANTIC_V2
from anthropic.types.beta.beta_message import BetaMessage
from anthropic.lib.streaming._beta_types import BetaMessageStreamEvent
from anthropic.resources.messages.messages import DEPRECATED_MODELS
from anthropic.lib.streaming._beta_messages import TRACKS_TOOL_INPUT, BetaMessageStream, BetaAsyncMessageStream

from .helpers import get_response, to_async_iter

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
api_key = "my-anthropic-api-key"

sync_client = Anthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True)
async_client = AsyncAnthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True)

_T = TypeVar("_T")

# Expected message fixtures
EXPECTED_BASIC_MESSAGE = {
    "id": "msg_4QpJur2dWWDjF6C758FbBw5vm12BaVipnK",
    "model": "claude-3-opus-latest",
    "role": "assistant",
    "stop_reason": "end_turn",
    "type": "message",
    "content": [{"type": "text", "text": "Hello there!"}],
    "usage": {"input_tokens": 11, "output_tokens": 6},
}

EXPECTED_BASIC_EVENT_TYPES = [
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

EXPECTED_TOOL_USE_MESSAGE = {
    "id": "msg_019Q1hrJbZG26Fb9BQhrkHEr",
    "model": "claude-sonnet-4-20250514",
    "role": "assistant",
    "stop_reason": "tool_use",
    "type": "message",
    "content": [
        {"type": "text", "text": "I'll check the current weather in Paris for you."},
        {
            "type": "tool_use",
            "id": "toolu_01NRLabsLyVHZPKxbKvkfSMn",
            "name": "get_weather",
            "input": {"location": "Paris"},
        },
    ],
    "usage": {
        "input_tokens": 377,
        "output_tokens": 65,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
        "service_tier": "standard",
    },
}

EXPECTED_TOOL_USE_EVENT_TYPES = [
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

EXPECTED_INCOMPLETE_MESSAGE = {
    "id": "msg_01UdjYBBipA9omjYhicnevgq",
    "model": "claude-3-7-sonnet-20250219",
    "role": "assistant",
    "stop_reason": "max_tokens",
    "type": "message",
    "content": [
        {
            "type": "text",
            "text": "I'll create a comprehensive tax guide for someone with multiple W2s and save it in a file called taxes.txt. Let me do that for you now.",
        },
        {
            "type": "tool_use",
            "id": "toolu_01EKqbqmZrGRXy18eN7m9kvY",
            "name": "make_file",
            "input": {
                "filename": "taxes.txt",
                "lines_of_text": [
                    "# COMPREHENSIVE TAX GUIDE FOR INDIVIDUALS WITH MULTIPLE W-2s",
                    "",
                    "## INTRODUCTION",
                    "",
                ],
            },
        },
    ],
    "usage": {
        "input_tokens": 450,
        "output_tokens": 124,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
        "service_tier": "standard",
    },
}

EXPECTED_INCOMPLETE_EVENT_TYPES = [
    "message_start",
    "content_block_start",
    "content_block_delta",
    "text",
    "content_block_delta",
    "text",
    "content_block_delta",
    "text",
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
    "message_delta",
]


def assert_message_matches(message: BetaMessage, expected: Dict[str, Any]) -> None:
    actual_message_json = message.model_dump_json(
        indent=2, exclude_none=True, exclude={"content": {"__all__": {"__json_buf"}}}
    )

    test_case = TestCase()
    test_case.maxDiff = None
    test_case.assertEqual(expected, json.loads(actual_message_json))


def assert_basic_response(events: list[BetaMessageStreamEvent], message: BetaMessage) -> None:
    assert_message_matches(message, EXPECTED_BASIC_MESSAGE)
    assert [e.type for e in events] == EXPECTED_BASIC_EVENT_TYPES


def assert_tool_use_response(events: list[BetaMessageStreamEvent], message: BetaMessage) -> None:
    assert_message_matches(message, EXPECTED_TOOL_USE_MESSAGE)
    assert [e.type for e in events] == EXPECTED_TOOL_USE_EVENT_TYPES


def assert_incomplete_partial_input_response(events: list[BetaMessageStreamEvent], message: BetaMessage) -> None:
    assert_message_matches(message, EXPECTED_INCOMPLETE_MESSAGE)
    assert [e.type for e in events] == EXPECTED_INCOMPLETE_EVENT_TYPES


class TestSyncMessages:
    @pytest.mark.respx(base_url=base_url)
    def test_basic_response(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=get_response("basic_response.txt"))
        )

        with sync_client.beta.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-3-opus-latest",
        ) as stream:
            assert isinstance(cast(Any, stream), BetaMessageStream)

            assert_basic_response([event for event in stream], stream.get_final_message())

    @pytest.mark.respx(base_url=base_url)
    def test_tool_use(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=get_response("tool_use_response.txt"))
        )

        with sync_client.beta.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-sonnet-4-20250514",
        ) as stream:
            assert isinstance(cast(Any, stream), BetaMessageStream)

            assert_tool_use_response([event for event in stream], stream.get_final_message())

    @pytest.mark.respx(base_url=base_url)
    def test_context_manager(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=get_response("basic_response.txt"))
        )

        with sync_client.beta.messages.stream(
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
                with sync_client.beta.messages.stream(
                    max_tokens=1024,
                    messages=[{"role": "user", "content": "Hello"}],
                    model=deprecated_model,
                ) as stream:
                    # Consume the stream to ensure the warning is triggered
                    stream.until_done()


class TestAsyncMessages:
    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_basic_response(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=to_async_iter(get_response("basic_response.txt")))
        )

        async with async_client.beta.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-opus-4-0",
        ) as stream:
            assert isinstance(cast(Any, stream), BetaAsyncMessageStream)

            assert_basic_response([event async for event in stream], await stream.get_final_message())

    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_context_manager(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, content=to_async_iter(get_response("basic_response.txt")))
        )

        async with async_client.beta.messages.stream(
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
                async with async_client.beta.messages.stream(
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

        async with async_client.beta.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-sonnet-4-20250514",
        ) as stream:
            assert isinstance(cast(Any, stream), BetaAsyncMessageStream)

            assert_tool_use_response([event async for event in stream], await stream.get_final_message())

    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_incomplete_response(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(
                200, content=to_async_iter(get_response("incomplete_partial_json_response.txt"))
            )
        )

        async with async_client.beta.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-sonnet-4-20250514",
        ) as stream:
            assert isinstance(cast(Any, stream), BetaAsyncMessageStream)

            assert_incomplete_partial_input_response(
                [event async for event in stream], await stream.get_final_message()
            )


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
def test_stream_method_definition_in_sync(sync: bool) -> None:
    client: Anthropic | AsyncAnthropic = sync_client if sync else async_client

    sig = inspect.signature(client.beta.messages.stream)
    generated_sig = inspect.signature(client.beta.messages.create)

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
def test_tracks_tool_input_type_alias_is_up_to_date() -> None:
    # only run this on Pydantic v2
    if not PYDANTIC_V2:
        pytest.skip("This test is only applicable for Pydantic v2")
    from typing import get_args

    from pydantic import BaseModel

    from anthropic.types.beta.beta_content_block import BetaContentBlock

    # Get the content block union type
    content_block_union = get_args(BetaContentBlock)[0]

    # Get all types from BetaContentBlock union
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
