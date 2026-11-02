"""Tests for the content-idle guard: keepalives must not keep a stalled stream alive."""

from __future__ import annotations

import time
from typing import Any, AsyncIterator, Iterator

import httpx2
import pytest
from typing_extensions import override

from anthropic import Anthropic, AsyncAnthropic
from anthropic._exceptions import APITimeoutError
from anthropic.lib.streaming._idle_timeout import _GuardedByteStream, guard_stream, idle_timeout_of

PING_EVENT = b'event: ping\ndata: {"type": "ping"}\n\n'
COMMENT = b": ping\n\n"
CONTENT = b'event: content_block_delta\ndata: {"type": "content_block_delta", "index": 0, \
"delta": {"type": "text_delta", "text": "x"}}\n\n'


class _Paced(httpx2.SyncByteStream):
    """Sends `frames` with `gap` seconds between them, and never finishes early."""

    def __init__(self, frames: list[bytes], gap: float = 0.05) -> None:
        self.frames = frames
        self.gap = gap
        self.sent = 0

    @override
    def __iter__(self) -> Iterator[bytes]:
        for frame in self.frames:
            time.sleep(self.gap)
            self.sent += 1
            yield frame


class _AsyncPaced(httpx2.AsyncByteStream):
    def __init__(self, frames: list[bytes], gap: float = 0.05) -> None:
        self.frames = frames
        self.gap = gap
        self.sent = 0

    @override
    async def __aiter__(self) -> AsyncIterator[bytes]:
        import anyio

        for frame in self.frames:
            await anyio.sleep(self.gap)
            self.sent += 1
            yield frame


def _response(stream: httpx2.SyncByteStream | httpx2.AsyncByteStream) -> httpx2.Response:
    return httpx2.Response(
        200,
        headers={"content-type": "text/event-stream"},
        stream=stream,
        request=httpx2.Request("POST", "https://api.anthropic.com/v1/messages"),
    )


def _drain(guard: _GuardedByteStream) -> list[bytes]:
    return list(guard)


def test_comment_keepalives_do_not_reset_the_idle_clock() -> None:
    """The frame LiteLLM's proxy writes must not keep a stalled stream alive."""
    stream = _Paced([COMMENT] * 20)
    guard = _GuardedByteStream(stream, _response(stream), 0.2)

    started = time.monotonic()
    with pytest.raises(APITimeoutError):
        _drain(guard)

    assert time.monotonic() - started < 1.0, "the guard must fire on its own clock, not at the end of the body"
    assert guard.idle_timeouts == 1


def test_ping_events_do_not_reset_the_idle_clock() -> None:
    stream = _Paced([PING_EVENT] * 20)
    guard = _GuardedByteStream(stream, _response(stream), 0.2)

    with pytest.raises(APITimeoutError):
        _drain(guard)


def test_content_resets_the_clock_and_is_never_truncated() -> None:
    """A long generation that keeps producing must not be cut, however long it runs."""
    stream = _Paced([CONTENT] * 20)
    guard = _GuardedByteStream(stream, _response(stream), 0.2)

    chunks = _drain(guard)

    assert len(chunks) == 20
    assert guard.idle_timeouts == 0


def test_a_keepalive_split_across_two_chunks_still_counts_as_a_keepalive() -> None:
    """TCP does not respect frame boundaries; half a comment is still a comment."""
    frames = [b": pi", b"ng\n\n", b": pi", b"ng\n\n", b": pi", b"ng\n\n"]
    stream = _Paced(frames)
    guard = _GuardedByteStream(stream, _response(stream), 0.12)

    with pytest.raises(APITimeoutError):
        _drain(guard)


def test_an_error_frame_counts_as_content() -> None:
    """An error is something the caller can act on, so it resets the clock like any other event."""
    stream = _Paced([b'event: error\ndata: {"type": "error", "error": {"type": "overloaded"}}\n\n'])
    guard = _GuardedByteStream(stream, _response(stream), 0.2)

    assert len(_drain(guard)) == 1


async def test_async_guard_fires_on_comment_keepalives() -> None:
    stream = _AsyncPaced([COMMENT] * 20)
    from anthropic.lib.streaming._idle_timeout import _GuardedAsyncByteStream

    guard = _GuardedAsyncByteStream(stream, _response(stream), 0.2)

    with pytest.raises(APITimeoutError):
        async for _ in guard:
            pass


def test_unguarded_stream_is_unchanged() -> None:
    """The baseline the issue is about: without the guard, keepalives keep it waiting, no error."""
    stream = _Paced([COMMENT] * 5, gap=0.01)

    chunks = list(stream)

    assert len(chunks) == 5


class _FakeStream:
    """The guard only needs `.response`; this is not a mock of the SDK's Stream."""

    def __init__(self, response: httpx2.Response) -> None:
        self.response = response


def test_guard_stream_attaches_to_a_real_response() -> None:
    frames = [COMMENT] * 20
    response = _response(_Paced(frames))
    stream = _FakeStream(response)

    guard_stream(stream, seconds=0.2)

    assert idle_timeout_of(stream) == 0.2
    with pytest.raises(APITimeoutError):
        list(response.iter_bytes())


def test_guard_refuses_a_consumed_response() -> None:
    response = _response(_Paced([COMMENT]))
    response.is_stream_consumed = True
    stream = _FakeStream(response)

    with pytest.raises(RuntimeError):
        guard_stream(stream, seconds=0.2)


def test_guard_rejects_a_non_positive_window() -> None:
    stream = _FakeStream(_response(_Paced([COMMENT])))

    with pytest.raises(ValueError):
        guard_stream(stream, seconds=0)


def _handler(request: httpx2.Request) -> httpx2.Response:
    return httpx2.Response(200, headers={"content-type": "text/event-stream"}, stream=_Paced([COMMENT] * 40))


def _async_handler(request: httpx2.Request) -> httpx2.Response:
    return httpx2.Response(200, headers={"content-type": "text/event-stream"}, stream=_AsyncPaced([COMMENT] * 40))


def test_through_the_client() -> None:
    """End to end: a real client, a transport that only sends keepalives, an exception the caller sees."""
    client = Anthropic(
        api_key="test",
        http_client=httpx2.Client(transport=httpx2.MockTransport(_handler)),
        base_url="http://test",
    )
    stream = client.messages.create(
        model="claude-sonnet-4-6", max_tokens=8, messages=[{"role": "user", "content": "hi"}], stream=True
    )
    guard_stream(stream, seconds=0.2)

    with pytest.raises(APITimeoutError):
        list(stream)


async def test_through_the_async_client() -> None:
    client = AsyncAnthropic(
        api_key="test",
        http_client=httpx2.AsyncClient(transport=httpx2.MockTransport(_async_handler)),
        base_url="http://test",
    )
    stream = await client.messages.create(
        model="claude-sonnet-4-6", max_tokens=8, messages=[{"role": "user", "content": "hi"}], stream=True
    )
    guard_stream(stream, seconds=0.2)

    with pytest.raises(APITimeoutError):
        async for _ in stream:
            pass
