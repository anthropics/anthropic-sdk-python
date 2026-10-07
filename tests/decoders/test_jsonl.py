from __future__ import annotations

import json
from typing import Any, Iterator, AsyncIterator
from typing_extensions import TypeVar

import httpx2
import pytest

from anthropic._decoders.jsonl import JSONLDecoder, AsyncJSONLDecoder

_T = TypeVar("_T")


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_basic(sync: bool) -> None:
    def body() -> Iterator[bytes]:
        yield b'{"foo":true}\n'
        yield b'{"bar":false}\n'

    iterator = make_jsonl_iterator(
        content=body(),
        sync=sync,
        line_type=object,
    )

    assert await iter_next(iterator) == {"foo": True}
    assert await iter_next(iterator) == {"bar": False}

    await assert_empty_iter(iterator)


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_new_lines_in_json(
    sync: bool,
) -> None:
    def body() -> Iterator[bytes]:
        yield b'{"content":"Hello, world!\\nHow are you doing?"}'

    iterator = make_jsonl_iterator(content=body(), sync=sync, line_type=object)

    assert await iter_next(iterator) == {"content": "Hello, world!\nHow are you doing?"}


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_multi_byte_character_multiple_chunks(
    sync: bool,
) -> None:
    def body() -> Iterator[bytes]:
        yield b'{"content":"'
        # bytes taken from the string 'известни' and arbitrarily split
        # so that some multi-byte characters span multiple chunks
        yield b"\xd0"
        yield b"\xb8\xd0\xb7\xd0"
        yield b"\xb2\xd0\xb5\xd1\x81\xd1\x82\xd0\xbd\xd0\xb8"
        yield b'"}\n'

    iterator = make_jsonl_iterator(content=body(), sync=sync, line_type=object)

    assert await iter_next(iterator) == {"content": "известни"}


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_close_on_json_decode_error(sync: bool) -> None:
    response = httpx2.Response(200, stream=httpx2.ByteStream(b"invalid json\n" + b" " * 64))
    if sync:
        decoder = JSONLDecoder(
            raw_iterator=response.iter_bytes(chunk_size=64),
            line_type=object,
            http_response=response,
        )
        with pytest.raises(json.JSONDecodeError):
            list(decoder)
    else:
        decoder = AsyncJSONLDecoder(
            raw_iterator=response.aiter_bytes(chunk_size=64),
            line_type=object,
            http_response=response,
        )
        with pytest.raises(json.JSONDecodeError):
            async for _ in decoder:
                pass

    assert response.is_closed


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_close_on_stream_error(sync: bool) -> None:
    def failing_sync_stream() -> Iterator[bytes]:
        yield b'{"valid": 1}\n'
        raise httpx2.ReadError("network dropped")

    async def failing_async_stream() -> AsyncIterator[bytes]:
        yield b'{"valid": 1}\n'
        raise httpx2.ReadError("network dropped")

    response = httpx2.Response(200)
    if sync:
        decoder = JSONLDecoder(
            raw_iterator=failing_sync_stream(),
            line_type=object,
            http_response=response,
        )
        with pytest.raises(httpx2.ReadError):
            list(decoder)
    else:
        decoder = AsyncJSONLDecoder(
            raw_iterator=failing_async_stream(),
            line_type=object,
            http_response=response,
        )
        with pytest.raises(httpx2.ReadError):
            async for _ in decoder:
                pass

    assert response.is_closed


async def to_aiter(iter: Iterator[bytes]) -> AsyncIterator[bytes]:
    for chunk in iter:
        yield chunk


async def iter_next(iter: Iterator[_T] | AsyncIterator[_T]) -> _T:
    if isinstance(iter, AsyncIterator):
        return await iter.__anext__()
    return next(iter)


async def assert_empty_iter(decoder: JSONLDecoder[Any] | AsyncJSONLDecoder[Any]) -> None:
    with pytest.raises((StopAsyncIteration, RuntimeError)):
        await iter_next(decoder)


def make_jsonl_iterator(
    content: Iterator[bytes],
    *,
    sync: bool,
    line_type: type[_T],
) -> JSONLDecoder[_T] | AsyncJSONLDecoder[_T]:
    if sync:
        return JSONLDecoder(line_type=line_type, raw_iterator=content, http_response=httpx2.Response(200))

    return AsyncJSONLDecoder(line_type=line_type, raw_iterator=to_aiter(content), http_response=httpx2.Response(200))
