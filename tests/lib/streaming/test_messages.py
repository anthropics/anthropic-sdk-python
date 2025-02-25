from __future__ import annotations

import os
import inspect
from typing import Any, TypeVar, cast
from typing_extensions import Iterator, AsyncIterator

import httpx
import pytest
from respx import MockRouter

from anthropic import Stream, Anthropic, AsyncStream, AsyncAnthropic
from anthropic.lib.streaming import MessageStreamEvent
from anthropic.types.message import Message
from anthropic.resources.messages import DEPRECATED_MODELS

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


def basic_response() -> Iterator[bytes]:
    for line in stream_example.splitlines():
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


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
def test_beta_stream_method_definition_in_sync(sync: bool) -> None:
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
