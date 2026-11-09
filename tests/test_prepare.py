from __future__ import annotations

import io
import os
import re
import sys
import enum
import json
import base64
import logging
import pathlib
import ipaddress
from types import MappingProxyType
from typing import Any, cast
from datetime import date, datetime, timezone, timedelta
from itertools import islice
from collections import UserString, deque
from collections.abc import Mapping, Callable, Iterator, Sequence
from typing_extensions import override

import httpx2
import pytest
import pydantic
from respx import MockRouter
from respx.models import Call as MockRequestCall

from anthropic import Anthropic, AsyncAnthropic
from anthropic._types import omit, not_given
from anthropic._utils import is_mapping, is_sequence
from anthropic._compat import PYDANTIC_V1, model_copy, model_parse
from anthropic._models import BaseModel, construct_type
from anthropic._constants import FILE_INPUT_MARKERS
from anthropic.pagination import SyncPage, AsyncPage
from anthropic._base_client import BaseClient, make_request_options
from anthropic._utils._json import openapi_dumps_str
from anthropic._utils._prepare import (
    serialize_data,
    async_serialize_data,
    prepare_request_data,
    async_prepare_request_data,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

SAMPLE_FILE_PATH = pathlib.Path(__file__).parent.joinpath("sample_file.txt")
SAMPLE_FILE_BASE64 = "SGVsbG8sIHdvcmxkIQo="

# where the client looks the file input markers up on each request; the package's own depend on the API
# spec and may be empty, so the tests that read file inputs pin `MARKERS` there
MARKERS_ATTR = "anthropic._utils._prepare.FILE_INPUT_MARKERS"
MARKERS = (("type", "base64", "data"),)


class Send:
    """Sends request params through a client whose transport records the request and answers `{}`."""

    request: httpx2.Request
    """the last request that went over the wire"""

    def __init__(self, client: Anthropic | AsyncAnthropic) -> None:
        transport = httpx2.MockTransport(self._record)
        self._client: Anthropic | AsyncAnthropic
        if isinstance(client, Anthropic):
            self._client = client.with_options(http_client=httpx2.Client(transport=transport), max_retries=0)
        else:
            self._client = client.with_options(http_client=httpx2.AsyncClient(transport=transport), max_retries=0)

    def _record(self, request: httpx2.Request) -> httpx2.Response:
        self.request = request
        return httpx2.Response(200, json={})

    async def __call__(self, body: object, *, extra_body: Mapping[str, object] | None = None) -> Any:
        """The JSON that `body` is sent as, or `None` when the request went out without content."""
        options = make_request_options(extra_body=extra_body)
        if isinstance(self._client, Anthropic):
            self._client.post("/foo", body=body, options=options, cast_to=httpx2.Response)
        else:
            await self._client.post("/foo", body=body, options=options, cast_to=httpx2.Response)
        return json.loads(self.request.content) if self.request.content else None

    async def query(
        self,
        query: Mapping[str, object] | None = None,
        *,
        extra_query: Mapping[str, object] | None = None,
        extra_body: Mapping[str, object] | None = None,
        default_query: Mapping[str, object] | None = None,
    ) -> dict[str, str]:
        """The query string that `query` is sent as, parsed back into a dict."""
        options = make_request_options(query=query, extra_query=extra_query, extra_body=extra_body)
        client = self._client.with_options(default_query=default_query)
        if isinstance(client, Anthropic):
            client.get("/foo", options=options, cast_to=httpx2.Response)
        else:
            await client.get("/foo", options=options, cast_to=httpx2.Response)
        return dict(self.request.url.params)

    async def form(self, body: Mapping[str, object]) -> bytes:
        """The multipart content that `body` is sent as next to a file."""
        options = make_request_options(extra_headers={"Content-Type": "multipart/form-data; boundary=boundary"})
        files = [("file", b"contents")]
        if isinstance(self._client, Anthropic):
            self._client.post("/foo", body=body, files=files, options=options, cast_to=httpx2.Response)
        else:
            await self._client.post("/foo", body=body, files=files, options=options, cast_to=httpx2.Response)
        return self.request.content


@pytest.fixture(params=[True, False], ids=["sync", "async"])
def client(
    request: pytest.FixtureRequest, client: Anthropic, async_client: AsyncAnthropic
) -> Anthropic | AsyncAnthropic:
    return client if request.param else async_client


@pytest.fixture
def send(client: Anthropic | AsyncAnthropic) -> Send:
    return Send(client)


def b64_obj(data: object) -> Any:
    return {"type": "base64", "media_type": "image/png", "data": data}


def image_block(data: object) -> Any:
    return {"type": "image", "source": b64_obj(data)}


def _no_retry_delay(*_args: Any, **_kwargs: Any) -> float:
    return 0.01


class Item(BaseModel):
    id: str


class DuckReader:
    """Has a `read` method, but is none of the types `is_base64_file_input` accepts."""

    def __init__(self) -> None:
        self.read_calls = 0

    def read(self) -> str:
        self.read_calls += 1
        return "a\nb\n"


class IterableDuckReader(DuckReader):
    """Defines `__iter__`, but is no sequence, set or iterator."""

    def __iter__(self) -> Iterator[str]:
        return iter(["a", "b"])


class BrokenIterable:
    def __iter__(self) -> Iterator[str]:
        raise AssertionError("must not be iterated")

    @override
    def __str__(self) -> str:
        return "broken"


class BarePathLike:
    """An `os.PathLike` that is not a `pathlib.Path`; nothing reads these."""

    def __fspath__(self) -> str:
        return str(SAMPLE_FILE_PATH)


class Perm(enum.IntFlag):
    R = 4
    W = 2
    X = 1


class Shade(enum.Flag):
    LIGHT = 1
    DARK = 2


class Level(enum.IntEnum):
    LOW = 1


class Tag(str):
    pass


class Count(int):
    pass


class Matryoshka(Sequence["Matryoshka"]):
    """Holds a fresh object of its own kind, however deep the walk goes."""

    @override
    def __len__(self) -> int:
        return 1

    @override
    def __getitem__(self, index: Any) -> Any:
        if index == 0:
            return Matryoshka()
        raise IndexError(index)


class StrPath(str):
    """A `str` that is also an `os.PathLike`."""

    def __fspath__(self) -> str:
        return str(self)


async def test_strips_omit_and_not_given(send: Send) -> None:
    assert await send({"foo": "bar", "baz": omit, "qux": not_given}) == {"foo": "bar"}
    assert await send({"a": {"b": omit, "c": {"d": not_given, "e": 1}}}) == {"a": {"c": {"e": 1}}}
    assert await send({"items": [{"keep": True, "drop": omit}, {"drop": not_given}]}) == {"items": [{"keep": True}, {}]}
    assert await send([{"a": omit}]) == [{}]


async def test_extra_body_is_merged_in(send: Send) -> None:
    assert await send(
        {"a": 1}, extra_body={"b": ("x",), "c": {"d": omit}, "e": [{"f": not_given}], "g": Item(id="1")}
    ) == {"a": 1, "b": ["x"], "c": {}, "e": [{}], "g": {"id": "1"}}
    assert await send(
        {"model": "m", "keep": True, "nested": {"a": 1}}, extra_body={"model": omit, "nested": {"b": ("x",), "c": omit}}
    ) == {"keep": True, "nested": {"b": ["x"]}}
    assert await send({"a": 1}, extra_body={"a": not_given}) == {"a": 1}


async def test_keeps_none(send: Send) -> None:
    assert await send({"foo": None, "bar": {"baz": None}, "items": [None]}) == {
        "foo": None,
        "bar": {"baz": None},
        "items": [None],
    }
    assert await send(None) is None


LISTS: list[Callable[[], object]] = [
    lambda: [1, 2],
    lambda: (1, 2),
    lambda: range(1, 3),
    lambda: deque([1, 2]),
    lambda: {1, 2},
    lambda: frozenset((1, 2)),
    lambda: {1: "a", 2: "b"}.keys(),
    lambda: {"a": 1, "b": 2}.values(),
    lambda: (i for i in (1, 2)),
    lambda: iter([1, 2]),
    lambda: map(int, "12"),
]


@pytest.mark.parametrize("make", LISTS)
async def test_sequences_sets_views_and_iterators_are_sent_as_lists(send: Send, make: Callable[[], object]) -> None:
    assert await send({"k": make(), "nested": [make()]}) == {"k": [1, 2], "nested": [[1, 2]]}
    assert await send(make()) == [1, 2]
    assert await send({"items": {1: "a"}.items()}) == {"items": [[1, "a"]]}

    await send.query({"k": [1, 2]})
    as_list = send.request.url.query
    await send.query({"k": make()})
    assert send.request.url.query == as_list


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(ipaddress.ip_network("10.0.0.0/30"), id="ip_network"),
        pytest.param(IterableDuckReader(), id="only __iter__"),
        pytest.param(BrokenIterable(), id="__iter__ raises"),
        pytest.param(Shade, id="Enum class"),
        pytest.param(memoryview(b"ab"), id="memoryview"),
    ],
)
async def test_other_iterables_are_not_iterated(send: Send, value: object) -> None:
    # in a body they are left to the encoder, in a query they are sent as their `str()`
    for body in ({"k": value}, [value]):
        with pytest.raises(TypeError, match="is not JSON serializable"):
            await send(body)
    assert await send.query({"k": value}) == {"k": str(value)}


