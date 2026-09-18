from __future__ import annotations

from typing import TypeVar, Iterator, AsyncIterator

import httpx2
import pytest

from anthropic import Anthropic, AsyncAnthropic, APITimeoutError, APIConnectionError
from anthropic._streaming import Stream, AsyncStream, ServerSentEvent
from anthropic._exceptions import APIStatusError

_T = TypeVar("_T")

_FIRST_EVENT = (
    b'event: message_start\ndata: {"type":"message_start","message":{"id":"msg_1","type":"message",'
    b'"role":"assistant","model":"claude-sonnet-4-6","content":[],"stop_reason":null,"stop_sequence":null,'
    b'"usage":{"input_tokens":1,"output_tokens":0}}}\n\n'
)


class _DiesMidStream(httpx2.SyncByteStream):
    def __iter__(self) -> Iterator[bytes]:
        yield _FIRST_EVENT
        raise httpx2.ReadTimeout("timed out while reading the stream")


class _AsyncDiesMidStream(httpx2.AsyncByteStream):
    async def __aiter__(self) -> AsyncIterator[bytes]:
        yield _FIRST_EVENT
        raise httpx2.ReadTimeout("timed out while reading the stream")


def test_sync_stream_wraps_mid_stream_transport_error() -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(200, headers={"content-type": "text/event-stream"}, stream=_DiesMidStream())

    client = Anthropic(
        api_key="My API Key",
        http_client=httpx2.Client(transport=httpx2.MockTransport(handler)),
        max_retries=0,
    )

    with pytest.raises(APITimeoutError):
        with client.messages.stream(model="claude-sonnet-4-6", max_tokens=8, messages=[{"role": "user", "content": "hi"}]) as s:
            for _ in s:
                pass


async def test_async_stream_wraps_mid_stream_transport_error() -> None:
    async def handler(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(200, headers={"content-type": "text/event-stream"}, stream=_AsyncDiesMidStream())

    client = AsyncAnthropic(
        api_key="My API Key",
        http_client=httpx2.AsyncClient(transport=httpx2.MockTransport(handler)),
        max_retries=0,
    )

    with pytest.raises(APITimeoutError):
        async with client.messages.stream(
            model="claude-sonnet-4-6", max_tokens=8, messages=[{"role": "user", "content": "hi"}]
        ) as s:
            async for _ in s:
                pass


def test_sync_stream_does_not_mislabel_a_parse_error_as_a_connection_error() -> None:
    """A bug in parsing an in-stream event (malformed JSON here) is a defect in our own
    code, not a transport failure — it must not come out the other end looking retryable."""

    def body() -> Iterator[bytes]:
        yield b"event: message_start\n"
        yield b"data: {not valid json\n"
        yield b"\n"

    def handler(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(200, headers={"content-type": "text/event-stream"}, content=body())

    client = Anthropic(
        api_key="My API Key",
        http_client=httpx2.Client(transport=httpx2.MockTransport(handler)),
        max_retries=0,
    )

    with pytest.raises(Exception) as exc_info:
        with client.messages.stream(model="claude-sonnet-4-6", max_tokens=8, messages=[{"role": "user", "content": "hi"}]) as s:
            for _ in s:
                pass

    assert not isinstance(exc_info.value, APIConnectionError)


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
    async_stream = AsyncStream(cast_to=object, client=async_client, response=httpx2.Response(200, content=b"foo"))
    assert isinstance(async_stream, AsyncStream)

    sync_stream = Stream(cast_to=object, client=client, response=httpx2.Response(200, content=b"foo"))
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
        return Stream(cast_to=object, client=client, response=httpx2.Response(200, content=content))._iter_events()

    return AsyncStream(
        cast_to=object, client=async_client, response=httpx2.Response(200, content=to_aiter(content))
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
            response=httpx2.Response(200, content=content, request=httpx2.Request("GET", "https://example.com")),
        ).__stream__()

    return AsyncStream(
        cast_to=object,
        client=async_client,
        response=httpx2.Response(200, content=to_aiter(content), request=httpx2.Request("GET", "https://example.com")),
    ).__stream__()
