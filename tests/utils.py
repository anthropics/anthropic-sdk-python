from __future__ import annotations

import gc
import os
import traceback
import contextlib
from typing import Any, Generic, TypeVar, Iterator, Sequence, cast
from datetime import date, datetime
from dataclasses import dataclass
from collections.abc import Callable, Awaitable, AsyncIterator
from typing_extensions import Literal, get_args, override, get_origin, assert_type

import anyio
import httpx2

from anthropic import Stream, Anthropic, AsyncStream, AsyncAnthropic
from anthropic._types import Omit, Headers, NoneType
from anthropic._utils import (
    is_dict,
    is_list,
    is_list_type,
    is_union_type,
    extract_type_arg,
    is_sequence_type,
    is_annotated_type,
    is_type_alias_type,
)
from anthropic._compat import PYDANTIC_V1, field_outer_type, get_model_fields
from anthropic._models import BaseModel
from anthropic._response import (
    APIResponse,
    AsyncAPIResponse,
    to_raw_response_wrapper,
    async_to_raw_response_wrapper,
)
from anthropic._base_client import make_request_options

BaseModelT = TypeVar("BaseModelT", bound=BaseModel)


def assert_matches_model(model: type[BaseModelT], value: BaseModelT, *, path: list[str]) -> bool:
    for name, field in get_model_fields(model).items():
        field_value = getattr(value, name)
        if PYDANTIC_V1:
            # in v1 nullability was structured differently
            # https://docs.pydantic.dev/2.0/migration/#required-optional-and-nullable-fields
            allow_none = getattr(field, "allow_none", False)
        else:
            allow_none = False

        assert_matches_type(
            field_outer_type(field),
            field_value,
            path=[*path, name],
            allow_none=allow_none,
        )

    return True


# Note: the `path` argument is only used to improve error messages when `--showlocals` is used
def assert_matches_type(
    type_: Any,
    value: object,
    *,
    path: list[str],
    allow_none: bool = False,
) -> None:
    if is_type_alias_type(type_):
        type_ = type_.__value__

    # unwrap `Annotated[T, ...]` -> `T`
    if is_annotated_type(type_):
        type_ = extract_type_arg(type_, 0)

    if allow_none and value is None:
        return

    if type_ is None or type_ is NoneType:
        assert value is None
        return

    origin = get_origin(type_) or type_

    if is_list_type(type_):
        return _assert_list_type(type_, value)

    if is_sequence_type(type_):
        assert isinstance(value, Sequence)
        inner_type = get_args(type_)[0]
        for entry in value:  # type: ignore
            assert_type(inner_type, entry)  # type: ignore
        return

    if origin == str:
        assert isinstance(value, str)
    elif origin == int:
        assert isinstance(value, int)
    elif origin == bool:
        assert isinstance(value, bool)
    elif origin == float:
        assert isinstance(value, float)
    elif origin == bytes:
        assert isinstance(value, bytes)
    elif origin == datetime:
        assert isinstance(value, datetime)
    elif origin == date:
        assert isinstance(value, date)
    elif origin == object:
        # nothing to do here, the expected type is unknown
        pass
    elif origin == Literal:
        assert value in get_args(type_)
    elif origin == dict:
        assert is_dict(value)

        args = get_args(type_)
        key_type = args[0]
        items_type = args[1]

        for key, item in value.items():
            assert_matches_type(key_type, key, path=[*path, "<dict key>"])
            assert_matches_type(items_type, item, path=[*path, "<dict item>"])
    elif is_union_type(type_):
        variants = get_args(type_)

        try:
            none_index = variants.index(type(None))
        except ValueError:
            pass
        else:
            # special case Optional[T] for better error messages
            if len(variants) == 2:
                if value is None:
                    # valid
                    return

                return assert_matches_type(type_=variants[not none_index], value=value, path=path)

        for i, variant in enumerate(variants):
            try:
                assert_matches_type(variant, value, path=[*path, f"variant {i}"])
                return
            except AssertionError:
                traceback.print_exc()
                continue

        raise AssertionError("Did not match any variants")
    elif issubclass(origin, BaseModel):
        assert isinstance(value, type_)
        assert assert_matches_model(type_, cast(Any, value), path=path)
    else:
        assert None, f"Unhandled field type: {type_}"


def _assert_list_type(type_: type[object], value: object) -> None:
    assert is_list(value)

    inner_type = get_args(type_)[0]
    for entry in value:
        assert_type(inner_type, entry)  # type: ignore


@contextlib.contextmanager
def update_env(**new_env: str | Omit) -> Iterator[None]:
    old = os.environ.copy()

    try:
        for name, value in new_env.items():
            if isinstance(value, Omit):
                os.environ.pop(name, None)
            else:
                os.environ[name] = value

        yield None
    finally:
        os.environ.clear()
        os.environ.update(old)


_T = TypeVar("_T")
_RequestedT = TypeVar("_RequestedT")
_KeptT = TypeVar("_KeptT")

EVENT = "event: unhandled\ndata: {}\n\n".encode()


