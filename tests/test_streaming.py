from __future__ import annotations

from typing import TypeVar, Iterator, AsyncIterator

import httpx
import pytest

from anthropic import Anthropic, AsyncAnthropic
from anthropic._streaming import Stream, AsyncStream, ServerSentEvent
from anthropic._exceptions import APIStatusError

_T = TypeVar("_T")


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_basic(sync: bool, client: Anthropic, async_client: AsyncAnthropic) -> None:
    def body() -> Iterator[bytes]:
        yield b"event: completion\n"
        yield b'data: {"foo":true}\n'
        yield b"\n"

    iterator = make_event_iterator(content=body(), sync=sync, client=client, async_client=async_client)

    sse = await iter_next(iterator)
    assert sse.event == "completion"
    assert sse.json() == {"foo": True}

    await assert_empty_iter(iterator)


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_data_missing_event(sync: bool, client: Anthropic, async_client: AsyncAnthropic) -> None:
    def body() -> Iterator[bytes]:
        yield b'data: {"foo":true}\n'
        yield b"\n"

    iterator = make_event_iterator(content=body(), sync=sync, client=client, async_client=async_client)

    sse = await iter_next(iterator)
    assert sse.event is None
    assert sse.json() == {"foo": True}

    await assert_empty_iter(iterator)


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_event_missing_data(sync: bool, client: Anthropic, async_client: AsyncAnthropic) -> None:
    def body() -> Iterator[bytes]:
        yield b"event: ping\n"
        yield b"\n"

    iterator = make_event_iterator(content=body(), sync=sync, client=client, async_client=async_client)

    sse = await iter_next(iterator)
    assert sse.event == "ping"
    assert sse.data == ""

    await assert_empty_iter(iterator)


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_multiple_events(sync: bool, client: Anthropic, async_client: AsyncAnthropic) -> None:
    def body() -> Iterator[bytes]:
        yield b"event: ping\n"
        yield b"\n"
        yield b"event: completion\n"
        yield b"\n"

    iterator = make_event_iterator(content=body(), sync=sync, client=client, async_client=async_client)

    sse = await iter_next(iterator)
    assert sse.event == "ping"
    assert sse.data == ""

    sse = await iter_next(iterator)
    assert sse.event == "completion"
    assert sse.data == ""

    await assert_empty_iter(iterator)


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_multiple_events_with_data(sync: bool, client: Anthropic, async_client: AsyncAnthropic) -> None:
    def body() -> Iterator[bytes]:
        yield b"event: ping\n"
        yield b'data: {"foo":true}\n'
        yield b"\n"
        yield b"event: completion\n"
        yield b'data: {"bar":false}\n'
        yield b"\n"

    iterator = make_event_iterator(content=body(), sync=sync, client=client, async_client=async_client)

    sse = await iter_next(iterator)
    assert sse.event == "ping"
    assert sse.json() == {"foo": True}

    sse = await iter_next(iterator)
    assert sse.event == "completion"
    assert sse.json() == {"bar": False}

    await assert_empty_iter(iterator)


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_multiple_data_lines_with_empty_line(sync: bool, client: Anthropic, async_client: AsyncAnthropic) -> None:
    def body() -> Iterator[bytes]:
        yield b"event: ping\n"
        yield b"data: {\n"
        yield b'data: "foo":\n'
        yield b"data: \n"
        yield b"data:\n"
        yield b"data: true}\n"
        yield b"\n\n"

    iterator = make_event_iterator(content=body(), sync=sync, client=client, async_client=async_client)

    sse = await iter_next(iterator)
    assert sse.event == "ping"
    assert sse.json() == {"foo": True}
    assert sse.data == '{\n"foo":\n\n\ntrue}'

    await assert_empty_iter(iterator)


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_data_json_escaped_double_new_line(sync: bool, client: Anthropic, async_client: AsyncAnthropic) -> None:
    def body() -> Iterator[bytes]:
        yield b"event: ping\n"
        yield b'data: {"foo": "my long\\n\\ncontent"}'
        yield b"\n\n"

    iterator = make_event_iterator(content=body(), sync=sync, client=client, async_client=async_client)

    sse = await iter_next(iterator)
    assert sse.event == "ping"
    assert sse.json() == {"foo": "my long\n\ncontent"}

    await assert_empty_iter(iterator)


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_multiple_data_lines(sync: bool, client: Anthropic, async_client: AsyncAnthropic) -> None:
    def body() -> Iterator[bytes]:
        yield b"event: ping\n"
        yield b"data: {\n"
        yield b'data: "foo":\n'
        yield b"data: true}\n"
        yield b"\n\n"

    iterator = make_event_iterator(content=body(), sync=sync, client=client, async_client=async_client)

    sse = await iter_next(iterator)
    assert sse.event == "ping"
    assert sse.json() == {"foo": True}

    await assert_empty_iter(iterator)


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_special_new_line_character(
    sync: bool,
    client: Anthropic,
    async_client: AsyncAnthropic,
) -> None:
    def body() -> Iterator[bytes]:
        yield b'data: {"content":" culpa"}\n'
        yield b"\n"
        yield b'data: {"content":" \xe2\x80\xa8"}\n'
        yield b"\n"
        yield b'data: {"content":"foo"}\n'
        yield b"\n"

    iterator = make_event_iterator(content=body(), sync=sync, client=client, async_client=async_client)

    sse = await iter_next(iterator)
    assert sse.event is None
    assert sse.json() == {"content": " culpa"}

    sse = await iter_next(iterator)
    assert sse.event is None
    assert sse.json() == {"content": "  "}

    sse = await iter_next(iterator)
    assert sse.event is None
    assert sse.json() == {"content": "foo"}

    await assert_empty_iter(iterator)


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_multi_byte_character_multiple_chunks(
    sync: bool,
    client: Anthropic,
    async_client: AsyncAnthropic,
) -> None:
    def body() -> Iterator[bytes]:
        yield b'data: {"content":"'
        # bytes taken from the string 'известни' and arbitrarily split
        # so that some multi-byte characters span multiple chunks
        yield b"\xd0"
        yield b"\xb8\xd0\xb7\xd0"
        yield b"\xb2\xd0\xb5\xd1\x81\xd1\x82\xd0\xbd\xd0\xb8"
        yield b'"}\n'
        yield b"\n"

    iterator = make_event_iterator(content=body(), sync=sync, client=client, async_client=async_client)

    sse = await iter_next(iterator)
    assert sse.event is None
    assert sse.json() == {"content": "известни"}


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_error_type(
    sync: bool,
    client: Anthropic,
    async_client: AsyncAnthropic,
) -> None:
    def body() -> Iterator[bytes]:
        yield b"event: error\n"
        yield b'data: {"type": "error", "error": {"type": "overloaded_error", "message": "Overloaded"}}\n\n'

    iterator = make_stream_iterator(content=body(), sync=sync, client=client, async_client=async_client)

    with pytest.raises(APIStatusError) as exc_info:
        await iter_next(iterator)

    assert exc_info.value.type == "overloaded_error"
    assert "Overloaded" in str(exc_info.value)