async def test_siblings_are_prepared_in_document_order(send: Send, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(MARKERS_ATTR, MARKERS)
    # two values drawing from one iterator are drained first to last
    words = iter(["FIRST", "SECOND"])
    assert await send({"messages": [{"content": islice(words, 1)}, {"content": islice(words, 1)}]}) == {
        "messages": [{"content": ["FIRST"]}, {"content": ["SECOND"]}]
    }

    # and a reader shared by two file inputs is read by the first of them
    reader = io.BytesIO(b"Hello, world!")
    assert await send({"content": [image_block(reader), image_block(reader)]}) == {
        "content": [image_block("SGVsbG8sIHdvcmxkIQ=="), image_block("")]
    }

    with pytest.raises(FileNotFoundError, match="first.png"):
        await send({"a": b64_obj(pathlib.Path("first.png")), "b": [b64_obj(pathlib.Path("second.png"))]})


async def test_scalars(send: Send) -> None:
    assert await send({"s": "str", "i": 1, "f": 1.5, "t": True}) == {"s": "str", "i": 1, "f": 1.5, "t": True}
    assert await send("bare") == "bare"
    assert await send(3) == 3


async def test_scalar_subclasses_are_sent_as_their_value(send: Send) -> None:
    # flags are iterable since Python 3.11, each member yielding itself
    assert await send(
        {
            "perm": Perm.R | Perm.W,
            "one": Perm.W,
            "none": Perm(0),
            "level": Level.LOW,
            "tag": Tag("t"),
            "count": Count(3),
        }
    ) == {"perm": 6, "one": 2, "none": 0, "level": 1, "tag": "t", "count": 3}
    assert await send(Perm.W) == 2
    assert await send([Perm.R | Perm.X, Tag("t")]) == [5, "t"]

    query = {"perm": Perm.R | Perm.W, "one": Perm.W, "none": Perm(0), "flags": re.I, "tag": Tag("t"), "count": Count(3)}
    assert await send.query(query) == {key: str(value) for key, value in query.items()}


async def test_user_strings_are_not_iterated(send: Send) -> None:
    # iterating one yields one-character `UserString`s, never reaching a plain value
    with pytest.raises(TypeError, match="is not JSON serializable"):
        await send({"s": UserString("ab")})
    assert await send.query({"s": UserString("ab")}) == {"s": "ab"}


async def test_endless_nesting_is_rejected(send: Send, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("anthropic._utils._prepare.MAX_DEPTH", 50)
    with pytest.raises(ValueError, match="maximum nesting depth"):
        await send({"x": Matryoshka()})
    with pytest.raises(ValueError, match="maximum nesting depth"):
        await send.query({"x": Matryoshka()})


@pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
async def test_serialize_data(sync: bool) -> None:
    def body() -> object:
        return {
            "nested": MappingProxyType({"keep": (1, 2), "drop": omit}),
            "when": datetime(2024, 1, 2, 3, 4, 5, tzinfo=timezone.utc),
        }

    if sync:
        serialized = serialize_data(body(), location="body")
        assert serialized == openapi_dumps_str(prepare_request_data(body(), location="body"))
    else:
        serialized = await async_serialize_data(body(), location="body")
        assert serialized == openapi_dumps_str(await async_prepare_request_data(body(), location="body"))
    assert serialized == '{"nested":{"keep":[1,2]},"when":"2024-01-02T03:04:05+00:00"}'


@pytest.mark.parametrize(
    "value, iso",
    [
        pytest.param(datetime(2024, 1, 2, 3, 4, 5, tzinfo=timezone.utc), "2024-01-02T03:04:05+00:00", id="aware"),
        pytest.param(datetime(2024, 1, 2, 3, 4, 5), "2024-01-02T03:04:05", id="naive"),
        pytest.param(
            datetime(2024, 1, 2, 3, 4, 5, 678901, tzinfo=timezone(timedelta(hours=-5))),
            "2024-01-02T03:04:05.678901-05:00",
            id="microseconds",
        ),
        pytest.param(date(2024, 1, 2), "2024-01-02", id="date"),
    ],
)
async def test_dates_are_prepared_as_iso_strings(
    send: Send, client: Anthropic | AsyncAnthropic, value: date, iso: str
) -> None:
    given = {"at": value, "nested": {"at": value}, "items": (value, {"at": [value]})}
    expected = {"at": iso, "nested": {"at": iso}, "items": [iso, {"at": [iso]}]}

    # what hooks and middleware see
    assert prepare_request_data(given, location="query") == expected
    if isinstance(client, Anthropic):
        assert prepare_request_data(given, location="body") == expected
    else:
        assert await async_prepare_request_data(given, location="body") == expected

    # and what goes over the wire, in a body, a query and a multipart form
    assert await send(given) == expected
    assert await send(value) == iso
    assert await send({"a": 1}, extra_body=given) == {"a": 1, **expected}
    await send.query(expected)
    as_strings = send.request.url.query
    await send.query(given)
    assert send.request.url.query == as_strings
    await send.query(extra_query=given)
    assert send.request.url.query == as_strings
    assert iso.encode() in await send.form(given)
    assert await send.form(given) == await send.form(expected)


async def test_preserves_key_order(send: Send) -> None:
    schema = {"type": "object", "properties": {"zeta": {"type": "string"}, "alpha": {"type": "integer"}, "mid": {}}}

    await send({"tools": ({"name": "t", "input_schema": MappingProxyType(schema), "beta": omit},), "model": "m"})

    assert (
        send.request.content
        == b'{"tools":[{"name":"t","input_schema":{"type":"object","properties":{"zeta":{"type":"string"},"alpha":{"type":"integer"},"mid":{}}}}],"model":"m"}'
    )


async def test_pydantic_models_are_dumped(send: Send) -> None:
    class MyModel(BaseModel):
        foo: str
        when: datetime
        unset: str | None = None
        from_: str | None = pydantic.Field(alias="from", default=None)

    def make(data: dict[str, Any]) -> dict[str, MyModel]:
        """The model holding `data`, made in each of the ways a model gets made."""
        return {
            "constructor": MyModel(**data),
            "validation": model_parse(MyModel, data),
            "construct": MyModel.construct(**data),
            "construct_type": cast(MyModel, construct_type(type_=MyModel, value=data)),
            "copy": model_copy(MyModel(**data)),
        }

    when = datetime(2023, 2, 23, 14, 16, 36, tzinfo=timezone.utc)
    sent_when = "2023-02-23T14:16:36Z" if not PYDANTIC_V1 else "2023-02-23T14:16:36+00:00"

    for made, model in make({"foo": "hi", "when": when, "from": "there"}).items():
        assert await send({"m": model, "l": [model]}) == {
            "m": {"foo": "hi", "when": sent_when, "from": "there"},
            "l": [{"foo": "hi", "when": sent_when, "from": "there"}],
        }, made
    for made, model in make({"foo": "hi", "when": when, "unset": None, "other": True}).items():
        # a `None` that was given counts as set, and unknown keys are kept
        assert await send(model) == {"foo": "hi", "when": sent_when, "unset": None, "other": True}, made

    assert await send(MyModel.construct(foo="hi!")) == {"foo": "hi!"}
    assert await send(MyModel.construct()) == {}


async def test_pydantic_mismatched_types(send: Send) -> None:
    class MyModel(BaseModel):
        foo: str

    model = MyModel.construct(foo=True)

    if PYDANTIC_V1:
        assert await send(model) == {"foo": True}
    else:
        with pytest.warns(UserWarning):
            assert await send(model) == {"foo": True}


async def test_api_exclude(send: Send) -> None:
    class Parsed(BaseModel):
        __api_exclude__ = {"parsed"}
        text: str
        parsed: object = None

    assert await send({"c": [Parsed.construct(text="x", parsed={"a": 1})]}) == {"c": [{"text": "x"}]}


class LateBoundBlock(BaseModel):
    type: str
    child: LateBoundChild | None = None


class LateBoundChild(BaseModel):
    x: int


class LateBoundMessage(BaseModel):
    content: list[LateBoundBlock]


async def test_models_with_unresolved_forward_references(send: Send) -> None:
    # response models may be instances of classes with unresolved forward references; the request options
    # holding them are still dumped for the debug log, which only works because the body was prepared first
    message = model_parse(LateBoundMessage, {"content": [{"type": "late"}]})

    assert await send({"messages": [{"role": "assistant", "content": message.content}]}) == {
        "messages": [{"role": "assistant", "content": [{"type": "late"}]}]
    }


async def test_query_params(send: Send) -> None:
    assert await send.query(
        {"created_at[gte]": datetime(2024, 1, 2, 3, 4, 5, tzinfo=timezone.utc), "x": omit, "y": not_given, "n": None},
        extra_query={"x": "1"},
    ) == {"created_at[gte]": "2024-01-02T03:04:05+00:00", "x": "1"}
    assert send.request.url.query == b"created_at%5Bgte%5D=2024-01-02T03%3A04%3A05%2B00%3A00&x=1"
    assert await send.query({"on": date(2024, 1, 2), "flag": True, "n": 3}) == {
        "on": "2024-01-02",
        "flag": "true",
        "n": "3",
    }


async def test_empty_query_params_are_left_unset(send: Send, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG, logger="anthropic._base_client")

    def logged_options() -> str:
        [message] = [m for m in (r.getMessage() for r in caplog.records) if m.startswith("Request options:")]
        caplog.clear()
        return message

    # so the logged request options, dumped with `exclude_unset`, only name them when there are any
    await send({"a": 1})
    assert "'params'" not in logged_options()
    await send.query({"limit": 10})
    assert "'params': {'limit': 10}" in logged_options()
    await send.query(extra_query={"limit": 10})
    assert "'params': {'limit': 10}" in logged_options()


async def test_extra_query_omit_removes_default_query(send: Send) -> None:
    default_query = {"foo": "bar", "keep": "1"}

    assert await send.query(extra_query={"foo": omit}, default_query=default_query) == {"keep": "1"}
    assert await send.query({"a": "b"}, extra_query={"other": omit, "x": not_given}, default_query=default_query) == {
        "foo": "bar",
        "keep": "1",
        "a": "b",
    }
    # whereas an `Omit` under `query` itself is dropped like any other
    assert await send.query({"foo": omit}, default_query=default_query) == {"foo": "bar", "keep": "1"}


async def test_base64_file_input(send: Send, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(MARKERS_ATTR, MARKERS)

    assert await send(b64_obj("bar")) == b64_obj("bar")
    assert await send(b64_obj(SAMPLE_FILE_PATH)) == b64_obj(SAMPLE_FILE_BASE64)
    assert await send(b64_obj(io.StringIO("Hello, world!"))) == b64_obj("SGVsbG8sIHdvcmxkIQ==")
    assert await send(b64_obj(io.BytesIO(b"Hello, world!"))) == b64_obj("SGVsbG8sIHdvcmxkIQ==")

    pdf = {"type": "base64", "media_type": "application/pdf", "data": SAMPLE_FILE_PATH}
    assert await send({"type": "document", "source": pdf}) == {
        "type": "document",
        "source": {"type": "base64", "media_type": "application/pdf", "data": SAMPLE_FILE_BASE64},
    }

    assert await send({"type": "base64"}) == {"type": "base64"}
    assert await send({"type": "base64", "data": None}) == {"type": "base64", "data": None}
    assert await send({"type": "base64", "data": [1]}) == {"type": "base64", "data": [1]}

    items = (b64_obj(SAMPLE_FILE_PATH), "given", MappingProxyType(b64_obj(io.BytesIO(b"Hello, world!"))))
    assert await send({"items": items}) == {
        "items": [b64_obj(SAMPLE_FILE_BASE64), "given", b64_obj("SGVsbG8sIHdvcmxkIQ==")]
    }
    assert await send({"items": (b for b in [b64_obj(SAMPLE_FILE_PATH)])}) == {"items": [b64_obj(SAMPLE_FILE_BASE64)]}
    assert await send({"x": {"a": b64_obj(SAMPLE_FILE_PATH), "b": "given"}}) == {
        "x": {"a": b64_obj(SAMPLE_FILE_BASE64), "b": "given"}
    }
    assert await send(
        {"a": 1}, extra_body={"doc": b64_obj(SAMPLE_FILE_PATH), "docs": [b64_obj(io.BytesIO(b"Hello, world!"))]}
    ) == {"a": 1, "doc": b64_obj(SAMPLE_FILE_BASE64), "docs": [b64_obj("SGVsbG8sIHdvcmxkIQ==")]}

    monkeypatch.setattr(MARKERS_ATTR, ())
    with pytest.raises(TypeError, match="is not JSON serializable"):
        await send(b64_obj(SAMPLE_FILE_PATH))


async def test_get_does_not_prepare_a_body(send: Send, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(MARKERS_ATTR, MARKERS)
    pulled: list[int] = []

    def items() -> Iterator[int]:
        pulled.append(1)
        yield 1

    missing = b64_obj(pathlib.Path("does-not-exist.png"))

    # nothing of a body is sent, so nothing in it is read either
    assert await send.query({"a": "b"}, extra_body={"doc": missing, "items": items()}) == {"a": "b"}
    assert not send.request.content
    assert pulled == []

    with pytest.raises(FileNotFoundError):
        await send({"a": 1}, extra_body={"doc": missing})


async def test_query_params_are_never_read(send: Send, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(MARKERS_ATTR, MARKERS)
    path = tmp_path.joinpath("note.txt")
    path.write_bytes(b"not its path")
    content = base64.b64encode(b"not its path").decode()

    for query in (await send.query({"doc": b64_obj(path)}), await send.query(extra_query={"doc": b64_obj(path)})):
        assert str(path) in query.values()
        assert content not in query.values()


@pytest.mark.parametrize(
    "body",
    [
        pytest.param({"b": b"bytes"}, id="bytes"),
        pytest.param({"data": SAMPLE_FILE_PATH}, id="untyped data"),
        pytest.param({"type": "text", "media_type": "text/plain", "data": SAMPLE_FILE_PATH}, id="text source"),
        pytest.param({"type": ["base64"], "data": SAMPLE_FILE_PATH}, id="list type"),
        pytest.param({"type": "base64", "file": SAMPLE_FILE_PATH, "data": "given"}, id="other data key"),
    ],
)
async def test_bytes_and_files_elsewhere_are_rejected(
    send: Send, body: object, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(MARKERS_ATTR, MARKERS)
    with pytest.raises(TypeError, match="is not JSON serializable"):
        await send(body)


async def test_text_mode_files_elsewhere_are_rejected(
    send: Send, tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(MARKERS_ATTR, MARKERS)
    # text-mode handles are iterables of `str` lines, but are never sent as a list of them
    path = tmp_path.joinpath("note.txt")
    path.write_text("a\nb\n")
    text = io.StringIO("a\nb\n")

    with open(path) as handle:
        for value in (text, handle):
            for body in ({"x": value}, {"l": [value]}, {"type": "text", "data": value}):
                with pytest.raises(TypeError, match="is not JSON serializable"):
                    await send({"nested": body})
            assert value.tell() == 0


async def test_objects_with_a_read_method_are_not_files(send: Send, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(MARKERS_ATTR, MARKERS)
    # not even inside a base64 source: what gets read is decided by type, not by the methods present
    duck = DuckReader()

    for body in ({"x": duck}, {"l": [duck]}, (duck,), image_block(duck)):
        with pytest.raises(TypeError, match="is not JSON serializable"):
            await send(body)

    assert duck.read_calls == 0


@pytest.mark.parametrize(
    "file",
    [
        pytest.param(BarePathLike(), id="bare PathLike"),
        pytest.param(StrPath(SAMPLE_FILE_PATH), id="PathLike str"),
    ],
)
async def test_other_path_likes_are_not_read(send: Send, file: object, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(MARKERS_ATTR, MARKERS)
    # whether in a typed image source or in any mapping of that shape, and without looking the path up
    for body in (image_block(file), {"metadata": b64_obj(file)}):
        with pytest.raises(TypeError, match="only pathlib.Path and file objects are read") as exc_info:
            await send(body)
        assert str(exc_info.value).startswith(f"Cannot read {type(file)};")


async def test_file_objects_must_read_as_bytes(send: Send, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(MARKERS_ATTR, MARKERS)

    class OddReader(io.RawIOBase):
        @override
        def read(self, size: int = -1) -> Any:  # noqa: ARG002
            return 3

    with pytest.raises(RuntimeError, match="Could not read bytes from .*; Received <class 'int'>"):
        await send(b64_obj(OddReader()))


async def test_pathlike_str_outside_file_slots_is_a_string(send: Send, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(MARKERS_ATTR, MARKERS)
    body = {"foo": StrPath("tests/sample_file.txt"), "items": [StrPath("x")]}

    assert await send(body) == {"foo": "tests/sample_file.txt", "items": ["x"]}


def layout(value: object) -> object:
    """The identity and contents of `value` and of everything inside it."""
    contents = value
    if is_mapping(value):
        contents = [(key, layout(item)) for key, item in value.items()]
    elif is_sequence(value) and not isinstance(value, str):
        contents = [layout(item) for item in value]
    return id(value), type(value), contents


@pytest.mark.parametrize(
    "make_body, sent",
    [
        pytest.param(
            lambda: {"a": {"b": omit, "c": 1}, "items": [{"d": None}, ({"t": (1, 2)},)]},
            {"a": {"c": 1}, "items": [{"d": None}, [{"t": [1, 2]}]]},
            id="nested",
        ),
        pytest.param(
            lambda: {
                "a": [{"b": omit, "c": (1, 2)}],
                "foo": b64_obj(SAMPLE_FILE_PATH),
                "items": [(b64_obj(SAMPLE_FILE_PATH),)],
            },
            {"a": [{"c": [1, 2]}], "foo": b64_obj(SAMPLE_FILE_BASE64), "items": [[b64_obj(SAMPLE_FILE_BASE64)]]},
            id="path",
        ),
        pytest.param(
            lambda: {"doc": b64_obj(io.BytesIO(b"Hello, world!"))},
            {"doc": b64_obj("SGVsbG8sIHdvcmxkIQ==")},
            id="file object",
        ),
    ],
)
async def test_idempotent_and_does_not_mutate_input(
    send: Send, make_body: Callable[[], object], sent: object, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(MARKERS_ATTR, MARKERS)
    body = make_body()
    before = layout(body)

    assert await send(body) == sent
    assert layout(body) == before
    assert await send(sent) == sent


async def test_deep_nesting(send: Send, client: Anthropic | AsyncAnthropic, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(MARKERS_ATTR, MARKERS)

    # untyped JSON fields (`input_schema`, ...) can nest past the recursion limit
    def nested(depth: int) -> object:
        data: object = {"type": "base64", "dropped": omit, "data": SAMPLE_FILE_PATH}
        for i in range(depth):
            data = {"k": data} if i % 2 else (data,)
        return data

    depth = 5 * sys.getrecursionlimit()
    if isinstance(client, Anthropic):
        prepared = prepare_request_data(nested(depth), location="body")
    else:
        prepared = await async_prepare_request_data(nested(depth), location="body")
    for i in reversed(range(depth)):
        prepared = prepared["k"] if i % 2 else prepared[0]
    assert prepared == {"type": "base64", "data": SAMPLE_FILE_BASE64}

    # sent end to end from less deep only because `json` itself recurses once per level before Python 3.12
    depth = sys.getrecursionlimit() - 100
    await send({"metadata": nested(depth)})

    assert send.request.content.endswith(
        b'{"type":"base64","data":"SGVsbG8sIHdvcmxkIQo="}' + b"]}" * (depth // 2) + b"}"
    )


async def test_circular_reference(send: Send) -> None:
    self_dict: dict[str, object] = {}
    self_dict["self"] = self_dict
    with pytest.raises(ValueError, match="Circular reference detected"):
        await send({"metadata": self_dict})

    self_list: list[object] = []
    self_list.append(self_list)
    with pytest.raises(ValueError, match="Circular reference detected"):
        await send({"items": self_list})

    inner: dict[str, object] = {}
    indirect = {"a": [{"b": (inner,)}]}
    inner["back"] = indirect
    with pytest.raises(ValueError, match="Circular reference detected"):
        await send(indirect)

    shared = {"a": 1, "l": [{"b": 2}]}
    assert await send({"x": shared, "y": shared, "both": (shared, shared)}) == {
        "x": shared,
        "y": shared,
        "both": [shared, shared],
    }

    # freed generator items can have their `id()` reused by later ones; that must not read as a cycle
    def rows() -> Iterator[dict[str, object]]:
        for i in range(50):
            yield {"k": [i]}

    def pages() -> Iterator[dict[str, object]]:
        for _ in range(3):
            yield {"x": rows()}

    assert await send({"items": pages()}) == {"items": [{"x": [{"k": [i]} for i in range(50)]} for _ in range(3)]}


class TestClient:
    # the route stays uncalled when the package has no file input markers
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_file_input_markers(self, respx_mock: MockRouter, client: Anthropic | AsyncAnthropic) -> None:
        route = respx_mock.post("/foo").mock(return_value=httpx2.Response(200, json={}))
        sources = [{discriminator: tag, field: SAMPLE_FILE_PATH} for discriminator, tag, field in FILE_INPUT_MARKERS]
        prepared = [{discriminator: tag, field: SAMPLE_FILE_BASE64} for discriminator, tag, field in FILE_INPUT_MARKERS]
        unmatched = {discriminator: [tag] for discriminator, tag, _ in FILE_INPUT_MARKERS}

        if isinstance(client, Anthropic):
            for source in sources:
                client.post("/foo", body={"x": source}, cast_to=httpx2.Response)
            with pytest.raises(TypeError, match="is not JSON serializable"):
                client.post("/foo", body={"x": {**unmatched, "data": SAMPLE_FILE_PATH}}, cast_to=httpx2.Response)
        else:
            for source in sources:
                await client.post("/foo", body={"x": source}, cast_to=httpx2.Response)
            with pytest.raises(TypeError, match="is not JSON serializable"):
                await client.post("/foo", body={"x": {**unmatched, "data": SAMPLE_FILE_PATH}}, cast_to=httpx2.Response)

        assert route.call_count == len(FILE_INPUT_MARKERS)
        bodies = [json.loads(call.request.content) for call in cast("list[MockRequestCall]", route.calls)]
        assert bodies == [{"x": source} for source in prepared]

    @pytest.mark.respx(base_url=base_url)
    async def test_generator_body_survives_retries(
        self, respx_mock: MockRouter, client: Anthropic | AsyncAnthropic, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(BaseClient, "_calculate_retry_timeout", _no_retry_delay)
        route = respx_mock.post("/foo").mock(
            side_effect=[httpx2.Response(500, json={}), httpx2.Response(200, json={})],
        )
        body = {"items": ({"i": i} for i in range(2))}
        options = make_request_options(extra_body={"x": (i for i in range(3))})

        if isinstance(client, Anthropic):
            client.with_options(max_retries=1).post("/foo", body=body, options=options, cast_to=httpx2.Response)
        else:
            await client.with_options(max_retries=1).post("/foo", body=body, options=options, cast_to=httpx2.Response)

        assert route.call_count == 2
        calls = cast("list[MockRequestCall]", route.calls)
        assert [c.request.content for c in calls] == [b'{"items":[{"i":0},{"i":1}],"x":[0,1,2]}'] * 2

    @pytest.mark.respx(base_url=base_url)
    async def test_extra_query_iterator_survives_pagination(
        self, respx_mock: MockRouter, client: Anthropic | AsyncAnthropic
    ) -> None:
        route = respx_mock.get("/foo").mock(
            side_effect=[
                httpx2.Response(200, json={"data": [{"id": "1"}], "last_id": "c1", "has_more": True}),
                httpx2.Response(200, json={"data": [{"id": "2"}], "last_id": None, "has_more": False}),
            ]
        )
        options = make_request_options(query={"limit": 1}, extra_query={"tags": iter(["red", "blue"])})

        if isinstance(client, Anthropic):
            pages = client.get_api_list("/foo", model=Item, page=SyncPage[Item], options=options)
            ids = [item.id for item in pages]
        else:
            async_pages = client.get_api_list("/foo", model=Item, page=AsyncPage[Item], options=options)
            ids = [item.id async for item in async_pages]

        assert ids == ["1", "2"]
        first, second = (call.request.url for call in cast("list[MockRequestCall]", route.calls))
        assert b"red" in first.query and b"blue" in first.query
        assert second.params["after_id"] == "c1"
        assert second.copy_remove_param("after_id").query == first.query