class Body(httpx2.SyncByteStream, httpx2.AsyncByteStream):
    """A response body that counts how often it is closed. It holds more than a test reads."""

    def __init__(self) -> None:
        self.chunks = [EVENT] * 100
        self.closes = 0

    @override
    def __iter__(self) -> Iterator[bytes]:
        yield from self.chunks

    @override
    async def __aiter__(self) -> AsyncIterator[bytes]:
        for chunk in self.chunks:
            yield chunk

    @override
    def close(self) -> None:
        self.closes += 1

    @override
    async def aclose(self) -> None:
        self.close()

    def transport(self) -> httpx2.MockTransport:
        return httpx2.MockTransport(lambda _: httpx2.Response(200, stream=self))

    async def wait_closed(self) -> None:
        """An event loop closes what was dropped once it gets to run, and one generator after the other."""
        with anyio.fail_after(10):
            while not self.closes:
                await anyio.sleep(0)


Request = Callable[..., Stream[object]]
AsyncRequest = Callable[..., Awaitable[AsyncStream[object]]]


def requester(client: Anthropic, body: Body, *, stream_cls: type[Stream[object]] = Stream[object]) -> Request:
    """A method shaped like a generated streaming method, whose response is `body`."""
    client = client.with_options(http_client=httpx2.Client(transport=body.transport()))

    def request(*, extra_headers: Headers | None = None) -> Stream[object]:
        return client.get(
            "/stream",
            cast_to=object,
            options=make_request_options(extra_headers=extra_headers),
            stream=True,
            stream_cls=stream_cls,
        )

    return request


def async_requester(
    client: AsyncAnthropic, body: Body, *, stream_cls: type[AsyncStream[object]] = AsyncStream[object]
) -> AsyncRequest:
    """A method shaped like a generated streaming method, whose response is `body`."""
    client = client.with_options(http_client=httpx2.AsyncClient(transport=body.transport()))

    async def request(*, extra_headers: Headers | None = None) -> AsyncStream[object]:
        return await client.get(
            "/stream",
            cast_to=object,
            options=make_request_options(extra_headers=extra_headers),
            stream=True,
            stream_cls=stream_cls,
        )

    return request


@contextlib.contextmanager
def without_collection() -> Iterator[None]:
    gc.disable()
    try:
        yield
    finally:
        gc.enable()


def itself(held: _T) -> _T:
    return held


def in_a_cycle(held: object) -> None:
    """Drops `held` in a way that leaves it to the garbage collector to free it."""
    cycle = [held]
    cycle.append(cycle)


def collect(client: Anthropic) -> None:
    """Collects garbage and checks that this closes what was dropped, so that it means something if the rest is open."""
    dropped = Body()
    stream = requester(client, dropped)()
    next(stream)
    in_a_cycle(stream)
    del stream
    gc.collect()
    assert dropped.closes == 1


async def async_collect(client: AsyncAnthropic) -> None:
    """Collects garbage and checks that this closes what was dropped, so that it means something if the rest is open."""
    dropped = Body()
    stream = await async_requester(client, dropped)()
    await anext(stream)
    in_a_cycle(stream)
    del stream
    gc.collect()
    await dropped.wait_closed()
    assert dropped.closes == 1


@dataclass(frozen=True)
class Held(Generic[_RequestedT, _KeptT]):
    """What the caller holds of a response."""

    request: Callable[[Request], _RequestedT]
    keep: Callable[[_RequestedT], _KeptT]
    iterate: Callable[[_KeptT], Iterator[object]]


def stream(request: Request) -> Stream[object]:
    return request()


def raw_response(request: Request) -> APIResponse[Stream[object]]:
    return to_raw_response_wrapper(request)()


STREAMS = {
    "stream": Held(stream, itself, itself),
    "iter(stream)": Held(stream, iter, itself),
    "raw_response": Held(raw_response, itself, lambda held: held.parse()),
    "raw_response.parse()": Held(raw_response, lambda r: r.parse(), itself),
}


@dataclass(frozen=True)
class AsyncHeld(Generic[_RequestedT, _KeptT]):
    """What the caller holds of a response."""

    request: Callable[[AsyncRequest], Awaitable[_RequestedT]]
    keep: Callable[[_RequestedT], _KeptT]
    iterate: Callable[[_KeptT], AsyncIterator[object]]


async def async_stream(request: AsyncRequest) -> AsyncStream[object]:
    return await request()


async def async_raw_response(request: AsyncRequest) -> AsyncAPIResponse[AsyncStream[object]]:
    return await async_to_raw_response_wrapper(request)()


async def async_parsed_raw_response(request: AsyncRequest) -> AsyncStream[object]:
    return await (await async_raw_response(request)).parse()


async def async_parse(response: AsyncAPIResponse[AsyncStream[object]]) -> AsyncIterator[object]:
    async for event in await response.parse():
        yield event


ASYNC_STREAMS = {
    "stream": AsyncHeld(async_stream, itself, itself),
    "aiter(stream)": AsyncHeld(async_stream, aiter, itself),
    "raw_response": AsyncHeld(async_raw_response, itself, async_parse),
    "await raw_response.parse()": AsyncHeld(async_parsed_raw_response, itself, itself),
}
