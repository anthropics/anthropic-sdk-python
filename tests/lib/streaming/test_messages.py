from __future__ import annotations

import os
from typing import TypeVar
from typing_extensions import Iterator, AsyncIterator, override

import httpx
import pytest
from respx import MockRouter

from anthropic import Anthropic, AsyncAnthropic
from anthropic.lib.streaming import MessageStream, AsyncMessageStream
from anthropic.types.beta.message import Message
from anthropic.types.beta.message_stream_event import MessageStreamEvent

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
api_key = "my-anthropic-api-key"

client = Anthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True)
async_client = AsyncAnthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True)

_T = TypeVar("_T")

# copied from the real API
stream_example = """
event: message_start
data: {"type":"message_start","message":{"id":"msg_4QpJur2dWWDjF6C758FbBw5vm12BaVipnK","type":"message","role":"assistant","content":[],"model":"claude-2.1","stop_reason":null,"stop_sequence":null,"usage":{"input_tokens":11,"output_tokens":1}}}

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


def basic_response() -> Iterator[bytes]:
    for line in stream_example.splitlines():
        yield line.encode() + b"\n"


async def to_async_iter(iter: Iterator[_T]) -> AsyncIterator[_T]:
    for event in iter:
        yield event


class SyncEventTracker(MessageStream):
    def __init__(self, *, cast_to: type[MessageStreamEvent], response: httpx.Response, client: Anthropic) -> None:
        super().__init__(cast_to=cast_to, response=response, client=client)

        self._events: list[MessageStreamEvent] = []

    @override
    def on_stream_event(self, event: MessageStreamEvent) -> None:
        self._events.append(event)


class AsyncEventTracker(AsyncMessageStream):
    def __init__(self, *, cast_to: type[MessageStreamEvent], response: httpx.Response, client: AsyncAnthropic) -> None:
        super().__init__(cast_to=cast_to, response=response, client=client)

        self._events: list[MessageStreamEvent] = []

    @override
    async def on_stream_event(self, event: MessageStreamEvent) -> None:
        self._events.append(event)


def assert_basic_response(stream: SyncEventTracker | AsyncEventTracker, message: Message) -> None:
    assert message.id == "msg_4QpJur2dWWDjF6C758FbBw5vm12BaVipnK"
    assert message.model == "claude-2.1"
    assert message.role == "assistant"
    assert message.stop_reason == "end_turn"
    assert message.stop_sequence is None
    assert message.type == "message"
    assert len(message.content) == 1

    content = message.content[0]
    assert content.type == "text"
    assert content.text == "Hello there!"

    assert [e.type for e in stream._events] == [
        "message_start",
        "content_block_start",
        "content_block_delta",
        "content_block_delta",
        "content_block_delta",
        "content_block_stop",
        "message_delta",
    ]


class TestSyncMessages:
    @pytest.mark.respx(base_url=base_url)
    def test_basic_response(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, content=basic_response()))

        with client.beta.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-2.1",
            event_handler=SyncEventTracker,
        ) as stream:
            assert_basic_response(stream, stream.get_final_message())

    @pytest.mark.respx(base_url=base_url)
    def test_context_manager(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, content=basic_response()))

        with client.beta.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-2.1",
        ) as stream:
            assert not stream.response.is_closed

        # response should be closed even if the body isn't read
        assert stream.response.is_closed


class TestAsyncMessages:
    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_basic_response(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, content=to_async_iter(basic_response())))

        async with async_client.beta.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-2.1",
            event_handler=AsyncEventTracker,
        ) as stream:
            assert_basic_response(stream, await stream.get_final_message())

    @pytest.mark.asyncio
    @pytest.mark.respx(base_url=base_url)
    async def test_context_manager(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, content=to_async_iter(basic_response())))

        async with async_client.beta.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello there!",
                }
            ],
            model="claude-2.1",
        ) as stream:
            assert not stream.response.is_closed

        # response should be closed even if the body isn't read
        assert stream.response.is_closed
