from __future__ import annotations

import gc
from typing import Any, Iterator, AsyncIterator
from typing_extensions import TypeVar, override

import anyio
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
async def test_dropped_decoder_lets_go_of_its_iterator_at_once(sync: bool) -> None:
    closed: list[bool] = []

    def body() -> Iterator[bytes]:
        try:
            yield b"1\n2\n"
        finally:
            closed.append(True)

    iterator = make_jsonl_iterator(content=body(), sync=sync, line_type=object)
    assert await iter_next(iterator) == 1
    assert await iter_next(iterator) == 2

    gc.disable()
    try:
        del iterator
        with anyio.fail_after(10):
            while not closed:
                # An event loop closes what was dropped once it gets to run.
                await anyio.sleep(0)
    finally:
        gc.enable()


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_decoder_has_what_its_subclass_sets_after_init(sync: bool) -> None:
    class Tagged(JSONLDecoder[object]):
        def __init__(self, **kwargs: Any) -> None:
            super().__init__(**kwargs)
            self.tag = "tag"

        @override
        def __decode__(self) -> Iterator[object]:
            for _ in super().__decode__():
                yield self.tag

    class AsyncTagged(AsyncJSONLDecoder[object]):
        def __init__(self, **kwargs: Any) -> None:
            super().__init__(**kwargs)
            self.tag = "tag"

        @override
        async def __decode__(self) -> AsyncIterator[object]:
            async for _ in super().__decode__():
                yield self.tag

    content = iter([b"1\n"])
    iterator = (
        Tagged(line_type=object, raw_iterator=content, http_response=httpx2.Response(200))
        if sync
        else AsyncTagged(line_type=object, raw_iterator=to_aiter(content), http_response=httpx2.Response(200))
    )

    assert await iter_next(iterator) == "tag"


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