def test_isinstance_check(client: Anthropic, async_client: AsyncAnthropic) -> None:
    async_stream = AsyncStream(cast_to=object, client=async_client, response=httpx.Response(200, content=b"foo"))
    assert isinstance(async_stream, AsyncStream)

    sync_stream = Stream(cast_to=object, client=client, response=httpx.Response(200, content=b"foo"))
    assert isinstance(sync_stream, Stream)


async def to_aiter(iter: Iterator[bytes]) -> AsyncIterator[bytes]:
    for chunk in iter:
        yield chunk


async def iter_next(iter: Iterator[_T] | AsyncIterator[_T]) -> _T:
    if isinstance(iter, AsyncIterator):
        return await iter.__anext__()

    return next(iter)


async def assert_empty_iter(iter: Iterator[ServerSentEvent] | AsyncIterator[ServerSentEvent]) -> None:
    with pytest.raises((StopAsyncIteration, RuntimeError)):
        await iter_next(iter)


def make_event_iterator(
    content: Iterator[bytes],
    *,
    sync: bool,
    client: Anthropic,
    async_client: AsyncAnthropic,
) -> Iterator[ServerSentEvent] | AsyncIterator[ServerSentEvent]:
    if sync:
        return Stream(cast_to=object, client=client, response=httpx.Response(200, content=content))._iter_events()

    return AsyncStream(
        cast_to=object, client=async_client, response=httpx.Response(200, content=to_aiter(content))
    )._iter_events()


# Unlike make_event_iterator which only parses SSE events using _iter_events(),
# this helper uses __stream__() to process the full stream pipeline including
# parsing message objects and converting error events into raised exceptions.
def make_stream_iterator(
    content: Iterator[bytes],
    *,
    sync: bool,
    client: Anthropic,
    async_client: AsyncAnthropic,
) -> AsyncIterator[object] | Iterator[object]:
    if sync:
        return Stream(
            cast_to=object,
            client=client,
            response=httpx.Response(200, content=content, request=httpx.Request("GET", "https://example.com")),
        ).__stream__()

    return AsyncStream(
        cast_to=object,
        client=async_client,
        response=httpx.Response(200, content=to_aiter(content), request=httpx.Request("GET", "https://example.com")),
    ).__stream__()
