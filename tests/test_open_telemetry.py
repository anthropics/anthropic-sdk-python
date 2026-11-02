from __future__ import annotations

import gc
import os
import re
import sys
import json
import asyncio
import inspect
import logging
import pathlib
import threading
import subprocess
from types import UnionType
from random import Random
from typing import Any, Union, Protocol, cast, get_args, get_origin
from contextlib import contextmanager, asynccontextmanager
from collections.abc import Mapping, Callable, Iterable, Iterator, Sequence, Collection, AsyncIterator
from typing_extensions import Final, Literal, Required, Annotated, NotRequired, override, is_typeddict, get_type_hints
from concurrent.futures import ThreadPoolExecutor

import httpx2
import pytest
import pydantic
from respx import MockRouter
from opentelemetry import trace, baggage, context, propagate
from opentelemetry.trace import SpanKind, StatusCode
from opentelemetry.context import Context
from opentelemetry.sdk.trace import Span as SdkSpan, ReadableSpan, SpanProcessor, TracerProvider, sampling
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.propagators.textmap import TextMapPropagator
from opentelemetry.sdk.trace.id_generator import RandomIdGenerator
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from anthropic import (
    NOT_GIVEN,
    Stream,
    Anthropic,
    APIResponse,
    AsyncStream,
    AnthropicAWS,
    MessageStream,
    APIStatusError,
    AsyncAnthropic,
    RateLimitError,
    AnthropicVertex,
    APITimeoutError,
    BadRequestError,
    AnthropicBedrock,
    AnthropicFoundry,
    AsyncAPIResponse,
    AsyncAnthropicAWS,
    APIConnectionError,
    AsyncMessageStream,
    InternalServerError,
    AnthropicGoogleCloud,
    AsyncAnthropicVertex,
    AsyncAnthropicBedrock,
    AsyncAnthropicFoundry,
    AnthropicBedrockMantle,
    AsyncAnthropicGoogleCloud,
    AsyncAnthropicBedrockMantle,
    _base_client,
)
from anthropic.types import (
    Usage,
    ContentBlock,
    ToolUseBlock,
    CacheCreation,
    TextBlockParam,
    ContentBlockParam,
    OutputTokensDetails,
    ToolResultBlockParam,
    RawMessageStreamEvent,
    SearchResultBlockParam,
    TextEditorCodeExecutionViewResultBlock,
    TextEditorCodeExecutionViewResultBlockParam,
)
from anthropic._types import OpenTelemetryTraces, OpenTelemetryOptions, OpenTelemetryClientOption
from anthropic._compat import PYDANTIC_V1, get_model_fields
from anthropic._tracing import defined_query, is_content_query, global_tracer_provider_loads
from anthropic.types.beta import (
    BetaUsage,
    BetaContentBlock,
    BetaToolUseBlock,
    BetaCacheCreation,
    BetaContentBlockParam,
    BetaOutputTokensDetails,
    BetaToolResultBlockParam,
    BetaRawMessageStreamEvent,
    BetaTextEditorCodeExecutionViewResultBlock,
    BetaTextEditorCodeExecutionViewResultBlockParam,
)
from anthropic.lib.streaming import _messages, _beta_messages
from anthropic.lib._tracing._utils import to_json
from anthropic.lib._tracing._content import (
    CONTENT_LIMIT,
    Part,
    TextPart,
    ChatMessage,
    InputMessages,
    OutputMessage,
    OutputMessages,
    fit_content,
    set_content_attributes,
)
from anthropic.lib._tracing._attributes import AttributeName

from .utils import update_env

base_url = "http://127.0.0.1:4010"

MESSAGE: dict[str, Any] = {
    "id": "msg_1",
    "type": "message",
    "role": "assistant",
    "model": "claude-test",
    "content": [{"type": "text", "text": "Hi there"}],
    "stop_reason": "end_turn",
    "stop_sequence": None,
    "usage": {
        "input_tokens": 10,
        "output_tokens": 5,
        "cache_read_input_tokens": 2,
        "cache_creation_input_tokens": 3,
        "cache_creation": {"ephemeral_5m_input_tokens": 1, "ephemeral_1h_input_tokens": 2},
        "service_tier": "standard",
    },
}

RESPONSE_HEADERS = {
    "request-id": "req_1",
    "anthropic-organization-id": "org_1",
    "anthropic-workspace-id": "wrkspc_1",
}


class Spans:
    """A tracer provider that records finished spans in memory."""

    def __init__(self) -> None:
        self.exporter = InMemorySpanExporter()
        self.provider = TracerProvider()
        self.provider.add_span_processor(SimpleSpanProcessor(self.exporter))

    @property
    def finished(self) -> Sequence[ReadableSpan]:
        return self.exporter.get_finished_spans()

    def named(self, name: str) -> list[ReadableSpan]:
        return [span for span in self.finished if span.name == name]

    def one(self, name: str) -> ReadableSpan:
        spans = self.named(name)
        assert len(spans) == 1, [span.name for span in self.finished]
        return spans[0]

    def option(self, **options: Any) -> OpenTelemetryOptions:
        return cast(OpenTelemetryOptions, {"tracer_provider": self.provider, **options})


@pytest.fixture
def spans() -> Spans:
    return Spans()


@pytest.fixture
def registered(spans: Spans, monkeypatch: pytest.MonkeyPatch) -> Spans:
    """`spans`, with its provider registered with the OpenTelemetry API for this test, which a client that is given none uses.

    A client that is given a `tracer_provider` is given an option, so it reads no environment variable. The API
    registers a provider once for each process, so this sets what it would have registered and puts it back afterwards.
    """
    monkeypatch.setattr(trace, "_TRACER_PROVIDER", spans.provider)
    return spans


def make_client(spans: Spans, **options: Any) -> Anthropic:
    options.setdefault("open_telemetry", spans.option())
    options.setdefault("_strict_response_validation", True)
    options.setdefault("base_url", base_url)
    return Anthropic(api_key="key", **options)


def make_async_client(spans: Spans, **options: Any) -> AsyncAnthropic:
    options.setdefault("open_telemetry", spans.option())
    options.setdefault("_strict_response_validation", True)
    options.setdefault("base_url", base_url)
    return AsyncAnthropic(api_key="key", **options)


class StartAttributes(sampling.Sampler):
    """Keeps the name and the attributes that each span starts with, which is all that a sampler is given."""

    def __init__(self) -> None:
        self.started: list[tuple[str, dict[str, Any]]] = []

    @override
    def should_sample(self, *args: Any, **kwargs: Any) -> sampling.SamplingResult:
        name, attributes = kwargs.get("name", args[2] if len(args) > 2 else None), kwargs.get("attributes")
        self.started.append((str(name), dict(attributes or (args[4] if len(args) > 4 else None) or {})))
        return sampling.ALWAYS_ON.should_sample(*args, **kwargs)

    @override
    def get_description(self) -> str:
        return "start attributes"


def attributes(span: ReadableSpan) -> dict[str, Any]:
    return dict(span.attributes or {})


def span_id(span: ReadableSpan | trace.Span) -> int:
    span_context = span.get_span_context()
    assert span_context is not None
    return span_context.span_id


def trace_id(span: ReadableSpan) -> int:
    span_context = span.get_span_context()
    assert span_context is not None
    return span_context.trace_id


def parent_id(span: ReadableSpan) -> int:
    assert span.parent is not None
    return span.parent.span_id


class MockRequestCall(Protocol):
    request: httpx2.Request


def requests(route: Any) -> list[httpx2.Request]:
    return [call.request for call in cast("list[MockRequestCall]", route.calls)]


def sigv4_signature(request: httpx2.Request, *, secret_key: str) -> str:
    """The SigV4 signature of `request` as it was sent, over the headers that its `Authorization` header lists."""
    from botocore.auth import SigV4Auth
    from botocore.awsrequest import AWSRequest
    from botocore.credentials import Credentials

    fields = dict(field.strip().split("=", 1) for field in request.headers["Authorization"].split(" ", 1)[1].split(","))
    access_key, _, region, service, _ = fields["Credential"].split("/")
    signed = {name: request.headers[name] for name in fields["SignedHeaders"].split(";")}
    sent = AWSRequest(method=request.method, url=str(request.url), headers=signed, data=request.content)
    sent.context["timestamp"] = request.headers["X-Amz-Date"]
    signer = SigV4Auth(Credentials(access_key, secret_key), service, region)
    return str(signer.signature(signer.string_to_sign(sent, signer.canonical_request(sent)), sent))


def respond_with_message(_request: httpx2.Request) -> httpx2.Response:
    return httpx2.Response(200, json=MESSAGE)


def create(client: Any, **kwargs: Any) -> Any:
    return client.messages.create(
        max_tokens=1024, messages=[{"role": "user", "content": "Hello"}], model="claude-test", **kwargs
    )


def requests_with_file(file: pathlib.Path) -> Any:
    """The requests of a Message Batch whose one message has the image in `file`, which the client reads when it prepares the body."""
    image = {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": file}}
    params = {"max_tokens": 1, "messages": [{"role": "user", "content": [image]}], "model": "claude-test"}
    return [{"custom_id": "a", "params": params}]


def sse(events: Sequence[dict[str, Any]]) -> bytes:
    return b"".join(f"event: {event['type']}\ndata: {json.dumps(event)}\n\n".encode() for event in events)


def utf8_size(text: str) -> int:
    return len(text.encode())


def content_size(span: ReadableSpan) -> int:
    """The bytes of UTF-8 that the content attributes of `span` that can be reduced hold."""
    names = ("gen_ai.input.messages", "gen_ai.output.messages", "gen_ai.system_instructions")
    return sum(utf8_size(attributes(span).get(name, "")) for name in names)


SYSTEM: Final = "gen_ai.system_instructions"
INPUT: Final = "gen_ai.input.messages"
OUTPUT: Final = "gen_ai.output.messages"
STOPS: Final = "gen_ai.request.stop_sequences"


def text_part(content: str) -> dict[str, Any]:
    return {"type": "text", "content": content}


def chat_message(role: str, *parts: dict[str, Any]) -> dict[str, Any]:
    return {"role": role, "parts": list(parts)}


SIZE_BOUND_CASES = [
    pytest.param(
        1000,
        {
            SYSTEM: [text_part("Be brief.")],
            INPUT: [chat_message("user", text_part("hi"))],
            OUTPUT: [chat_message("assistant", text_part("hello"))],
        },
        {
            SYSTEM: [text_part("Be brief.")],
            INPUT: [chat_message("user", text_part("hi"))],
            OUTPUT: [chat_message("assistant", text_part("hello"))],
        },
        False,
        (163, 163),
        id="under_the_bound_is_unchanged",
    ),
    pytest.param(
        163,
        {
            SYSTEM: [text_part("Be brief.")],
            INPUT: [chat_message("user", text_part("hi"))],
            OUTPUT: [chat_message("assistant", text_part("hello"))],
        },
        {
            SYSTEM: [text_part("Be brief.")],
            INPUT: [chat_message("user", text_part("hi"))],
            OUTPUT: [chat_message("assistant", text_part("hello"))],
        },
        False,
        (163, 163),
        id="exactly_at_the_bound_is_unchanged",
    ),
    pytest.param(
        260,
        {
            SYSTEM: [
                text_part("S1-ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss"),
                text_part("S2 stays"),
            ],
            INPUT: [chat_message("user", text_part("question"))],
            OUTPUT: [chat_message("assistant", text_part("answer"))],
        },
        {
            SYSTEM: [text_part("S2 stays")],
            INPUT: [chat_message("user", text_part("question"))],
            OUTPUT: [chat_message("assistant", text_part("answer"))],
        },
        True,
        (261, 169),
        id="system_parts_go_first",
    ),
    pytest.param(
        222,
        {
            SYSTEM: [text_part("sys-ssssssssssssssssssssssssssssss")],
            INPUT: [
                chat_message(
                    "user", text_part("old-oooooooooooooooooooooooooooooooooooooooo"), {"type": "anthropic_image"}
                ),
                chat_message("assistant", text_part("mid")),
                chat_message("user", text_part("last")),
            ],
            OUTPUT: [chat_message("assistant", text_part("answer"))],
        },
        {
            SYSTEM: [],
            INPUT: [
                chat_message("user"),
                chat_message("assistant", text_part("mid")),
                chat_message("user", text_part("last")),
            ],
            OUTPUT: [chat_message("assistant", text_part("answer"))],
        },
        True,
        (380, 219),
        id="input_parts_follow_and_a_message_is_left_without_parts",
    ),
    pytest.param(
        180,
        {
            INPUT: [
                chat_message(
                    "user",
                    text_part("a-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"),
                    text_part("b-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"),
                    text_part("c stays"),
                ),
                chat_message("user", text_part("newest")),
            ]
        },
        {INPUT: [chat_message("user", text_part("c stays")), chat_message("user", text_part("newest"))]},
        True,
        (246, 124),
        id="parts_not_whole_messages_are_removed_and_absent_attributes_stay_absent",
    ),
    pytest.param(
        183,
        {
            SYSTEM: [text_part("sys")],
            INPUT: [chat_message("user", text_part("question qqqqqqqqqqqqqqqqqqqq"))],
            OUTPUT: [
                chat_message(
                    "assistant",
                    {"type": "reasoning", "content": "think-tttttttttttttttttttttttttttttttttttttttttttttttttt"},
                    text_part("final answer"),
                )
            ],
        },
        {SYSTEM: [], INPUT: [chat_message("user")], OUTPUT: [chat_message("assistant", text_part("final answer"))]},
        True,
        (281, 103),
        id="output_parts_go_from_the_start_and_reasoning_goes_whole",
    ),
    pytest.param(
        126,
        {
            SYSTEM: [text_part("sys")],
            INPUT: [chat_message("user", text_part("question"))],
            OUTPUT: [
                chat_message(
                    "assistant",
                    {"type": "tool_call", "id": "toolu_1", "name": "get_weather", "arguments": {"city": "Paris"}},
                    text_part("012345678901234567890123456789012345678901234567890123456789"),
                )
            ],
        },
        {
            SYSTEM: [],
            INPUT: [chat_message("user")],
            OUTPUT: [chat_message("assistant", text_part("01234567890123456789012345678901234"))],
        },
        True,
        (304, 126),
        id="last_remaining_text_part_is_cut_from_its_end",
    ),
    pytest.param(
        133,
        {
            INPUT: [
                chat_message(
                    "user",
                    text_part('say "hi"\nsay "hi"\nsay "hi"\nsay "hi"\nsay "hi"\nsay "hi"\nsay "hi"\nsay "hi"\n'),
                )
            ]
        },
        {INPUT: [chat_message("user", text_part('say "hi"\nsay "hi"\nsay "hi"\nsay "hi"\nsay "hi"\nsay "hi"\nsay '))]},
        True,
        (152, 132),
        id="cut_counts_the_serialized_escapes",
    ),
    pytest.param(
        117,
        {
            OUTPUT: [
                chat_message(
                    "assistant",
                    text_part(
                        "a\u20ac\U0001f600\u00e9a\u20ac\U0001f600\u00e9a\u20ac\U0001f600\u00e9a\u20ac\U0001f600\u00e9a\u20ac\U0001f600\u00e9a\u20ac\U0001f600\u00e9"
                    ),
                )
            ]
        },
        {
            OUTPUT: [
                chat_message(
                    "assistant",
                    text_part(
                        "a\u20ac\U0001f600\u00e9a\u20ac\U0001f600\u00e9a\u20ac\U0001f600\u00e9a\u20ac\U0001f600\u00e9a\u20ac\U0001f600\u00e9a\u20ac"
                    ),
                )
            ]
        },
        True,
        (121, 115),
        id="cut_is_at_a_character_boundary",
    ),
    pytest.param(
        120,
        {
            SYSTEM: [text_part("sys")],
            INPUT: [chat_message("user", text_part("question"))],
            OUTPUT: [
                chat_message(
                    "assistant",
                    {
                        "type": "tool_call",
                        "id": "toolu_1",
                        "name": "write_file",
                        "arguments": {
                            "path": "a.txt",
                            "text": "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
                        },
                    },
                )
            ],
        },
        {SYSTEM: [], INPUT: [chat_message("user")], OUTPUT: [chat_message("assistant")]},
        True,
        (304, 63),
        id="last_remaining_part_that_is_not_text_is_removed_whole",
    ),
    pytest.param(
        110,
        {
            INPUT: [chat_message("user", text_part("q"))],
            OUTPUT: [
                chat_message(
                    "assistant",
                    {
                        "type": "reasoning",
                        "content": "rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr",
                    },
                )
            ],
        },
        {INPUT: [chat_message("user")], OUTPUT: [chat_message("assistant")]},
        True,
        (223, 61),
        id="last_remaining_reasoning_part_is_removed_whole",
    ),
    pytest.param(
        100,
        {
            STOPS: [
                "STOP-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            ],
            SYSTEM: [text_part("sys")],
            INPUT: [chat_message("user", text_part("question"))],
            OUTPUT: [chat_message("assistant", {"type": "tool_call", "id": "toolu_1", "name": "f", "arguments": {}})],
        },
        {STOPS: None, SYSTEM: [], INPUT: [chat_message("user")], OUTPUT: [chat_message("assistant")]},
        True,
        (296, 63),
        id="stop_sequences_alone_over_the_bound_are_removed_whole_then_parts",
    ),
    pytest.param(
        100,
        {
            STOPS: [
                "STOP-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            ],
            INPUT: [chat_message("user")],
        },
        {STOPS: None, INPUT: [chat_message("user")]},
        True,
        (133, 28),
        id="stop_sequences_alone_over_the_bound_are_removed_whole",
    ),
    pytest.param(
        10,
        {
            SYSTEM: [text_part("sys")],
            INPUT: [chat_message("user", text_part("question"))],
            OUTPUT: [chat_message("assistant", {"type": "tool_call", "id": "toolu_1", "name": "f", "arguments": {}})],
        },
        {SYSTEM: [], INPUT: [chat_message("user")], OUTPUT: [chat_message("assistant")]},
        True,
        (191, 63),
        id="kept_structure_alone_over_a_tiny_bound_is_exported_as_it_is",
    ),
    pytest.param(
        100,
        {INPUT: [chat_message("user", text_part("\u00e9" * 30))]},
        {INPUT: [chat_message("user", text_part("\u00e9" * 22))]},
        True,
        (116, 100),
        id="multibyte_text_is_measured_in_utf8_bytes",
    ),
    pytest.param(
        100,
        {
            INPUT: [
                chat_message(
                    "user",
                    text_part(
                        "cost 5\u20ac \U0001f600 cost 5\u20ac \U0001f600 total: 10\u20ac\U0001f600 thanks, see you again next week! Bye for now."
                    ),
                )
            ]
        },
        {INPUT: [chat_message("user", text_part("cost 5\u20ac \U0001f600 cost 5\u20ac \U0001f600 total: 10\u20ac"))]},
        True,
        (148, 98),
        id="cut_lands_on_a_whole_character_in_multibyte_text",
    ),
]


def stream_events(*, index: object = 0) -> list[dict[str, Any]]:
    start: dict[str, Any] = {
        **MESSAGE,
        "content": [],
        "stop_reason": None,
        "usage": {**MESSAGE["usage"], "output_tokens": 0},
    }
    return [
        {"type": "message_start", "message": start},
        {"type": "content_block_start", "index": index, "content_block": {"type": "text", "text": ""}},
        {"type": "content_block_delta", "index": index, "delta": {"type": "text_delta", "text": "Hi there"}},
        {"type": "content_block_stop", "index": index},
        {"type": "message_delta", "delta": {"stop_reason": "end_turn"}, "usage": {"output_tokens": 5}},
        {"type": "message_stop"},
    ]


def stream_response(events: Sequence[dict[str, Any]] | None = None) -> httpx2.Response:
    body = sse(stream_events() if events is None else events)
    return httpx2.Response(200, content=body, headers={"content-type": "text/event-stream", **RESPONSE_HEADERS})


STREAM_ENDS = [
    pytest.param(stream_events(), StatusCode.OK, None, id="read to the end"),
    pytest.param(stream_events()[:3], StatusCode.ERROR, "api_error", id="ends before message_stop"),
    pytest.param([], StatusCode.ERROR, "api_error", id="ends before the first event"),
    pytest.param(
        [stream_events()[0], {"type": "error", "error": {"type": "overloaded_error", "message": "busy"}}],
        StatusCode.ERROR,
        "overloaded_error",
        id="error event",
    ),
]


class LostConnection(httpx2.SyncByteStream, httpx2.AsyncByteStream):
    """A response body whose connection is lost after the first chunk."""

    @override
    def __iter__(self) -> Iterator[bytes]:
        yield b"{"
        raise httpx2.ReadError("The connection was lost.")

    @override
    async def __aiter__(self) -> AsyncIterator[bytes]:
        yield b"{"
        raise httpx2.ReadError("The connection was lost.")


class StandInResponse:
    """What an application's test may give a stream in place of a response. It has no `stream`."""

    def iter_bytes(self) -> Iterator[bytes]:
        yield sse(stream_events())

    async def aiter_bytes(self) -> AsyncIterator[bytes]:
        yield sse(stream_events())

    def close(self) -> None:
        pass

    async def aclose(self) -> None:
        pass


@asynccontextmanager
async def serve_stream() -> AsyncIterator[str]:
    """Serves the `stream_events` to each request on a local port, and gives the base URL."""

    async def respond(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        await reader.readuntil(b"\r\n\r\n")
        body = sse(stream_events())
        writer.write(b"HTTP/1.1 200 OK\r\ncontent-type: text/event-stream\r\ntransfer-encoding: chunked\r\n\r\n")
        writer.write(b"%x\r\n%b\r\n0\r\n\r\n" % (len(body), body))
        await writer.drain()
        await reader.read()
        writer.close()

    server = await asyncio.start_server(respond, "127.0.0.1", 0)
    async with server:
        yield f"http://127.0.0.1:{server.sockets[0].getsockname()[1]}"


FIRST_DELTAS = [
    pytest.param({"type": "text", "text": ""}, {"type": "text_delta", "text": "Hi"}, id="text_delta"),
    pytest.param(
        {"type": "tool_use", "id": "toolu_1", "name": "get_weather", "input": {}},
        {"type": "input_json_delta", "partial_json": ""},
        id="input_json_delta",
    ),
    pytest.param(
        {"type": "thinking", "thinking": "", "signature": ""},
        {"type": "thinking_delta", "thinking": "Hm"},
        id="thinking_delta",
    ),
    pytest.param(
        {"type": "thinking", "thinking": "", "signature": ""},
        {"type": "signature_delta", "signature": "sig"},
        id="signature_delta",
    ),
]


def events_with_first_delta(content_block: dict[str, Any], delta: dict[str, Any]) -> list[dict[str, Any]]:
    """The events of `stream_events` with `delta`, twice, as the deltas of `content_block`, and a `ping` before them."""
    start, block_start, block_delta, *rest = stream_events()
    first_delta = {**block_delta, "delta": delta}
    return [start, {"type": "ping"}, {**block_start, "content_block": content_block}, first_delta, first_delta, *rest]


class StartedSpans(SpanProcessor):
    """Keeps each span from its start, so that a test can read the attributes of one that has not ended."""

    def __init__(self) -> None:
        self.spans: list[SdkSpan] = []

    @override
    def on_start(self, span: SdkSpan, parent_context: context.Context | None = None) -> None:
        self.spans.append(span)


def assert_time_to_first_chunk_is_set_at_the_first_delta(
    times: list[tuple[str, float | None]], span: ReadableSpan
) -> None:
    """`times` has the type of each event that the application read, and the span's time to first chunk then."""
    assert [event_type for event_type, time in times if time is None] == ["message_start", "content_block_start"]
    # The second delta and the events after it left the time of the first.
    [time_to_first_chunk] = {time for _, time in times[2:]}
    assert attributes(span)["gen_ai.response.time_to_first_chunk"] == time_to_first_chunk


def events_without_a_delta() -> list[dict[str, Any]]:
    """The events of `stream_events`, with the text block whole in its `content_block_start`."""
    start, block_start, _, *rest = stream_events()
    return [start, {**block_start, "content_block": {"type": "text", "text": "Hi there"}}, *rest]


def iteration(
    type: str, input_tokens: int = 10, output_tokens: int = 5, cache_read: int = 0, cache_creation: int = 0
) -> dict[str, Any]:
    """An entry of a response's `usage.iterations`."""
    return {
        "type": type,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_read_input_tokens": cache_read,
        "cache_creation_input_tokens": cache_creation,
    }


def message_with(iterations: list[dict[str, Any]] | None) -> dict[str, Any]:
    """`MESSAGE` with `iterations` in its usage."""
    return {**MESSAGE, "usage": {**MESSAGE["usage"], "iterations": iterations}}


REQUEST: dict[str, Any] = {
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello"}],
    "model": "claude-test",
}


def messages_resource(client: Any, *, beta: bool) -> Any:
    return client.beta.messages if beta else client.messages


def tool_stream_events() -> list[dict[str, Any]]:
    """The events of `stream_events`, with a `tool_use` block after the text."""
    events = stream_events()
    events[4:4] = [
        {
            "type": "content_block_start",
            "index": 1,
            "content_block": {"type": "tool_use", "id": "toolu_1", "name": "get_weather", "input": {}},
        },
        {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": '{"city": '}},
        {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": '"SF"}'}},
        {"type": "content_block_stop", "index": 1},
    ]
    return events


TOOL_STREAM_OUTPUT: list[dict[str, Any]] = [
    {
        "role": "assistant",
        "parts": [
            {"type": "text", "content": "Hi there"},
            {"type": "tool_call", "id": "toolu_1", "name": "get_weather", "arguments": {"city": "SF"}},
        ],
    }
]


def cut_tool_stream_events() -> list[dict[str, Any]]:
    """The events of `tool_stream_events` up to a delta that leaves the input of its `tool_use` block open."""
    delta = {"type": "input_json_delta", "partial_json": '{"city": "SF", "days": '}
    return [*tool_stream_events()[:5], {"type": "content_block_delta", "index": 1, "delta": delta}]


# The events of a stream that ends before `message_stop`, and the parts that a stream helper has accumulated by then.
CUT_STREAMS = [
    pytest.param(stream_events()[:3], [{"type": "text", "content": "Hi there"}], id="after_a_text_delta"),
    pytest.param(
        cut_tool_stream_events(),
        [
            {"type": "text", "content": "Hi there"},
            {"type": "tool_call", "id": "toolu_1", "name": "get_weather", "arguments": {"city": "SF"}},
        ],
        id="inside_a_tool_use_block",
    ),
]

STREAM_ERROR_EVENT: dict[str, Any] = {"type": "error", "error": {"type": "overloaded_error", "message": "busy"}}


def fallback_stream_events() -> list[dict[str, Any]]:
    """The events of `stream_events`, after a `fallback` block: another model serves the rest of the response."""
    fallback = {
        "type": "fallback",
        "from": {"model": "claude-test"},
        "to": {"model": "claude-fallback"},
        "trigger": {"type": "refusal", "category": None},
    }
    start, *rest = stream_events(index=1)
    return [
        start,
        {"type": "content_block_start", "index": 0, "content_block": fallback},
        {"type": "content_block_stop", "index": 0},
        *rest,
    ]


def count_accumulated_events(monkeypatch: pytest.MonkeyPatch, *, beta: bool) -> list[str]:
    """Wraps the stable or the beta `accumulate_event`, which the stream helpers and the spans share, so that
    the type of each event it takes is added to the list returned.
    """
    module = _beta_messages if beta else _messages
    accumulate_event = module.accumulate_event
    accumulated: list[str] = []

    def counting(**kwargs: Any) -> Any:
        accumulated.append(kwargs["event"].type)
        return accumulate_event(**kwargs)

    monkeypatch.setattr(module, "accumulate_event", counting)
    return accumulated


def events_up_to_message_delta() -> list[dict[str, Any]]:
    """The events of a stream that ends before `message_stop`, whose `message_delta` has all that one can have."""
    *events, message_delta, _message_stop = stream_events()
    usage = {
        "output_tokens": 5,
        "output_tokens_details": {"thinking_tokens": 3},
        "iterations": [iteration("compaction", 100, 20, 10)],
    }
    return [*events, {**message_delta, "usage": usage}]


def assert_span_has_what_message_delta_gave(span: ReadableSpan, *, beta: bool) -> None:
    # The stream still ended early, which fails the span as before.
    assert span.status.status_code == StatusCode.ERROR
    assert attributes(span)["error.type"] == "api_error"
    assert attributes(span)["anthropic.message.stop_reason"] == "end_turn"
    assert attributes(span)["gen_ai.usage.output_tokens"] == 5
    assert attributes(span)["gen_ai.usage.reasoning.output_tokens"] == 3
    # Only the beta usage has the iterations.
    compaction = {
        key: value for key, value in attributes(span).items() if key.startswith("anthropic.usage.compaction.")
    }
    assert compaction == (
        {"anthropic.usage.compaction.input_tokens": 110, "anthropic.usage.compaction.output_tokens": 20} if beta else {}
    )


def assert_span_has_nothing_that_message_delta_gives(span: ReadableSpan) -> None:
    assert span.status.status_code == StatusCode.ERROR
    assert attributes(span)["error.type"] == "api_error"
    assert attributes(span)["gen_ai.response.id"] == "msg_1"
    assert attributes(span)["gen_ai.usage.input_tokens"] == 15
    for name in (
        "anthropic.message.stop_reason",
        "gen_ai.usage.output_tokens",
        "gen_ai.usage.reasoning.output_tokens",
        "anthropic.usage.compaction.input_tokens",
        "anthropic.usage.compaction.output_tokens",
    ):
        assert name not in attributes(span)


class TestCallSpans:
    @pytest.mark.respx(base_url=base_url)
    def test_unary_attributes(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE, headers=RESPONSE_HEADERS))
        client = make_client(spans, open_telemetry=spans.option(conversation_id="conv_1"))

        tracer = spans.provider.get_tracer("app")
        with tracer.start_as_current_span("app") as app:
            create(
                client,
                output_config={"effort": "high"},
                service_tier="auto",
                thinking={"type": "enabled", "budget_tokens": 2048},
                extra_headers={"anthropic-beta": "beta-one, beta-two"},
            )

        span = spans.one("anthropic.messages.create")
        assert span.kind == SpanKind.CLIENT
        assert span.status.status_code == StatusCode.OK
        assert parent_id(span) == span_id(app)
        assert span.instrumentation_scope is not None
        assert span.instrumentation_scope.name == "com.anthropic.sdk.python"
        assert span.instrumentation_scope.version == client._version
        assert attributes(span) == {
            "gen_ai.provider.name": "anthropic",
            "gen_ai.conversation.id": "conv_1",
            "gen_ai.operation.name": "chat",
            "gen_ai.request.model": "claude-test",
            "gen_ai.request.max_tokens": 1024,
            "gen_ai.request.reasoning.level": "high",
            "anthropic.request.service_tier": "auto",
            "anthropic.thinking.type": "enabled",
            "anthropic.thinking.budget_tokens": 2048,
            "anthropic.beta": ("beta-one", "beta-two"),
            "server.address": "127.0.0.1",
            "server.port": 4010,
            "http.request.method": "POST",
            "http.route": "/v1/messages",
            "url.scheme": "http",
            "url.path": "/v1/messages",
            "url.full": "http://127.0.0.1:4010/v1/messages",
            "http.response.status_code": 200,
            "anthropic.request.id": "req_1",
            "anthropic.organization.id": "org_1",
            "anthropic.workspace.id": "wrkspc_1",
            "gen_ai.response.id": "msg_1",
            "gen_ai.response.model": "claude-test",
            "gen_ai.usage.input_tokens": 15,
            "gen_ai.usage.output_tokens": 5,
            "gen_ai.usage.cache_write.input_tokens": 3,
            "gen_ai.usage.cache_read.input_tokens": 2,
            "anthropic.usage.cache_creation.ephemeral_5m_input_tokens": 1,
            "anthropic.usage.cache_creation.ephemeral_1h_input_tokens": 2,
            "anthropic.response.service_tier": "standard",
            "anthropic.message.stop_reason": "end_turn",
        }
        assert "gen_ai.input.messages" not in attributes(span)

    @pytest.mark.respx(base_url=base_url)
    def test_temperature_and_top_p_are_doubles(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        client = make_client(spans)

        create(client, extra_body={"temperature": 1, "top_p": 1})

        span = spans.one("anthropic.messages.create")
        # An exporter sends an `int` as an integer, and these two attributes are doubles.
        assert isinstance(attributes(span)["gen_ai.request.temperature"], float)
        assert isinstance(attributes(span)["gen_ai.request.top_p"], float)
        assert attributes(span)["gen_ai.request.temperature"] == 1.0
        assert attributes(span)["gen_ai.request.top_p"] == 1.0

    @pytest.mark.respx(base_url=base_url)
    def test_error_response(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx2.Response(
                429,
                json={"type": "error", "error": {"type": "rate_limit_error", "message": "slow down"}},
                headers=RESPONSE_HEADERS,
            )
        )
        client = make_client(spans, max_retries=0)

        with pytest.raises(RateLimitError):
            create(client)

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.ERROR
        assert attributes(span)["error.type"] == "rate_limit_error"
        assert attributes(span)["http.response.status_code"] == 429
        assert attributes(span)["anthropic.request.id"] == "req_1"
        assert "gen_ai.response.id" not in attributes(span)
        assert "anthropic.message.stop_reason" not in attributes(span)

    @pytest.mark.respx(base_url=base_url)
    def test_error_response_without_envelope(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(502, text="bad gateway"))
        client = make_client(spans, max_retries=0)

        with pytest.raises(APIStatusError):
            create(client)

        assert attributes(spans.one("anthropic.messages.create"))["error.type"] == "502"

    def test_request_body_that_cannot_be_prepared_has_no_span(self, spans: Spans, tmp_path: pathlib.Path) -> None:
        client = make_client(spans)

        # The body is prepared before the span starts, for every endpoint.
        with pytest.raises(FileNotFoundError):
            client.messages.batches.create(requests=requests_with_file(tmp_path / "missing.png"))

        assert not spans.finished

    async def test_async_request_body_that_cannot_be_prepared_has_no_span(
        self, spans: Spans, tmp_path: pathlib.Path
    ) -> None:
        client = make_async_client(spans)

        with pytest.raises(FileNotFoundError):
            await client.messages.batches.create(requests=requests_with_file(tmp_path / "missing.png"))

        assert not spans.finished

    @pytest.mark.respx(base_url=base_url)
    def test_connection_error(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=httpx2.ConnectError("refused"))
        client = make_client(spans, max_retries=0)

        with pytest.raises(APIConnectionError):
            create(client)

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.ERROR
        assert attributes(span)["error.type"] == "connection_error"
        assert attributes(span)["server.address"] == "127.0.0.1"
        assert attributes(span)["server.port"] == 4010
        assert "http.response.status_code" not in attributes(span)

    @pytest.mark.respx(base_url=base_url)
    def test_timeout(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=httpx2.ReadTimeout("timeout"))
        client = make_client(spans, max_retries=0)

        with pytest.raises(APITimeoutError):
            create(client)

        assert attributes(spans.one("anthropic.messages.create"))["error.type"] == "client_timeout_error"

    @pytest.mark.respx(base_url=base_url)
    def test_a_retried_call_has_one_span(self, spans: Spans, respx_mock: MockRouter) -> None:
        overloaded = {"type": "error", "error": {"type": "overloaded_error", "message": "busy"}}
        route = respx_mock.post("/v1/messages").mock(
            side_effect=[
                httpx2.Response(529, json=overloaded),
                httpx2.Response(529, json=overloaded),
                httpx2.Response(200, json=MESSAGE),
            ]
        )
        client = make_client(spans, max_retries=2)

        with update_env(ANTHROPIC_LOG="info"):
            client = client.with_options(max_retries=2)
            client._calculate_retry_timeout = lambda *_args, **_kwargs: 0.0  # type: ignore[method-assign]
            create(client)

        # The SDK emits no span for an attempt, so the call span, with the final attempt's status, is the only one.
        [call] = spans.finished
        assert call.name == "anthropic.messages.create"
        assert call.status.status_code == StatusCode.OK
        assert attributes(call)["http.response.status_code"] == 200
        context = "00-{:032x}-{:016x}-".format(trace_id(call), span_id(call))
        assert [request.headers["traceparent"][: len(context)] for request in requests(route)] == [context] * 3

    @pytest.mark.respx(base_url=base_url)
    def test_time_to_first_chunk_counts_from_the_first_attempt(self, spans: Spans, respx_mock: MockRouter) -> None:
        overloaded = {"type": "error", "error": {"type": "overloaded_error", "message": "busy"}}
        respx_mock.post("/v1/messages").mock(side_effect=[httpx2.Response(529, json=overloaded), stream_response()])
        client = make_client(spans, max_retries=1)
        client._calculate_retry_timeout = lambda *_args, **_kwargs: 0.2  # type: ignore[method-assign]

        for _ in create(client, stream=True):
            pass

        span = spans.one("anthropic.messages.create")
        assert attributes(span)["gen_ai.response.time_to_first_chunk"] >= 0.2

    @pytest.mark.respx(base_url=base_url)
    def test_batch_results_span_covers_the_download(self, spans: Spans, respx_mock: MockRouter) -> None:
        batch = {"results_url": "/v1/messages/batches/msgbatch_1/results"}
        lines = [json.dumps({"custom_id": str(i), "result": {"type": "expired"}}) for i in range(3)]
        respx_mock.get("/v1/messages/batches/msgbatch_1").mock(return_value=httpx2.Response(200, json=batch))
        respx_mock.get("/v1/messages/batches/msgbatch_1/results").mock(
            side_effect=[httpx2.Response(200, content="\n".join(lines), headers=RESPONSE_HEADERS) for _ in range(3)]
        )
        client = make_client(spans, _strict_response_validation=False)

        results = client.messages.batches.results("msgbatch_1")
        assert spans.named("anthropic.messages.batches.results") == []
        assert [result.custom_id for result in results] == ["0", "1", "2"]
        span = spans.one("anthropic.messages.batches.results")
        assert span.status.status_code == StatusCode.OK
        assert attributes(span)["anthropic.message.batch.id"] == "msgbatch_1"
        assert attributes(span)["anthropic.request.id"] == "req_1"

        results = client.messages.batches.results("msgbatch_1")
        assert next(results).custom_id == "0"
        results.close()
        assert spans.named("anthropic.messages.batches.results")[1].status.status_code == StatusCode.UNSET

        client.messages.batches.results("msgbatch_1").close()
        assert spans.named("anthropic.messages.batches.results")[2].status.status_code == StatusCode.UNSET

    @pytest.mark.respx(base_url=base_url)
    def test_batch_results_download_failure_fails_the_span(self, spans: Spans, respx_mock: MockRouter) -> None:
        class Dropped(httpx2.SyncByteStream):
            @override
            def __iter__(self) -> Iterator[bytes]:
                yield json.dumps({"custom_id": "0", "result": {"type": "expired"}}).encode() + b"\n"
                raise httpx2.ReadError("connection dropped")

        batch = {"results_url": "/v1/messages/batches/msgbatch_1/results"}
        respx_mock.get("/v1/messages/batches/msgbatch_1").mock(return_value=httpx2.Response(200, json=batch))
        respx_mock.get("/v1/messages/batches/msgbatch_1/results").mock(
            return_value=httpx2.Response(200, stream=Dropped())
        )
        client = make_client(spans, _strict_response_validation=False)

        results = client.messages.batches.results("msgbatch_1")
        with pytest.raises(httpx2.ReadError):
            for _ in results:
                pass

        span = spans.one("anthropic.messages.batches.results")
        assert span.status.status_code == StatusCode.ERROR
        assert attributes(span)["error.type"] == "connection_error"

    @pytest.mark.respx(base_url=base_url)
    async def test_async_batch_results_span_covers_the_download(self, spans: Spans, respx_mock: MockRouter) -> None:
        batch = {"results_url": "/v1/messages/batches/msgbatch_1/results"}
        lines = [json.dumps({"custom_id": str(i), "result": {"type": "expired"}}) for i in range(3)]
        respx_mock.get("/v1/messages/batches/msgbatch_1").mock(return_value=httpx2.Response(200, json=batch))
        respx_mock.get("/v1/messages/batches/msgbatch_1/results").mock(
            side_effect=[httpx2.Response(200, content="\n".join(lines)) for _ in range(2)]
        )
        client = make_async_client(spans, _strict_response_validation=False)

        results = await client.messages.batches.results("msgbatch_1")
        assert spans.named("anthropic.messages.batches.results") == []
        assert [result.custom_id async for result in results] == ["0", "1", "2"]
        assert spans.one("anthropic.messages.batches.results").status.status_code == StatusCode.OK

        results = await client.messages.batches.results("msgbatch_1")
        await results.close()
        closed = spans.named("anthropic.messages.batches.results")[1]
        assert closed.status.status_code == StatusCode.UNSET
        assert closed.end_time is not None

    @pytest.mark.respx(base_url=base_url)
    def test_a_failure_to_record_attributes_does_not_fail_the_api_call(
        self, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE, headers=RESPONSE_HEADERS))

        def fail(*_args: object) -> None:
            raise RuntimeError("cannot record")

        monkeypatch.setattr("anthropic.lib._tracing._api_call.record_messages_create", fail)

        message = make_client(spans).messages.create(
            max_tokens=1024, messages=[{"role": "user", "content": "Hello"}], model="claude-test"
        )

        assert message.id == "msg_1"
        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.OK
        assert attributes(span)["http.response.status_code"] == 200
        assert attributes(span)["gen_ai.provider.name"] == "anthropic"

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_ends_the_span_with_its_body(
        self, spans: Spans, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE, headers=RESPONSE_HEADERS))
        client = make_client(spans)

        with caplog.at_level(logging.WARNING, logger="opentelemetry"):
            with create(client.with_streaming_response) as response:
                assert not spans.finished
                assert response.parse().id == "msg_1"
                spans.one("anthropic.messages.create")
            assert create(client.with_raw_response).parse().id == "msg_1"

        assert [record.message for record in caplog.records if record.name.startswith("opentelemetry")] == []
        streamed, raw = spans.named("anthropic.messages.create")
        for span in (streamed, raw):
            assert span.status.status_code == StatusCode.OK
            assert attributes(span)["http.response.status_code"] == 200
            assert attributes(span)["anthropic.request.id"] == "req_1"
            assert attributes(span)["gen_ai.request.model"] == "claude-test"
        assert "gen_ai.usage.output_tokens" not in attributes(streamed)
        # `.with_raw_response` has read the body when the call returns, so its span has the response's attributes.
        assert attributes(raw)["gen_ai.usage.output_tokens"] == 5
        assert attributes(raw)["gen_ai.response.id"] == "msg_1"

    @pytest.mark.respx(base_url=base_url)
    async def test_async_raw_response_ends_the_span_with_its_body(
        self, spans: Spans, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE, headers=RESPONSE_HEADERS))
        client = make_async_client(spans)

        with caplog.at_level(logging.WARNING, logger="opentelemetry"):
            async with create(client.with_streaming_response) as response:
                assert not spans.finished
                assert (await response.parse()).id == "msg_1"
                span = spans.one("anthropic.messages.create")
            raw = await create(client.with_raw_response)
            assert (await raw.parse()).id == "msg_1"

        assert [record.message for record in caplog.records if record.name.startswith("opentelemetry")] == []
        assert span.status.status_code == StatusCode.OK
        assert attributes(span)["anthropic.request.id"] == "req_1"
        assert "gen_ai.usage.output_tokens" not in attributes(span)
        assert attributes(spans.named("anthropic.messages.create")[1])["gen_ai.usage.output_tokens"] == 5

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_whose_body_is_not_read_to_the_end_has_no_status(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=MESSAGE, headers=RESPONSE_HEADERS), stream_response()]
        )
        client = make_client(spans)

        with create(client.with_streaming_response) as response:
            assert response.headers["request-id"] == "req_1"
        closed = spans.one("anthropic.messages.create")
        raw = create(client.with_raw_response, stream=True)
        assert len(spans.finished) == 1
        del raw
        gc.collect()

        _, dropped = spans.named("anthropic.messages.create")
        for span in (closed, dropped):
            assert span.status.status_code == StatusCode.UNSET
            assert "error.type" not in attributes(span)
            assert attributes(span)["anthropic.request.id"] == "req_1"

    @pytest.mark.respx(base_url=base_url)
    async def test_async_raw_response_whose_body_is_not_read_to_the_end_has_no_status(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=MESSAGE, headers=RESPONSE_HEADERS), stream_response()]
        )
        client = make_async_client(spans)

        async with create(client.with_streaming_response) as response:
            assert response.headers["request-id"] == "req_1"
        closed = spans.one("anthropic.messages.create")
        raw = await create(client.with_raw_response, stream=True)
        assert len(spans.finished) == 1
        del raw
        gc.collect()

        _, dropped = spans.named("anthropic.messages.create")
        for span in (closed, dropped):
            assert span.status.status_code == StatusCode.UNSET
            assert "error.type" not in attributes(span)
            assert attributes(span)["anthropic.request.id"] == "req_1"

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.parametrize(("events", "status", "error_type"), STREAM_ENDS)
    @pytest.mark.respx(base_url=base_url)
    def test_stream_parsed_from_a_raw_response_is_recorded_like_a_stream(
        self,
        spans: Spans,
        respx_mock: MockRouter,
        events: list[dict[str, Any]],
        status: StatusCode,
        error_type: str | None,
        beta: bool,
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[stream_response(events) for _ in range(2)])
        messages = messages_resource(make_client(spans), beta=beta)

        for finished, stream in enumerate(
            (
                messages.create(**REQUEST, stream=True),
                messages.with_raw_response.create(**REQUEST, stream=True).parse(),
            )
        ):
            assert len(spans.finished) == finished
            try:
                for _ in stream:
                    pass
            except APIStatusError:
                assert error_type == "overloaded_error"

        plain, raw = spans.named("anthropic.messages.create")
        assert raw.status.status_code == plain.status.status_code == status
        assert attributes(raw).get("error.type") == attributes(plain).get("error.type") == error_type
        response_id = "msg_1" if events else None
        assert attributes(raw).get("gen_ai.response.id") == attributes(plain).get("gen_ai.response.id") == response_id
        assert attributes(raw).get("gen_ai.usage.output_tokens") == attributes(plain).get("gen_ai.usage.output_tokens")

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.parametrize(("events", "status", "error_type"), STREAM_ENDS)
    @pytest.mark.respx(base_url=base_url)
    async def test_async_stream_parsed_from_a_raw_response_is_recorded_like_a_stream(
        self,
        spans: Spans,
        respx_mock: MockRouter,
        events: list[dict[str, Any]],
        status: StatusCode,
        error_type: str | None,
        beta: bool,
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[stream_response(events) for _ in range(2)])
        messages = messages_resource(make_async_client(spans), beta=beta)

        for finished, stream in enumerate(
            (
                await messages.create(**REQUEST, stream=True),
                await (await messages.with_raw_response.create(**REQUEST, stream=True)).parse(),
            )
        ):
            assert len(spans.finished) == finished
            try:
                async for _ in stream:
                    pass
            except APIStatusError:
                assert error_type == "overloaded_error"

        plain, raw = spans.named("anthropic.messages.create")
        assert raw.status.status_code == plain.status.status_code == status
        assert attributes(raw).get("error.type") == attributes(plain).get("error.type") == error_type
        response_id = "msg_1" if events else None
        assert attributes(raw).get("gen_ai.response.id") == attributes(plain).get("gen_ai.response.id") == response_id
        assert attributes(raw).get("gen_ai.usage.output_tokens") == attributes(plain).get("gen_ai.usage.output_tokens")

    @pytest.mark.parametrize(("events", "status", "error_type"), STREAM_ENDS)
    def test_stream_over_a_body_that_was_read_before_the_call_returned(
        self, spans: Spans, events: list[dict[str, Any]], status: StatusCode, error_type: str | None
    ) -> None:
        # A response that is made from bytes is closed from the start, as is one that a middleware has read.
        transport = httpx2.MockTransport(lambda _: stream_response(events))
        client = make_client(spans, http_client=httpx2.Client(transport=transport))

        stream = create(client, stream=True)
        assert stream.response.is_closed
        assert not spans.finished
        try:
            for _ in stream:
                pass
        except APIStatusError:
            assert error_type == "overloaded_error"

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == status
        assert attributes(span).get("error.type") == error_type
        assert attributes(span).get("gen_ai.response.id") == ("msg_1" if events else None)

    @pytest.mark.parametrize(("events", "status", "error_type"), STREAM_ENDS)
    async def test_async_stream_over_a_body_that_was_read_before_the_call_returned(
        self, spans: Spans, events: list[dict[str, Any]], status: StatusCode, error_type: str | None
    ) -> None:
        transport = httpx2.MockTransport(lambda _: stream_response(events))
        client = make_async_client(spans, http_client=httpx2.AsyncClient(transport=transport))

        stream = await create(client, stream=True)
        assert stream.response.is_closed
        assert not spans.finished
        try:
            async for _ in stream:
                pass
        except APIStatusError:
            assert error_type == "overloaded_error"

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == status
        assert attributes(span).get("error.type") == error_type
        assert attributes(span).get("gen_ai.response.id") == ("msg_1" if events else None)

    def test_stream_over_a_body_that_was_read_is_closed_or_read_with_the_helper(self, spans: Spans) -> None:
        transport = httpx2.MockTransport(lambda _: stream_response())
        client = make_client(spans, http_client=httpx2.Client(transport=transport))

        stream = create(client, stream=True)
        next(stream)
        assert not spans.finished
        stream.close()
        closed = spans.one("anthropic.messages.create")
        with client.messages.stream(**REQUEST) as helper:
            helper.until_done()

        assert closed.status.status_code == StatusCode.UNSET
        _, read = spans.named("anthropic.messages.create")
        assert read.status.status_code == StatusCode.OK
        assert attributes(read)["gen_ai.usage.output_tokens"] == 5

    async def test_async_stream_over_a_body_that_was_read_is_closed_or_read_with_the_helper(self, spans: Spans) -> None:
        transport = httpx2.MockTransport(lambda _: stream_response())
        client = make_async_client(spans, http_client=httpx2.AsyncClient(transport=transport))

        stream = await create(client, stream=True)
        await stream.__anext__()
        assert not spans.finished
        await stream.close()
        closed = spans.one("anthropic.messages.create")
        async with client.messages.stream(**REQUEST) as helper:
            await helper.until_done()

        assert closed.status.status_code == StatusCode.UNSET
        _, read = spans.named("anthropic.messages.create")
        assert read.status.status_code == StatusCode.OK
        assert attributes(read)["gen_ai.usage.output_tokens"] == 5

    def test_stream_over_a_response_that_a_middleware_made_from_bytes(self, spans: Spans) -> None:
        def replay(request: Any, call_next: Callable[[Any], Any]) -> Any:
            sent = call_next(request)
            sent.close()
            # The body of a response that is made from bytes is a sync and an async one at once.
            raw = stream_response()
            return APIResponse(
                raw=raw,
                cast_to=request.cast_to,
                client=client,
                stream=True,
                stream_cls=request.stream_cls,
                options=request.options,
            )

        transport = httpx2.MockTransport(lambda _: stream_response())
        client = make_client(spans, http_client=httpx2.Client(transport=transport), middleware=[replay])

        for _ in create(client, stream=True):
            pass
        stream = create(client, stream=True)
        next(stream)
        stream.close()

        read, closed = spans.named("anthropic.messages.create")
        assert read.status.status_code == StatusCode.OK
        assert attributes(read)["gen_ai.usage.output_tokens"] == 5
        assert closed.status.status_code == StatusCode.UNSET

    async def test_async_stream_over_a_response_that_a_middleware_made_from_bytes(self, spans: Spans) -> None:
        async def replay(request: Any, call_next: Callable[[Any], Any]) -> Any:
            sent = await call_next(request)
            await sent.close()
            raw = stream_response()
            return AsyncAPIResponse(
                raw=raw,
                cast_to=request.cast_to,
                client=client,
                stream=True,
                stream_cls=request.stream_cls,
                options=request.options,
            )

        transport = httpx2.MockTransport(lambda _: stream_response())
        client = make_async_client(spans, http_client=httpx2.AsyncClient(transport=transport), middleware=[replay])

        async for _ in await create(client, stream=True):
            pass
        stream = await create(client, stream=True)
        await stream.__anext__()
        await stream.close()

        read, closed = spans.named("anthropic.messages.create")
        assert read.status.status_code == StatusCode.OK
        assert attributes(read)["gen_ai.usage.output_tokens"] == 5
        assert closed.status.status_code == StatusCode.UNSET

    @pytest.mark.respx(base_url=base_url)
    def test_events_read_after_the_response_was_closed_leave_the_span_alone(
        self, spans: Spans, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response())
        client = make_client(spans)

        with caplog.at_level(logging.WARNING, logger="opentelemetry"):
            raw = create(client.with_raw_response, stream=True)
            stream = raw.parse()
            next(stream)
            raw.http_response.close()
            for _ in stream:
                pass

        assert spans.one("anthropic.messages.create").status.status_code == StatusCode.UNSET
        assert [record.message for record in caplog.records if record.name.startswith("opentelemetry")] == []

    @pytest.mark.respx(base_url=base_url)
    async def test_async_events_read_after_the_response_was_closed_leave_the_span_alone(
        self, spans: Spans, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response())
        client = make_async_client(spans)

        with caplog.at_level(logging.WARNING, logger="opentelemetry"):
            raw = await create(client.with_raw_response, stream=True)
            stream = await raw.parse()
            await stream.__anext__()
            await raw.http_response.aclose()
            async for _ in stream:
                pass

        assert spans.one("anthropic.messages.create").status.status_code == StatusCode.UNSET
        assert [record.message for record in caplog.records if record.name.startswith("opentelemetry")] == []

    @pytest.mark.respx(base_url=base_url)
    async def test_a_body_read_the_wrong_way_can_still_be_read_the_right_way(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[stream_response() for _ in range(2)])

        stream = create(make_client(spans), stream=True)
        for wrong in (stream.response.aread, stream.response.aclose):
            with pytest.raises(RuntimeError):
                await wrong()
        assert len(list(stream)) == len(stream_events())
        async_stream = await create(make_async_client(spans), stream=True)
        for async_wrong in (async_stream.response.read, async_stream.response.close):
            with pytest.raises(RuntimeError):
                async_wrong()
        assert len([event async for event in async_stream]) == len(stream_events())

        assert [span.status.status_code for span in spans.finished] == [StatusCode.OK, StatusCode.OK]

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_whose_events_the_application_reads_itself(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(stream_events()[:3]))
        client = make_client(spans)

        with create(client.with_streaming_response, stream=True) as response:
            assert len(list(response.iter_lines())) > 0

        # The SDK has not parsed the events, so it cannot tell that `message_stop` is missing.
        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.OK
        assert "gen_ai.response.id" not in attributes(span)

    @pytest.mark.respx(base_url=base_url)
    async def test_async_raw_response_whose_events_the_application_reads_itself(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(stream_events()[:3]))
        client = make_async_client(spans)

        async with create(client.with_streaming_response, stream=True) as response:
            assert len([line async for line in response.iter_lines()]) > 0

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.OK
        assert "gen_ai.response.id" not in attributes(span)

    @pytest.mark.respx(base_url=base_url)
    def test_stream_whose_bytes_the_application_reads_itself(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(stream_events()[:3]))
        client = make_client(spans)

        stream = create(client, stream=True)
        assert len(list(stream.response.iter_bytes())) > 0

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.OK
        assert "error.type" not in attributes(span)

    @pytest.mark.respx(base_url=base_url)
    async def test_async_stream_whose_bytes_the_application_reads_itself(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(stream_events()[:3]))
        client = make_async_client(spans)

        stream = await create(client, stream=True)
        assert len([chunk async for chunk in stream.response.aiter_bytes()]) > 0

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.OK
        assert "error.type" not in attributes(span)

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_whose_connection_is_lost_in_the_body(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx2.Response(200, stream=LostConnection(), headers=RESPONSE_HEADERS)
        )
        client = make_client(spans)

        with create(client.with_streaming_response) as response:
            with pytest.raises(httpx2.ReadError):
                response.read()

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.ERROR
        assert attributes(span)["error.type"] == "connection_error"

    @pytest.mark.respx(base_url=base_url)
    async def test_async_raw_response_whose_connection_is_lost_in_the_body(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx2.Response(200, stream=LostConnection(), headers=RESPONSE_HEADERS)
        )
        client = make_async_client(spans)

        async with create(client.with_streaming_response) as response:
            with pytest.raises(httpx2.ReadError):
                await response.read()

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.ERROR
        assert attributes(span)["error.type"] == "connection_error"

    @pytest.mark.respx(base_url=base_url)
    def test_elapsed_of_a_response_whose_body_ends_the_span(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response())
        client = make_client(spans)

        stream = create(client, stream=True)
        for _ in stream:
            pass

        assert stream.response.elapsed.total_seconds() >= 0

    @pytest.mark.respx(base_url=base_url)
    async def test_async_elapsed_of_a_response_whose_body_ends_the_span(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response())
        client = make_async_client(spans)

        stream = await create(client, stream=True)
        async for _ in stream:
            pass

        assert stream.response.elapsed.total_seconds() >= 0

    @pytest.mark.parametrize("reads", [0, 2], ids=["never read", "read in part"])
    @pytest.mark.respx(base_url=base_url)
    def test_dropped_stream(self, spans: Spans, respx_mock: MockRouter, reads: int) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response())
        client = make_client(spans)

        stream = create(client, stream=True)
        for _ in range(reads):
            next(stream)
        assert not spans.finished
        del stream
        gc.collect()

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.UNSET
        assert "error.type" not in attributes(span)
        assert attributes(span).get("gen_ai.response.id") == ("msg_1" if reads else None)

    @pytest.mark.parametrize("reads", [0, 2], ids=["never read", "read in part"])
    async def test_async_dropped_stream(self, spans: Spans, caplog: pytest.LogCaptureFixture, reads: int) -> None:
        # Over a real connection, where closing the response waits: the event loop closes the generators that read
        # a dropped stream each in a task of its own, and logs what one of them raises.
        async with serve_stream() as url:
            async with make_async_client(spans, base_url=url) as client:
                stream = await create(client, stream=True)
                for _ in range(reads):
                    await stream.__anext__()
                assert not spans.finished
                del stream
                gc.collect()
                for _ in range(10):
                    await asyncio.sleep(0)

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.UNSET
        assert "error.type" not in attributes(span)
        assert attributes(span).get("gen_ai.response.id") == ("msg_1" if reads else None)
        assert [record.getMessage() for record in caplog.records if record.name == "asyncio"] == []

    @pytest.mark.respx(base_url=base_url)
    def test_trace_context_headers(self, spans: Spans, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        client = make_client(spans)

        parent = trace.NonRecordingSpan(
            trace.SpanContext(
                trace_id=0x1234,
                span_id=0x5678,
                is_remote=True,
                trace_flags=trace.TraceFlags(trace.TraceFlags.SAMPLED),
                trace_state=trace.TraceState([("vendor", "value")]),
            )
        )
        token = context.attach(trace.set_span_in_context(parent))
        try:
            create(client)
        finally:
            context.detach(token)

        request = requests(route)[0]
        call = spans.one("anthropic.messages.create")
        assert request.headers["traceparent"] == "00-{:032x}-{:016x}-01".format(0x1234, span_id(call))
        assert request.headers["tracestate"] == "vendor=value"
        assert trace_id(call) == 0x1234

    @pytest.mark.respx(base_url=base_url)
    def test_stream_read_to_the_end(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response())
        client = make_client(spans)

        with client.messages.stream(
            max_tokens=1024, messages=[{"role": "user", "content": "Hello"}], model="claude-test"
        ) as stream:
            message = stream.get_final_message()
        assert message.content[0].type == "text"

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.OK
        assert attributes(span)["gen_ai.request.stream"] is True
        assert attributes(span)["gen_ai.response.id"] == "msg_1"
        assert attributes(span)["gen_ai.usage.output_tokens"] == 5
        assert attributes(span)["anthropic.message.stop_reason"] == "end_turn"
        assert attributes(span)["anthropic.response.service_tier"] == "standard"
        assert isinstance(attributes(span)["gen_ai.response.time_to_first_chunk"], float)

    @pytest.mark.respx(base_url=base_url)
    def test_stream_closed_early(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response())
        client = make_client(spans)

        stream = create(client, stream=True)
        event = next(iter(stream))
        assert event.type == "message_start"
        stream.close()

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.UNSET
        assert "error.type" not in attributes(span)
        assert attributes(span)["gen_ai.response.id"] == "msg_1"
        assert attributes(span)["anthropic.response.service_tier"] == "standard"
        assert attributes(span)["gen_ai.usage.input_tokens"] == 15
        assert "gen_ai.usage.output_tokens" not in attributes(span)
        assert "anthropic.message.stop_reason" not in attributes(span)
        assert "gen_ai.response.time_to_first_chunk" not in attributes(span)

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_stream_closed_after_message_stop_before_the_end_of_the_body(
        self, beta: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[stream_response(), stream_response()])
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        stream = messages_resource(client, beta=beta).create(**REQUEST, stream=True)
        for event in stream:
            if event.type == "message_stop":
                break
        stream.close()
        with messages_resource(client, beta=beta).stream(**REQUEST) as helper:
            for event in helper:
                if event.type == "message_stop":
                    break

        # The application closed both before the API did, so neither is `OK`, with every attribute of a whole Message.
        read, read_by_the_helper = spans.named("anthropic.messages.create")
        for span in (read, read_by_the_helper):
            assert span.status.status_code == StatusCode.UNSET
            assert "error.type" not in attributes(span)
            assert attributes(span)["gen_ai.response.id"] == "msg_1"
            assert attributes(span)["gen_ai.usage.output_tokens"] == 5
            assert attributes(span)["anthropic.message.stop_reason"] == "end_turn"
            assert isinstance(attributes(span)["gen_ai.response.time_to_first_chunk"], float)
        assert "gen_ai.output.messages" not in attributes(read)
        assert json.loads(attributes(read_by_the_helper)["gen_ai.output.messages"]) == [
            {"role": "assistant", "parts": [{"type": "text", "content": "Hi there"}]}
        ]

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_stream_closed_after_message_stop_before_the_end_of_the_body(
        self, beta: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[stream_response(), stream_response()])
        client = make_async_client(spans)

        stream = await messages_resource(client, beta=beta).create(**REQUEST, stream=True)
        async for event in stream:
            if event.type == "message_stop":
                break
        await stream.close()
        async with messages_resource(client, beta=beta).stream(**REQUEST) as helper:
            async for event in helper:
                if event.type == "message_stop":
                    break

        calls = spans.named("anthropic.messages.create")
        assert len(calls) == 2
        for span in calls:
            assert span.status.status_code == StatusCode.UNSET
            assert "error.type" not in attributes(span)
            assert attributes(span)["gen_ai.usage.output_tokens"] == 5
            assert attributes(span)["anthropic.message.stop_reason"] == "end_turn"

    @pytest.mark.parametrize(("content_block", "delta"), FIRST_DELTAS)
    @pytest.mark.respx(base_url=base_url)
    def test_time_to_first_chunk_is_set_at_the_first_content_block_delta(
        self, content_block: dict[str, Any], delta: dict[str, Any], spans: Spans, respx_mock: MockRouter
    ) -> None:
        events = events_with_first_delta(content_block, delta)
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events))
        started = StartedSpans()
        spans.provider.add_span_processor(started)

        times: list[tuple[str, float | None]] = []
        for event in create(make_client(spans).beta, stream=True):
            [call] = started.spans
            times.append((event.type, attributes(call).get("gen_ai.response.time_to_first_chunk")))

        assert_time_to_first_chunk_is_set_at_the_first_delta(times, spans.one("anthropic.messages.create"))

    @pytest.mark.respx(base_url=base_url)
    async def test_async_time_to_first_chunk_is_set_at_the_first_content_block_delta(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        events = events_with_first_delta({"type": "text", "text": ""}, {"type": "text_delta", "text": "Hi"})
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events))
        started = StartedSpans()
        spans.provider.add_span_processor(started)

        times: list[tuple[str, float | None]] = []
        async for event in await create(make_async_client(spans), stream=True):
            [call] = started.spans
            times.append((event.type, attributes(call).get("gen_ai.response.time_to_first_chunk")))

        assert_time_to_first_chunk_is_set_at_the_first_delta(times, spans.one("anthropic.messages.create"))

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_stream_without_a_content_block_delta_has_no_time_to_first_chunk(
        self, beta: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        events = events_without_a_delta()
        respx_mock.post("/v1/messages").mock(side_effect=[stream_response(events), stream_response(events)])
        client = make_client(spans)

        list(messages_resource(client, beta=beta).create(**REQUEST, stream=True))
        with messages_resource(client, beta=beta).stream(**REQUEST) as stream:
            assert stream.get_final_text() == "Hi there"

        calls = spans.named("anthropic.messages.create")
        assert len(calls) == 2
        for span in calls:
            assert span.status.status_code == StatusCode.OK
            assert attributes(span)["gen_ai.usage.output_tokens"] == 5
            assert "gen_ai.response.time_to_first_chunk" not in attributes(span)

    @pytest.mark.respx(base_url=base_url)
    async def test_async_stream_without_a_content_block_delta_has_no_time_to_first_chunk(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events_without_a_delta()))

        async for _ in await create(make_async_client(spans), stream=True):
            pass

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.OK
        assert "gen_ai.response.time_to_first_chunk" not in attributes(span)

    @pytest.mark.respx(base_url=base_url)
    def test_stream_closed_before_the_first_read(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[stream_response() for _ in range(2)])
        client = make_client(spans)

        create(client, stream=True).close()
        with client.messages.stream(
            max_tokens=1024, messages=[{"role": "user", "content": "Hello"}], model="claude-test"
        ):
            pass

        first, second = spans.named("anthropic.messages.create")
        for span in (first, second):
            assert span.status.status_code == StatusCode.UNSET
            assert "error.type" not in attributes(span)
            assert attributes(span)["gen_ai.request.stream"] is True
            assert "gen_ai.response.id" not in attributes(span)
            assert "gen_ai.response.time_to_first_chunk" not in attributes(span)

    @pytest.mark.respx(base_url=base_url)
    def test_stream_closed_before_the_first_read_has_the_requests_content(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[stream_response() for _ in range(2)])
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))
        request: dict[str, Any] = {**REQUEST, "system": "Be brief", "stop_sequences": ["END"]}

        client.messages.create(**request, stream=True).close()
        with client.messages.stream(**request):
            pass

        for span in spans.named("anthropic.messages.create"):
            assert span.status.status_code == StatusCode.UNSET
            assert json.loads(attributes(span)["gen_ai.input.messages"]) == [
                {"role": "user", "parts": [{"type": "text", "content": "Hello"}]}
            ]
            assert json.loads(attributes(span)["gen_ai.system_instructions"]) == [
                {"type": "text", "content": "Be brief"}
            ]
            assert attributes(span)["gen_ai.request.stop_sequences"] == ("END",)
            assert "gen_ai.output.messages" not in attributes(span)

    @pytest.mark.parametrize("traced", [False, True], ids=["untraced", "traced"])
    @pytest.mark.respx(base_url=base_url)
    def test_stream_closed_from_another_thread_while_it_is_read(
        self, traced: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        class Body:
            """A response body whose second read waits until the test lets it go."""

            def __init__(self) -> None:
                self.chunks = iter([sse(stream_events()[:1])])
                self.waiting = threading.Event()
                self.released = threading.Event()

            def __iter__(self) -> "Body":
                return self

            def __next__(self) -> bytes:
                for chunk in self.chunks:
                    return chunk
                self.waiting.set()
                self.released.wait(5)
                raise StopIteration

        body = Body()
        respx_mock.post("/v1/messages").mock(
            return_value=httpx2.Response(200, content=body, headers={"content-type": "text/event-stream"})
        )
        stream = create(make_client(spans, open_telemetry=spans.option() if traced else False), stream=True)

        def read() -> None:
            try:
                for _ in stream:
                    pass
            except Exception:
                pass

        reader = threading.Thread(target=read)
        reader.start()
        assert body.waiting.wait(5)
        # The read is in progress. Closing the stream ends the span as closed by the application, and the read then
        # ends by itself, which changes nothing on the span.
        stream.close()
        body.released.set()
        reader.join(5)
        assert not reader.is_alive()
        if traced:
            span = spans.one("anthropic.messages.create")
            assert span.status.status_code == StatusCode.UNSET
            assert "error.type" not in attributes(span)
            assert attributes(span)["gen_ai.response.id"] == "msg_1"

    @pytest.mark.respx(base_url=base_url)
    async def test_async_stream_closed_before_the_first_read(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[stream_response() for _ in range(2)])
        client = make_async_client(spans)

        stream = await create(client, stream=True)
        await stream.close()
        async with client.messages.stream(
            max_tokens=1024, messages=[{"role": "user", "content": "Hello"}], model="claude-test"
        ):
            pass

        first, second = spans.named("anthropic.messages.create")
        for span in (first, second):
            assert span.status.status_code == StatusCode.UNSET
            assert "error.type" not in attributes(span)
            assert "gen_ai.response.id" not in attributes(span)

    @pytest.mark.respx(base_url=base_url)
    def test_stream_ended_by_the_server_before_message_stop(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(stream_events()[:3]))
        client = make_client(spans)

        assert [event.type for event in create(client, stream=True)] == [
            "message_start",
            "content_block_start",
            "content_block_delta",
        ]

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.ERROR
        assert attributes(span)["error.type"] == "api_error"
        assert attributes(span)["gen_ai.response.id"] == "msg_1"
        assert "gen_ai.usage.output_tokens" not in attributes(span)
        assert "anthropic.message.stop_reason" not in attributes(span)

    @pytest.mark.parametrize("content_mode", ["metadata", "content"])
    @pytest.mark.parametrize("raw", [False, True], ids=["parsed", "raw"])
    @pytest.mark.respx(base_url=base_url)
    def test_compaction_tokens(self, raw: bool, content_mode: str, spans: Spans, respx_mock: MockRouter) -> None:
        iterations = [iteration("compaction", 100, 20, 10, 5), iteration("message"), iteration("compaction", 200, 30)]
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=message_with(iterations)))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": content_mode}))
        messages: Any = client.beta.messages.with_raw_response if raw else client.beta.messages

        messages.create(**REQUEST)

        span = attributes(spans.one("anthropic.messages.create"))
        # The sums of the compactions only, with their cached tokens as input tokens.
        assert span["anthropic.usage.compaction.input_tokens"] == 100 + 10 + 5 + 200
        assert span["anthropic.usage.compaction.output_tokens"] == 20 + 30
        assert span["gen_ai.usage.input_tokens"] == 15
        assert span["gen_ai.usage.output_tokens"] == 5

    @pytest.mark.respx(base_url=base_url)
    def test_compaction_tokens_of_a_response_without_usage_of_its_own(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        usage = {"input_tokens": 0, "output_tokens": 0, "iterations": [iteration("compaction", 100, 20)]}
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json={**MESSAGE, "usage": usage}))

        create(make_client(spans).beta)

        span = attributes(spans.one("anthropic.messages.create"))
        assert span["anthropic.usage.compaction.input_tokens"] == 100
        assert span["anthropic.usage.compaction.output_tokens"] == 20
        assert span["gen_ai.usage.input_tokens"] == 0
        assert span["gen_ai.usage.output_tokens"] == 0

    @pytest.mark.parametrize(
        "iterations", [None, [], [iteration("message")]], ids=["none", "empty", "without a compaction"]
    )
    @pytest.mark.respx(base_url=base_url)
    def test_no_compaction_tokens_without_a_compaction(
        self, iterations: list[dict[str, Any]] | None, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=MESSAGE), httpx2.Response(200, json=message_with(iterations))]
        )
        client = make_client(spans)

        create(client.beta)
        create(client.beta)

        for span in spans.named("anthropic.messages.create"):
            assert "anthropic.usage.compaction.input_tokens" not in attributes(span)
            assert "anthropic.usage.compaction.output_tokens" not in attributes(span)

    @pytest.mark.respx(base_url=base_url)
    def test_stable_usage_has_no_compaction_tokens(self, spans: Spans, respx_mock: MockRouter) -> None:
        iterations = [iteration("compaction", 100, 20)]
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=message_with(iterations)))

        create(make_client(spans))

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.OK
        assert attributes(span)["gen_ai.usage.output_tokens"] == 5
        assert "anthropic.usage.compaction.input_tokens" not in attributes(span)

    @pytest.mark.parametrize("content_mode", ["metadata", "content"])
    @pytest.mark.respx(base_url=base_url)
    def test_streamed_compaction_tokens(self, content_mode: str, spans: Spans, respx_mock: MockRouter) -> None:
        events = stream_events()
        events[4] = {**events[4], "usage": {"output_tokens": 5, "iterations": [iteration("compaction", 100, 20, 10)]}}
        respx_mock.post("/v1/messages").mock(side_effect=[stream_response(events), stream_response(events)])
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": content_mode}))

        list(create(client.beta, stream=True))
        with client.beta.messages.stream(**REQUEST) as stream:
            stream.until_done()

        calls = spans.named("anthropic.messages.create")
        assert len(calls) == 2
        for span in calls:
            assert attributes(span)["anthropic.usage.compaction.input_tokens"] == 110
            assert attributes(span)["anthropic.usage.compaction.output_tokens"] == 20
            assert attributes(span)["gen_ai.usage.input_tokens"] == 15
            assert attributes(span)["gen_ai.usage.output_tokens"] == 5

    @pytest.mark.respx(base_url=base_url)
    async def test_async_streamed_compaction_tokens(self, spans: Spans, respx_mock: MockRouter) -> None:
        events = stream_events()
        events[4] = {**events[4], "usage": {"output_tokens": 5, "iterations": [iteration("compaction", 100, 20)]}}
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events))
        client = make_async_client(spans)

        async for _ in await create(client.beta, stream=True):
            pass

        span = attributes(spans.one("anthropic.messages.create"))
        assert span["anthropic.usage.compaction.input_tokens"] == 100
        assert span["anthropic.usage.compaction.output_tokens"] == 20

    @pytest.mark.parametrize("helper", [False, True], ids=["events", "stream_helper"])
    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_stream_ended_after_message_delta_has_what_message_delta_gave(
        self, beta: bool, helper: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events_up_to_message_delta()))
        messages = messages_resource(make_client(spans), beta=beta)

        if helper:
            with messages.stream(**REQUEST) as stream:
                stream.until_done()
        else:
            list(messages.create(**REQUEST, stream=True))

        assert_span_has_what_message_delta_gave(spans.one("anthropic.messages.create"), beta=beta)

    @pytest.mark.parametrize("helper", [False, True], ids=["events", "stream_helper"])
    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_stream_ended_after_message_delta_has_what_message_delta_gave(
        self, beta: bool, helper: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events_up_to_message_delta()))
        messages = messages_resource(make_async_client(spans), beta=beta)

        if helper:
            async with messages.stream(**REQUEST) as stream:
                await stream.until_done()
        else:
            async for _ in await messages.create(**REQUEST, stream=True):
                pass

        assert_span_has_what_message_delta_gave(spans.one("anthropic.messages.create"), beta=beta)

    @pytest.mark.parametrize("helper", [False, True], ids=["events", "stream_helper"])
    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_stream_ended_before_message_delta_has_nothing_that_message_delta_gives(
        self, beta: bool, helper: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events_up_to_message_delta()[:-1]))
        messages = messages_resource(make_client(spans), beta=beta)

        if helper:
            with messages.stream(**REQUEST) as stream:
                stream.until_done()
        else:
            list(messages.create(**REQUEST, stream=True))

        assert_span_has_nothing_that_message_delta_gives(spans.one("anthropic.messages.create"))

    @pytest.mark.parametrize("helper", [False, True], ids=["events", "stream_helper"])
    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_stream_ended_before_message_delta_has_nothing_that_message_delta_gives(
        self, beta: bool, helper: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events_up_to_message_delta()[:-1]))
        messages = messages_resource(make_async_client(spans), beta=beta)

        if helper:
            async with messages.stream(**REQUEST) as stream:
                await stream.until_done()
        else:
            async for _ in await messages.create(**REQUEST, stream=True):
                pass

        assert_span_has_nothing_that_message_delta_gives(spans.one("anthropic.messages.create"))

    @pytest.mark.parametrize("helper", [False, True], ids=["events", "stream_helper"])
    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_stream_ended_after_a_message_delta_that_cannot_be_accumulated_has_nothing_of_it(
        self, beta: bool, helper: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        *events, message_delta = events_up_to_message_delta()
        respx_mock.post("/v1/messages").mock(return_value=stream_response([*events, without(message_delta, "usage")]))
        messages = messages_resource(make_client(spans, _strict_response_validation=False), beta=beta)

        if helper:
            # The helper fails on the event that it cannot accumulate, and reads no further.
            with pytest.raises(AttributeError):
                with messages.stream(**REQUEST) as stream:
                    stream.until_done()
        else:
            list(messages.create(**REQUEST, stream=True))

        # The snapshot lacks what the event has, so the span has only what the events before it gave.
        span = spans.one("anthropic.messages.create")
        assert attributes(span)["gen_ai.response.id"] == "msg_1"
        assert "anthropic.message.stop_reason" not in attributes(span)
        assert "gen_ai.usage.output_tokens" not in attributes(span)

    @pytest.mark.parametrize("stop_reason", ["tool_use", "max_tokens", "a_later_stop_reason"])
    @pytest.mark.respx(base_url=base_url)
    def test_stop_reason_is_the_one_in_the_response(
        self, stop_reason: str, spans: Spans, respx_mock: MockRouter
    ) -> None:
        events = stream_events()
        events[4] = {**events[4], "delta": {"stop_reason": stop_reason}}
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                httpx2.Response(200, json={**MESSAGE, "stop_reason": stop_reason}),
                stream_response(events),
                stream_response(events),
            ]
        )
        client = make_client(spans, _strict_response_validation=False)

        create(client)
        list(create(client, stream=True))
        with client.messages.stream(**REQUEST) as stream:
            stream.until_done()

        # Not content, so it is there by default, and with the API's own value.
        calls = spans.named("anthropic.messages.create")
        assert len(calls) == 3
        for span in calls:
            assert attributes(span)["anthropic.message.stop_reason"] == stop_reason
            assert "gen_ai.response.finish_reasons" not in attributes(span)

    @pytest.mark.respx(base_url=base_url)
    async def test_async_stream_ended_by_the_server_before_message_stop(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(stream_events()[:3]))
        client = make_async_client(spans)

        stream = await create(client, stream=True)
        assert [event.type async for event in stream] == ["message_start", "content_block_start", "content_block_delta"]

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.ERROR
        assert attributes(span)["error.type"] == "api_error"

    @pytest.mark.respx(base_url=base_url)
    def test_streamed_response_model_is_the_one_that_a_fallback_block_names(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        events = fallback_stream_events()
        respx_mock.post("/v1/messages").mock(side_effect=[stream_response(events), stream_response(events)])
        client = make_client(spans)

        read = list(client.beta.messages.create(**REQUEST, stream=True))
        with client.beta.messages.stream(**REQUEST) as stream:
            message = stream.get_final_message()

        # `message_start` has the model that declined, and the Message has the one that answered.
        start = read[0]
        assert start.type == "message_start" and start.message.model == "claude-test"
        assert message.model == "claude-fallback"
        raw_stream, helper_stream = spans.named("anthropic.messages.create")
        for span in (raw_stream, helper_stream):
            assert span.status.status_code == StatusCode.OK
            assert attributes(span)["gen_ai.request.model"] == "claude-test"
            assert attributes(span)["gen_ai.response.model"] == "claude-fallback"

    @pytest.mark.respx(base_url=base_url)
    async def test_async_streamed_response_model_is_the_one_that_a_fallback_block_names(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        events = fallback_stream_events()
        respx_mock.post("/v1/messages").mock(side_effect=[stream_response(events), stream_response(events)])
        client = make_async_client(spans)

        read = [event async for event in await client.beta.messages.create(**REQUEST, stream=True)]
        async with client.beta.messages.stream(**REQUEST) as stream:
            message = await stream.get_final_message()

        start = read[0]
        assert start.type == "message_start" and start.message.model == "claude-test"
        assert message.model == "claude-fallback"
        raw_stream, helper_stream = spans.named("anthropic.messages.create")
        for span in (raw_stream, helper_stream):
            assert span.status.status_code == StatusCode.OK
            assert attributes(span)["gen_ai.response.model"] == "claude-fallback"

    @pytest.mark.respx(base_url=base_url)
    def test_event_stream_closed_early(self, spans: Spans, respx_mock: MockRouter) -> None:
        event = {"type": "session.status_running", "id": "sevt_1", "processed_at": "2026-01-01T00:00:00Z"}
        respx_mock.get("/v1/sessions/sesn_1/events/stream").mock(
            return_value=httpx2.Response(
                200, content=sse([event, event]), headers={"content-type": "text/event-stream"}
            )
        )
        client = make_client(spans)

        with client.beta.sessions.events.stream("sesn_1") as stream:
            assert next(iter(stream)).type == "session.status_running"

        span = spans.one("anthropic.sessions.events.stream")
        assert span.status.status_code == StatusCode.UNSET
        assert "error.type" not in attributes(span)

    @pytest.mark.parametrize("raw", [False, True], ids=["stream", "parsed from a raw response"])
    @pytest.mark.respx(base_url=base_url)
    def test_event_stream_ended_by_the_server(self, spans: Spans, respx_mock: MockRouter, raw: bool) -> None:
        event = {"type": "session.status_running", "id": "sevt_1", "processed_at": "2026-01-01T00:00:00Z"}
        respx_mock.get("/v1/sessions/sesn_1/events/stream").mock(
            return_value=httpx2.Response(200, content=sse([event]), headers={"content-type": "text/event-stream"})
        )
        events = make_client(spans).beta.sessions.events

        with events.with_raw_response.stream("sesn_1").parse() if raw else events.stream("sesn_1") as stream:
            assert [item.type for item in stream] == ["session.status_running"]

        # A stream without an end event is never read to the end, so the server ending it sets no status.
        span = spans.one("anthropic.sessions.events.stream")
        assert span.end_time is not None
        assert span.status.status_code == StatusCode.UNSET
        assert "error.type" not in attributes(span)
        assert attributes(span)["http.response.status_code"] == 200
        assert attributes(span)["gen_ai.provider.name"] == "anthropic"

    @pytest.mark.parametrize("raw", [False, True], ids=["stream", "parsed from a raw response"])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_event_stream_ended_by_the_server(
        self, spans: Spans, respx_mock: MockRouter, raw: bool
    ) -> None:
        event = {"type": "session.status_running", "id": "sevt_1", "processed_at": "2026-01-01T00:00:00Z"}
        respx_mock.get("/v1/sessions/sesn_1/events/stream").mock(
            return_value=httpx2.Response(200, content=sse([event]), headers={"content-type": "text/event-stream"})
        )
        events = make_async_client(spans).beta.sessions.events

        async with (
            await (await events.with_raw_response.stream("sesn_1")).parse() if raw else await events.stream("sesn_1")
        ) as stream:
            assert [item.type async for item in stream] == ["session.status_running"]

        span = spans.one("anthropic.sessions.events.stream")
        assert span.end_time is not None
        assert span.status.status_code == StatusCode.UNSET
        assert "error.type" not in attributes(span)
        assert attributes(span)["http.response.status_code"] == 200

    @pytest.mark.respx(base_url=base_url)
    def test_stream_error_event(self, spans: Spans, respx_mock: MockRouter) -> None:
        events: list[dict[str, Any]] = [
            stream_events()[0],
            {"type": "error", "error": {"type": "overloaded_error", "message": "busy"}},
        ]
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events))
        client = make_client(spans)

        with pytest.raises(APIStatusError):
            for _ in create(client, stream=True):
                pass

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.ERROR
        assert attributes(span)["error.type"] == "overloaded_error"

    @pytest.mark.respx(base_url=base_url)
    def test_stream_error_event_without_a_type(self, spans: Spans, respx_mock: MockRouter) -> None:
        events: list[dict[str, Any]] = [stream_events()[0], {"type": "error", "error": {"message": "busy"}}]
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events))
        client = make_client(spans)

        with pytest.raises(APIStatusError):
            for _ in create(client, stream=True):
                pass

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.ERROR
        # The status of the response that opened the stream is no error, so it is no error type either.
        assert attributes(span)["error.type"] == "client_error"
        assert attributes(span)["http.response.status_code"] == 200

    @pytest.mark.respx(base_url=base_url)
    def test_concurrent_calls_sharing_options_get_their_own_spans(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=respond_with_message)
        client = make_client(spans, open_telemetry=spans.option(conversation_id="shared"))
        options: dict[str, Any] = {"extra_headers": {"x-test": "1"}}

        def call(_: int) -> None:
            create(client, **options)

        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(call, range(8)))

        calls = spans.named("anthropic.messages.create")
        assert len(calls) == 8
        assert len({span_id(span) for span in calls}) == 8
        assert len({trace_id(span) for span in calls}) == 8
        assert all(span.status.status_code == StatusCode.OK for span in calls)

    @pytest.mark.respx(base_url=base_url)
    async def test_concurrent_async_calls_get_their_own_spans(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=respond_with_message)
        client = make_async_client(spans, open_telemetry=spans.option(conversation_id="shared"))
        options: dict[str, Any] = {"extra_headers": {"x-test": "1"}}

        async def call() -> None:
            await client.messages.create(
                max_tokens=1024, messages=[{"role": "user", "content": "Hello"}], model="claude-test", **options
            )

        await asyncio.gather(*(call() for _ in range(8)))

        calls = spans.named("anthropic.messages.create")
        assert len(calls) == 8
        assert len({trace_id(span) for span in calls}) == 8

    @pytest.mark.respx(base_url=base_url)
    async def test_async_call_reads_the_platform_off_the_event_loop(
        self, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=respond_with_message)
        threads: list[threading.Thread] = []

        def get_platform() -> str:
            threads.append(threading.current_thread())
            return "Linux"

        monkeypatch.setattr(_base_client, "get_platform", get_platform)
        cast(Any, _base_client.platform_headers).cache_clear()

        # The span starts with `anthropic.beta`, which is read from the client's headers.
        await create(make_async_client(spans, default_headers={"anthropic-beta": "beta-1"}))

        assert attributes(spans.one("anthropic.messages.create"))["anthropic.beta"] == ("beta-1",)
        assert threads and threading.current_thread() not in threads

    @pytest.mark.respx(base_url=base_url)
    def test_environment_variable_disables_spans(self, registered: Spans, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))

        with update_env(ANTHROPIC_OPEN_TELEMETRY="FALSE"):
            client = Anthropic(base_url=base_url, api_key="key")
            create(client)
            assert registered.finished == ()
            assert "traceparent" not in requests(route)[0].headers

            # The variable is for a client that is given no option.
            create(Anthropic(base_url=base_url, api_key="key", open_telemetry={}))
            create(Anthropic(base_url=base_url, api_key="key", open_telemetry={"traces": True}))
            create(Anthropic(base_url=base_url, api_key="key", open_telemetry={"traces": {"enabled": True}}))
            assert len(registered.named("anthropic.messages.create")) == 3

    @pytest.mark.respx(base_url=base_url)
    def test_option_disables_spans(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))

        create(make_client(spans, open_telemetry=False))
        create(make_client(spans, open_telemetry=spans.option(traces=False)))

        assert spans.finished == ()

    @pytest.mark.respx(base_url=base_url)
    def test_disabled_spans_leave_the_body_of_the_response_alone(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[stream_response() for _ in range(4)])

        for traced, client in enumerate((make_client(spans, open_telemetry=False), make_client(spans))):
            stream = create(client, stream=True)
            raw = create(client.with_raw_response, stream=True)

            for response in (stream.response, raw.http_response):
                assert type(response.stream).__module__.startswith("anthropic") == bool(traced)
            assert len(list(stream)) == len(list(raw.parse())) == len(stream_events())

    @pytest.mark.respx(base_url=base_url)
    async def test_async_disabled_spans_leave_the_body_of_the_response_alone(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[stream_response() for _ in range(4)])

        for traced, client in enumerate((make_async_client(spans, open_telemetry=False), make_async_client(spans))):
            stream = await create(client, stream=True)
            raw = await create(client.with_raw_response, stream=True)

            for response in (stream.response, raw.http_response):
                assert type(response.stream).__module__.startswith("anthropic") == bool(traced)
            assert len([event async for event in stream]) == len(stream_events())
            assert len([event async for event in await raw.parse()]) == len(stream_events())

    @pytest.mark.parametrize("traces", [True, False], ids=["spans_on", "spans_off"])
    async def test_stream_over_a_stand_in_for_the_response(self, spans: Spans, traces: bool) -> None:
        response = cast(httpx2.Response, StandInResponse())
        option = spans.option(traces=traces)

        stream = Stream(cast_to=object, response=response, client=make_client(spans, open_telemetry=option))
        async_stream = AsyncStream(
            cast_to=object, response=response, client=make_async_client(spans, open_telemetry=option)
        )

        assert len(list(stream)) == len([event async for event in async_stream]) == len(stream_events())
        assert spans.finished == ()

    async def test_stream_helper_over_a_stand_in_for_the_stream(self) -> None:
        class StandInStream:
            def __iter__(self) -> Iterator[RawMessageStreamEvent]:
                return iter(())

            async def __aiter__(self) -> AsyncIterator[RawMessageStreamEvent]:
                for event in ():
                    yield event

        stand_in: Any = StandInStream()

        assert list(MessageStream(stand_in, NOT_GIVEN)) == []
        assert [event async for event in AsyncMessageStream(stand_in, NOT_GIVEN)] == []

    @pytest.mark.respx(base_url=base_url)
    def test_other_methods(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages/count_tokens").mock(return_value=httpx2.Response(200, json={"input_tokens": 7}))
        batch = {
            "id": "msgbatch_1",
            "type": "message_batch",
            "processing_status": "in_progress",
            "request_counts": {"processing": 1, "succeeded": 0, "errored": 0, "canceled": 0, "expired": 0},
            "created_at": "2024-01-01T00:00:00Z",
            "expires_at": "2024-01-02T00:00:00Z",
            "ended_at": None,
            "cancel_initiated_at": None,
            "archived_at": None,
            "results_url": None,
        }
        respx_mock.post("/v1/messages/batches").mock(return_value=httpx2.Response(200, json=batch))
        respx_mock.post("/v1/messages/batches/msgbatch_1/cancel").mock(return_value=httpx2.Response(200, json=batch))
        models: dict[str, Any] = {"data": [], "has_more": False, "first_id": None, "last_id": None}
        respx_mock.get("/v1/models").mock(return_value=httpx2.Response(200, json=models))
        client = make_client(spans)

        client.messages.count_tokens(messages=[{"role": "user", "content": "Hello"}], model="claude-test")
        client.messages.batches.create(
            requests=[
                {
                    "custom_id": "a",
                    "params": {"max_tokens": 1, "messages": [{"role": "user", "content": "Hi"}], "model": "m"},
                }
            ]
        )
        client.messages.batches.cancel("msgbatch_1")
        client.beta.models.list()

        count = spans.one("anthropic.messages.count_tokens")
        assert attributes(count)["gen_ai.request.model"] == "claude-test"
        assert attributes(count)["anthropic.message.count_tokens.input_tokens"] == 7
        assert "gen_ai.operation.name" not in attributes(count)
        assert attributes(spans.one("anthropic.messages.batches.create"))["anthropic.message.batch.id"] == "msgbatch_1"
        assert attributes(spans.one("anthropic.messages.batches.cancel"))["anthropic.message.batch.id"] == "msgbatch_1"
        # The `beta` namespace is not part of the name.
        assert spans.one("anthropic.models.list").status.status_code == StatusCode.OK

    @pytest.mark.respx(base_url=base_url)
    def test_output_type_is_json_when_the_request_sets_a_json_output_format(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        answer = {**MESSAGE, "content": [{"type": "text", "text": '{"city": "SF"}'}]}
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=answer))
        client = make_client(spans, _strict_response_validation=False)
        schema: dict[str, object] = {"type": "object", "properties": {"city": {"type": "string"}}}

        class City(pydantic.BaseModel):
            city: str

        client.messages.create(**REQUEST, output_config={"format": {"type": "json_schema", "schema": schema}})
        client.messages.create(**REQUEST, output_config={"effort": "high"})
        client.messages.create(**REQUEST, extra_body={"output_config": {"format": {"type": "other"}}})
        client.beta.messages.create(**REQUEST, extra_body={"output_format": {"type": "other"}})
        client.beta.messages.create(**REQUEST, extra_body={"output_format": {"type": "json_schema", "schema": schema}})
        # The helpers make a schema of `output_format`, which needs Pydantic 2.
        if not PYDANTIC_V1:
            client.beta.messages.parse(**REQUEST, output_format=City)
            with client.beta.messages.stream(**REQUEST, output_format=City) as stream:
                stream.close()

        with_format, without, other, other_deprecated, deprecated, *helpers = spans.named("anthropic.messages.create")
        for span in (without, other, other_deprecated):
            assert "gen_ai.output.type" not in attributes(span)
        assert len(helpers) == (0 if PYDANTIC_V1 else 2)
        for span in (with_format, deprecated, *helpers):
            assert attributes(span)["gen_ai.output.type"] == "json"

    @pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
    async def test_spans_that_start_during_the_call_are_children_of_the_call_span(
        self, sync: bool, spans: Spans
    ) -> None:
        tracer = spans.provider.get_tracer("app")

        def handler(_request: httpx2.Request) -> httpx2.Response:
            # What an application's transport, event hook or HTTP instrumentation does while the SDK sends.
            with tracer.start_as_current_span("app.transport"):
                return httpx2.Response(200, json=MESSAGE)

        if sync:
            client = make_client(spans, http_client=httpx2.Client(transport=httpx2.MockTransport(handler)))
            create(client)
        else:
            async_client = make_async_client(
                spans, http_client=httpx2.AsyncClient(transport=httpx2.MockTransport(handler))
            )
            await create(async_client)

        call = spans.one("anthropic.messages.create")
        assert parent_id(spans.one("app.transport")) == span_id(call)
        assert trace_id(spans.one("app.transport")) == trace_id(call)
        assert not trace.get_current_span().get_span_context().is_valid

    @pytest.mark.respx(base_url=base_url)
    def test_call_span_is_open_but_not_current_while_the_application_reads_a_stream(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response())
        tracer = spans.provider.get_tracer("app")

        stream = create(make_client(spans), stream=True)
        assert not trace.get_current_span().get_span_context().is_valid
        for _ in stream:
            assert not trace.get_current_span().get_span_context().is_valid
            assert spans.named("anthropic.messages.create") == []
            # So what the application does between events is not a child of the call span.
            with tracer.start_as_current_span("app.work"):
                pass

        call = spans.one("anthropic.messages.create")
        assert call.status.status_code == StatusCode.OK
        assert all(span.parent is None for span in spans.named("app.work"))

    @pytest.mark.respx(base_url=base_url)
    def test_request_attributes_are_on_the_span_from_its_start(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        respx_mock.post("/v1/messages/count_tokens").mock(return_value=httpx2.Response(200, json={"input_tokens": 7}))
        sampler = StartAttributes()
        provider = TracerProvider(sampler=sampler)
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry={"tracer_provider": provider})

        create(
            client.with_options(open_telemetry={**client.open_telemetry, "conversation_id": "conv_1"}),
            service_tier="auto",
            extra_headers={"anthropic-beta": "a, b"},
        )
        client.messages.count_tokens(model="claude-test", messages=[{"role": "user", "content": "Hello"}])

        assert sampler.started == [
            (
                "anthropic.messages.create",
                {
                    "server.address": "127.0.0.1",
                    "server.port": 4010,
                    "http.request.method": "POST",
                    "http.route": "/v1/messages",
                    "gen_ai.provider.name": "anthropic",
                    "gen_ai.conversation.id": "conv_1",
                    "gen_ai.operation.name": "chat",
                    "gen_ai.request.model": "claude-test",
                    "gen_ai.request.max_tokens": 1024,
                    "anthropic.request.service_tier": "auto",
                    "anthropic.beta": ["a", "b"],
                },
            ),
            (
                "anthropic.messages.count_tokens",
                {
                    "server.address": "127.0.0.1",
                    "server.port": 4010,
                    "http.request.method": "POST",
                    "http.route": "/v1/messages/count_tokens",
                    "gen_ai.provider.name": "anthropic",
                    "gen_ai.request.model": "claude-test",
                },
            ),
        ]

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_batch_create_starts_its_span_with_the_request_count(self, beta: bool, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages/batches").mock(return_value=httpx2.Response(200, json={"id": "msgbatch_1"}))
        respx_mock.get("/v1/messages/batches/msgbatch_1").mock(
            return_value=httpx2.Response(200, json={"id": "msgbatch_1"})
        )
        batches_page: dict[str, Any] = {"data": [], "has_more": False, "first_id": None, "last_id": None}
        respx_mock.get("/v1/messages/batches").mock(return_value=httpx2.Response(200, json=batches_page))
        sampler = StartAttributes()
        client = Anthropic(
            base_url=base_url,
            api_key="key",
            open_telemetry={"tracer_provider": TracerProvider(sampler=sampler)},
            _strict_response_validation=False,
        )
        batches: Any = client.beta.messages.batches if beta else client.messages.batches
        params = {"max_tokens": 1, "messages": [{"role": "user", "content": "Hi"}], "model": "claude-test"}

        # The requests can be any iterable: the count is that of the prepared body.
        batches.create(requests=({"custom_id": custom_id, "params": params} for custom_id in ("a", "b", "c")))
        batches.retrieve("msgbatch_1")
        batches.list()

        started = dict(sampler.started)
        assert started["anthropic.messages.batches.create"]["anthropic.message.batch.request_count"] == 3
        assert "anthropic.message.batch.request_count" not in started["anthropic.messages.batches.retrieve"]
        assert "anthropic.message.batch.request_count" not in started["anthropic.messages.batches.list"]

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_batch_create_starts_its_span_with_the_request_count(
        self, beta: bool, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages/batches").mock(return_value=httpx2.Response(200, json={"id": "msgbatch_1"}))
        sampler = StartAttributes()
        client = AsyncAnthropic(
            base_url=base_url,
            api_key="key",
            open_telemetry={"tracer_provider": TracerProvider(sampler=sampler)},
            _strict_response_validation=False,
        )
        batches: Any = client.beta.messages.batches if beta else client.messages.batches

        await batches.create(requests=[])

        assert dict(sampler.started)["anthropic.messages.batches.create"]["anthropic.message.batch.request_count"] == 0

    @pytest.mark.respx()
    def test_server_attributes_are_on_the_span_from_its_start_only(
        self, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        respx_mock.post(f"{base_url}/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=MESSAGE), stream_response(), stream_response()]
        )
        respx_mock.post(f"{base_url}/v1/messages/count_tokens").mock(
            return_value=httpx2.Response(200, json={"input_tokens": 7})
        )
        respx_mock.get(f"{base_url}/v1/messages/batches/msgbatch_1").mock(
            return_value=httpx2.Response(200, json={"id": "msgbatch_1", "results_url": None})
        )
        model = {"id": "model_1", "type": "model", "display_name": "Model", "created_at": "2024-01-01T00:00:00Z"}
        respx_mock.get(f"{base_url}/v1/models").mock(
            side_effect=[
                httpx2.Response(
                    200, json={"data": [model], "has_more": True, "first_id": "model_1", "last_id": "model_1"}
                ),
                httpx2.Response(
                    200, json={"data": [model], "has_more": False, "first_id": "model_1", "last_id": "model_1"}
                ),
            ]
        )
        respx_mock.post(host="bedrock-runtime.us-east-1.amazonaws.com").mock(
            return_value=httpx2.Response(200, json=MESSAGE)
        )
        respx_mock.post(host="us-east5-aiplatform.googleapis.com").mock(return_value=httpx2.Response(200, json=MESSAGE))
        sampler = StartAttributes()
        option: OpenTelemetryOptions = {"tracer_provider": TracerProvider(sampler=sampler)}
        set_later: list[str] = []
        set_attribute = SdkSpan.set_attribute

        def observed_set_attribute(span: SdkSpan, key: str, value: Any) -> None:
            set_later.append(key)
            set_attribute(span, key, value)

        monkeypatch.setattr(SdkSpan, "set_attribute", observed_set_attribute)

        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=option)
        create(client)
        for _ in create(client, stream=True):
            pass
        with client.messages.stream(**REQUEST) as stream:
            stream.until_done()
        client.messages.count_tokens(model="claude-test", messages=[{"role": "user", "content": "Hello"}])
        client.messages.batches.retrieve("msgbatch_1")
        assert len(list(client.models.list())) == 2
        create(
            AnthropicBedrock(
                aws_region="us-east-1", aws_access_key="access", aws_secret_key="secret", open_telemetry=option
            )
        )
        create(AnthropicVertex(region="us-east5", project_id="project", access_token="token", open_telemetry=option))

        assert [(name, started["server.address"], started["server.port"]) for name, started in sampler.started] == [
            ("anthropic.messages.create", "127.0.0.1", 4010),
            ("anthropic.messages.create", "127.0.0.1", 4010),
            ("anthropic.messages.create", "127.0.0.1", 4010),
            ("anthropic.messages.count_tokens", "127.0.0.1", 4010),
            ("anthropic.messages.batches.retrieve", "127.0.0.1", 4010),
            ("anthropic.models.list", "127.0.0.1", 4010),
            ("anthropic.models.list", "127.0.0.1", 4010),
            ("anthropic.messages.create", "bedrock-runtime.us-east-1.amazonaws.com", 443),
            ("anthropic.messages.create", "us-east5-aiplatform.googleapis.com", 443),
        ]
        # The spans do get attributes after they start, and never these two.
        assert "gen_ai.response.id" in set_later
        assert "server.address" not in set_later and "server.port" not in set_later

    @pytest.mark.respx(base_url=base_url)
    def test_batch_methods_record_the_batch_id_that_they_are_given(self, spans: Spans, respx_mock: MockRouter) -> None:
        # The ID comes from the method's argument, so the span has it whatever the URL is and however the call ends.
        batch = {"id": "msgbatch_1", "results_url": "https://files.example.com/download/abc"}
        respx_mock.get("/v1/messages/batches/msgbatch_1").mock(return_value=httpx2.Response(200, json=batch))
        respx_mock.get("https://files.example.com/download/abc").mock(return_value=httpx2.Response(200, text=""))
        respx_mock.delete("/v1/messages/batches/msgbatch_1").mock(return_value=httpx2.Response(404, json={}))
        client = make_client(spans, max_retries=0, _strict_response_validation=False)
        beta = make_client(spans, max_retries=0, _strict_response_validation=False).beta

        client.messages.batches.retrieve("msgbatch_1")
        client.messages.batches.results("msgbatch_1").close()
        beta.messages.batches.retrieve("msgbatch_1")
        with pytest.raises(APIStatusError):
            client.messages.batches.delete("msgbatch_1")

        retrieves = spans.named("anthropic.messages.batches.retrieve")
        assert len(retrieves) == 3
        for span in (*retrieves, spans.one("anthropic.messages.batches.results")):
            assert attributes(span)["anthropic.message.batch.id"] == "msgbatch_1"
        failed = spans.one("anthropic.messages.batches.delete")
        assert failed.status.status_code == StatusCode.ERROR
        assert attributes(failed)["anthropic.message.batch.id"] == "msgbatch_1"

    @pytest.mark.respx()
    def test_third_party_provider_names(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post().mock(return_value=httpx2.Response(200, json=MESSAGE))

        bedrock = AnthropicBedrock(
            aws_region="us-east-1",
            aws_access_key="access",
            aws_secret_key="secret",
            open_telemetry=spans.option(),
        )
        create(bedrock)
        vertex = AnthropicVertex(
            region="us-east5", project_id="project", access_token="token", open_telemetry=spans.option()
        )
        create(vertex.with_options(timeout=10))

        bedrock_span, vertex_span = spans.named("anthropic.messages.create")
        assert attributes(bedrock_span)["gen_ai.provider.name"] == "aws.bedrock"
        assert attributes(bedrock_span)["server.address"] == "bedrock-runtime.us-east-1.amazonaws.com"
        assert attributes(bedrock_span)["server.port"] == 443
        assert attributes(vertex_span)["gen_ai.provider.name"] == "gcp.vertex_ai"
        # These clients move the model from the body that they send into the URL. The span reads the body of the call.
        for span in (bedrock_span, vertex_span):
            assert attributes(span)["gen_ai.request.model"] == "claude-test"
            assert attributes(span)["gen_ai.request.max_tokens"] == 1024
            assert attributes(span)["gen_ai.response.id"] == "msg_1"
            # The route is the one of the method that the application called, and the URL is where the request went.
            assert attributes(span)["http.request.method"] == "POST"
            assert attributes(span)["http.route"] == "/v1/messages"
        assert url_attributes(bedrock_span) == {
            "url.scheme": "https",
            "url.path": "/model/claude-test/invoke",
            "url.full": "https://bedrock-runtime.us-east-1.amazonaws.com/model/claude-test/invoke",
        }
        vertex_path = "/v1/projects/project/locations/us-east5/publishers/anthropic/models/claude-test:rawPredict"
        assert url_attributes(vertex_span) == {
            "url.scheme": "https",
            "url.path": vertex_path,
            "url.full": "https://us-east5-aiplatform.googleapis.com" + vertex_path,
        }

    @pytest.mark.respx()
    def test_third_party_streams_and_token_counts_have_the_request_model(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        vertex = AnthropicVertex(
            region="us-east5", project_id="project", access_token="token", open_telemetry=spans.option()
        )
        respx_mock.post(url__regex=r".*:streamRawPredict$").mock(return_value=stream_response())
        respx_mock.post(url__regex=r".*/count-tokens:rawPredict$").mock(
            return_value=httpx2.Response(200, json={"input_tokens": 7})
        )

        for _ in create(vertex, stream=True):
            pass
        vertex.messages.count_tokens(model="claude-test", messages=[{"role": "user", "content": "Hello"}])

        stream = spans.one("anthropic.messages.create")
        assert attributes(stream)["gen_ai.request.model"] == "claude-test"
        assert attributes(stream)["gen_ai.request.stream"] is True
        assert attributes(stream)["gen_ai.usage.output_tokens"] == 5
        count = spans.one("anthropic.messages.count_tokens")
        assert attributes(count)["gen_ai.request.model"] == "claude-test"
        assert attributes(count)["anthropic.message.count_tokens.input_tokens"] == 7

    @pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
    @pytest.mark.respx()
    async def test_sigv4_signature_does_not_cover_the_trace_headers_that_the_sdk_replaces(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        route = respx_mock.post().mock(return_value=httpx2.Response(200, json=MESSAGE))
        options: dict[str, Any] = {
            "aws_region": "us-east-1",
            "aws_access_key": "access",
            "aws_secret_key": "secret",
            "open_telemetry": spans.option(),
        }
        # A header of the application is a signed header like any other, and the SDK replaces this one's value.
        headers = {"traceparent": "00-{:032x}-{:016x}-01".format(0xABCD, 0xEF)}

        if sync:
            create(AnthropicBedrock(**options), extra_headers=headers)
        else:
            await create(AsyncAnthropicBedrock(**options), extra_headers=headers)

        request = requests(route)[0]
        call = spans.one("anthropic.messages.create")
        assert request.headers["traceparent"].startswith("00-{:032x}-{:016x}-".format(trace_id(call), span_id(call)))
        authorization = request.headers["Authorization"]
        # The header is not signed, so that replacing it, here or in an instrumented HTTP client, keeps the signature valid.
        assert "traceparent" not in authorization.split("SignedHeaders=")[1].split(",")[0].split(";")
        assert authorization.endswith("Signature=" + sigv4_signature(request, secret_key="secret"))


def url_attributes(span: ReadableSpan) -> dict[str, Any]:
    return {key: value for key, value in attributes(span).items() if key.startswith("url.")}


async def call_client(sync: bool, spans: Spans, invoke: Callable[[Any], Any], **options: Any) -> Any:
    """What `invoke` returns for a client of `spans`: the synchronous one, or else the asynchronous one, awaited."""
    if sync:
        return invoke(make_client(spans, **options))
    return await invoke(make_async_client(spans, **options))


SYNC_AND_ASYNC = pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])

EMPTY_PAGE: dict[str, Any] = {"data": [], "has_more": False, "first_id": None, "last_id": None}


def no_wait(*_args: object, **_kwargs: object) -> float:
    return 0.0


# A call whose query has a parameter that its method declares and that is no content: what makes it, its path, the
# query that the span has of it, and the span's name.
DeclaredQueryCall = tuple[Callable[[Any], Any], str, str, str]
DECLARED_QUERY_CALLS: list[DeclaredQueryCall] = [
    (
        lambda client: client.models.list(lifecycle=["active", "retired"]),
        "/v1/models",
        "lifecycle%5B%5D=active&lifecycle%5B%5D=retired",
        "anthropic.models.list",
    ),
    (
        lambda client: client.beta.models.list(lifecycle=["active"]),
        "/v1/models",
        "lifecycle%5B%5D=active",
        "anthropic.models.list",
    ),
    (
        lambda client: client.organization.workspaces.list(include_default=True),
        "/v1/organizations/workspaces",
        "include_default=true",
        "anthropic.organization.workspaces.list",
    ),
    (
        lambda client: client.beta.organization.workspaces.list(include_default=True),
        "/v1/organizations/workspaces",
        "include_default=true",
        "anthropic.organization.workspaces.list",
    ),
    (
        lambda client: client.beta.sessions.threads.list("sesn_1", statuses=["running", "idle"]),
        "/v1/sessions/sesn_1/threads",
        "statuses%5B%5D=running&statuses%5B%5D=idle",
        "anthropic.sessions.threads.list",
    ),
]

# A call whose query has a parameter that is content on every endpoint, which no method has to say: what makes it, its
# request, the query that the span has of it, and the span's name.
ContentQueryCall = tuple[Callable[[Any], Any], str, str, str, str]
CONTENT_QUERY_CALLS: list[ContentQueryCall] = [
    (
        lambda client: client.beta.organization.users.list(email="a@example.com", limit=5),
        "GET",
        "/v1/organizations/users",
        "email=a%40example.com&limit=5",
        "anthropic.organization.users.list",
    ),
    (
        lambda client: client.beta.memory_stores.memories.list("memstore_1", path_prefix="/notes"),
        "GET",
        "/v1/memory_stores/memstore_1/memories",
        "path_prefix=%2Fnotes",
        "anthropic.memory_stores.memories.list",
    ),
    (
        lambda client: client.beta.memory_stores.memories.delete(
            "mem_1", memory_store_id="memstore_1", expected_content_sha256="0" * 64
        ),
        "DELETE",
        "/v1/memory_stores/memstore_1/memories/mem_1",
        "expected_content_sha256=" + "0" * 64,
        "anthropic.memory_stores.memories.delete",
    ),
]

# The Analytics list methods, which all define `filter`: what calls one, its path, its span's name, and whether
# `filter` matches names on that endpoint, which makes it content there and is for the method to say.
FilterCall = tuple[Callable[[Any, list[str]], Any], str, str, bool]
FILTER_CALLS: list[FilterCall] = [
    (
        lambda client, filter: client.beta.organization.analytics.skills.list(filter=filter),
        "/v1/organizations/analytics/skills",
        "anthropic.organization.analytics.skills.list",
        True,
    ),
    (
        lambda client, filter: client.beta.organization.analytics.plugins.list(filter=filter),
        "/v1/organizations/analytics/plugins",
        "anthropic.organization.analytics.plugins.list",
        True,
    ),
    (
        lambda client, filter: client.beta.organization.analytics.connectors.list(filter=filter),
        "/v1/organizations/analytics/connectors",
        "anthropic.organization.analytics.connectors.list",
        True,
    ),
    (
        lambda client, filter: client.beta.organization.analytics.users.list(filter=filter),
        "/v1/organizations/analytics/users",
        "anthropic.organization.analytics.users.list",
        False,
    ),
    (
        lambda client, filter: client.beta.organization.analytics.artifacts.list(date="2026-01-01", filter=filter),
        "/v1/organizations/analytics/artifacts",
        "anthropic.organization.analytics.artifacts.list",
        False,
    ),
    (
        lambda client, filter: client.beta.organization.analytics.apps.chat.projects.list(filter=filter),
        "/v1/organizations/analytics/apps/chat/projects",
        "anthropic.organization.analytics.apps.chat.projects.list",
        False,
    ),
    (
        lambda client, filter: client.beta.organization.analytics.summaries.list(
            starting_date="2026-01-01", filter=filter
        ),
        "/v1/organizations/analytics/summaries",
        "anthropic.organization.analytics.summaries.list",
        False,
    ),
]

# A parameter that is content only where its value is, which is for the method to say: the parameter, what calls a
# method with a value of it, the method's path, route and span name, and whether the parameter is content there.
ScopedContentCall = tuple[str, Callable[[Any, Any], Any], str, str, str, bool]
SCOPED_CONTENT_CALLS: list[ScopedContentCall] = [
    *[("filter", invoke, path, path, name, is_content) for invoke, path, name, is_content in FILTER_CALLS],
    # A `page` cursor has a value of the row it ends at in it: an email address here, and a memory's path below.
    (
        "page",
        lambda client, page: client.beta.organization.analytics.users.list(page=page),
        "/v1/organizations/analytics/users",
        "/v1/organizations/analytics/users",
        "anthropic.organization.analytics.users.list",
        True,
    ),
    (
        "page",
        lambda client, page: client.beta.memory_stores.memories.list("memstore_1", page=page),
        "/v1/memory_stores/memstore_1/memories",
        "/v1/memory_stores/{memory_store_id}/memories",
        "anthropic.memory_stores.memories.list",
        True,
    ),
    (
        "page",
        lambda client, page: client.beta.organization.analytics.skills.list(page=page),
        "/v1/organizations/analytics/skills",
        "/v1/organizations/analytics/skills",
        "anthropic.organization.analytics.skills.list",
        False,
    ),
]


class TestHttpAttributes:
    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_method_and_route_are_on_the_span_from_its_start(self, sync: bool, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/messages/batches/msgbatch_1").mock(
            return_value=httpx2.Response(200, json={"id": "msgbatch_1"})
        )
        respx_mock.delete("/v1/files/file_1").mock(return_value=httpx2.Response(200, json={"id": "file_1"}))
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        sampler = StartAttributes()
        spans = Spans()
        spans.provider = TracerProvider(sampler=sampler)

        invokes: list[Callable[[Any], Any]] = [
            lambda client: client.messages.batches.retrieve("msgbatch_1"),
            lambda client: client.beta.messages.batches.retrieve("msgbatch_1"),
            lambda client: client.beta.files.delete("file_1"),
            create,
        ]
        for invoke in invokes:
            await call_client(sync, spans, invoke, _strict_response_validation=False)

        started = [(name, start["http.request.method"], start["http.route"]) for name, start in sampler.started]
        assert started == [
            ("anthropic.messages.batches.retrieve", "GET", "/v1/messages/batches/{message_batch_id}"),
            ("anthropic.messages.batches.retrieve", "GET", "/v1/messages/batches/{message_batch_id}"),
            ("anthropic.files.delete", "DELETE", "/v1/files/{file_id}"),
            ("anthropic.messages.create", "POST", "/v1/messages"),
        ]
        # The URL is known only once the first request is built, which is after the span started.
        assert not [key for _, start in sampler.started for key in start if key.startswith("url.")]

    @pytest.mark.skipif(PYDANTIC_V1, reason="parse() needs pydantic v2")
    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_stream_and_parse_helpers_have_the_route(self, beta: bool, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[stream_response(), httpx2.Response(200, json=MESSAGE)])
        messages = messages_resource(make_client(spans), beta=beta)

        with messages.stream(**REQUEST) as stream:
            stream.until_done()
        messages.parse(**REQUEST)

        for span in spans.named("anthropic.messages.create"):
            assert attributes(span)["http.request.method"] == "POST"
            assert attributes(span)["http.route"] == "/v1/messages"
            assert attributes(span)["url.full"] == f"{base_url}/v1/messages"

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_stream_and_parse_helpers_have_the_route(
        self, beta: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        if PYDANTIC_V1:
            pytest.skip("parse() needs pydantic v2")
        respx_mock.post("/v1/messages").mock(side_effect=[stream_response(), httpx2.Response(200, json=MESSAGE)])
        messages = messages_resource(make_async_client(spans), beta=beta)

        async with messages.stream(**REQUEST) as stream:
            await stream.until_done()
        await messages.parse(**REQUEST)

        for span in spans.named("anthropic.messages.create"):
            assert attributes(span)["http.request.method"] == "POST"
            assert attributes(span)["http.route"] == "/v1/messages"
            assert attributes(span)["url.full"] == f"{base_url}/v1/messages"

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url="https://api.example.com:8443/proxy")
    async def test_url_attributes_are_the_parts_of_the_url_that_the_request_goes_to(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/v1/files/a%2Fb").mock(return_value=httpx2.Response(200, json={"id": "a/b"}))

        await call_client(
            sync,
            spans,
            lambda client: client.beta.files.retrieve_metadata("a/b"),
            base_url="https://api.example.com:8443/proxy",
            _strict_response_validation=False,
        )

        span = spans.one("anthropic.files.retrieve_metadata")
        assert attributes(span)["http.route"] == "/v1/files/{file_id}"
        assert attributes(span)["server.address"] == "api.example.com"
        assert attributes(span)["server.port"] == 8443
        assert url_attributes(span) == {
            "url.scheme": "https",
            "url.path": "/proxy/v1/files/a%2Fb",
            "url.full": "https://api.example.com:8443/proxy/v1/files/a%2Fb",
        }

    @pytest.mark.respx(base_url=base_url)
    def test_url_full_has_a_port_only_when_the_url_has_one(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("https://api.example.com/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        respx_mock.post("http://[::1]:4010/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))

        create(make_client(spans, base_url="https://api.example.com"))
        create(make_client(spans, base_url="http://[::1]:4010"))

        default_port, ipv6 = spans.named("anthropic.messages.create")
        assert attributes(default_port)["server.port"] == 443
        assert attributes(default_port)["url.full"] == "https://api.example.com/v1/messages"
        assert attributes(ipv6)["server.address"] == "::1"
        assert attributes(ipv6)["url.full"] == "http://[::1]:4010/v1/messages"

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize(
        "client_base_url, port",
        [
            ("https://api.example.com", 443),
            ("http://api.example.com", 80),
            ("https://api.example.com:443", 443),
            ("http://api.example.com:8080/proxy", 8080),
        ],
    )
    @pytest.mark.respx()
    async def test_server_port_is_the_base_urls_or_else_the_one_of_its_scheme(
        self, client_base_url: str, port: int, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post(host="api.example.com").mock(return_value=httpx2.Response(200, json=MESSAGE))

        await call_client(sync, spans, create, base_url=client_base_url)

        span = spans.one("anthropic.messages.create")
        assert attributes(span)["server.address"] == "api.example.com"
        assert attributes(span)["server.port"] == port
        # The full URL has a port only when the request's URL names one, which a scheme's own port is not.
        in_url = f":{port}" if port == 8080 else ""
        assert attributes(span)["url.full"].startswith(
            f"{client_base_url.partition('://')[0]}://api.example.com{in_url}/"
        )

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize("content_mode", ["metadata_only", "content"])
    @pytest.mark.parametrize(
        "call", CONTENT_QUERY_CALLS, ids=[call[3].partition("=")[0] for call in CONTENT_QUERY_CALLS]
    )
    @pytest.mark.respx(base_url=base_url)
    async def test_a_query_that_is_content_needs_content_mode_and_so_does_the_full_url(
        self, call: ContentQueryCall, content_mode: str, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        invoke, method, path, query, name = call
        route = respx_mock.route(method=method, path=path).mock(
            return_value=httpx2.Response(200, json={"data": [], "next_page": None, "has_more": False})
        )

        await call_client(
            sync,
            spans,
            invoke,
            open_telemetry=spans.option(traces={"content_mode": content_mode}),
            _strict_response_validation=False,
        )

        [request] = requests(route)
        assert query in request.url.query.decode()
        span = spans.one(name)
        if content_mode == "content":
            assert attributes(span)["url.query"] == query
            assert attributes(span)["url.full"] == f"{base_url}{path}?{query}"
        else:
            assert "url.query" not in attributes(span)
            assert "url.full" not in attributes(span)
        # Whatever the mode, the span has every other attribute of the request.
        assert attributes(span)["url.scheme"] == "http"
        assert_http_attributes(span, method, path)

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize("content_mode", ["metadata_only", "content"])
    @pytest.mark.respx(base_url=base_url)
    async def test_an_organization_method_has_a_span_and_its_email_query_needs_content_mode(
        self, content_mode: str, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        route = respx_mock.get("/v1/organizations/users").mock(return_value=httpx2.Response(200, json=EMPTY_PAGE))

        await call_client(
            sync,
            spans,
            lambda client: client.organization.users.list(email="a@example.com", limit=5),
            open_telemetry=spans.option(traces={"content_mode": content_mode}),
        )

        [request] = requests(route)
        assert request.url.query == b"email=a%40example.com&limit=5"
        span = spans.one("anthropic.organization.users.list")
        assert attributes(span)["http.request.method"] == "GET"
        assert attributes(span)["http.route"] == "/v1/organizations/users"
        assert attributes(span)["url.path"] == "/v1/organizations/users"
        if content_mode == "content":
            assert attributes(span)["url.query"] == "email=a%40example.com&limit=5"
            assert attributes(span)["url.full"] == f"{base_url}/v1/organizations/users?email=a%40example.com&limit=5"
        else:
            assert "url.query" not in attributes(span)
            assert "url.full" not in attributes(span)

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize("content_mode", ["metadata_only", "content"])
    @pytest.mark.parametrize(
        "call",
        SCOPED_CONTENT_CALLS,
        ids=[f"{call[0]}-{call[2].rpartition('/')[2]}" for call in SCOPED_CONTENT_CALLS],
    )
    @pytest.mark.respx(base_url=base_url)
    async def test_a_parameter_is_content_only_on_the_endpoints_where_its_value_is(
        self, call: ScopedContentCall, content_mode: str, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        parameter, invoke, path, http_route, name, is_content = call
        route = respx_mock.get(path).mock(return_value=httpx2.Response(200, json={"data": [], "next_page": None}))
        argument: Any
        if parameter == "filter":
            # A name where the endpoint matches names, and an ID on the others.
            value = "skill_name:Quarterly" if is_content else "user_id:user_1"
            argument, query = [value], "filter%5B%5D=" + value.replace(":", "%3A")
        else:
            argument, query = "page_abc", "page=page_abc"

        await call_client(
            sync,
            spans,
            lambda client: invoke(client, argument),
            open_telemetry=spans.option(traces={"content_mode": content_mode}),
            _strict_response_validation=False,
        )

        [request] = requests(route)
        assert query in request.url.query.decode().split("&")
        span = spans.one(name)
        assert attributes(span)["http.route"] == http_route
        assert attributes(span)["url.path"] == path
        if is_content and content_mode == "metadata_only":
            assert "url.query" not in attributes(span)
            assert "url.full" not in attributes(span)
        else:
            assert query in attributes(span)["url.query"].split("&")
            assert attributes(span)["url.full"] == f"{base_url}{path}?" + attributes(span)["url.query"]

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize("content_mode", ["metadata_only", "content"])
    @pytest.mark.respx(base_url=base_url)
    async def test_a_query_that_is_no_content_is_there_in_both_modes(
        self, content_mode: str, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/v1/files").mock(return_value=httpx2.Response(200, json=EMPTY_PAGE))

        await call_client(
            sync,
            spans,
            # This endpoint defines no `email`, so the query that the span has is without the caller's.
            lambda client: client.beta.files.list(limit=5, extra_query={"email": "a@example.com"}),
            open_telemetry=spans.option(traces={"content_mode": content_mode}),
        )

        span = spans.one("anthropic.files.list")
        assert attributes(span)["url.query"] == "limit=5"
        assert attributes(span)["url.full"] == f"{base_url}/v1/files?limit=5"

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_a_name_that_only_starts_with_a_content_parameter_is_left_out(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        path = "/v1/organizations/analytics/skills"
        route = respx_mock.get(path).mock(return_value=httpx2.Response(200, json={"data": [], "next_page": None}))

        await call_client(
            sync,
            spans,
            lambda client: client.beta.organization.analytics.skills.list(
                limit=5, extra_query={"filter[a]": "skill_name:Quarterly"}
            ),
            _strict_response_validation=False,
        )

        [request] = requests(route)
        assert "filter%5Ba%5D=skill_name%3AQuarterly" in request.url.query.decode().split("&")
        span = spans.one("anthropic.organization.analytics.skills.list")
        assert attributes(span)["url.query"] == "limit=5"
        assert attributes(span)["url.full"] == f"{base_url}{path}?limit=5"

    @pytest.mark.parametrize(
        "query, content_names, content",
        [
            # A name of `CONTENT_QUERY_PARAMS` is content whether or not the method names it.
            ("email=a%40example.com", (), True),
            ("limit=5&path_prefix=%2Fnotes", (), True),
            ("expected_content_sha256=abc", ("filter",), True),
            ("filter%5B%5D=skill_name%3AQuarterly&limit=5", ("filter",), True),
            ("filter[]=skill_name%3AQuarterly", ("filter",), True),
            ("%66ilter%5B%5D=skill_name%3AQuarterly", ("filter",), True),
            ("filter=skill_name%3AQuarterly", ("filter",), True),
            # Only the whole name, or the array of it, is the parameter.
            ("filter[a]=x", ("filter",), False),
            ("filter%5Ba%5D%5B%5D=x&email[x]=a%40example.com", ("filter",), False),
            ("created_at%5Bgte%5D=1", ("created_at[gte]",), True),
            ("filter%5B%5D=user_id%3Auser_1&limit=5", (), False),
            ("limit=5&after_id=user_1", ("filter",), False),
            ("email_domain=example.com", (), False),
            ("", ("filter",), False),
        ],
    )
    def test_is_content_query(self, query: str, content_names: tuple[str, ...], content: bool) -> None:
        assert is_content_query(query, content_names) is content

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_url_query_has_only_the_parameters_that_the_endpoint_defines(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        route = respx_mock.get("/v1/files").mock(return_value=httpx2.Response(200, json=EMPTY_PAGE))

        await call_client(
            sync,
            spans,
            lambda client: client.beta.files.list(
                limit=5, ids=["file 1", "file_2"], extra_query={"trace": "on", "scope_id": "a&b", "limit[x]": "1"}
            ),
            default_query={"tenant": "t1"},
        )

        [request] = requests(route)
        assert (
            request.url.query
            == b"tenant=t1&ids%5B%5D=file+1&ids%5B%5D=file_2&limit=5&trace=on&scope_id=a%26b&limit%5Bx%5D=1"
        )
        span = spans.one("anthropic.files.list")
        # What is left is as it was sent, in the order it was sent. A defined parameter stays however the caller set it.
        # `limit[x]` is no parameter of the endpoint, though `limit` is.
        assert attributes(span)["url.query"] == "ids%5B%5D=file+1&ids%5B%5D=file_2&limit=5&scope_id=a%26b"
        assert attributes(span)["url.full"] == f"{base_url}/v1/files?" + attributes(span)["url.query"]

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_url_query_keeps_a_parameter_whose_name_has_brackets_of_its_own(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/v1/sessions").mock(return_value=httpx2.Response(200, json={"data": [], "next_page": None}))

        await call_client(
            sync,
            spans,
            lambda client: client.beta.sessions.list(
                created_at_gte="2024-01-01T00:00:00Z", extra_query={"created_at[before]": "x"}
            ),
        )

        # `created_at[gte]` is a parameter of the endpoint, and `created_at` is not, so `created_at[before]` is none.
        assert url_attributes(spans.one("anthropic.sessions.list"))["url.query"] == (
            "created_at%5Bgte%5D=2024-01-01T00%3A00%3A00Z"
        )

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize(
        "call",
        DECLARED_QUERY_CALLS,
        ids=["lifecycle", "beta_lifecycle", "include_default", "beta_include_default", "statuses"],
    )
    @pytest.mark.respx(base_url=base_url)
    async def test_url_query_has_each_parameter_that_the_method_declares(
        self, call: DeclaredQueryCall, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        invoke, path, query, name = call
        respx_mock.get(path).mock(return_value=httpx2.Response(200, json={**EMPTY_PAGE, "next_page": None}))

        await call_client(sync, spans, invoke, _strict_response_validation=False)

        span = spans.one(name)
        assert attributes(span)["url.query"] == query
        assert attributes(span)["url.full"] == f"{base_url}{path}?{query}"

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_no_url_query_when_no_defined_parameter_is_sent(
        self, beta: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/v1/messages/batches").mock(return_value=httpx2.Response(200, json=EMPTY_PAGE))
        client = make_client(spans)

        (client.beta if beta else client).messages.batches.list(extra_query={"trace": "on"})

        span = spans.one("anthropic.messages.batches.list")
        assert "url.query" not in attributes(span)
        assert attributes(span)["url.full"] == f"{base_url}/v1/messages/batches"

    @pytest.mark.parametrize(
        ("query", "names", "kept"),
        [
            ("limit=1&beta=true", ("limit",), "limit=1"),
            ("ids[]=a&ids%5B%5D=b&ids%5b%5d=c", ("ids",), "ids[]=a&ids%5B%5D=b&ids%5b%5d=c"),
            ("%6Cimit=1&l%69mit=2&limits=3", ("limit",), "%6Cimit=1&l%69mit=2"),
            ("created_at%5Bgte%5D=1&created_at%5Blt%5D=2", ("created_at[gte]",), "created_at%5Bgte%5D=1"),
            # A name is whole: one that only starts with a defined name is not that parameter.
            ("filter[a][b]=1&filterx[a]=2", ("filter",), ""),
            ("limit%5Bx%5D=1&limit=5&ids%5B%5D=a", ("limit", "ids"), "limit=5&ids%5B%5D=a"),
            ("ids[][]=a&ids[0]=b&[]=c", ("ids",), ""),
            ("page=a%3Db&page&flag", ("page", "flag"), "page=a%3Db&page&flag"),
            ("b=2&a=1&b=3", ("a", "b"), "b=2&a=1&b=3"),
            ("beta=true", ("limit",), ""),
            ("limit=1", (), ""),
            ("", ("limit",), ""),
        ],
    )
    def test_defined_query(self, query: str, names: tuple[str, ...], kept: str) -> None:
        assert defined_query(query, names) == kept

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_a_retried_call_has_the_url_of_its_first_request_and_counts_the_others(
        self, sync: bool, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        overloaded = {"type": "error", "error": {"type": "overloaded_error", "message": "busy"}}
        route = respx_mock.get("/v1/messages/batches").mock(
            side_effect=[
                httpx2.Response(529, json=overloaded),
                httpx2.Response(529, json=overloaded),
                httpx2.Response(200, json=EMPTY_PAGE),
            ]
        )
        monkeypatch.setattr(_base_client.BaseClient, "_calculate_retry_timeout", no_wait)

        def renumber(request: Any, call_next: Callable[[Any], Any]) -> Any:
            return call_next(request.copy(params={"limit": request.retries_taken + 1}))

        async def async_renumber(request: Any, call_next: Callable[[Any], Any]) -> Any:
            return await call_next(request.copy(params={"limit": request.retries_taken + 1}))

        await call_client(
            sync,
            spans,
            lambda client: client.messages.batches.list(),
            max_retries=2,
            middleware=[renumber if sync else async_renumber],
        )

        assert [request.url.query for request in requests(route)] == [b"limit=1", b"limit=2", b"limit=3"]
        span = spans.one("anthropic.messages.batches.list")
        assert attributes(span)["url.query"] == "limit=1"
        assert attributes(span)["url.full"] == f"{base_url}/v1/messages/batches?limit=1"
        assert attributes(span)["http.request.resend_count"] == 2
        assert attributes(span)["http.response.status_code"] == 200

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_a_call_that_is_sent_once_has_no_resend_count(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=MESSAGE), httpx2.Response(400, json={})]
        )

        await call_client(sync, spans, create)
        with pytest.raises(APIStatusError):
            await call_client(sync, spans, create)

        succeeded, failed = spans.named("anthropic.messages.create")
        assert "http.request.resend_count" not in attributes(succeeded)
        assert "http.request.resend_count" not in attributes(failed)

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_a_call_whose_retries_all_fail_counts_them(
        self, sync: bool, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=httpx2.ConnectError("refused"))
        monkeypatch.setattr(_base_client.BaseClient, "_calculate_retry_timeout", no_wait)

        with pytest.raises(APIConnectionError):
            await call_client(sync, spans, create, max_retries=1)

        span = spans.one("anthropic.messages.create")
        assert attributes(span)["http.request.resend_count"] == 1
        assert attributes(span)["url.full"] == f"{base_url}/v1/messages"

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_a_fallback_request_is_a_resend_and_keeps_the_first_url(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        route = respx_mock.get("/v1/messages/batches").mock(return_value=httpx2.Response(200, json=EMPTY_PAGE))

        def send_twice(request: Any, call_next: Callable[[Any], Any]) -> Any:
            call_next(request.copy(params={"limit": 1})).http_response.close()
            return call_next(request.copy(params={"limit": 2}))

        async def async_send_twice(request: Any, call_next: Callable[[Any], Any]) -> Any:
            await (await call_next(request.copy(params={"limit": 1}))).http_response.aclose()
            return await call_next(request.copy(params={"limit": 2}))

        await call_client(
            sync,
            spans,
            lambda client: client.messages.batches.list(),
            middleware=[send_twice if sync else async_send_twice],
        )

        assert len(requests(route)) == 2
        span = spans.one("anthropic.messages.batches.list")
        assert attributes(span)["url.query"] == "limit=1"
        assert attributes(span)["http.request.resend_count"] == 1

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_a_call_that_fails_before_it_sends_a_request_has_no_url(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        def refuse(_request: Any, _call_next: Callable[[Any], Any]) -> Any:
            raise ValueError("refused")

        async def async_refuse(_request: Any, _call_next: Callable[[Any], Any]) -> Any:
            raise ValueError("refused")

        with pytest.raises(ValueError):
            await call_client(sync, spans, create, middleware=[refuse if sync else async_refuse])

        assert not respx_mock.calls
        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.ERROR
        assert attributes(span)["http.request.method"] == "POST"
        assert attributes(span)["http.route"] == "/v1/messages"
        assert url_attributes(span) == {}
        assert "http.request.resend_count" not in attributes(span)

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_a_streamed_call_that_was_retried_has_the_resend_count(
        self, sync: bool, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        overloaded = {"type": "error", "error": {"type": "overloaded_error", "message": "busy"}}
        respx_mock.post("/v1/messages").mock(side_effect=[httpx2.Response(529, json=overloaded), stream_response()])
        monkeypatch.setattr(_base_client.BaseClient, "_calculate_retry_timeout", no_wait)

        stream = await call_client(sync, spans, lambda client: create(client, stream=True), max_retries=1)
        if sync:
            for _ in stream:
                pass
        else:
            async for _ in stream:
                pass

        assert attributes(spans.one("anthropic.messages.create"))["http.request.resend_count"] == 1

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_a_raw_response_that_was_retried_has_the_resend_count(
        self, sync: bool, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        overloaded = {"type": "error", "error": {"type": "overloaded_error", "message": "busy"}}
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(529, json=overloaded), httpx2.Response(200, json=MESSAGE)]
        )
        monkeypatch.setattr(_base_client.BaseClient, "_calculate_retry_timeout", no_wait)

        await call_client(
            sync, spans, lambda client: client.messages.with_raw_response.create(**REQUEST), max_retries=1
        )

        assert attributes(spans.one("anthropic.messages.create"))["http.request.resend_count"] == 1

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_a_redirect_is_not_a_request_of_the_sdk(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(307, headers={"location": "/moved"}))
        respx_mock.post("/moved").mock(return_value=httpx2.Response(200, json=MESSAGE))

        await call_client(sync, spans, create)

        span = spans.one("anthropic.messages.create")
        assert attributes(span)["url.path"] == "/v1/messages"
        assert attributes(span)["url.full"] == f"{base_url}/v1/messages"
        assert "http.request.resend_count" not in attributes(span)

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    async def test_batch_results_has_the_route_whatever_url_the_batch_names(
        self, beta: bool, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        batch = {"id": "msgbatch_1", "results_url": f"{base_url}/v1/messages/batches/msgbatch_1/results?token=abc"}
        respx_mock.get("/v1/messages/batches/msgbatch_1").mock(return_value=httpx2.Response(200, json=batch))
        respx_mock.get("/v1/messages/batches/msgbatch_1/results").mock(return_value=httpx2.Response(200, text=""))

        results = await call_client(
            sync,
            spans,
            lambda client: (client.beta if beta else client).messages.batches.results("msgbatch_1"),
            _strict_response_validation=False,
        )
        if sync:
            results.close()
        else:
            await results.close()

        span = spans.one("anthropic.messages.batches.results")
        assert attributes(span)["http.request.method"] == "GET"
        assert attributes(span)["http.route"] == "/v1/messages/batches/{message_batch_id}/results"
        # `token` is not a parameter that the endpoint defines.
        assert url_attributes(span) == {
            "url.scheme": "http",
            "url.path": "/v1/messages/batches/msgbatch_1/results",
            "url.full": f"{base_url}/v1/messages/batches/msgbatch_1/results",
        }

    @pytest.mark.respx(base_url=base_url)
    def test_batch_results_on_another_host_has_that_host_in_its_url(self, spans: Spans, respx_mock: MockRouter) -> None:
        batch = {"id": "msgbatch_1", "results_url": "https://files.example.com/download/abc"}
        respx_mock.get("/v1/messages/batches/msgbatch_1").mock(return_value=httpx2.Response(200, json=batch))
        respx_mock.get("https://files.example.com/download/abc").mock(return_value=httpx2.Response(200, text=""))

        make_client(spans, _strict_response_validation=False).messages.batches.results("msgbatch_1").close()

        span = spans.one("anthropic.messages.batches.results")
        # `server.address` is the host of the client, and the URL is the one that the request went to.
        assert attributes(span)["server.address"] == "127.0.0.1"
        assert attributes(span)["http.route"] == "/v1/messages/batches/{message_batch_id}/results"
        assert url_attributes(span) == {
            "url.scheme": "https",
            "url.path": "/download/abc",
            "url.full": "https://files.example.com/download/abc",
        }


# Each method whose path has a Session thread's ID: what calls it, and its span's name.
ThreadCall = tuple[Callable[[Any], Any], str]
THREAD_CALLS: list[ThreadCall] = [
    (
        lambda client: client.beta.sessions.threads.retrieve("sthr_1", session_id="sesn_1"),
        "anthropic.sessions.threads.retrieve",
    ),
    (
        lambda client: client.beta.sessions.threads.archive("sthr_1", session_id="sesn_1"),
        "anthropic.sessions.threads.archive",
    ),
    (
        lambda client: client.beta.sessions.threads.events.list("sthr_1", session_id="sesn_1"),
        "anthropic.sessions.threads.events.list",
    ),
    (
        lambda client: client.beta.sessions.threads.events.stream("sthr_1", session_id="sesn_1"),
        "anthropic.sessions.threads.events.stream",
    ),
]


def mock_session_routes(respx_mock: MockRouter) -> None:
    thread = {"id": "sthr_1", "type": "session_thread"}
    page: dict[str, Any] = {"data": [], "next_page": None}
    respx_mock.get("/v1/sessions/sesn_1").mock(return_value=httpx2.Response(200, json={"id": "sesn_1"}))
    respx_mock.get("/v1/sessions/sesn_1/threads").mock(return_value=httpx2.Response(200, json=page))
    respx_mock.get("/v1/sessions/sesn_1/threads/sthr_1").mock(return_value=httpx2.Response(200, json=thread))
    respx_mock.post("/v1/sessions/sesn_1/threads/sthr_1/archive").mock(return_value=httpx2.Response(200, json=thread))
    respx_mock.get("/v1/sessions/sesn_1/threads/sthr_1/events").mock(return_value=httpx2.Response(200, json=page))
    respx_mock.get("/v1/sessions/sesn_1/threads/sthr_1/stream").mock(
        return_value=httpx2.Response(200, content=sse([]), headers={"content-type": "text/event-stream"})
    )


async def close_stream(result: object) -> None:
    """Closes `result` when it is a stream, which ends the span of its call."""
    if isinstance(result, Stream):
        result.close()
    elif isinstance(result, AsyncStream):
        await result.close()


def test_option_types_are_exported() -> None:
    import anthropic
    from anthropic import _types

    for name in (
        "OpenTelemetryClientOption",
        "OpenTelemetryOptions",
        "OpenTelemetryTraces",
        "ResolvedOpenTelemetryOptions",
        "ResolvedOpenTelemetryTraces",
    ):
        assert name in anthropic.__all__
        assert getattr(anthropic, name) is getattr(_types, name)

    traces: anthropic.OpenTelemetryTraces = {"enabled": False, "content_mode": "content", "max_content_bytes": 1}
    options: anthropic.OpenTelemetryOptions = {"traces": traces}
    option: anthropic.OpenTelemetryClientOption = options
    assert Anthropic(api_key="key", open_telemetry=option) is not None
    assert not hasattr(anthropic, "OpenTelemetrySignals")


def test_the_option_read_from_a_client_type_checks_as_an_option_of_a_copy() -> None:
    """The type checker checks these lines, which have no cast: what a client reads back spreads into an option."""
    import anthropic

    client = Anthropic(api_key="key", open_telemetry={"traces": {"max_content_bytes": 4096}})
    async_client = AsyncAnthropic(api_key="key")

    resolved: anthropic.ResolvedOpenTelemetryOptions = client.open_telemetry
    traces: anthropic.ResolvedOpenTelemetryTraces = async_client.open_telemetry["traces"]
    enabled: bool = client.open_telemetry["traces"]["enabled"]
    max_content_bytes: int = client.open_telemetry["traces"]["max_content_bytes"]
    option: anthropic.OpenTelemetryOptions = {**resolved, "conversation_id": "conv_1"}
    copy = client.with_options(open_telemetry={**client.open_telemetry, "conversation_id": "conv_1"})
    async_copy = async_client.copy(open_telemetry={**async_client.open_telemetry, "traces": traces})
    rebuilt = Anthropic(api_key="key", open_telemetry={**resolved})

    assert (enabled, max_content_bytes) == (True, 4096)
    assert copy.open_telemetry == option == {**resolved, "conversation_id": "conv_1"}
    assert async_copy.open_telemetry == async_client.open_telemetry
    assert rebuilt.open_telemetry == resolved


async def call(client: Any) -> Any:
    """Creates a Message with a synchronous or an asynchronous client."""
    result = create(client)
    return await result if inspect.isawaitable(result) else result


@SYNC_AND_ASYNC
@pytest.mark.parametrize("traces", [True, False], ids=["spans_on", "spans_off"])
@pytest.mark.respx(base_url=base_url)
async def test_debug_logging_dumps_the_request_options_with_their_span_fields(
    traces: bool, sync: bool, spans: Spans, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
) -> None:
    route = respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
    make: Callable[..., Any] = make_client if sync else make_async_client
    client = make(spans, open_telemetry=spans.option(traces=traces))

    # The debug log is what dumps the request options model, which pydantic has to have built in full by then.
    with caplog.at_level(logging.DEBUG, logger="anthropic"):
        await call(client)

    assert len(requests(route)) == 1
    [logged] = [record.getMessage() for record in caplog.records if record.msg == "Request options: %s"]
    assert "'span_attributes'" in logged


def platform_clients(open_telemetry: OpenTelemetryClientOption) -> list[Any]:
    """One client of each platform class, sync and async, with the `open_telemetry` option."""
    aws: dict[str, Any] = {"aws_region": "us-east-1", "aws_access_key": "access", "aws_secret_key": "secret"}
    vertex: dict[str, Any] = {"region": "us-east5", "project_id": "project", "access_token": "token"}
    google_cloud: dict[str, Any] = {
        "base_url": base_url,
        "workspace_id": "wrkspc_1",
        "token_provider": lambda: "token",
    }
    return [
        AnthropicBedrock(**aws, open_telemetry=open_telemetry),
        AsyncAnthropicBedrock(**aws, open_telemetry=open_telemetry),
        AnthropicBedrockMantle(aws_region="us-east-1", api_key="key", open_telemetry=open_telemetry),
        AsyncAnthropicBedrockMantle(aws_region="us-east-1", api_key="key", open_telemetry=open_telemetry),
        AnthropicVertex(**vertex, open_telemetry=open_telemetry),
        AsyncAnthropicVertex(**vertex, open_telemetry=open_telemetry),
        AnthropicFoundry(api_key="key", resource="resource", open_telemetry=open_telemetry),
        AsyncAnthropicFoundry(api_key="key", resource="resource", open_telemetry=open_telemetry),
        AnthropicAWS(skip_auth=True, base_url=base_url, open_telemetry=open_telemetry),
        AsyncAnthropicAWS(skip_auth=True, base_url=base_url, open_telemetry=open_telemetry),
        AnthropicGoogleCloud(**google_cloud, open_telemetry=open_telemetry),
        AsyncAnthropicGoogleCloud(**google_cloud, open_telemetry=open_telemetry),
    ]


DEFAULT_TRACES: dict[str, Any] = {
    "enabled": True,
    "content_mode": "metadata_only",
    "max_content_bytes": CONTENT_LIMIT,
}

# A request whose content is over 300 characters with its first message and under it without.
OLD_AND_NEW: list[dict[str, Any]] = [
    {"role": "user", "content": "old " + "x" * 200},
    {"role": "user", "content": "new"},
]


class TestTracesOption:
    @SYNC_AND_ASYNC
    @pytest.mark.parametrize(
        "traces",
        [
            False,
            {"enabled": False},
            # The other settings of disabled traces are not used.
            {"enabled": False, "content_mode": "content", "max_content_bytes": 100},
        ],
        ids=["false", "enabled_false", "enabled_false_with_other_settings"],
    )
    @pytest.mark.respx(base_url=base_url)
    async def test_disabled_traces_have_no_spans(
        self, traces: Any, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        route = respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        make: Callable[..., Any] = make_client if sync else make_async_client

        # The variable does not enable what the option disables.
        with update_env(ANTHROPIC_OPEN_TELEMETRY="true"):
            client = make(spans, open_telemetry=spans.option(traces=traces))
        await call(client)

        assert spans.finished == ()
        assert "traceparent" not in requests(route)[0].headers
        assert client.open_telemetry["traces"]["enabled"] is False

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize("traces", [True, {"enabled": True}], ids=["true", "enabled_true"])
    @pytest.mark.respx(base_url=base_url)
    async def test_enabled_traces_have_spans(
        self, traces: Any, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        make: Callable[..., Any] = make_client if sync else make_async_client

        # The variable is for a client that is given no option.
        with update_env(ANTHROPIC_OPEN_TELEMETRY="false"):
            client = make(spans, open_telemetry=spans.option(traces=traces))
        await call(client)

        assert len(spans.named("anthropic.messages.create")) == 1
        assert client.open_telemetry["traces"] == DEFAULT_TRACES

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize(
        "option",
        [
            {},
            {"conversation_id": "c"},
            {"traces": {}},
            {"traces": True},
            {"traces": {"max_content_bytes": 4096}},
            {"traces": {"enabled": None, "content_mode": None, "max_content_bytes": None}},
        ],
        ids=["tracer_provider_alone", "conversation_id", "empty_traces", "traces_true", "max_content_bytes", "none"],
    )
    @pytest.mark.respx(base_url=base_url)
    async def test_the_variables_do_not_reach_a_client_that_is_given_the_option(
        self, option: dict[str, Any], sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        make: Callable[..., Any] = make_client if sync else make_async_client

        with update_env(
            ANTHROPIC_OPEN_TELEMETRY="false",
            ANTHROPIC_OPEN_TELEMETRY_TRACES_CONTENT_MODE="content",
            ANTHROPIC_OPEN_TELEMETRY_TRACES_MAX_CONTENT_BYTES="300",
            ANTHROPIC_OPEN_TELEMETRY_PROPAGATION="false",
        ):
            client = make(spans, open_telemetry=spans.option(**option))
        await call(client)

        # What the option leaves out has the default.
        traces: dict[str, Any] = option["traces"] if isinstance(option.get("traces"), dict) else {}
        given = {name: value for name, value in traces.items() if value is not None}
        assert client.open_telemetry["traces"] == {**DEFAULT_TRACES, **given}
        assert client.open_telemetry["propagation"] is True
        assert "gen_ai.input.messages" not in attributes(spans.one("anthropic.messages.create"))

    @SYNC_AND_ASYNC
    def test_the_variables_do_not_reach_a_client_that_is_given_false(self, sync: bool) -> None:
        make = cast("Callable[..., Any]", Anthropic if sync else AsyncAnthropic)

        with update_env(
            ANTHROPIC_OPEN_TELEMETRY="true",
            ANTHROPIC_OPEN_TELEMETRY_TRACES_CONTENT_MODE="content",
            ANTHROPIC_OPEN_TELEMETRY_TRACES_MAX_CONTENT_BYTES="300",
            ANTHROPIC_OPEN_TELEMETRY_PROPAGATION="false",
        ):
            client = make(api_key="key", open_telemetry=False)

        assert client.open_telemetry == {"propagation": True, "traces": {**DEFAULT_TRACES, "enabled": False}}

    def test_the_variables_do_not_reach_a_platform_client_that_is_given_the_option(self, spans: Spans) -> None:
        options: list[tuple[OpenTelemetryClientOption, dict[str, Any]]] = [
            ({}, {}),
            (spans.option(), {}),
            ({"traces": {"max_content_bytes": 4096}}, {"max_content_bytes": 4096}),
        ]

        with update_env(
            ANTHROPIC_OPEN_TELEMETRY="false",
            ANTHROPIC_OPEN_TELEMETRY_TRACES_CONTENT_MODE="content",
            ANTHROPIC_OPEN_TELEMETRY_TRACES_MAX_CONTENT_BYTES="300",
            ANTHROPIC_OPEN_TELEMETRY_PROPAGATION="false",
        ):
            for option, given in options:
                for client in platform_clients(option):
                    # A copy that is given its own option is resolved as a new client is.
                    for resolved in (client.open_telemetry, client.copy(open_telemetry=option).open_telemetry):
                        assert resolved["propagation"] is True
                        assert resolved["traces"] == {**DEFAULT_TRACES, **given}
            for client in platform_clients(False):
                assert client.open_telemetry == {"propagation": True, "traces": {**DEFAULT_TRACES, "enabled": False}}

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize("source", ["option", "variable"])
    @pytest.mark.respx(base_url=base_url)
    async def test_max_content_bytes_is_the_size_bound(
        self, source: str, sync: bool, registered: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        make: Callable[..., Any] = make_client if sync else make_async_client
        if source == "option":
            with update_env(ANTHROPIC_OPEN_TELEMETRY_TRACES_MAX_CONTENT_BYTES="100000"):
                bounded = make(
                    registered, open_telemetry={"traces": {"content_mode": "content", "max_content_bytes": 300}}
                )
        else:
            with update_env(
                ANTHROPIC_OPEN_TELEMETRY_TRACES_CONTENT_MODE="content",
                ANTHROPIC_OPEN_TELEMETRY_TRACES_MAX_CONTENT_BYTES="300",
            ):
                bounded = make(registered, open_telemetry=None)
        assert bounded.open_telemetry["traces"]["max_content_bytes"] == 300

        await call_messages(bounded, OLD_AND_NEW)
        await call_messages(make(registered, open_telemetry={"traces": {"content_mode": "content"}}), OLD_AND_NEW)

        cut, whole = registered.named("anthropic.messages.create")
        # The oldest part goes, as it does over the default bound.
        assert [message["parts"] for message in json.loads(attributes(cut)[INPUT])] == [[], [text_part("new")]]
        assert attributes(cut)["anthropic.content.truncated"] is True
        assert content_size(cut) <= 300
        assert [len(message["parts"]) for message in json.loads(attributes(whole)[INPUT])] == [1, 1]
        assert "anthropic.content.truncated" not in attributes(whole)

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    async def test_max_content_bytes_bounds_a_streamed_message_too(
        self, beta: bool, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response())
        make: Callable[..., Any] = make_client if sync else make_async_client
        client = make(spans, open_telemetry=spans.option(traces={"content_mode": "content", "max_content_bytes": 300}))
        request = {**REQUEST, "messages": OLD_AND_NEW}

        if sync:
            with messages_resource(client, beta=beta).stream(**request) as stream:
                stream.until_done()
        else:
            async with messages_resource(client, beta=beta).stream(**request) as async_stream:
                await async_stream.until_done()

        span = spans.one("anthropic.messages.create")
        assert [message["parts"] for message in json.loads(attributes(span)[INPUT])] == [[], [text_part("new")]]
        assert json.loads(attributes(span)[OUTPUT])[0]["parts"] == [text_part("Hi there")]
        assert attributes(span)["anthropic.content.truncated"] is True
        assert content_size(span) <= 300

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize(
        "value",
        ["", " ", "0", "-5", "+5", "1.5", "many", "1e3", "1_000", "3 00", "\u0663\u0660\u0660", "9" * 5000],
        ids=["empty", "space", "0", "-5", "+5", "1.5", "many", "1e3", "1_000", "3 00", "arabic_digits", "5000_digits"],
    )
    @pytest.mark.respx(base_url=base_url)
    async def test_a_max_content_bytes_variable_that_is_not_valid_is_ignored(
        self, value: str, sync: bool, registered: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        make: Callable[..., Any] = make_client if sync else make_async_client

        with update_env(
            ANTHROPIC_OPEN_TELEMETRY_TRACES_CONTENT_MODE="content",
            ANTHROPIC_OPEN_TELEMETRY_TRACES_MAX_CONTENT_BYTES=value,
        ):
            client = make(registered, open_telemetry=None)
        await call_messages(client, OLD_AND_NEW)

        assert client.open_telemetry["traces"]["max_content_bytes"] == CONTENT_LIMIT
        assert "anthropic.content.truncated" not in attributes(registered.one("anthropic.messages.create"))

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize("value", ["300", " 300 ", "\t300\n", "0300"])
    def test_a_max_content_bytes_variable_is_decimal_digits_with_or_without_whitespace_around_them(
        self, value: str, sync: bool
    ) -> None:
        make = cast("Callable[..., Any]", Anthropic if sync else AsyncAnthropic)

        with update_env(ANTHROPIC_OPEN_TELEMETRY_TRACES_MAX_CONTENT_BYTES=value):
            client = make(api_key="key")

        assert client.open_telemetry["traces"]["max_content_bytes"] == 300

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize(("given", "resolved"), [(0, CONTENT_LIMIT), (-1, CONTENT_LIMIT), (1, 1)])
    def test_a_max_content_bytes_option_below_1_is_the_default(self, given: int, resolved: int, sync: bool) -> None:
        make = cast("Callable[..., Any]", Anthropic if sync else AsyncAnthropic)

        # The variable is for a client that is given no option, so it does not stand in for the option.
        with update_env(ANTHROPIC_OPEN_TELEMETRY_TRACES_MAX_CONTENT_BYTES="4096"):
            client = make(api_key="key", open_telemetry={"traces": {"max_content_bytes": given}})

        assert client.open_telemetry["traces"]["max_content_bytes"] == resolved

    @SYNC_AND_ASYNC
    def test_the_variables_are_read_under_their_traces_names_only(self, sync: bool) -> None:
        make = cast("Callable[..., Any]", Anthropic if sync else AsyncAnthropic)

        with update_env(
            ANTHROPIC_OPEN_TELEMETRY_CONTENT_MODE="content", ANTHROPIC_OPEN_TELEMETRY_MAX_CONTENT_BYTES="300"
        ):
            assert make(api_key="key").open_telemetry == {"propagation": True, "traces": DEFAULT_TRACES}

        with update_env(
            ANTHROPIC_OPEN_TELEMETRY_TRACES_CONTENT_MODE="content",
            ANTHROPIC_OPEN_TELEMETRY_TRACES_MAX_CONTENT_BYTES="300",
        ):
            assert make(api_key="key").open_telemetry == {
                "propagation": True,
                "traces": {"enabled": True, "content_mode": "content", "max_content_bytes": 300},
            }
            assert make(api_key="key", open_telemetry=None).open_telemetry == make(api_key="key").open_telemetry
            # An empty option is an option.
            assert make(api_key="key", open_telemetry={}).open_telemetry == {
                "propagation": True,
                "traces": DEFAULT_TRACES,
            }


TRACE_CONTEXT_HEADERS = ("traceparent", "tracestate", "baggage")


class CountingPropagator(TextMapPropagator):
    """The propagator that the application registered, counting what it is asked to inject."""

    def __init__(self, inner: TextMapPropagator) -> None:
        self.inner = inner
        self.injections = 0

    @override
    def extract(self, carrier: Any, context: Context | None = None, getter: Any = None) -> Context:
        return self.inner.extract(carrier, context)

    @override
    def inject(self, carrier: Any, context: Context | None = None, setter: Any = None) -> None:
        self.injections += 1
        self.inner.inject(carrier, context)

    @property
    @override
    def fields(self) -> set[str]:
        return self.inner.fields


class KeptSpanIds(RandomIdGenerator):
    """Keeps the ID of each span that its provider starts, which a span that the sampler drops shows nowhere else."""

    def __init__(self) -> None:
        self.span_ids: list[int] = []

    @override
    def generate_span_id(self) -> int:
        self.span_ids.append(super().generate_span_id())
        return self.span_ids[-1]


@contextmanager
def application_trace_context() -> Iterator[CountingPropagator]:
    """Runs with a sampled span and a baggage entry current, as an instrumented application calls the SDK."""
    parent = trace.NonRecordingSpan(
        trace.SpanContext(
            trace_id=0x1234,
            span_id=0x5678,
            is_remote=True,
            trace_flags=trace.TraceFlags(trace.TraceFlags.SAMPLED),
            trace_state=trace.TraceState([("vendor", "value")]),
        )
    )
    registered = propagate.get_global_textmap()
    counting = CountingPropagator(registered)
    propagate.set_global_textmap(counting)
    token = context.attach(baggage.set_baggage("tenant", "acme", trace.set_span_in_context(parent)))
    try:
        yield counting
    finally:
        context.detach(token)
        propagate.set_global_textmap(registered)


class TestPropagationOption:
    @SYNC_AND_ASYNC
    @pytest.mark.parametrize("provider", ["recording", "no_op"])
    @pytest.mark.respx(base_url=base_url)
    async def test_requests_carry_the_trace_context_by_default(
        self, provider: str, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        route = respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        make: Callable[..., Any] = make_client if sync else make_async_client
        option = spans.option() if provider == "recording" else {"tracer_provider": trace.NoOpTracerProvider()}
        client = make(spans, open_telemetry=option)

        with application_trace_context():
            await call(client)

        [request] = requests(route)
        assert client.open_telemetry["propagation"] is True
        assert request.headers["baggage"] == "tenant=acme"
        assert request.headers["tracestate"] == "vendor=value"
        if provider == "recording":
            call_span = spans.one("anthropic.messages.create")
            assert request.headers["traceparent"] == "00-{:032x}-{:016x}-01".format(0x1234, span_id(call_span))

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize("provider", ["recording", "no_op"])
    @pytest.mark.respx(base_url=base_url)
    async def test_false_sends_no_trace_context_and_keeps_the_span(
        self, provider: str, sync: bool, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(_base_client.BaseClient, "_calculate_retry_timeout", no_wait)
        route = respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(500, json={}), httpx2.Response(200, json=MESSAGE)]
        )
        make: Callable[..., Any] = make_client if sync else make_async_client
        option = spans.option() if provider == "recording" else {"tracer_provider": trace.NoOpTracerProvider()}
        client = make(spans, open_telemetry={**option, "propagation": False}, max_retries=1)

        with application_trace_context() as propagator:
            await call(client)

        # The retry carries none either, and the SDK does not ask the propagator for anything.
        assert len(requests(route)) == 2
        for request in requests(route):
            assert [name for name in TRACE_CONTEXT_HEADERS if name in request.headers] == []
        assert propagator.injections == 0
        assert client.open_telemetry["propagation"] is False
        if provider == "recording":
            call_span = spans.one("anthropic.messages.create")
            assert call_span.status.status_code == StatusCode.OK
            assert call_span.end_time is not None
            assert trace_id(call_span) == 0x1234
            assert attributes(call_span)["http.request.resend_count"] == 1

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_false_keeps_a_span_that_the_sampler_dropped_current_for_the_requests(
        self, sync: bool, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(_base_client.BaseClient, "_calculate_retry_timeout", no_wait)
        current: list[trace.SpanContext] = []

        def respond(_request: httpx2.Request) -> httpx2.Response:
            # What instrumentation of the HTTP client makes the parent of its own span.
            current.append(trace.get_current_span().get_span_context())
            return httpx2.Response(500, json={}) if len(current) == 1 else httpx2.Response(200, json=MESSAGE)

        route = respx_mock.post("/v1/messages").mock(side_effect=respond)
        make: Callable[..., Any] = make_client if sync else make_async_client
        ids = KeptSpanIds()
        dropping = TracerProvider(sampler=sampling.ALWAYS_OFF, id_generator=ids)
        client = make(spans, open_telemetry={"tracer_provider": dropping, "propagation": False}, max_retries=1)

        with application_trace_context() as propagator:
            await call(client)

        # Both requests ran under the call span, which carries the sampler's decision and is not the application's span.
        [call_span_id] = ids.span_ids
        assert call_span_id != 0x5678
        assert [(seen.trace_id, seen.span_id, seen.trace_flags, seen.is_valid) for seen in current] == [
            (0x1234, call_span_id, trace.TraceFlags.DEFAULT, True)
        ] * 2
        # The SDK still writes nothing itself, and does not ask the propagator for anything.
        for request in requests(route):
            assert [name for name in TRACE_CONTEXT_HEADERS if name in request.headers] == []
        assert propagator.injections == 0

        # With no tracer provider and no span of the application, the call span has no valid context and is not current.
        no_provider = {"tracer_provider": trace.NoOpTracerProvider(), "propagation": False}
        await call(make(spans, open_telemetry=no_provider))
        assert not current[-1].is_valid

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize(
        ("variable", "option", "propagates"),
        [
            ("false", None, False),
            ("FALSE", None, False),
            ("true", None, True),
            ("0", None, True),
            ("", None, True),
            # The variable is for a client that is given no option.
            ("false", {}, True),
            ("false", {"traces": True}, True),
            ("false", {"propagation": True}, True),
            ("true", {"propagation": False}, False),
        ],
    )
    @pytest.mark.respx(base_url=base_url)
    async def test_the_variable_sets_propagation_for_a_client_that_is_given_no_option(
        self,
        variable: str,
        option: OpenTelemetryClientOption,
        propagates: bool,
        sync: bool,
        registered: Spans,
        respx_mock: MockRouter,
    ) -> None:
        route = respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        make: Callable[..., Any] = make_client if sync else make_async_client

        with update_env(ANTHROPIC_OPEN_TELEMETRY_PROPAGATION=variable):
            client = make(registered, open_telemetry=option)
        # The variable is read when the client is constructed, and not again.
        with update_env(ANTHROPIC_OPEN_TELEMETRY_PROPAGATION="true" if not propagates else "false"):
            with application_trace_context():
                await call(client)
                await call(client.copy())

        assert client.open_telemetry["propagation"] is propagates
        for request in requests(route):
            assert [name in request.headers for name in TRACE_CONTEXT_HEADERS] == [propagates] * 3
        assert len(registered.named("anthropic.messages.create")) == 2

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_disabled_open_telemetry_sends_no_trace_context(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        route = respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        make: Callable[..., Any] = make_client if sync else make_async_client

        with application_trace_context() as propagator:
            await call(make(spans, open_telemetry=False))
            await call(make(spans, open_telemetry=spans.option(traces=False, propagation=True)))

        for request in requests(route):
            assert [name for name in TRACE_CONTEXT_HEADERS if name in request.headers] == []
        assert propagator.injections == 0
        assert spans.finished == ()

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_with_options_replaces_propagation_with_the_rest_of_the_option(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        route = respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        make: Callable[..., Any] = make_client if sync else make_async_client
        client = make(spans, open_telemetry=spans.option(propagation=False))
        spread = client.with_options(open_telemetry={**client.open_telemetry, "conversation_id": "conv_1"})
        replaced = client.with_options(open_telemetry=spans.option())

        with application_trace_context():
            for called in (client, client.copy(), spread, replaced):
                await call(called)

        sent = [["baggage" in request.headers, "traceparent" in request.headers] for request in requests(route)]
        assert sent == [[False, False], [False, False], [False, False], [True, True]]
        assert [called.open_telemetry["propagation"] for called in (spread, replaced)] == [False, True]
        assert attributes(spans.named("anthropic.messages.create")[2])["gen_ai.conversation.id"] == "conv_1"

    def test_platform_clients_have_the_option(self, spans: Spans) -> None:
        with update_env(ANTHROPIC_OPEN_TELEMETRY_PROPAGATION="false"):
            from_variable = platform_clients(None)
        from_option = platform_clients(spans.option(propagation=False))

        for client in (*from_variable, *from_option):
            assert client.open_telemetry["propagation"] is False
            assert client.copy().open_telemetry["propagation"] is False
        assert all(client.open_telemetry["propagation"] for client in platform_clients(spans.option()))

    @SYNC_AND_ASYNC
    @pytest.mark.respx()
    async def test_signed_request_without_propagation_keeps_a_valid_signature(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        route = respx_mock.post().mock(return_value=httpx2.Response(200, json=MESSAGE))
        options: dict[str, Any] = {
            "aws_region": "us-east-1",
            "aws_access_key": "access",
            "aws_secret_key": "secret",
            "open_telemetry": spans.option(propagation=False),
        }
        # The SDK leaves the header of the application alone, so it is signed and sent as it was given.
        headers = {"traceparent": "00-{:032x}-{:016x}-01".format(0xABCD, 0xEF)}

        with application_trace_context():
            if sync:
                create(AnthropicBedrock(**options), extra_headers=headers)
            else:
                await create(AsyncAnthropicBedrock(**options), extra_headers=headers)

        [request] = requests(route)
        assert request.headers["traceparent"] == headers["traceparent"]
        assert "baggage" not in request.headers and "tracestate" not in request.headers
        authorization = request.headers["Authorization"]
        assert "traceparent" in authorization.split("SignedHeaders=")[1].split(",")[0].split(";")
        assert authorization.endswith("Signature=" + sigv4_signature(request, secret_key="secret"))
        assert spans.one("anthropic.messages.create").status.status_code == StatusCode.OK


async def call_messages(client: Any, messages: list[dict[str, Any]]) -> Any:
    """Creates a Message from `messages` with a synchronous or an asynchronous client."""
    result = client.messages.create(max_tokens=1024, model="claude-test", messages=messages)
    return await result if inspect.isawaitable(result) else result


class TestConversationId:
    @pytest.mark.respx(base_url=base_url)
    def test_client_option(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        respx_mock.get("/v1/models").mock(return_value=httpx2.Response(200, json={"data": [], "has_more": False}))
        client = make_client(spans, open_telemetry=spans.option(conversation_id="conv_1"))

        create(client)
        client.models.list()

        assert attributes(spans.one("anthropic.messages.create"))["gen_ai.conversation.id"] == "conv_1"
        assert attributes(spans.one("anthropic.models.list"))["gen_ai.conversation.id"] == "conv_1"

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize("call", THREAD_CALLS, ids=[call[1] for call in THREAD_CALLS])
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_a_session_threads_span_starts_with_the_threads_id_as_the_conversations(
        self, call: ThreadCall, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        invoke, name = call
        mock_session_routes(respx_mock)
        sampler = StartAttributes()
        spans.provider = TracerProvider(sampler=sampler)

        await close_stream(await call_client(sync, spans, invoke, _strict_response_validation=False))

        # Both are there when the span starts, so a sampler sees them.
        [(started_name, started)] = sampler.started
        assert started_name == name
        assert started["anthropic.session.thread.id"] == "sthr_1"
        assert started["gen_ai.conversation.id"] == "sthr_1"

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize("call", THREAD_CALLS, ids=[call[1] for call in THREAD_CALLS])
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_the_applications_conversation_id_goes_before_a_session_threads(
        self, call: ThreadCall, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        invoke, name = call
        mock_session_routes(respx_mock)
        option = spans.option(conversation_id="conv_1")

        await close_stream(
            await call_client(sync, spans, invoke, open_telemetry=option, _strict_response_validation=False)
        )

        span = spans.one(name)
        assert attributes(span)["gen_ai.conversation.id"] == "conv_1"
        assert attributes(span)["anthropic.session.thread.id"] == "sthr_1"

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_a_span_without_a_session_thread_in_its_path_has_no_conversation_id_of_its_own(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        mock_session_routes(respx_mock)

        await call_client(
            sync, spans, lambda client: client.beta.sessions.retrieve("sesn_1"), _strict_response_validation=False
        )
        await call_client(sync, spans, lambda client: client.beta.sessions.threads.list("sesn_1"))

        for name in ("anthropic.sessions.retrieve", "anthropic.sessions.threads.list"):
            assert attributes(spans.one(name))["anthropic.session.id"] == "sesn_1"
            assert "gen_ai.conversation.id" not in attributes(spans.one(name))

    def test_methods_have_no_keyword_for_it(self, spans: Spans) -> None:
        client = make_client(spans)
        keyword: dict[str, Any] = {"open_telemetry": {"conversation_id": "conv_1"}}

        with pytest.raises(TypeError, match="open_telemetry"):
            create(client, **keyword)
        with pytest.raises(TypeError, match="open_telemetry"):
            client.beta.messages.tool_runner(**REQUEST, tools=[], **keyword)

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_with_options_replaces_the_clients_whole_option(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        make: Callable[..., Any] = make_client if sync else make_async_client
        other = Spans()
        client = make(spans, open_telemetry=spans.option(traces={"content_mode": "content"}, conversation_id="conv_1"))

        # A copy has what it is given and nothing of the client's: no content mode, no conversation ID, no provider.
        await call(client.with_options(open_telemetry=spans.option()))
        await call(client.copy(open_telemetry=spans.option(conversation_id="conv_2")))
        await call(client.with_options(open_telemetry=other.option()))
        await call(client)

        bare, renamed, own = spans.named("anthropic.messages.create")
        assert "gen_ai.conversation.id" not in attributes(bare)
        assert attributes(renamed)["gen_ai.conversation.id"] == "conv_2"
        for span in (bare, renamed, other.one("anthropic.messages.create")):
            assert "gen_ai.input.messages" not in attributes(span)
        # The client keeps its own option.
        assert attributes(own)["gen_ai.conversation.id"] == "conv_1"
        assert "gen_ai.input.messages" in attributes(own)

    @SYNC_AND_ASYNC
    def test_with_options_replaces_traces_whole_too(self, sync: bool, spans: Spans) -> None:
        make: Callable[..., Any] = make_client if sync else make_async_client
        client = make(spans, open_telemetry=spans.option(traces={"content_mode": "content", "max_content_bytes": 100}))

        copy = client.with_options(open_telemetry={"traces": {"max_content_bytes": 200}})

        assert copy.open_telemetry == {
            "propagation": True,
            "traces": {"enabled": True, "content_mode": "metadata_only", "max_content_bytes": 200},
        }
        assert client.open_telemetry == spans.option(
            propagation=True, traces={"enabled": True, "content_mode": "content", "max_content_bytes": 100}
        )

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_a_copy_that_is_not_given_the_option_has_the_clients(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        make: Callable[..., Any] = make_client if sync else make_async_client
        client = make(spans, open_telemetry=spans.option(traces={"content_mode": "content"}, conversation_id="conv_1"))

        for copy in (client.copy(), client.with_options(timeout=5), client.copy().with_options(max_retries=1)):
            assert copy.open_telemetry == client.open_telemetry
            await call(copy)

        created = spans.named("anthropic.messages.create")
        assert [attributes(span)["gen_ai.conversation.id"] for span in created] == ["conv_1"] * 3
        assert all("gen_ai.input.messages" in attributes(span) for span in created)

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_a_copy_that_changes_one_field_starts_from_the_option_read_from_the_client(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        make: Callable[..., Any] = make_client if sync else make_async_client
        client = make(spans, open_telemetry=spans.option(traces={"content_mode": "content", "max_content_bytes": 4096}))
        assert client.open_telemetry == {
            "tracer_provider": spans.provider,
            "propagation": True,
            "traces": {"enabled": True, "content_mode": "content", "max_content_bytes": 4096},
        }

        copy = client.with_options(open_telemetry={**client.open_telemetry, "conversation_id": "conv_1"})
        assert copy.open_telemetry == {**client.open_telemetry, "conversation_id": "conv_1"}
        await call(copy)
        await call(client)

        first, second = spans.named("anthropic.messages.create")
        assert attributes(first)["gen_ai.conversation.id"] == "conv_1"
        assert "gen_ai.conversation.id" not in attributes(second)
        for span in (first, second):
            assert json.loads(attributes(span)["gen_ai.output.messages"])[0]["parts"] == [
                {"type": "text", "content": "Hi there"}
            ]

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_the_option_read_from_a_client_is_a_copy(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        make: Callable[..., Any] = make_client if sync else make_async_client
        client = make(spans, open_telemetry=spans.option(traces=True))
        before = client.open_telemetry

        read: Any = client.open_telemetry
        read["conversation_id"] = "conv_1"
        read["traces"]["enabled"] = False
        read["traces"]["content_mode"] = "content"
        await call(client)
        await call(client.copy())

        assert client.open_telemetry == before
        for span in spans.named("anthropic.messages.create"):
            assert "gen_ai.conversation.id" not in attributes(span)
            assert "gen_ai.input.messages" not in attributes(span)
        assert len(spans.finished) == 2

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize(
        ("given", "traces"),
        [
            (None, {"enabled": True, "content_mode": "metadata_only", "max_content_bytes": CONTENT_LIMIT}),
            ({}, {"enabled": True, "content_mode": "metadata_only", "max_content_bytes": CONTENT_LIMIT}),
            (False, {"enabled": False, "content_mode": "metadata_only", "max_content_bytes": CONTENT_LIMIT}),
            (
                {"traces": False},
                {"enabled": False, "content_mode": "metadata_only", "max_content_bytes": CONTENT_LIMIT},
            ),
            ({"traces": True}, {"enabled": True, "content_mode": "metadata_only", "max_content_bytes": CONTENT_LIMIT}),
            (
                {"traces": {"content_mode": "content"}},
                {"enabled": True, "content_mode": "content", "max_content_bytes": CONTENT_LIMIT},
            ),
            (
                {"traces": {"enabled": False, "max_content_bytes": 10}},
                {"enabled": False, "content_mode": "metadata_only", "max_content_bytes": 10},
            ),
        ],
        ids=["none", "empty", "false", "traces_false", "traces_true", "content_mode", "disabled_with_settings"],
    )
    def test_the_option_read_from_a_client_has_every_field_of_traces(
        self, given: Any, traces: dict[str, Any], sync: bool
    ) -> None:
        client = (Anthropic if sync else AsyncAnthropic)(api_key="key", open_telemetry=given)

        resolved = {"propagation": True, "traces": traces}
        assert client.open_telemetry == resolved
        # It is an option like another: a client that is given it reads back the same.
        assert client.with_options(open_telemetry={**client.open_telemetry}).open_telemetry == resolved

    @pytest.mark.respx(base_url=base_url)
    def test_stream_helpers_have_the_clients(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[stream_response(), stream_response()])
        client = make_client(spans).with_options(open_telemetry=spans.option(conversation_id="conv_1"))

        with client.messages.stream(**REQUEST) as stream:
            stream.until_done()
        with client.beta.messages.stream(**REQUEST) as beta_stream:
            beta_stream.until_done()

        stable, beta = spans.named("anthropic.messages.create")
        assert attributes(stable)["gen_ai.conversation.id"] == "conv_1"
        assert attributes(beta)["gen_ai.conversation.id"] == "conv_1"

    @pytest.mark.skipif(PYDANTIC_V1, reason="parse() needs pydantic v2")
    @pytest.mark.respx(base_url=base_url)
    def test_parse_helper_has_the_clients(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        client = make_client(spans).with_options(open_telemetry=spans.option(conversation_id="conv_1"))

        client.beta.messages.parse(**REQUEST)

        assert attributes(spans.one("anthropic.messages.create"))["gen_ai.conversation.id"] == "conv_1"

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_a_client_without_spans_reads_back_an_option_without_them(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        make: Callable[..., Any] = make_client if sync else make_async_client
        quiet = make(spans, open_telemetry=False)

        # So a copy that starts from that option stays without spans, whatever else it sets.
        own = quiet.open_telemetry
        await call(quiet.with_options(open_telemetry={**own, "conversation_id": "conv_1"}))
        await call(quiet.copy(open_telemetry={**own, "tracer_provider": spans.provider}))
        assert spans.finished == ()

        # A copy that is given another option has that one alone.
        await call(quiet.with_options(open_telemetry=spans.option(conversation_id="conv_1")))
        assert len(spans.named("anthropic.messages.create")) == 1

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_with_options_false_and_empty_replace_the_clients_option(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        make: Callable[..., Any] = make_client if sync else make_async_client
        client = make(spans, open_telemetry=spans.option(conversation_id="conv_1"))

        await call(client.with_options(open_telemetry=False))
        assert client.with_options(open_telemetry=False).open_telemetry["traces"]["enabled"] is False

        # This copy has no tracer provider of its own left, so its spans go to the registered one.
        copy = client.with_options(open_telemetry={})
        assert "tracer_provider" not in copy.open_telemetry
        assert "conversation_id" not in copy.open_telemetry
        await call(copy)
        assert spans.finished == ()

        await call(client.with_options(timeout=5))
        assert attributes(spans.one("anthropic.messages.create"))["gen_ai.conversation.id"] == "conv_1"

    @pytest.mark.respx()
    async def test_platform_clients_replace_the_whole_option_too(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post().mock(return_value=httpx2.Response(200, json=MESSAGE))
        option = spans.option(traces={"content_mode": "content"}, conversation_id="conv_0")

        for client in platform_clients(option):
            replaced = client.with_options(open_telemetry=spans.option(conversation_id="conv_1"))
            spread = client.copy(open_telemetry={**client.open_telemetry, "conversation_id": "conv_1"})
            assert type(replaced) is type(spread) is type(client)

            spans.exporter.clear()
            for called in (client, replaced, spread, spread.copy(), spread.copy(open_telemetry=False)):
                await call(called)

            own, bare, kept, copied = spans.named("anthropic.messages.create")
            assert attributes(own)["gen_ai.conversation.id"] == "conv_0"
            assert "gen_ai.input.messages" in attributes(own)
            assert attributes(bare)["gen_ai.conversation.id"] == "conv_1"
            assert "gen_ai.input.messages" not in attributes(bare)
            for span in (kept, copied):
                assert attributes(span)["gen_ai.conversation.id"] == "conv_1"
                assert "gen_ai.input.messages" in attributes(span)
            for span in (bare, kept, copied):
                assert attributes(span)["gen_ai.provider.name"] == attributes(own)["gen_ai.provider.name"]

    @pytest.mark.respx()
    async def test_platform_clients_without_spans_read_back_an_option_without_them(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post().mock(return_value=httpx2.Response(200, json=MESSAGE))
        clients = platform_clients(spans.option(traces=False))

        for client in clients:
            await call(client.with_options(open_telemetry={**client.open_telemetry, "conversation_id": "conv_1"}))
        assert spans.finished == ()

        for client in clients:
            await call(client.copy(open_telemetry=spans.option(traces=True)))
        assert len(spans.named("anthropic.messages.create")) == len(clients)

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_copy_of_a_client_whose_constructor_takes_no_open_telemetry_keeps_the_option(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        option = spans.option(traces={"content_mode": "content"})

        # As the constructor of a subclass with its own list of keywords does, these take no `open_telemetry`.
        class Fixed(Anthropic):
            _otel_platform = "aws"

            def __init__(self, **options: Any) -> None:
                assert "open_telemetry" not in options
                super().__init__(**options, open_telemetry=option)

        class AsyncFixed(AsyncAnthropic):
            _otel_platform = "aws"

            def __init__(self, **options: Any) -> None:
                assert "open_telemetry" not in options
                super().__init__(**options, open_telemetry=option)

        client: Any = (Fixed if sync else AsyncFixed)(base_url=base_url, api_key="key")
        copy = client.with_options(open_telemetry={**client.open_telemetry, "conversation_id": "conv_1"})
        assert type(copy) is type(client)

        for called in (client, copy, copy.copy(), copy.copy(open_telemetry=False)):
            await call(called)

        own, changed, copied = spans.named("anthropic.messages.create")
        assert "gen_ai.conversation.id" not in attributes(own)
        for span in (changed, copied):
            assert attributes(span)["gen_ai.conversation.id"] == "conv_1"
        for span in (own, changed, copied):
            assert "gen_ai.input.messages" in attributes(span)
            assert span.instrumentation_scope and span.instrumentation_scope.name == "com.anthropic.sdk.python.aws"

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_environment_is_read_when_the_client_is_constructed(
        self, sync: bool, registered: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        make: Callable[..., Any] = make_client if sync else make_async_client

        with update_env(
            ANTHROPIC_OPEN_TELEMETRY_TRACES_CONTENT_MODE="content",
            ANTHROPIC_OPEN_TELEMETRY_TRACES_MAX_CONTENT_BYTES="4096",
        ):
            verbose = make(registered, open_telemetry=None)
        with update_env(ANTHROPIC_OPEN_TELEMETRY="false"):
            quiet = make(registered, open_telemetry=None)
        assert verbose.open_telemetry["traces"] == {
            "enabled": True,
            "content_mode": "content",
            "max_content_bytes": 4096,
        }
        assert quiet.open_telemetry["traces"]["enabled"] is False

        # A later change to the environment reaches neither the clients, nor their copies that are given no option,
        # nor those that start from the client's own.
        with update_env(ANTHROPIC_OPEN_TELEMETRY="true", ANTHROPIC_OPEN_TELEMETRY_TRACES_CONTENT_MODE="metadata_only"):
            for client in (
                quiet,
                quiet.with_options(timeout=5),
                quiet.copy(open_telemetry={**quiet.open_telemetry, "conversation_id": "c"}),
            ):
                await call(client)
            assert registered.finished == ()

        with update_env(ANTHROPIC_OPEN_TELEMETRY="false", ANTHROPIC_OPEN_TELEMETRY_TRACES_CONTENT_MODE="metadata_only"):
            for client in (
                verbose,
                verbose.with_options(timeout=5),
                verbose.copy(open_telemetry={**verbose.open_telemetry, "conversation_id": "c"}),
            ):
                assert client.open_telemetry["traces"] == verbose.open_telemetry["traces"]
                await call(client)
            created = registered.named("anthropic.messages.create")
            assert len(created) == 3
            assert all("gen_ai.input.messages" in attributes(span) for span in created)

            # A copy that is given another option is resolved as a new client is, and does not read the environment.
            await call(verbose.with_options(open_telemetry={}))
            assert "gen_ai.input.messages" not in attributes(registered.named("anthropic.messages.create")[3])
            # `None` is no option, so the copy has the client's own.
            await call(verbose.with_options(open_telemetry=None))
            assert "gen_ai.input.messages" in attributes(registered.named("anthropic.messages.create")[4])

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_a_copy_that_is_given_none_keeps_the_clients_option(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        make: Callable[..., Any] = make_client if sync else make_async_client

        quiet = make(spans, open_telemetry=False)
        for copy in (quiet.with_options(open_telemetry=None), quiet.copy(open_telemetry=None)):
            assert copy.open_telemetry == quiet.open_telemetry
            await call(copy)
        assert spans.finished == ()

        verbose = make(spans, open_telemetry=spans.option(traces={"content_mode": "content"}, conversation_id="c"))
        assert verbose.with_options(open_telemetry=None).open_telemetry == verbose.open_telemetry

    def test_a_copy_of_a_platform_client_that_is_given_none_keeps_the_clients_option(self, spans: Spans) -> None:
        option = spans.option(traces={"content_mode": "content"}, propagation=False, conversation_id="c")
        with update_env(ANTHROPIC_OPEN_TELEMETRY_TRACES_MAX_CONTENT_BYTES="300"):
            from_variable = platform_clients(None)

        # The variables do not reach the copy, whose option is the client's own.
        with update_env(ANTHROPIC_OPEN_TELEMETRY="false", ANTHROPIC_OPEN_TELEMETRY_TRACES_MAX_CONTENT_BYTES="4096"):
            for client in (*platform_clients(False), *platform_clients(option), *from_variable):
                for copy in (client.with_options(open_telemetry=None), client.copy(open_telemetry=None)):
                    assert type(copy) is type(client)
                    assert copy.open_telemetry == client.open_telemetry
        assert all(client.open_telemetry["traces"]["max_content_bytes"] == 300 for client in from_variable)

    @pytest.mark.respx()
    async def test_platform_clients_read_the_environment_when_they_are_constructed(
        self, registered: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post().mock(return_value=httpx2.Response(200, json=MESSAGE))
        with update_env(ANTHROPIC_OPEN_TELEMETRY_TRACES_CONTENT_MODE="content"):
            verbose = platform_clients(None)
        with update_env(ANTHROPIC_OPEN_TELEMETRY="false"):
            quiet = platform_clients(None)

        with update_env(ANTHROPIC_OPEN_TELEMETRY="true"):
            for client in quiet:
                changed = client.with_options(open_telemetry={**client.open_telemetry, "conversation_id": "conv_1"})
                for copy in (client.copy(), changed):
                    await call(copy)
            assert registered.finished == ()

        with update_env(ANTHROPIC_OPEN_TELEMETRY="false", ANTHROPIC_OPEN_TELEMETRY_TRACES_CONTENT_MODE="metadata_only"):
            for client in verbose:
                changed = client.with_options(open_telemetry={**client.open_telemetry, "conversation_id": "conv_1"})
                for copy in (client.copy(), changed):
                    await call(copy)
            created = registered.named("anthropic.messages.create")
            assert len(created) == 2 * len(verbose)
            assert all("gen_ai.input.messages" in attributes(span) for span in created)

    @pytest.mark.parametrize(
        ("platform", "sync_client", "async_client", "options"),
        [
            (
                "bedrock",
                AnthropicBedrock,
                AsyncAnthropicBedrock,
                {"aws_region": "us-east-1", "aws_access_key": "access", "aws_secret_key": "secret"},
            ),
            (
                "bedrock",
                AnthropicBedrockMantle,
                AsyncAnthropicBedrockMantle,
                {"aws_region": "us-east-1", "api_key": "key"},
            ),
            (
                "vertex",
                AnthropicVertex,
                AsyncAnthropicVertex,
                {"region": "us-east5", "project_id": "project", "access_token": "token"},
            ),
            ("foundry", AnthropicFoundry, AsyncAnthropicFoundry, {"api_key": "key", "resource": "resource"}),
            ("aws", AnthropicAWS, AsyncAnthropicAWS, {"skip_auth": True, "base_url": base_url}),
            (
                "google_cloud",
                AnthropicGoogleCloud,
                AsyncAnthropicGoogleCloud,
                {"base_url": base_url, "workspace_id": "wrkspc_1", "token_provider": lambda: "token"},
            ),
        ],
        ids=["bedrock", "bedrock_mantle", "vertex", "foundry", "aws", "google_cloud"],
    )
    @pytest.mark.respx()
    async def test_platform_client_spans_have_the_platform_in_their_scope(
        self,
        platform: str,
        sync_client: Callable[..., Any],
        async_client: Callable[..., Any],
        options: dict[str, Any],
        spans: Spans,
        respx_mock: MockRouter,
    ) -> None:
        respx_mock.post().mock(return_value=httpx2.Response(200, json=MESSAGE))
        clients = [
            make(**options, open_telemetry=spans.option(traces={"content_mode": "content"}))
            for make in (sync_client, async_client)
        ]

        # A copy keeps its client's resolved option, and its tracer has the scope of the platform too.
        for client in clients:
            conversation = client.with_options(open_telemetry={**client.open_telemetry, "conversation_id": "conv_1"})
            for called in (client, client.copy(), conversation):
                await call(called)
        create(sync_client(**options, open_telemetry=False))

        created = spans.named("anthropic.messages.create")
        scopes = [span.instrumentation_scope for span in created]
        assert [scope and (scope.name, scope.version) for scope in scopes] == [
            (f"com.anthropic.sdk.python.{platform}", clients[0]._version)
        ] * 6
        assert all("gen_ai.input.messages" in attributes(span) for span in created)
        assert ["gen_ai.conversation.id" in attributes(span) for span in created] == [False, False, True] * 2

    @pytest.mark.respx()
    def test_platform_client_span(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post().mock(return_value=httpx2.Response(200, json=MESSAGE))
        vertex = AnthropicVertex(
            region="us-east5", project_id="project", access_token="token", open_telemetry=spans.option()
        )

        create(vertex.with_options(open_telemetry={**vertex.open_telemetry, "conversation_id": "conv_1"}))

        span = spans.one("anthropic.messages.create")
        assert attributes(span)["gen_ai.conversation.id"] == "conv_1"
        assert attributes(span)["gen_ai.provider.name"] == "gcp.vertex_ai"


class TestContent:
    @pytest.mark.respx(base_url=base_url)
    def test_content_mode(self, spans: Spans, respx_mock: MockRouter) -> None:
        response = {
            **MESSAGE,
            "content": [
                {"type": "text", "text": "Let me check"},
                {"type": "tool_use", "id": "toolu_1", "name": "get_weather", "input": {"city": "SF"}},
            ],
        }
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=response))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        client.messages.create(
            max_tokens=1024,
            model="claude-test",
            system="Be brief",
            messages=[
                {"role": "user", "content": "Weather?"},
                {
                    "role": "assistant",
                    "content": [{"type": "tool_use", "id": "toolu_0", "name": "get_weather", "input": {"city": "LA"}}],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "tool_result", "tool_use_id": "toolu_0", "content": "sunny"},
                        {"type": "image", "source": {"type": "url", "url": "https://example.com/cat.png"}},
                        {"type": "document", "source": {"type": "text", "media_type": "text/plain", "data": "Cats"}},
                    ],
                },
            ],
        )

        span = spans.one("anthropic.messages.create")
        assert json.loads(attributes(span)["gen_ai.system_instructions"]) == [{"type": "text", "content": "Be brief"}]
        assert json.loads(attributes(span)["gen_ai.input.messages"]) == [
            {"role": "user", "parts": [{"type": "text", "content": "Weather?"}]},
            {
                "role": "assistant",
                "parts": [{"type": "tool_call", "id": "toolu_0", "name": "get_weather", "arguments": {"city": "LA"}}],
            },
            {
                "role": "user",
                "parts": [
                    {"type": "tool_call_response", "id": "toolu_0", "response": [{"type": "text", "text": "sunny"}]},
                    # Any other block is its type after `anthropic_`.
                    {"type": "anthropic_image"},
                    {"type": "anthropic_document"},
                ],
            },
        ]
        assert json.loads(attributes(span)["gen_ai.output.messages"]) == [
            {
                "role": "assistant",
                "parts": [
                    {"type": "text", "content": "Let me check"},
                    {"type": "tool_call", "id": "toolu_1", "name": "get_weather", "arguments": {"city": "SF"}},
                ],
            }
        ]

    @pytest.mark.respx(base_url=base_url)
    def test_tool_result_content_is_content_blocks(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))
        text: TextBlockParam = {
            "type": "text",
            "text": "Cats sleep a lot.",
            "citations": [
                {
                    "type": "char_location",
                    "cited_text": "Cats sleep",
                    "document_index": 0,
                    "document_title": "Cats",
                    "start_char_index": 0,
                    "end_char_index": 10,
                }
            ],
            "cache_control": {"type": "ephemeral"},
        }
        search_result: SearchResultBlockParam = {
            "type": "search_result",
            "source": "https://example.com/cats",
            "title": "Cats",
            "content": [{"type": "text", "text": "Cats sleep a lot."}],
            "citations": {"enabled": True},
        }

        client.messages.create(
            max_tokens=1024,
            model="claude-test",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "tool_result", "tool_use_id": "toolu_0", "content": "sunny"},
                        {
                            "type": "tool_result",
                            "tool_use_id": "toolu_1",
                            "content": [
                                text,
                                search_result,
                                {"type": "image", "source": {"type": "url", "url": "https://example.com/cat.png"}},
                                cast(Any, {"data": "no type"}),
                            ],
                        },
                        {"type": "tool_result", "tool_use_id": "toolu_2"},
                        cast(Any, {"data": "no type"}),
                    ],
                }
            ],
        )

        [message] = json.loads(attributes(spans.one("anthropic.messages.create"))["gen_ai.input.messages"])
        assert message["parts"] == [
            {"type": "tool_call_response", "id": "toolu_0", "response": [{"type": "text", "text": "sunny"}]},
            # A text block and a search result keep all of their fields. Any other block is its type, with no prefix.
            {
                "type": "tool_call_response",
                "id": "toolu_1",
                "response": [text, search_result, {"type": "image"}, {"type": "unknown"}],
            },
            {"type": "tool_call_response", "id": "toolu_2", "response": []},
            {"type": "anthropic_unknown"},
        ]

    @pytest.mark.respx(base_url=base_url)
    def test_tool_result_content_leaves_out_encrypted_fields(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))
        text: TextBlockParam = {
            "type": "text",
            "text": "Cats sleep a lot.",
            "citations": [
                {
                    "type": "web_search_result_location",
                    "cited_text": "Cats sleep",
                    "encrypted_index": "encrypted_0",
                    "title": "Cats",
                    "url": "https://example.com/cats",
                }
            ],
        }

        client.messages.create(
            max_tokens=1024,
            model="claude-test",
            messages=[
                {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "toolu_0", "content": [text]}]}
            ],
        )

        [message] = json.loads(attributes(spans.one("anthropic.messages.create"))["gen_ai.input.messages"])
        assert message["parts"] == [
            {
                "type": "tool_call_response",
                "id": "toolu_0",
                "response": [
                    {
                        "type": "text",
                        "text": "Cats sleep a lot.",
                        "citations": [
                            {
                                "type": "web_search_result_location",
                                "cited_text": "Cats sleep",
                                "title": "Cats",
                                "url": "https://example.com/cats",
                            }
                        ],
                    }
                ],
            }
        ]

    @pytest.mark.respx(base_url=base_url)
    def test_server_and_mcp_tool_blocks_are_tool_calls_and_their_responses(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        document = {
            "type": "document",
            "source": {"type": "text", "media_type": "text/plain", "data": "Cats sleep a lot."},
            "title": "Cats",
        }
        response = {
            **MESSAGE,
            "content": [
                # Only a `tool_use` block has a `toolset_name`: on any other block it is left out.
                {
                    "type": "server_tool_use",
                    "id": "srvtoolu_1",
                    "name": "code_execution",
                    "input": {"code": "1 + 1"},
                    "toolset_name": "computer",
                },
                {
                    "type": "code_execution_tool_result",
                    "tool_use_id": "srvtoolu_1",
                    "content": {
                        "type": "code_execution_result",
                        "stdout": "2",
                        "stderr": "",
                        "return_code": 0,
                        "content": [{"type": "code_execution_output", "file_id": "file_1"}],
                    },
                },
                {
                    "type": "web_search_tool_result",
                    "tool_use_id": "srvtoolu_2",
                    "content": {"type": "web_search_tool_result_error", "error_code": "too_many_requests"},
                },
                {
                    "type": "text_editor_code_execution_tool_result",
                    "tool_use_id": "srvtoolu_3",
                    "content": {
                        "type": "text_editor_code_execution_view_result",
                        "file_type": "image",
                        "content": "aGVsbG8=",
                        "num_lines": None,
                    },
                },
                {
                    "type": "web_fetch_tool_result",
                    "tool_use_id": "srvtoolu_4",
                    "content": {"type": "web_fetch_result", "url": "https://example.com/cats", "content": document},
                },
                {
                    "type": "mcp_tool_use",
                    "id": "mcptoolu_1",
                    "name": "echo",
                    "server_name": "tools",
                    "input": {"x": 1},
                    "toolset_name": "computer",
                },
                {
                    "type": "mcp_tool_result",
                    "tool_use_id": "mcptoolu_1",
                    "is_error": False,
                    "content": [{"type": "text", "text": "one"}],
                },
            ],
        }
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=response))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        client.beta.messages.create(
            max_tokens=1024,
            model="claude-test",
            messages=[
                {"role": "user", "content": "Cats?"},
                {
                    "role": "assistant",
                    "content": [
                        cast(
                            Any,
                            {
                                "type": "server_tool_use",
                                "id": "srvtoolu_0",
                                "name": "web_search",
                                "input": {"query": "cats"},
                                "toolset_name": "computer",
                            },
                        ),
                        {
                            "type": "web_search_tool_result",
                            "tool_use_id": "srvtoolu_0",
                            "content": [
                                {
                                    "type": "web_search_result",
                                    "url": "https://example.com/cats",
                                    "title": "Cats",
                                    "encrypted_content": "encrypted_0",
                                    "page_age": "1 day",
                                }
                            ],
                        },
                        cast(
                            Any,
                            {
                                "type": "mcp_tool_use",
                                "id": "mcptoolu_0",
                                "name": "echo",
                                "server_name": "tools",
                                "input": {"x": 0},
                                "toolset_name": "computer",
                            },
                        ),
                        {"type": "mcp_tool_result", "tool_use_id": "mcptoolu_0", "content": "zero"},
                        cast(Any, {"type": "mcp_tool_result", "tool_use_id": "mcptoolu_9"}),
                    ],
                },
                {"role": "user", "content": "More"},
            ],
        )

        span = spans.one("anthropic.messages.create")
        _, assistant, _ = json.loads(attributes(span)["gen_ai.input.messages"])
        assert assistant["parts"] == [
            {"type": "tool_call", "id": "srvtoolu_0", "name": "web_search", "arguments": {"query": "cats"}},
            {
                "type": "tool_call_response",
                "id": "srvtoolu_0",
                # A web search result is kept, without the field that is encrypted.
                "response": [
                    {
                        "type": "web_search_result",
                        "url": "https://example.com/cats",
                        "title": "Cats",
                        "page_age": "1 day",
                    }
                ],
            },
            {
                "type": "tool_call",
                "id": "mcptoolu_0",
                "name": "echo",
                "arguments": {"x": 0},
                "anthropic_mcp_server_name": "tools",
            },
            {"type": "tool_call_response", "id": "mcptoolu_0", "response": [{"type": "text", "text": "zero"}]},
            {"type": "tool_call_response", "id": "mcptoolu_9", "response": []},
        ]
        [output] = json.loads(attributes(span)["gen_ai.output.messages"])
        assert output["parts"] == [
            {"type": "tool_call", "id": "srvtoolu_1", "name": "code_execution", "arguments": {"code": "1 + 1"}},
            {
                "type": "tool_call_response",
                "id": "srvtoolu_1",
                "response": {
                    "type": "code_execution_result",
                    "stdout": "2",
                    "stderr": "",
                    "return_code": 0,
                    "content": [{"type": "code_execution_output", "file_id": "file_1"}],
                },
            },
            {
                "type": "tool_call_response",
                "id": "srvtoolu_2",
                "response": {"type": "web_search_tool_result_error", "error_code": "too_many_requests"},
            },
            # The data of an image or of a document is left out.
            {
                "type": "tool_call_response",
                "id": "srvtoolu_3",
                "response": {"type": "text_editor_code_execution_view_result", "file_type": "image", "num_lines": None},
            },
            {
                "type": "tool_call_response",
                "id": "srvtoolu_4",
                "response": {
                    "type": "web_fetch_result",
                    "url": "https://example.com/cats",
                    "content": {"type": "document"},
                },
            },
            {
                "type": "tool_call",
                "id": "mcptoolu_1",
                "name": "echo",
                "arguments": {"x": 1},
                "anthropic_mcp_server_name": "tools",
            },
            {"type": "tool_call_response", "id": "mcptoolu_1", "response": [{"type": "text", "text": "one"}]},
        ]
        for name in ("gen_ai.input.messages", "gen_ai.output.messages"):
            assert "encrypted_" not in attributes(span)[name] and "aGVsbG8=" not in attributes(span)[name]

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    async def test_toolset_name_of_a_tool_use_block_is_on_its_tool_call(
        self, beta: bool, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        response: dict[str, Any] = {
            **MESSAGE,
            "content": [
                {"type": "tool_use", "id": "toolu_4", "name": "screenshot", "input": {}, "toolset_name": "computer"},
                {"type": "tool_use", "id": "toolu_5", "name": "get_weather", "input": {}, "toolset_name": None},
                {"type": "tool_use", "id": "toolu_6", "name": "get_time", "input": {}},
            ],
        }
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=response))
        make: Callable[..., Any] = make_client if sync else make_async_client
        client = make(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))
        block: Callable[..., Any] = BetaToolUseBlock if beta else ToolUseBlock

        result = messages_resource(client, beta=beta).create(
            max_tokens=1024,
            model="claude-test",
            messages=[
                {"role": "user", "content": "Look"},
                {
                    "role": "assistant",
                    "content": [
                        {"type": "tool_use", "id": "toolu_0", "name": "click", "input": {}, "toolset_name": "computer"},
                        {"type": "tool_use", "id": "toolu_1", "name": "get_weather", "input": {}, "toolset_name": None},
                        {"type": "tool_use", "id": "toolu_2", "name": "get_time", "input": {}},
                        # A block of an earlier response, sent back as it is.
                        block(type="tool_use", id="toolu_3", name="type", input={}, toolset_name="computer"),
                        block(type="tool_use", id="toolu_9", name="get_date", input={}),
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "tool_result", "tool_use_id": "toolu_0", "content": "done", "toolset_name": "computer"}
                    ],
                },
            ],
        )
        if inspect.isawaitable(result):
            await result

        span = spans.one("anthropic.messages.create")
        _, assistant, user = json.loads(attributes(span)[INPUT])
        assert assistant["parts"] == [
            {
                "type": "tool_call",
                "id": "toolu_0",
                "name": "click",
                "arguments": {},
                "anthropic_toolset_name": "computer",
            },
            # A `toolset_name` that is null is left out, like one that is absent.
            {"type": "tool_call", "id": "toolu_1", "name": "get_weather", "arguments": {}},
            {"type": "tool_call", "id": "toolu_2", "name": "get_time", "arguments": {}},
            {
                "type": "tool_call",
                "id": "toolu_3",
                "name": "type",
                "arguments": {},
                "anthropic_toolset_name": "computer",
            },
            {"type": "tool_call", "id": "toolu_9", "name": "get_date", "arguments": {}},
        ]
        assert user["parts"] == [
            {"type": "tool_call_response", "id": "toolu_0", "response": [{"type": "text", "text": "done"}]}
        ]
        [output] = json.loads(attributes(span)[OUTPUT])
        assert output["parts"] == [
            {
                "type": "tool_call",
                "id": "toolu_4",
                "name": "screenshot",
                "arguments": {},
                "anthropic_toolset_name": "computer",
            },
            {"type": "tool_call", "id": "toolu_5", "name": "get_weather", "arguments": {}},
            {"type": "tool_call", "id": "toolu_6", "name": "get_time", "arguments": {}},
        ]
        # The key comes after `arguments`.
        assert list(output["parts"][0]) == ["type", "id", "name", "arguments", "anthropic_toolset_name"]

    @pytest.mark.respx(base_url=base_url)
    def test_streamed_server_and_mcp_tool_blocks_are_tool_calls_and_their_responses(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        events = stream_events(index=4)
        events[1:1] = [
            {
                "type": "content_block_start",
                "index": 0,
                "content_block": {
                    "type": "server_tool_use",
                    "id": "srvtoolu_1",
                    "name": "web_search",
                    "input": {},
                    "toolset_name": "computer",
                },
            },
            {
                "type": "content_block_delta",
                "index": 0,
                "delta": {"type": "input_json_delta", "partial_json": '{"query": '},
            },
            {
                "type": "content_block_delta",
                "index": 0,
                "delta": {"type": "input_json_delta", "partial_json": '"cats"}'},
            },
            {"type": "content_block_stop", "index": 0},
            {
                "type": "content_block_start",
                "index": 1,
                "content_block": {
                    "type": "web_search_tool_result",
                    "tool_use_id": "srvtoolu_1",
                    "content": [
                        {
                            "type": "web_search_result",
                            "url": "https://example.com/cats",
                            "title": "Cats",
                            "encrypted_content": "encrypted_1",
                            "page_age": None,
                        }
                    ],
                },
            },
            {"type": "content_block_stop", "index": 1},
            {
                "type": "content_block_start",
                "index": 2,
                "content_block": {
                    "type": "mcp_tool_use",
                    "id": "mcptoolu_1",
                    "name": "echo",
                    "server_name": "tools",
                    "input": {},
                    "toolset_name": "computer",
                },
            },
            {
                "type": "content_block_delta",
                "index": 2,
                "delta": {"type": "input_json_delta", "partial_json": '{"x": 1}'},
            },
            {"type": "content_block_stop", "index": 2},
            {
                "type": "content_block_start",
                "index": 3,
                "content_block": {
                    "type": "mcp_tool_result",
                    "tool_use_id": "mcptoolu_1",
                    "is_error": False,
                    "content": "one",
                },
            },
            {"type": "content_block_stop", "index": 3},
        ]
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        with client.beta.messages.stream(**REQUEST) as stream:
            stream.until_done()

        [output] = json.loads(attributes(spans.one("anthropic.messages.create"))["gen_ai.output.messages"])
        assert output["parts"] == [
            {"type": "tool_call", "id": "srvtoolu_1", "name": "web_search", "arguments": {"query": "cats"}},
            {
                "type": "tool_call_response",
                "id": "srvtoolu_1",
                "response": [
                    {"type": "web_search_result", "url": "https://example.com/cats", "title": "Cats", "page_age": None}
                ],
            },
            {
                "type": "tool_call",
                "id": "mcptoolu_1",
                "name": "echo",
                "arguments": {"x": 1},
                "anthropic_mcp_server_name": "tools",
            },
            {"type": "tool_call_response", "id": "mcptoolu_1", "response": [{"type": "text", "text": "one"}]},
            {"type": "text", "content": "Hi there"},
        ]

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    async def test_streamed_toolset_name_of_a_tool_use_block_is_on_its_tool_call(
        self, beta: bool, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        def tool_use(index: int, name: str, **fields: object) -> list[dict[str, Any]]:
            block: dict[str, Any] = {"type": "tool_use", "id": f"toolu_{index}", "name": name, "input": {}, **fields}
            delta = {"type": "input_json_delta", "partial_json": "{}"}
            return [
                {"type": "content_block_start", "index": index, "content_block": block},
                {"type": "content_block_delta", "index": index, "delta": delta},
                {"type": "content_block_stop", "index": index},
            ]

        events = stream_events(index=3)
        events[1:1] = [
            *tool_use(0, "screenshot", toolset_name="computer"),
            *tool_use(1, "get_weather", toolset_name=None),
            *tool_use(2, "get_time"),
        ]
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events))
        make: Callable[..., Any] = make_client if sync else make_async_client
        client = make(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        if sync:
            with messages_resource(client, beta=beta).stream(**REQUEST) as stream:
                stream.until_done()
        else:
            async with messages_resource(client, beta=beta).stream(**REQUEST) as stream:
                await stream.until_done()

        [output] = json.loads(attributes(spans.one("anthropic.messages.create"))[OUTPUT])
        assert output["parts"] == [
            {
                "type": "tool_call",
                "id": "toolu_0",
                "name": "screenshot",
                "arguments": {},
                "anthropic_toolset_name": "computer",
            },
            {"type": "tool_call", "id": "toolu_1", "name": "get_weather", "arguments": {}},
            {"type": "tool_call", "id": "toolu_2", "name": "get_time", "arguments": {}},
            {"type": "text", "content": "Hi there"},
        ]

    @pytest.mark.respx(base_url=base_url)
    def test_thinking_is_a_reasoning_part_without_its_signature(self, spans: Spans, respx_mock: MockRouter) -> None:
        response = {
            **MESSAGE,
            "content": [
                {"type": "thinking", "thinking": "SF is foggy in summer.", "signature": "sig_response"},
                # The API hides the thinking of this block.
                {"type": "thinking", "thinking": "", "signature": "sig_hidden"},
                {"type": "redacted_thinking", "data": "encrypted_response"},
                {"type": "text", "text": "Foggy"},
            ],
        }
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=response))
        request: dict[str, Any] = {
            **REQUEST,
            "messages": [
                {"role": "user", "content": "Weather?"},
                {
                    "role": "assistant",
                    "content": [
                        {"type": "thinking", "thinking": "I should ask where.", "signature": "sig_request"},
                        {"type": "redacted_thinking", "data": "encrypted_request"},
                        {"type": "text", "text": "Where?"},
                    ],
                },
                {"role": "user", "content": "SF"},
            ],
        }

        make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"})).messages.create(**request)
        make_client(spans).messages.create(**request)

        span, without_content = spans.named("anthropic.messages.create")
        assert json.loads(attributes(span)["gen_ai.input.messages"]) == [
            {"role": "user", "parts": [{"type": "text", "content": "Weather?"}]},
            {
                "role": "assistant",
                "parts": [
                    {"type": "reasoning", "content": "I should ask where."},
                    {"type": "anthropic_redacted_thinking"},
                    {"type": "text", "content": "Where?"},
                ],
            },
            {"role": "user", "parts": [{"type": "text", "content": "SF"}]},
        ]
        assert json.loads(attributes(span)["gen_ai.output.messages"]) == [
            {
                "role": "assistant",
                "parts": [
                    {"type": "reasoning", "content": "SF is foggy in summer."},
                    {"type": "reasoning", "content": ""},
                    {"type": "anthropic_redacted_thinking"},
                    {"type": "text", "content": "Foggy"},
                ],
            }
        ]
        for value in attributes(span).values():
            assert "sig_" not in str(value) and "encrypted_" not in str(value)
        assert "gen_ai.input.messages" not in attributes(without_content)
        assert "gen_ai.output.messages" not in attributes(without_content)

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_streamed_thinking_is_a_reasoning_part_without_its_signature(
        self, beta: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        events = stream_events(index=2)
        events[1:1] = [
            {
                "type": "content_block_start",
                "index": 0,
                "content_block": {"type": "thinking", "thinking": "", "signature": ""},
            },
            {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "SF is "}},
            {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "foggy."}},
            {"type": "content_block_delta", "index": 0, "delta": {"type": "signature_delta", "signature": "sig_1"}},
            {"type": "content_block_stop", "index": 0},
            {
                "type": "content_block_start",
                "index": 1,
                "content_block": {"type": "redacted_thinking", "data": "encrypted_1"},
            },
            {"type": "content_block_stop", "index": 1},
        ]
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        with messages_resource(client, beta=beta).stream(**REQUEST) as stream:
            stream.until_done()

        span = spans.one("anthropic.messages.create")
        assert json.loads(attributes(span)["gen_ai.output.messages"]) == [
            {
                "role": "assistant",
                "parts": [
                    {"type": "reasoning", "content": "SF is foggy."},
                    {"type": "anthropic_redacted_thinking"},
                    {"type": "text", "content": "Hi there"},
                ],
            }
        ]
        assert "sig_1" not in attributes(span)["gen_ai.output.messages"]
        assert "encrypted_1" not in attributes(span)["gen_ai.output.messages"]

    @pytest.mark.respx(base_url=base_url)
    def test_environment_variable_enables_content(self, registered: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))

        with update_env(ANTHROPIC_OPEN_TELEMETRY_TRACES_CONTENT_MODE="Content"):
            create(make_client(registered, open_telemetry=None))
            # The variable is for a client that is given no option.
            create(make_client(registered, open_telemetry={"traces": True}))
            create(make_client(registered, open_telemetry={"traces": {"max_content_bytes": 4096}}))
            create(make_client(registered, open_telemetry={"traces": {"content_mode": "metadata_only"}}))

        with_content, *without_content = registered.named("anthropic.messages.create")
        assert len(without_content) == 3
        assert "gen_ai.input.messages" in attributes(with_content)
        assert not any("gen_ai.input.messages" in attributes(span) for span in without_content)

    @pytest.mark.respx(base_url=base_url)
    def test_the_former_name_of_the_content_mode_variable_is_not_read(
        self, registered: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))

        with update_env(ANTHROPIC_OPEN_TELEMETRY_CONTENT_MODE="content"):
            create(make_client(registered, open_telemetry=None))

        assert "gen_ai.input.messages" not in attributes(registered.one("anthropic.messages.create"))

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_stream_helper_content_comes_from_its_snapshot(
        self, beta: bool, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(tool_stream_events()))
        accumulated = count_accumulated_events(monkeypatch, beta=beta)
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        with messages_resource(client, beta=beta).stream(**REQUEST) as stream:
            stream.until_done()
            # The span has ended, with the content of the Message that the helper still holds.
            span = spans.one("anthropic.messages.create")
            assert [block.type for block in stream.current_message_snapshot.content] == ["text", "tool_use"]

        assert span.status.status_code == StatusCode.OK
        assert json.loads(attributes(span)["gen_ai.output.messages"]) == TOOL_STREAM_OUTPUT
        # Only the helper accumulated the events.
        assert len(accumulated) == len(tool_stream_events())

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_stream_helper_content_comes_from_its_snapshot(
        self, beta: bool, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(tool_stream_events()))
        accumulated = count_accumulated_events(monkeypatch, beta=beta)
        client = make_async_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        async with messages_resource(client, beta=beta).stream(**REQUEST) as stream:
            await stream.until_done()
            span = spans.one("anthropic.messages.create")
            assert [block.type for block in stream.current_message_snapshot.content] == ["text", "tool_use"]

        assert span.status.status_code == StatusCode.OK
        assert json.loads(attributes(span)["gen_ai.output.messages"]) == TOOL_STREAM_OUTPUT
        assert len(accumulated) == len(tool_stream_events())

    @pytest.mark.parametrize("events, parts", CUT_STREAMS)
    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_stream_helper_stream_ended_by_the_server_has_the_partial_output(
        self,
        beta: bool,
        events: list[dict[str, Any]],
        parts: list[dict[str, Any]],
        spans: Spans,
        respx_mock: MockRouter,
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        with messages_resource(client, beta=beta).stream(**REQUEST) as stream:
            stream.until_done()

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.ERROR
        assert attributes(span)["error.type"] == "api_error"
        assert json.loads(attributes(span)["gen_ai.output.messages"]) == [{"role": "assistant", "parts": parts}]
        assert attributes(span)["gen_ai.response.id"] == "msg_1"
        assert "anthropic.message.stop_reason" not in attributes(span)
        assert "gen_ai.usage.output_tokens" not in attributes(span)

    @pytest.mark.parametrize("events, parts", CUT_STREAMS)
    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_stream_helper_stream_ended_by_the_server_has_the_partial_output(
        self,
        beta: bool,
        events: list[dict[str, Any]],
        parts: list[dict[str, Any]],
        spans: Spans,
        respx_mock: MockRouter,
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events))
        client = make_async_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        async with messages_resource(client, beta=beta).stream(**REQUEST) as stream:
            await stream.until_done()

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.ERROR
        assert attributes(span)["error.type"] == "api_error"
        assert json.loads(attributes(span)["gen_ai.output.messages"]) == [{"role": "assistant", "parts": parts}]
        assert "anthropic.message.stop_reason" not in attributes(span)

    @pytest.mark.respx(base_url=base_url)
    def test_partial_output_is_content(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(stream_events()[:3]))

        with make_client(spans).messages.stream(**REQUEST) as stream:
            stream.until_done()

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.ERROR
        assert "gen_ai.output.messages" not in attributes(span)

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_stream_helper_error_event_has_the_partial_output(
        self, beta: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response([*stream_events()[:3], STREAM_ERROR_EVENT]))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        with pytest.raises(APIStatusError):
            with messages_resource(client, beta=beta).stream(**REQUEST) as stream:
                stream.until_done()

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.ERROR
        assert attributes(span)["error.type"] == "overloaded_error"
        assert json.loads(attributes(span)["gen_ai.output.messages"]) == [
            {"role": "assistant", "parts": [{"type": "text", "content": "Hi there"}]}
        ]

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_stream_helper_error_event_has_the_partial_output(
        self, beta: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response([*stream_events()[:3], STREAM_ERROR_EVENT]))
        client = make_async_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        with pytest.raises(APIStatusError):
            async with messages_resource(client, beta=beta).stream(**REQUEST) as stream:
                await stream.until_done()

        span = spans.one("anthropic.messages.create")
        assert attributes(span)["error.type"] == "overloaded_error"
        assert json.loads(attributes(span)["gen_ai.output.messages"]) == [
            {"role": "assistant", "parts": [{"type": "text", "content": "Hi there"}]}
        ]

    @pytest.mark.respx(base_url=base_url)
    def test_stream_helper_read_error_has_the_partial_output(self, spans: Spans, respx_mock: MockRouter) -> None:
        class Dropped(httpx2.SyncByteStream):
            @override
            def __iter__(self) -> Iterator[bytes]:
                yield sse(cut_tool_stream_events())
                raise httpx2.ReadError("connection dropped")

        headers = {"content-type": "text/event-stream", **RESPONSE_HEADERS}
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, stream=Dropped(), headers=headers))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        with pytest.raises(httpx2.ReadError):
            with client.messages.stream(**REQUEST) as stream:
                stream.until_done()

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.ERROR
        assert attributes(span)["error.type"] == "connection_error"
        [output] = json.loads(attributes(span)["gen_ai.output.messages"])
        assert output["parts"][1]["arguments"] == {"city": "SF"}

    @pytest.mark.parametrize(
        "last_event, parts", [("message_start", []), ("text", [{"type": "text", "content": "Hi there"}])]
    )
    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_stream_helper_closed_early_has_the_partial_output(
        self, beta: bool, last_event: str, parts: list[dict[str, Any]], spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(tool_stream_events()))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        with messages_resource(client, beta=beta).stream(**REQUEST) as stream:
            for event in stream:
                if event.type == last_event:
                    break

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.UNSET
        assert "error.type" not in attributes(span)
        assert "gen_ai.input.messages" in attributes(span)
        assert json.loads(attributes(span)["gen_ai.output.messages"]) == [{"role": "assistant", "parts": parts}]

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_stream_helper_closed_early_has_the_partial_output(
        self, beta: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(tool_stream_events()))
        client = make_async_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        async with messages_resource(client, beta=beta).stream(**REQUEST) as stream:
            async for event in stream:
                if event.type == "text":
                    break

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.UNSET
        assert json.loads(attributes(span)["gen_ai.output.messages"]) == [
            {"role": "assistant", "parts": [{"type": "text", "content": "Hi there"}]}
        ]

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_stream_helper_without_a_message_start_has_no_output(
        self, beta: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[stream_response([]), stream_response()])
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        with messages_resource(client, beta=beta).stream(**REQUEST) as stream:
            stream.until_done()
        with messages_resource(client, beta=beta).stream(**REQUEST):
            pass

        ended_by_the_server, closed_before_the_first_read = spans.named("anthropic.messages.create")
        assert ended_by_the_server.status.status_code == StatusCode.ERROR
        assert closed_before_the_first_read.status.status_code == StatusCode.UNSET
        for span in (ended_by_the_server, closed_before_the_first_read):
            assert "gen_ai.input.messages" in attributes(span)
            assert "gen_ai.output.messages" not in attributes(span)

    @pytest.mark.respx(base_url=base_url)
    async def test_async_stream_helper_without_a_message_start_has_no_output(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response([]))
        client = make_async_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        async with client.messages.stream(**REQUEST) as stream:
            await stream.until_done()

        span = spans.one("anthropic.messages.create")
        assert "gen_ai.input.messages" in attributes(span)
        assert "gen_ai.output.messages" not in attributes(span)

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_stream_helper_that_cannot_accumulate_an_event_has_no_output(
        self, beta: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        events = tool_stream_events()
        events[5] = {**events[5], "delta": {"type": "input_json_delta", "partial_json": '{"city": nowhere'}}
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        with pytest.raises(ValueError, match="Unable to parse tool parameter JSON"):
            with messages_resource(client, beta=beta).stream(**REQUEST) as stream:
                stream.until_done()

        # The snapshot stopped following the stream, so it is no output. What the span has from it besides stays.
        span = spans.one("anthropic.messages.create")
        assert attributes(span)["gen_ai.response.id"] == "msg_1"
        assert "gen_ai.input.messages" in attributes(span)
        assert "gen_ai.output.messages" not in attributes(span)

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_stream_helper_that_cannot_accumulate_an_event_has_no_output(
        self, beta: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        events = tool_stream_events()
        events[5] = {**events[5], "delta": {"type": "input_json_delta", "partial_json": '{"city": nowhere'}}
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events))
        client = make_async_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        with pytest.raises(ValueError, match="Unable to parse tool parameter JSON"):
            async with messages_resource(client, beta=beta).stream(**REQUEST) as stream:
                await stream.until_done()

        span = spans.one("anthropic.messages.create")
        assert attributes(span)["gen_ai.response.id"] == "msg_1"
        assert "gen_ai.output.messages" not in attributes(span)

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_stream_read_without_the_stream_helper_records_everything_but_its_content(
        self, beta: bool, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(tool_stream_events()))
        accumulated = count_accumulated_events(monkeypatch, beta=beta)
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        for _ in messages_resource(client, beta=beta).create(**REQUEST, stream=True):
            pass

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.OK
        assert attributes(span)["gen_ai.response.id"] == "msg_1"
        assert attributes(span)["gen_ai.usage.output_tokens"] == 5
        assert attributes(span)["anthropic.message.stop_reason"] == "end_turn"
        assert "gen_ai.input.messages" in attributes(span)
        # `create(stream=True)` accumulates no Message for the application, and the span accumulates no block's deltas either.
        assert "gen_ai.output.messages" not in attributes(span)
        assert accumulated == ["message_start", "content_block_start", "content_block_start", "message_delta"]

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_stream_read_without_the_stream_helper_records_everything_but_its_content(
        self, beta: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(tool_stream_events()))
        client = make_async_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        async for _ in await messages_resource(client, beta=beta).create(**REQUEST, stream=True):
            pass

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.OK
        assert attributes(span)["gen_ai.usage.output_tokens"] == 5
        assert "gen_ai.input.messages" in attributes(span)
        assert "gen_ai.output.messages" not in attributes(span)

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_stream_read_without_the_stream_helper_that_ends_early_has_no_output(
        self, beta: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(cut_tool_stream_events()))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        for _ in messages_resource(client, beta=beta).create(**REQUEST, stream=True):
            pass

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.ERROR
        assert "gen_ai.input.messages" in attributes(span)
        assert "gen_ai.output.messages" not in attributes(span)

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_stream_read_without_the_stream_helper_that_ends_early_has_no_output(
        self, beta: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response(cut_tool_stream_events()))
        client = make_async_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        async for _ in await messages_resource(client, beta=beta).create(**REQUEST, stream=True):
            pass

        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.ERROR
        assert "gen_ai.input.messages" in attributes(span)
        assert "gen_ai.output.messages" not in attributes(span)

    @pytest.mark.respx(base_url=base_url)
    def test_closed_stream_has_no_output(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=stream_response())
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        stream = create(client, stream=True)
        next(iter(stream))
        stream.close()

        span = spans.one("anthropic.messages.create")
        assert "gen_ai.input.messages" in attributes(span)
        assert "gen_ai.output.messages" not in attributes(span)

    @pytest.mark.respx(base_url=base_url)
    def test_size_bound_removes_the_oldest_input_parts(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))
        big = "x" * 300_000

        client.messages.create(
            max_tokens=1024,
            model="claude-test",
            messages=[
                {"role": "user", "content": "first " + big},
                {"role": "assistant", "content": "second " + big},
                {"role": "user", "content": "third " + big},
                {"role": "assistant", "content": "fourth"},
                {"role": "user", "content": "fifth"},
            ],
        )

        span = spans.one("anthropic.messages.create")
        messages = json.loads(attributes(span)["gen_ai.input.messages"])
        # Removing the part of the first message brings the three large ones under the bound. The message stays.
        assert [message["role"] for message in messages] == ["user", "assistant", "user", "assistant", "user"]
        assert messages[0]["parts"] == []
        # The span says that content was removed, and the content itself holds no marker.
        assert messages[1]["parts"] == [{"type": "text", "content": "second " + big}]
        assert attributes(span)["anthropic.content.truncated"] is True
        assert content_size(span) <= CONTENT_LIMIT

    @pytest.mark.respx(base_url=base_url)
    def test_size_bound_counts_the_content_of_a_tool_result(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))
        big = "x" * 600_000
        search_result: SearchResultBlockParam = {
            "type": "search_result",
            "source": "https://example.com/cats",
            "title": "Cats",
            "content": [{"type": "text", "text": big}],
        }

        client.messages.create(
            max_tokens=1024,
            model="claude-test",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "tool_result", "tool_use_id": "toolu_0", "content": [{"type": "text", "text": big}]}
                    ],
                },
                {
                    "role": "user",
                    "content": [{"type": "tool_result", "tool_use_id": "toolu_1", "content": [search_result]}],
                },
                {"role": "user", "content": "third"},
            ],
        )

        span = spans.one("anthropic.messages.create")
        messages = json.loads(attributes(span)["gen_ai.input.messages"])
        # The two tool results are over the bound together, so the part of the first one is removed whole.
        assert [message["parts"] for message in messages] == [
            [],
            [{"type": "tool_call_response", "id": "toolu_1", "response": [search_result]}],
            [{"type": "text", "content": "third"}],
        ]
        assert attributes(span)["anthropic.content.truncated"] is True
        assert content_size(span) <= CONTENT_LIMIT

    @pytest.mark.respx(base_url=base_url)
    def test_size_bound_counts_a_result_that_is_one_object(self, spans: Spans, respx_mock: MockRouter) -> None:
        def result(tool_use_id: str, stdout: str) -> dict[str, Any]:
            return {
                "type": "code_execution_tool_result",
                "tool_use_id": tool_use_id,
                "content": {
                    "type": "code_execution_result",
                    "stdout": stdout,
                    "stderr": "",
                    "return_code": 0,
                    "content": [],
                },
            }

        big = "x" * 600_000
        response = {**MESSAGE, "content": [{"type": "text", "text": "Done"}, result("srvtoolu_2", big)]}
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=MESSAGE), httpx2.Response(200, json=response)]
        )
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        client.messages.create(
            max_tokens=1024,
            model="claude-test",
            messages=[
                {"role": "assistant", "content": [cast(Any, result("srvtoolu_0", big))]},
                {"role": "assistant", "content": [cast(Any, result("srvtoolu_1", big))]},
                {"role": "user", "content": "third"},
            ],
        )
        client.messages.create(**REQUEST, system="s" * 600_000)

        of_input, of_output = spans.named("anthropic.messages.create")
        # The two large results are over the bound together, so the part of the first one is removed whole.
        first, second, _ = json.loads(attributes(of_input)["gen_ai.input.messages"])
        assert first == {"role": "assistant", "parts": []}
        assert second["parts"][0]["id"] == "srvtoolu_1"
        # The output's large result counts too: the system instructions make room for it, and it stays whole.
        assert attributes(of_output)["gen_ai.system_instructions"] == "[]"
        (output,) = json.loads(attributes(of_output)["gen_ai.output.messages"])
        assert [part["type"] for part in output["parts"]] == ["text", "tool_call_response"]
        assert output["parts"][1]["response"]["stdout"] == big
        for span in (of_input, of_output):
            assert attributes(span)["anthropic.content.truncated"] is True
            assert content_size(span) <= CONTENT_LIMIT

    @pytest.mark.respx(base_url=base_url)
    def test_span_without_content_attributes_is_never_marked_truncated(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        client = make_client(spans)
        big = "x" * 600_000

        client.messages.create(
            max_tokens=1024,
            model="claude-test",
            messages=[{"role": "user", "content": big}, {"role": "assistant", "content": big}],
        )

        span = spans.one("anthropic.messages.create")
        assert "gen_ai.input.messages" not in attributes(span)
        assert "anthropic.content.truncated" not in attributes(span)

    @pytest.mark.respx(base_url=base_url)
    def test_size_bound_counts_streamed_output_and_removes_the_oldest_input_parts(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        events = stream_events()
        delta = {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "y" * 225_000}}
        events[2:3] = [delta] * 2
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))
        big = "x" * 225_000
        inputs: list[Any] = [
            {"role": "user", "content": "first " + big},
            {"role": "assistant", "content": "second " + big},
            {"role": "user", "content": "third"},
        ]

        with client.messages.stream(max_tokens=1024, model="claude-test", messages=inputs) as stream:
            stream.until_done()

        span = spans.one("anthropic.messages.create")
        # The output is whole, and the part of the oldest input message makes room for it.
        assert json.loads(attributes(span)["gen_ai.output.messages"]) == [
            {"role": "assistant", "parts": [{"type": "text", "content": "y" * 450_000}]}
        ]
        assert json.loads(attributes(span)["gen_ai.input.messages"]) == [
            {"role": "user", "parts": []},
            {"role": "assistant", "parts": [{"type": "text", "content": "second " + big}]},
            {"role": "user", "parts": [{"type": "text", "content": "third"}]},
        ]
        assert attributes(span)["anthropic.content.truncated"] is True
        assert content_size(span) <= CONTENT_LIMIT

    @pytest.mark.respx(base_url=base_url)
    def test_one_streamed_output_part_over_the_bound_is_cut_from_its_end(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        events = stream_events()
        delta = {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "y" * 300_000}}
        events[2:3] = [delta] * 4
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        with client.messages.stream(
            max_tokens=1024, model="claude-test", messages=[{"role": "user", "content": "only"}]
        ) as stream:
            stream.until_done()

        span = spans.one("anthropic.messages.create")
        # The input's part goes first, and then the end of the output's only part. The input message stays.
        assert json.loads(attributes(span)["gen_ai.input.messages"]) == [{"role": "user", "parts": []}]
        (message,) = json.loads(attributes(span)["gen_ai.output.messages"])
        assert message["parts"] == [{"type": "text", "content": "y" * len(message["parts"][0]["content"])}]
        assert content_size(span) == CONTENT_LIMIT
        assert attributes(span)["anthropic.content.truncated"] is True

    @pytest.mark.respx(base_url=base_url)
    def test_size_bound_removes_the_first_output_parts_once_no_input_part_remains(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        big = "y" * 300_000
        blocks = [{"type": "text", "text": text + big} for text in ("first ", "second ", "third ")]
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json={**MESSAGE, "content": blocks}))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        client.messages.create(
            max_tokens=1024,
            model="claude-test",
            system="be brief",
            messages=[{"role": "user", "content": "first"}, {"role": "user", "content": "second"}],
        )

        span = spans.one("anthropic.messages.create")
        # The system instructions go first, and then the parts of the input messages, all of them.
        assert attributes(span)["gen_ai.system_instructions"] == "[]"
        assert json.loads(attributes(span)["gen_ai.input.messages"]) == [{"role": "user", "parts": []}] * 2
        # Then the output's first part goes, whole. That is enough, so the newest two are whole.
        assert json.loads(attributes(span)["gen_ai.output.messages"]) == [
            {
                "role": "assistant",
                "parts": [{"type": "text", "content": "second " + big}, {"type": "text", "content": "third " + big}],
            }
        ]
        assert attributes(span)["anthropic.content.truncated"] is True

    @pytest.mark.respx(base_url=base_url)
    def test_size_bound_removes_the_output_parts_of_a_stream_from_the_start(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        events = stream_events()
        blocks: list[dict[str, Any]] = []
        for index, text in enumerate(["first ", "second ", "third "]):
            blocks += [
                {"type": "content_block_start", "index": index, "content_block": {"type": "text", "text": ""}},
                {"type": "content_block_delta", "index": index, "delta": {"type": "text_delta", "text": text}},
                {"type": "content_block_delta", "index": index, "delta": {"type": "text_delta", "text": "y" * 600_000}},
                {"type": "content_block_stop", "index": index},
            ]
        events[1:4] = blocks
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        with client.messages.stream(
            max_tokens=1024, model="claude-test", messages=[{"role": "user", "content": "only"}]
        ) as stream:
            stream.until_done()

        span = spans.one("anthropic.messages.create")
        # The part of the only input message went, and then the output's first two parts. The last is whole.
        assert json.loads(attributes(span)["gen_ai.input.messages"]) == [{"role": "user", "parts": []}]
        assert json.loads(attributes(span)["gen_ai.output.messages"]) == [
            {"role": "assistant", "parts": [{"type": "text", "content": "third " + "y" * 600_000}]}
        ]
        assert attributes(span)["anthropic.content.truncated"] is True

    @pytest.mark.respx(base_url=base_url)
    def test_one_output_part_over_the_bound_is_cut_from_its_end(self, spans: Spans, respx_mock: MockRouter) -> None:
        text = "y" * 1_100_000
        message = {**MESSAGE, "content": [{"type": "text", "text": text}]}
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=message))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        client.messages.create(max_tokens=1024, model="claude-test", messages=[{"role": "user", "content": "only"}])

        span = spans.one("anthropic.messages.create")
        # The message without parts stays in its attribute, and the last part keeps the start of its text that fits.
        assert json.loads(attributes(span)["gen_ai.input.messages"]) == [{"role": "user", "parts": []}]
        (message,) = json.loads(attributes(span)["gen_ai.output.messages"])
        assert message["parts"] == [{"type": "text", "content": text[: len(message["parts"][0]["content"])]}]
        assert content_size(span) == CONTENT_LIMIT
        assert attributes(span)["anthropic.content.truncated"] is True

    @pytest.mark.respx(base_url=base_url)
    def test_one_input_part_over_the_bound_leaves_a_message_without_parts(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        client.messages.create(
            max_tokens=1024, model="claude-test", messages=[{"role": "user", "content": "x" * 1_100_000}]
        )

        span = spans.one("anthropic.messages.create")
        # It was the last part until the response came, so it was cut. With the output after it, it is removed whole.
        assert json.loads(attributes(span)["gen_ai.input.messages"]) == [{"role": "user", "parts": []}]
        # That was enough, so the output is whole.
        assert json.loads(attributes(span)["gen_ai.output.messages"]) == [
            {"role": "assistant", "parts": [{"type": "text", "content": "Hi there"}]}
        ]
        assert attributes(span)["anthropic.content.truncated"] is True

    def test_size_bound_removes_the_output_parts_from_the_start(self) -> None:
        part: TextPart = {"type": "text", "content": "x" * 100}
        last: TextPart = {"type": "text", "content": "y" * 100}
        output: OutputMessages = [{"role": "assistant", "parts": [part, part]}, {"role": "assistant", "parts": [last]}]
        whole = to_json(output)

        assert fit_content({OUTPUT: output}, len(whole)) == ({OUTPUT: whole}, False)

        values, truncated = fit_content({OUTPUT: output}, len(whole) - 1)

        # A part goes whole, however little there is to remove, and the comma after it goes with it.
        assert truncated is True
        assert json.loads(values[OUTPUT]) == [{"role": "assistant", "parts": [part]}, output[1]]
        assert len(values[OUTPUT]) == len(whole) - len(to_json(part)) - 1

        # The parts of every message are one list: a message that lost all of its parts stays, and the next one loses
        # parts after it.
        values, truncated = fit_content({OUTPUT: output}, len(whole) - 2 * len(to_json(part)) - 2)

        assert truncated is True
        shell: OutputMessage = {"role": "assistant", "parts": []}
        assert json.loads(values[OUTPUT]) == [
            shell,
            {"role": "assistant", "parts": [{"type": "text", "content": "y" * 99}]},
        ]
        assert len(values[OUTPUT]) == len(whole) - 2 * len(to_json(part)) - 2

        assert fit_content({OUTPUT: [shell, shell]}, -100) == ({OUTPUT: to_json([shell, shell])}, False)

    def test_size_bound_keeps_the_last_text_part_with_empty_content_when_none_of_it_fits(self) -> None:
        text: TextPart = {"type": "text", "content": "x" * 100}
        emptied: InputMessages = [
            {"role": "user", "parts": []},
            {"role": "user", "parts": [{"type": "text", "content": ""}]},
        ]
        messages: InputMessages = [{"role": "user", "parts": [text]}, {"role": "user", "parts": [text]}]

        # There is room for the part and not for any of its text, and then for neither: the part stays either way.
        for limit in (len(to_json(emptied)), len(to_json(emptied)) - 1, -100):
            assert fit_content({INPUT: messages}, limit) == ({INPUT: to_json(emptied)}, True)

        # A part that has no text to lose is no reason to mark the span.
        assert fit_content({INPUT: emptied}, -100) == ({INPUT: to_json(emptied)}, False)

    def test_size_bound_cuts_text_between_two_characters(self) -> None:
        # Each of these is one character of the text. In JSON they take three bytes, four, two, and six.
        characters = ["\u4e16", "\U0001f600", "\n", "\x01"]
        text = "".join(characters * 5)
        part: TextPart = {"type": "text", "content": text}
        whole = to_json([part])

        for limit in range(utf8_size(to_json([{"type": "text", "content": ""}])), utf8_size(whole)):
            values, truncated = fit_content({SYSTEM: [part]}, limit)

            assert truncated is True
            assert utf8_size(values[SYSTEM]) <= limit
            (cut,) = json.loads(values[SYSTEM])
            assert text.startswith(cut["content"])
            # The next character would not have fitted.
            assert utf8_size(to_json([{"type": "text", "content": text[: len(cut["content"]) + 1]}])) > limit

    def test_size_bound_removes_a_part_without_text_whole(self) -> None:
        text: Part = {"type": "text", "content": "x" * 100}
        call: Part = {"type": "tool_call", "id": "toolu_1", "name": "f", "arguments": {"content": "y" * 100}}
        reasoning: Part = {"type": "reasoning", "content": "z" * 100}
        image: Part = {"type": "anthropic_image"}

        def fit(parts: list[Part], limit: int) -> tuple[str, bool]:
            values, truncated = fit_content({OUTPUT: [{"role": "assistant", "parts": parts}]}, limit)
            return to_json(json.loads(values[OUTPUT])[0]["parts"]), truncated

        def size(parts: list[Part]) -> int:
            return len(to_json([{"role": "assistant", "parts": parts}]))

        assert fit([image, call, reasoning, text], size([image, call, reasoning, text])) == (
            to_json([image, call, reasoning, text]),
            False,
        )
        assert fit([image, call, reasoning, text], size([image, call, reasoning, text]) - 1) == (
            to_json([call, reasoning, text]),
            True,
        )
        # The tool call goes whole, which is more than it takes, so the parts after it stay whole.
        assert fit([call, reasoning, text], size([call, reasoning, text]) - 1) == (to_json([reasoning, text]), True)
        # The reasoning is not cut as text is: it goes whole when it is the first part, and when it is the last one left.
        assert fit([reasoning, text], size([reasoning, text]) - 1) == (to_json([text]), True)
        assert fit([text, reasoning], size([reasoning]) - 1) == ("[]", True)
        assert fit([text, call], size([call]) - 1) == ("[]", True)
        assert fit([text, image], size([image]) - 1) == ("[]", True)
        # Only the text of the last part left is cut.
        assert fit([call, text], size([text]) - 1) == (to_json([{"type": "text", "content": "x" * 99}]), True)

    @pytest.mark.respx(base_url=base_url)
    def test_size_bound_removes_the_tool_call_before_the_text_that_it_cuts(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        text = "\U0001f600" * 1_100_000
        blocks = [
            {"type": "tool_use", "id": "toolu_1", "name": "f", "input": {"a": 1}},
            {"type": "text", "text": text},
        ]
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json={**MESSAGE, "content": blocks}))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        client.messages.create(max_tokens=1024, model="claude-test", messages=[{"role": "user", "content": "only"}])

        span = spans.one("anthropic.messages.create")
        assert json.loads(attributes(span)["gen_ai.input.messages"]) == [{"role": "user", "parts": []}]
        (message,) = json.loads(attributes(span)["gen_ai.output.messages"])
        assert message["parts"] == [{"type": "text", "content": text[: len(message["parts"][0]["content"])]}]
        # Each character of the text is four bytes, and the cut is not inside one.
        assert CONTENT_LIMIT - 4 < content_size(span) <= CONTENT_LIMIT
        assert attributes(span)["anthropic.content.truncated"] is True

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_over_the_bound_is_recorded_like_a_parsed_one(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        text = "y" * 1_100_000
        message = {**MESSAGE, "content": [{"type": "text", "text": text}]}
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=message))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        raw = client.messages.with_raw_response.create(
            max_tokens=1024,
            model="claude-test",
            messages=[
                {"role": "user", "content": "first"},
                {"role": "assistant", "content": "second"},
                {"role": "user", "content": "third"},
            ],
        )

        assert len(raw.http_response.content) > CONTENT_LIMIT
        span = spans.one("anthropic.messages.create")
        assert attributes(span)["gen_ai.response.id"] == "msg_1"
        assert attributes(span)["gen_ai.response.model"] == "claude-test"
        assert attributes(span)["gen_ai.usage.output_tokens"] == 5
        assert attributes(span)["anthropic.message.stop_reason"] == "end_turn"
        assert json.loads(attributes(span)["gen_ai.input.messages"]) == [
            {"role": "user", "parts": []},
            {"role": "assistant", "parts": []},
            {"role": "user", "parts": []},
        ]
        (output,) = json.loads(attributes(span)["gen_ai.output.messages"])
        assert output["parts"] == [{"type": "text", "content": text[: len(output["parts"][0]["content"])]}]
        assert content_size(span) == CONTENT_LIMIT
        assert attributes(span)["anthropic.content.truncated"] is True

    @pytest.mark.respx(base_url=base_url)
    def test_size_bound_counts_bytes_not_characters(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))
        # 225,000 characters that are 675,000 bytes of UTF-8: two such messages fit as characters, not as bytes.
        big = "\u20ac" * 225_000

        client.messages.create(
            max_tokens=1024,
            model="claude-test",
            messages=[
                {"role": "user", "content": big},
                {"role": "assistant", "content": big},
                {"role": "user", "content": "last"},
            ],
        )

        span = spans.one("anthropic.messages.create")
        assert json.loads(attributes(span)["gen_ai.input.messages"]) == [
            chat_message("user"),
            chat_message("assistant", text_part(big)),
            chat_message("user", text_part("last")),
        ]
        assert 675_000 < content_size(span) <= CONTENT_LIMIT
        assert attributes(span)["anthropic.content.truncated"] is True

    @pytest.mark.respx(base_url=base_url)
    def test_input_messages_under_the_bound_are_the_json_of_the_whole_list(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        client.messages.create(
            max_tokens=1024,
            model="claude-test",
            messages=[
                {"role": "user", "content": "h\u00e9llo \u20ac, [1]"},
                {
                    "role": "assistant",
                    "content": [
                        {"type": "text", "text": "hi"},
                        {"type": "tool_use", "id": "toolu_1", "name": "f", "input": {"a": [1, "\u00e9"], "b": None}},
                    ],
                },
                {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "toolu_1", "content": "done"}]},
            ],
        )

        expected: InputMessages = [
            {"role": "user", "parts": [{"type": "text", "content": "h\u00e9llo \u20ac, [1]"}]},
            {
                "role": "assistant",
                "parts": [
                    {"type": "text", "content": "hi"},
                    {"type": "tool_call", "id": "toolu_1", "name": "f", "arguments": {"a": [1, "\u00e9"], "b": None}},
                ],
            },
            {
                "role": "user",
                "parts": [
                    {"type": "tool_call_response", "id": "toolu_1", "response": [{"type": "text", "text": "done"}]}
                ],
            },
        ]
        span = spans.one("anthropic.messages.create")
        assert attributes(span)["gen_ai.input.messages"] == json.dumps(
            expected, separators=(",", ":"), ensure_ascii=False
        )
        assert "anthropic.content.truncated" not in attributes(span)
        assert fit_content({INPUT: expected}, CONTENT_LIMIT) == ({INPUT: to_json(expected)}, False)

    def test_size_bound_removes_input_parts_not_whole_messages(self) -> None:
        part: TextPart = {"type": "text", "content": "x" * 100}
        message: ChatMessage = {"role": "user", "parts": [part, part]}
        messages: InputMessages = [message] * 3
        whole = to_json(messages)
        # One part less, and the comma after it: nothing is set aside for a marker.
        limit = len(whole) - len(to_json(part)) - 1

        for room in (len(whole) - 1, limit):
            values, truncated = fit_content({INPUT: messages}, room)

            assert truncated is True
            assert json.loads(values[INPUT]) == [{"role": "user", "parts": [part]}, message, message]
            assert len(values[INPUT]) == limit

        values, truncated = fit_content({INPUT: messages}, limit - 1)

        assert truncated is True
        assert json.loads(values[INPUT]) == [{"role": "user", "parts": []}, message, message]

    def test_size_bound_cuts_the_newest_input_part_when_no_other_is_left(self) -> None:
        messages: InputMessages = [
            {"role": "user", "parts": [{"type": "text", "content": "old"}]},
            {"role": "user", "parts": [{"type": "text", "content": "x" * 1000}]},
        ]
        kept: InputMessages = [
            {"role": "user", "parts": []},
            {"role": "user", "parts": [{"type": "text", "content": "x" * 30}]},
        ]

        assert fit_content({INPUT: messages}, len(to_json(kept))) == ({INPUT: to_json(kept)}, True)
        # The older part goes although the newer one is cut all the same.
        assert fit_content({INPUT: messages}, len(to_json(kept)) + len('{"type":"text","content":"old"}')) == (
            {INPUT: to_json([kept[0], {"role": "user", "parts": [{"type": "text", "content": "x" * 61}]}])},
            True,
        )

    def test_size_bound_gives_what_removing_one_part_or_character_at_a_time_gives(self) -> None:
        def size(values: Mapping[Any, Any]) -> int:
            return sum(utf8_size(to_json(value)) for value in values.values())

        def one_at_a_time(attributes: dict[AttributeName, Any], limit: int) -> tuple[dict[str, str], bool]:
            values: dict[str, Any] = json.loads(json.dumps({k: v for k, v in attributes.items() if v is not None}))
            lists = [values[SYSTEM]] if SYSTEM in values else []
            lists += [message["parts"] for key in (INPUT, OUTPUT) for message in values.get(key, [])]
            truncated = False
            while size(values) > limit and sum(map(len, lists)) > 1:
                next(parts for parts in lists if parts).pop(0)
                truncated = True
            for parts in lists:
                if size(values) > limit and parts and parts[0]["type"] != "text":
                    parts.pop(0)
                    truncated = True
                while size(values) > limit and parts and parts[0]["content"]:
                    parts[0]["content"] = parts[0]["content"][:-1]
                    truncated = True
            return {key: to_json(value) for key, value in values.items()}, truncated

        def some_of(parts: list[Part]) -> list[Part]:
            return parts[random.randrange(len(parts) + 1) :]

        random = Random(613)
        for _ in range(500):
            parts: list[Part] = [
                cast(Part, {"type": kind, "content": "\u00e9\n" * random.randrange(1, 20)})
                if kind != "anthropic_image"
                else {"type": kind}
                for kind in random.choices(["text", "reasoning", "anthropic_image"], [3, 1, 1], k=random.randrange(6))
            ]

            attributes: dict[AttributeName, Any] = {
                SYSTEM: random.choice([None, some_of(parts)]),
                INPUT: [{"role": "user", "parts": some_of(parts)} for _ in range(random.randrange(4))],
                OUTPUT: random.choice(
                    [None, [{"role": "assistant", "parts": some_of(parts)} for _ in range(random.randrange(1, 3))]]
                ),
            }
            limit = random.randrange(
                -5, size({key: value for key, value in attributes.items() if value is not None}) + 5
            )

            assert fit_content(attributes, limit) == one_at_a_time(attributes, limit)

    @pytest.mark.parametrize(("limit", "content", "expected", "truncated", "sizes"), SIZE_BOUND_CASES)
    def test_size_bound_cases(
        self,
        spans: Spans,
        limit: int,
        content: dict[str, Any],
        expected: dict[str, Any],
        truncated: bool,
        sizes: tuple[int, int],
    ) -> None:
        stops: list[str] = content.get(STOPS, [])
        given: dict[AttributeName, Any] = {key: content.get(key) for key in (SYSTEM, INPUT, OUTPUT)}
        values_before = [to_json(value) for value in given.values() if value is not None]
        size_before = sum(map(utf8_size, [*stops, *values_before]))
        span = spans.provider.get_tracer("test").start_span("anthropic.messages.create")
        assert isinstance(span, ReadableSpan)

        assert size_before == sizes[0]

        set_content_attributes(span, given, limit=limit, stop_sequences=stops)

        # An attribute that the span does not have is not created. One that it has stays, except for stop sequences
        # that exceed the bound by themselves: `None` for them in `expected` says that the span has none.
        expected_stops = expected.get(STOPS)
        kept_stops = attributes(span).get(STOPS)
        values = {key: attributes(span)[key] for key in (SYSTEM, INPUT, OUTPUT) if key in attributes(span)}
        assert kept_stops == (None if expected_stops is None else tuple(expected_stops))
        assert {key: json.loads(value) for key, value in values.items()} == {
            key: value for key, value in expected.items() if key != STOPS
        }
        assert attributes(span).get("anthropic.content.truncated", False) is truncated
        assert sum(map(utf8_size, [*(kept_stops or ()), *values.values()])) == sizes[1]

    @pytest.mark.respx(base_url=base_url)
    def test_system_instructions_are_removed_first(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))
        inputs: list[Any] = [
            {"role": "user", "content": "first"},
            {"role": "assistant", "content": "second"},
            {"role": "user", "content": "third"},
        ]

        client.messages.create(max_tokens=1024, model="claude-test", system="s" * 1_100_000, messages=inputs)

        span = spans.one("anthropic.messages.create")
        # The system instructions go first, whole. The emptied list stays, and so does everything after it.
        assert attributes(span)["gen_ai.system_instructions"] == "[]"
        assert json.loads(attributes(span)["gen_ai.input.messages"]) == [
            {"role": message["role"], "parts": [{"type": "text", "content": message["content"]}]} for message in inputs
        ]
        assert json.loads(attributes(span)["gen_ai.output.messages"]) == [
            {"role": "assistant", "parts": [{"type": "text", "content": "Hi there"}]}
        ]
        assert attributes(span)["anthropic.content.truncated"] is True

    @pytest.mark.respx(base_url=base_url)
    def test_system_instructions_go_before_the_input_and_the_output(self, spans: Spans, respx_mock: MockRouter) -> None:
        text = "y" * 600_000
        message = {**MESSAGE, "content": [{"type": "text", "text": text}]}
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=message))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))
        system: list[TextBlockParam] = [{"type": "text", "text": "first"}, {"type": "text", "text": "s" * 600_000}]

        client.messages.create(
            max_tokens=1024, model="claude-test", system=system, messages=[{"role": "user", "content": "only"}]
        )

        span = spans.one("anthropic.messages.create")
        assert attributes(span)["gen_ai.system_instructions"] == "[]"
        assert json.loads(attributes(span)["gen_ai.input.messages"]) == [
            {"role": "user", "parts": [{"type": "text", "content": "only"}]}
        ]
        assert json.loads(attributes(span)["gen_ai.output.messages"]) == [
            {"role": "assistant", "parts": [{"type": "text", "content": text}]}
        ]
        assert attributes(span)["anthropic.content.truncated"] is True

    @pytest.mark.respx(base_url=base_url)
    def test_system_instructions_lose_parts_from_their_start(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))
        system: list[TextBlockParam] = [
            {"type": "text", "text": "a" * 600_000},
            {"type": "text", "text": "b" * 600_000},
            {"type": "text", "text": "c" * 600_000},
        ]

        client.messages.create(
            max_tokens=1024, model="claude-test", system=system, messages=[{"role": "user", "content": "only"}]
        )

        span = spans.one("anthropic.messages.create")
        assert json.loads(attributes(span)["gen_ai.system_instructions"]) == [
            {"type": "text", "content": "c" * 600_000}
        ]
        assert json.loads(attributes(span)["gen_ai.input.messages"]) == [
            {"role": "user", "parts": [{"type": "text", "content": "only"}]}
        ]
        assert json.loads(attributes(span)["gen_ai.output.messages"]) == [
            {"role": "assistant", "parts": [{"type": "text", "content": "Hi there"}]}
        ]
        assert attributes(span)["anthropic.content.truncated"] is True

    @pytest.mark.respx(base_url=base_url)
    def test_no_input_messages_are_an_empty_list_even_when_the_other_content_attributes_exceed_the_limit(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        client.messages.create(max_tokens=1024, model="claude-test", system="s" * 1_100_000, messages=[])

        span = spans.one("anthropic.messages.create")
        assert attributes(span)["gen_ai.input.messages"] == "[]"
        # There was no input part to remove, and the system instructions went before the output's part.
        assert attributes(span)["gen_ai.system_instructions"] == "[]"
        assert json.loads(attributes(span)["gen_ai.output.messages"]) == [
            {"role": "assistant", "parts": [{"type": "text", "content": "Hi there"}]}
        ]
        assert attributes(span)["anthropic.content.truncated"] is True
        assert fit_content({INPUT: []}, -100) == ({INPUT: "[]"}, False)

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_stop_sequences(self, beta: bool, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=MESSAGE), stream_response(), stream_response()]
        )
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))
        messages = messages_resource(client, beta=beta)

        messages.create(**REQUEST, stop_sequences=["END", "\n\nHuman:"])
        for _ in messages.create(**REQUEST, stop_sequences=["END", "\n\nHuman:"], stream=True):
            pass
        with messages.stream(**REQUEST, stop_sequences=["END", "\n\nHuman:"]) as stream:
            stream.until_done()

        unary, raw_stream, helper_stream = spans.named("anthropic.messages.create")
        for span in (unary, raw_stream, helper_stream):
            # An array with one element for each stop sequence, not a JSON string.
            assert attributes(span)["gen_ai.request.stop_sequences"] == ("END", "\n\nHuman:")
            assert "anthropic.content.truncated" not in attributes(span)

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_stop_sequences(self, beta: bool, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[httpx2.Response(200, json=MESSAGE), stream_response()])
        client = make_async_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))
        messages = messages_resource(client, beta=beta)

        await messages.create(**REQUEST, stop_sequences=["END"])
        async with messages.stream(**REQUEST, stop_sequences=["END"]) as stream:
            await stream.until_done()

        for span in spans.named("anthropic.messages.create"):
            assert attributes(span)["gen_ai.request.stop_sequences"] == ("END",)

    @pytest.mark.respx(base_url=base_url)
    def test_stop_sequences_are_content(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))

        create(make_client(spans), stop_sequences=["END"])

        assert "gen_ai.request.stop_sequences" not in attributes(spans.one("anthropic.messages.create"))

    @pytest.mark.respx(base_url=base_url)
    def test_no_stop_sequences_set_no_attribute(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))

        create(client)
        create(client, stop_sequences=[])

        unset, empty = spans.named("anthropic.messages.create")
        assert "gen_ai.input.messages" in attributes(unset)
        assert "gen_ai.request.stop_sequences" not in attributes(unset)
        assert "gen_ai.request.stop_sequences" not in attributes(empty)

    @pytest.mark.respx(base_url=base_url)
    def test_size_bound_counts_the_stop_sequences_that_stay(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))
        big = "x" * 300_000

        client.messages.create(
            max_tokens=1024,
            model="claude-test",
            stop_sequences=["a" + big, "b" + big],
            messages=[{"role": "user", "content": "first " + big}, {"role": "user", "content": "second"}],
        )

        span = spans.one("anthropic.messages.create")
        # The messages alone are under the limit: the part of the first goes because the stop sequences count too.
        assert attributes(span)["gen_ai.request.stop_sequences"] == ("a" + big, "b" + big)
        assert json.loads(attributes(span)["gen_ai.input.messages"]) == [
            {"role": "user", "parts": []},
            {"role": "user", "parts": [{"type": "text", "content": "second"}]},
        ]
        assert attributes(span)["anthropic.content.truncated"] is True

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_stop_sequences_exactly_at_the_bound_stay(self, beta: bool, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[httpx2.Response(200, json=MESSAGE), stream_response()])
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))
        messages = messages_resource(client, beta=beta)
        stops = ["a" * 50_000, "b" * 700_000]
        assert sum(map(len, stops)) == CONTENT_LIMIT

        messages.create(**REQUEST, stop_sequences=stops)
        with messages.stream(**REQUEST, stop_sequences=stops) as stream:
            stream.until_done()

        unary, streamed = spans.named("anthropic.messages.create")
        for span in (unary, streamed):
            # They leave no room, so everything that can go does. The last part left is text: it stays, without its text.
            assert attributes(span)["gen_ai.request.stop_sequences"] == tuple(stops)
            assert json.loads(attributes(span)["gen_ai.input.messages"]) == [{"role": "user", "parts": []}]
            assert json.loads(attributes(span)["gen_ai.output.messages"]) == [
                {"role": "assistant", "parts": [{"type": "text", "content": ""}]}
            ]
            assert attributes(span)["anthropic.content.truncated"] is True

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_stop_sequences_alone_over_the_bound_are_removed_whole(
        self, beta: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[httpx2.Response(200, json=MESSAGE), stream_response()])
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))
        messages = messages_resource(client, beta=beta)
        stops = ["a" * 50_001, "b" * 700_000]
        assert sum(map(len, stops)) == CONTENT_LIMIT + 1

        messages.create(**REQUEST, stop_sequences=stops)
        with messages.stream(**REQUEST, stop_sequences=stops) as stream:
            stream.until_done()

        unary, streamed = spans.named("anthropic.messages.create")
        for span in (unary, streamed):
            # The stop sequences go whole and no longer count, so everything else has the whole limit and stays.
            assert "gen_ai.request.stop_sequences" not in attributes(span)
            assert json.loads(attributes(span)["gen_ai.input.messages"]) == [
                {"role": "user", "parts": [{"type": "text", "content": "Hello"}]}
            ]
            assert json.loads(attributes(span)["gen_ai.output.messages"]) == [
                {"role": "assistant", "parts": [{"type": "text", "content": "Hi there"}]}
            ]
            assert attributes(span)["anthropic.content.truncated"] is True

    @pytest.mark.parametrize("over", [False, True], ids=["at_the_bound", "one_over"])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_stop_sequences_alone_over_the_bound_are_removed_whole(
        self, over: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[httpx2.Response(200, json=MESSAGE), stream_response()])
        traces: OpenTelemetryTraces = {"content_mode": "content", "max_content_bytes": 100}
        client = make_async_client(spans, open_telemetry=spans.option(traces=traces))
        stops = ["a" * 40, "b" * (61 if over else 60)]

        await client.messages.create(**REQUEST, stop_sequences=stops)
        async with client.messages.stream(**REQUEST, stop_sequences=stops) as stream:
            await stream.until_done()

        unary, streamed = spans.named("anthropic.messages.create")
        for span in (unary, streamed):
            assert attributes(span).get("gen_ai.request.stop_sequences") == (None if over else tuple(stops))
            # Without the stop sequences there is room for the output, and not for the input before it.
            assert json.loads(attributes(span)["gen_ai.input.messages"]) == [{"role": "user", "parts": []}]
            assert json.loads(attributes(span)["gen_ai.output.messages"]) == [
                {"role": "assistant", "parts": [{"type": "text", "content": "Hi there" if over else ""}]}
            ]
            assert attributes(span)["anthropic.content.truncated"] is True

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize("over", [False, True], ids=["at_the_bound", "one_byte_over"])
    @pytest.mark.respx(base_url=base_url)
    async def test_stop_sequences_are_measured_in_bytes(
        self, over: bool, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        traces: OpenTelemetryTraces = {"content_mode": "content", "max_content_bytes": 100}
        make: Callable[..., Any] = make_client if sync else make_async_client
        client = make(spans, open_telemetry=spans.option(traces=traces))
        # Each `\u00e9` is one character and two bytes, so these are 80 or 81 characters, and 100 or 101 bytes.
        stops = ["\u00e9" * 20, "b" * (61 if over else 60)]
        assert sum(map(utf8_size, stops)) == (101 if over else 100)

        result = client.messages.create(**REQUEST, stop_sequences=stops)
        if inspect.isawaitable(result):
            await result

        span = spans.one("anthropic.messages.create")
        assert attributes(span).get("gen_ai.request.stop_sequences") == (None if over else tuple(stops))
        assert json.loads(attributes(span)[INPUT]) == [chat_message("user")]
        assert json.loads(attributes(span)[OUTPUT]) == [
            chat_message("assistant", text_part("Hi there" if over else ""))
        ]
        assert attributes(span)["anthropic.content.truncated"] is True

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize(
        ("limit", "input_parts", "output_characters", "size"),
        [
            # The input is 61 bytes, and the output 61 and its text. The text is 10 characters and 20 bytes.
            pytest.param(142, [text_part("Hello")], 10, 142, id="parts_at_the_bound"),
            pytest.param(141, [], 10, 109, id="parts_one_byte_over"),
            # Without its part the input is 28 bytes, which leaves 12 or 11 for the text, and so 6 or 5 characters.
            pytest.param(101, [], 6, 101, id="cut_at_the_bound"),
            pytest.param(100, [], 5, 99, id="cut_one_byte_over"),
        ],
    )
    @pytest.mark.respx(base_url=base_url)
    async def test_parts_and_the_cut_of_the_last_text_part_are_measured_in_bytes(
        self,
        limit: int,
        input_parts: list[dict[str, Any]],
        output_characters: int,
        size: int,
        sync: bool,
        spans: Spans,
        respx_mock: MockRouter,
    ) -> None:
        message = {**MESSAGE, "content": [{"type": "text", "text": "\u00e9" * 10}]}
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=message))
        traces: OpenTelemetryTraces = {"content_mode": "content", "max_content_bytes": limit}
        make: Callable[..., Any] = make_client if sync else make_async_client
        client = make(spans, open_telemetry=spans.option(traces=traces))

        await call_messages(client, REQUEST["messages"])

        span = spans.one("anthropic.messages.create")
        assert json.loads(attributes(span)[INPUT]) == [chat_message("user", *input_parts)]
        assert json.loads(attributes(span)[OUTPUT]) == [
            chat_message("assistant", text_part("\u00e9" * output_characters))
        ]
        assert content_size(span) == size <= limit
        assert attributes(span).get("anthropic.content.truncated", False) is (limit < 142)

    @pytest.mark.respx(base_url=base_url)
    def test_stop_sequences_over_the_bound_are_removed_before_the_parts(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        client = make_client(spans, open_telemetry=spans.option(traces={"content_mode": "content"}))
        big = "x" * 300_000

        client.messages.create(
            max_tokens=1024,
            model="claude-test",
            stop_sequences=["a" + big, "b" + big, "c" + big],
            messages=[
                {"role": "user", "content": "first " + big},
                {"role": "user", "content": "second " + big},
                {"role": "user", "content": "third " + big},
            ],
        )

        span = spans.one("anthropic.messages.create")
        # Without the stop sequences the messages are still over the limit, so the oldest part goes as it did before.
        assert "gen_ai.request.stop_sequences" not in attributes(span)
        assert json.loads(attributes(span)["gen_ai.input.messages"]) == [
            {"role": "user", "parts": []},
            {"role": "user", "parts": [{"type": "text", "content": "second " + big}]},
            {"role": "user", "parts": [{"type": "text", "content": "third " + big}]},
        ]
        assert content_size(span) <= CONTENT_LIMIT
        assert attributes(span)["anthropic.content.truncated"] is True


def resource_ids(span: ReadableSpan) -> dict[str, Any]:
    """The attributes of `span` that hold the ID of an API object."""
    common = ("anthropic.request.id", "anthropic.organization.id", "anthropic.workspace.id")
    return {key: value for key, value in attributes(span).items() if key.endswith(".id") and key not in common}


def assert_http_attributes(span: ReadableSpan, method: str, path: str) -> None:
    """Checks that `span` is of a `method` request to `path`, and that its route is `path` with a placeholder for each ID."""
    assert attributes(span)["http.request.method"] == method
    assert attributes(span)["url.path"] == path
    route = str(attributes(span)["http.route"])
    assert re.fullmatch(re.sub(r"\\\{\w+\\\}", "[^/]+", re.escape(route)), path), route
    assert route.count("{") == sum(part not in route.split("/") for part in path.split("/")), route


# One method of each resource: what calls it, the request it makes, the body of its response, and its span's name and IDs.
ResourceCall = tuple[Callable[[Any], Any], str, str, dict[str, Any], str, dict[str, str]]
RESOURCE_CALLS: list[ResourceCall] = [
    (
        lambda client: client.messages.batches.retrieve("msgbatch_1"),
        "GET",
        "/v1/messages/batches/msgbatch_1",
        {"id": "msgbatch_1"},
        "anthropic.messages.batches.retrieve",
        {"anthropic.message.batch.id": "msgbatch_1"},
    ),
    (
        lambda client: client.beta.messages.batches.cancel("msgbatch_1"),
        "POST",
        "/v1/messages/batches/msgbatch_1/cancel",
        {"id": "msgbatch_1"},
        "anthropic.messages.batches.cancel",
        {"anthropic.message.batch.id": "msgbatch_1"},
    ),
    # The value is the one in the path, which can be an alias.
    (
        lambda client: client.models.retrieve("claude-latest"),
        "GET",
        "/v1/models/claude-latest",
        {"id": "claude-1"},
        "anthropic.models.retrieve",
        {"anthropic.model.id": "claude-latest"},
    ),
    (
        lambda client: client.beta.files.upload(file=("notes.txt", b"Hello")),
        "POST",
        "/v1/files",
        {"id": "file_1"},
        "anthropic.files.upload",
        {"anthropic.file.id": "file_1"},
    ),
    (
        lambda client: client.files.delete("file_1"),
        "DELETE",
        "/v1/files/file_1",
        {"id": "file_1"},
        "anthropic.files.delete",
        {"anthropic.file.id": "file_1"},
    ),
    (
        lambda client: client.beta.skills.create(files=[("skill/SKILL.md", b"Hello")]),
        "POST",
        "/v1/skills",
        {"id": "skill_1"},
        "anthropic.skills.create",
        {"anthropic.skill.id": "skill_1"},
    ),
    # A path parameter that is not an ID has an attribute too, with the value in the path.
    (
        lambda client: client.skills.versions.retrieve("latest", skill_id="skill_1"),
        "GET",
        "/v1/skills/skill_1/versions/latest",
        {"id": "skillver_1", "version": "1759178010641129"},
        "anthropic.skills.versions.retrieve",
        {"anthropic.skill.id": "skill_1", "anthropic.skill.version.id": "latest"},
    ),
    (
        lambda client: client.beta.skills.versions.create("skill_1", files=[("skill/SKILL.md", b"Hello")]),
        "POST",
        "/v1/skills/skill_1/versions",
        {"id": "skillver_1", "version": "1759178010641129"},
        "anthropic.skills.versions.create",
        {"anthropic.skill.id": "skill_1", "anthropic.skill.version.id": "skillver_1"},
    ),
    (
        lambda client: client.beta.deployments.retrieve("depl_1"),
        "GET",
        "/v1/deployments/depl_1",
        {"id": "depl_1"},
        "anthropic.deployments.retrieve",
        {"anthropic.deployment.id": "depl_1"},
    ),
    # A Run's methods are at another path, so the method that starts one has no ID for it.
    (
        lambda client: client.beta.deployments.run("depl_1"),
        "POST",
        "/v1/deployments/depl_1/run",
        {"id": "drun_1"},
        "anthropic.deployments.run",
        {"anthropic.deployment.id": "depl_1"},
    ),
    (
        lambda client: client.beta.deployment_runs.retrieve("drun_1"),
        "GET",
        "/v1/deployment_runs/drun_1",
        {"id": "drun_1"},
        "anthropic.deployment_runs.retrieve",
        {"anthropic.deployment_run.id": "drun_1"},
    ),
    (
        lambda client: client.beta.dreams.retrieve("dream_1"),
        "GET",
        "/v1/dreams/dream_1",
        {"id": "dream_1"},
        "anthropic.dreams.retrieve",
        {"anthropic.dream.id": "dream_1"},
    ),
    (
        lambda client: client.beta.environments.create(name="Sandbox"),
        "POST",
        "/v1/environments",
        {"id": "env_1"},
        "anthropic.environments.create",
        {"anthropic.environment.id": "env_1"},
    ),
    (
        lambda client: client.beta.environments.work.retrieve("work_1", environment_id="env_1"),
        "GET",
        "/v1/environments/env_1/work/work_1",
        {"id": "work_1"},
        "anthropic.environments.work.retrieve",
        {"anthropic.environment.id": "env_1", "anthropic.environment.work.id": "work_1"},
    ),
    # A Memory Store and a Memory have `gen_ai.*` attributes.
    (
        lambda client: client.beta.memory_stores.retrieve("memstore_1"),
        "GET",
        "/v1/memory_stores/memstore_1",
        {"id": "memstore_1"},
        "anthropic.memory_stores.retrieve",
        {"gen_ai.memory.store.id": "memstore_1"},
    ),
    (
        lambda client: client.beta.memory_stores.memories.create("memstore_1", content="Hello", path="/notes.md"),
        "POST",
        "/v1/memory_stores/memstore_1/memories",
        {"id": "mem_1"},
        "anthropic.memory_stores.memories.create",
        {"gen_ai.memory.store.id": "memstore_1", "gen_ai.memory.record.id": "mem_1"},
    ),
    (
        lambda client: client.beta.memory_stores.memories.retrieve("mem_1", memory_store_id="memstore_1"),
        "GET",
        "/v1/memory_stores/memstore_1/memories/mem_1",
        {"id": "mem_1"},
        "anthropic.memory_stores.memories.retrieve",
        {"gen_ai.memory.store.id": "memstore_1", "gen_ai.memory.record.id": "mem_1"},
    ),
    (
        lambda client: client.beta.memory_stores.memory_versions.retrieve("memver_1", memory_store_id="memstore_1"),
        "GET",
        "/v1/memory_stores/memstore_1/memory_versions/memver_1",
        {"id": "memver_1"},
        "anthropic.memory_stores.memory_versions.retrieve",
        {"gen_ai.memory.store.id": "memstore_1", "anthropic.memory_store.memory_version.id": "memver_1"},
    ),
    (
        lambda client: client.beta.sessions.resources.add("sesn_1", file_id="file_1", type="file"),
        "POST",
        "/v1/sessions/sesn_1/resources",
        {"id": "sesrsc_1", "file_id": "file_1"},
        "anthropic.sessions.resources.add",
        {"anthropic.session.id": "sesn_1", "anthropic.session.resource.id": "sesrsc_1"},
    ),
    (
        lambda client: client.beta.tunnels.certificates.create("tunnel_1", ca_certificate_pem="pem"),
        "POST",
        "/v1/tunnels/tunnel_1/certificates",
        {"id": "cert_1"},
        "anthropic.tunnels.certificates.create",
        {"anthropic.tunnel.id": "tunnel_1", "anthropic.tunnel.certificate.id": "cert_1"},
    ),
    (
        lambda client: client.beta.user_profiles.retrieve("uprof_1"),
        "GET",
        "/v1/user_profiles/uprof_1",
        {"id": "uprof_1"},
        "anthropic.user_profiles.retrieve",
        {"anthropic.user_profile.id": "uprof_1"},
    ),
    (
        lambda client: client.beta.vaults.credentials.retrieve("cred_1", vault_id="vault_1"),
        "GET",
        "/v1/vaults/vault_1/credentials/cred_1",
        {"id": "cred_1"},
        "anthropic.vaults.credentials.retrieve",
        {"anthropic.vault.id": "vault_1", "anthropic.vault.credential.id": "cred_1"},
    ),
    (
        lambda client: client.beta.organization.api_keys.retrieve("apikey_1"),
        "GET",
        "/v1/organizations/api_keys/apikey_1",
        {"id": "apikey_1"},
        "anthropic.organization.api_keys.retrieve",
        {"anthropic.organization.api_key.id": "apikey_1"},
    ),
    (
        lambda client: client.beta.organization.external_keys.retrieve("extkey_1"),
        "GET",
        "/v1/organizations/external_keys/extkey_1",
        {"id": "extkey_1"},
        "anthropic.organization.external_keys.retrieve",
        {"anthropic.organization.external_key.id": "extkey_1"},
    ),
    (
        lambda client: client.beta.organization.invites.create(email="user@example.com", role="user"),
        "POST",
        "/v1/organizations/invites",
        {"id": "invite_1"},
        "anthropic.organization.invites.create",
        {"anthropic.organization.invite.id": "invite_1"},
    ),
    (
        lambda client: client.beta.organization.users.retrieve("user_1"),
        "GET",
        "/v1/organizations/users/user_1",
        {"id": "user_1"},
        "anthropic.organization.users.retrieve",
        {"anthropic.organization.user.id": "user_1"},
    ),
    (
        lambda client: client.beta.organization.service_accounts.retrieve("svcacct_1"),
        "GET",
        "/v1/organizations/service_accounts/svcacct_1",
        {"id": "svcacct_1"},
        "anthropic.organization.service_accounts.retrieve",
        {"anthropic.organization.service_account.id": "svcacct_1"},
    ),
    # Named after the path, which keeps a Workspace in a path or a response apart from `anthropic.workspace.id`,
    # the workspace that the client makes its requests for.
    (
        lambda client: client.beta.organization.workspaces.create(name="Research"),
        "POST",
        "/v1/organizations/workspaces",
        {"id": "wrkspc_1"},
        "anthropic.organization.workspaces.create",
        {"anthropic.organization.workspace.id": "wrkspc_1"},
    ),
    (
        lambda client: client.beta.organization.workspaces.retrieve("wrkspc_1"),
        "GET",
        "/v1/organizations/workspaces/wrkspc_1",
        {"id": "wrkspc_1"},
        "anthropic.organization.workspaces.retrieve",
        {"anthropic.organization.workspace.id": "wrkspc_1"},
    ),
    (
        lambda client: client.beta.organization.federation.issuers.retrieve("fdis_1"),
        "GET",
        "/v1/organizations/federation_issuers/fdis_1",
        {"id": "fdis_1"},
        "anthropic.organization.federation.issuers.retrieve",
        {"anthropic.organization.federation_issuer.id": "fdis_1"},
    ),
    (
        lambda client: client.beta.organization.federation.rules.retrieve("fdrl_1"),
        "GET",
        "/v1/organizations/federation_rules/fdrl_1",
        {"id": "fdrl_1"},
        "anthropic.organization.federation.rules.retrieve",
        {"anthropic.organization.federation_rule.id": "fdrl_1"},
    ),
    # A membership has no `id`. The ID of what the method added is in the field that the path's parameter names.
    (
        lambda client: client.beta.organization.workspaces.members.add(
            "wrkspc_1", user_id="user_1", workspace_role="workspace_user"
        ),
        "POST",
        "/v1/organizations/workspaces/wrkspc_1/members",
        {"type": "workspace_member", "user_id": "user_1", "workspace_id": "wrkspc_1"},
        "anthropic.organization.workspaces.members.add",
        {"anthropic.organization.workspace.id": "wrkspc_1", "anthropic.organization.workspace.member.id": "user_1"},
    ),
    (
        lambda client: client.beta.organization.workspaces.service_accounts.add(
            "wrkspc_1", service_account_id="svcacct_1", workspace_role="workspace_user"
        ),
        "POST",
        "/v1/organizations/workspaces/wrkspc_1/service_accounts",
        {"service_account_id": "svcacct_1", "workspace_id": "wrkspc_1"},
        "anthropic.organization.workspaces.service_accounts.add",
        {
            "anthropic.organization.workspace.id": "wrkspc_1",
            "anthropic.organization.workspace.service_account.id": "svcacct_1",
        },
    ),
    (
        lambda client: client.beta.organization.service_accounts.workspaces.add(
            "svcacct_1", workspace_id="wrkspc_1", workspace_role="workspace_user"
        ),
        "POST",
        "/v1/organizations/service_accounts/svcacct_1/workspaces",
        {"service_account_id": "svcacct_1", "workspace_id": "wrkspc_1"},
        "anthropic.organization.service_accounts.workspaces.add",
        {
            "anthropic.organization.service_account.id": "svcacct_1",
            "anthropic.organization.service_account.workspace.id": "wrkspc_1",
        },
    ),
    (
        lambda client: client.beta.organization.federation.rules.workspaces.add("fdrl_1", workspace_id="wrkspc_1"),
        "POST",
        "/v1/organizations/federation_rules/fdrl_1/workspaces",
        {"federation_rule_id": "fdrl_1", "workspace_id": "wrkspc_1"},
        "anthropic.organization.federation.rules.workspaces.add",
        {
            "anthropic.organization.federation_rule.id": "fdrl_1",
            "anthropic.organization.federation_rule.workspace.id": "wrkspc_1",
        },
    ),
]

# A list method of each kind of page: what calls it, the path it requests, its two pages, its span's name and IDs,
# and the `url.query` of the request for the second page, which is none where the cursor is content.
ResourceList = tuple[Callable[[Any], Any], str, list[dict[str, Any]], str, dict[str, str], str | None]
RESOURCE_LISTS: list[ResourceList] = [
    (
        lambda client: client.beta.organization.workspaces.members.list("wrkspc_1"),
        "/v1/organizations/workspaces/wrkspc_1/members",
        [
            {"data": [{"user_id": "user_1"}], "has_more": True, "first_id": "user_1", "last_id": "user_1"},
            {"data": [{"user_id": "user_2"}], "has_more": False, "first_id": "user_2", "last_id": "user_2"},
        ],
        "anthropic.organization.workspaces.members.list",
        {"anthropic.organization.workspace.id": "wrkspc_1"},
        "after_id=user_1",
    ),
    (
        lambda client: client.beta.skills.versions.list("skill_1"),
        "/v1/skills/skill_1/versions",
        [{"data": [{"id": "skillver_1"}], "next_page": "page_2"}, {"data": [{"id": "skillver_2"}], "next_page": None}],
        "anthropic.skills.versions.list",
        {"anthropic.skill.id": "skill_1"},
        "page=page_2",
    ),
    (
        lambda client: client.beta.memory_stores.memories.list("memstore_1"),
        "/v1/memory_stores/memstore_1/memories",
        [{"data": [{"id": "mem_1"}], "next_page": "page_2"}, {"data": [{"id": "mem_2"}], "next_page": None}],
        "anthropic.memory_stores.memories.list",
        {"gen_ai.memory.store.id": "memstore_1"},
        None,
    ),
]


# A Session as the API returns it, as far as its spans read it.
SESSION: dict[str, Any] = {
    "id": "sesn_1",
    "type": "session",
    "environment_id": "env_1",
    "agent": {"type": "agent", "id": "agent_1", "version": 2, "name": "Researcher", "model": {"id": "claude-test"}},
}


class TestResourceIds:
    @pytest.mark.respx(base_url=base_url)
    def test_ids_in_the_path(self, spans: Spans, respx_mock: MockRouter) -> None:
        thread = {"id": "sthr_1", "type": "session_thread"}
        respx_mock.get("/v1/sessions/sesn_1/threads/sthr_1").mock(return_value=httpx2.Response(200, json=thread))
        respx_mock.post("/v1/sessions/sesn_1/threads/sthr_1/archive").mock(
            return_value=httpx2.Response(200, json=thread)
        )
        respx_mock.get("/v1/sessions/sesn_1").mock(return_value=httpx2.Response(200, json={"id": "sesn_1"}))
        client = make_client(spans, _strict_response_validation=False)

        client.beta.sessions.threads.retrieve("sthr_1", session_id="sesn_1")
        client.beta.sessions.threads.archive("sthr_1", session_id="sesn_1")
        client.beta.sessions.retrieve("sesn_1")

        # One attribute for each ID in the path, named after the resources down to the one it identifies.
        # The thread's ID is the conversation's ID too.
        thread_ids = {
            "anthropic.session.id": "sesn_1",
            "anthropic.session.thread.id": "sthr_1",
            "gen_ai.conversation.id": "sthr_1",
        }
        assert resource_ids(spans.one("anthropic.sessions.threads.retrieve")) == thread_ids
        assert resource_ids(spans.one("anthropic.sessions.threads.archive")) == thread_ids
        assert resource_ids(spans.one("anthropic.sessions.retrieve")) == {"anthropic.session.id": "sesn_1"}

    @pytest.mark.respx(base_url=base_url)
    async def test_async_ids_in_the_path(self, spans: Spans, respx_mock: MockRouter) -> None:
        thread = {"id": "sthr_1", "type": "session_thread"}
        respx_mock.get("/v1/sessions/sesn_1/threads/sthr_1").mock(return_value=httpx2.Response(200, json=thread))
        respx_mock.post("/v1/sessions").mock(return_value=httpx2.Response(200, json={"id": "sesn_2"}))
        client = make_async_client(spans, _strict_response_validation=False)

        await client.beta.sessions.threads.retrieve("sthr_1", session_id="sesn_1")
        await client.beta.sessions.create(agent="agent_1", environment_id="env_1")

        assert resource_ids(spans.one("anthropic.sessions.threads.retrieve")) == {
            "anthropic.session.id": "sesn_1",
            "anthropic.session.thread.id": "sthr_1",
            "gen_ai.conversation.id": "sthr_1",
        }
        assert resource_ids(spans.one("anthropic.sessions.create")) == {
            "anthropic.session.id": "sesn_2",
            "gen_ai.agent.id": "agent_1",
            "anthropic.session.environment.id": "env_1",
        }

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_a_value_in_the_path_that_is_no_id_is_recorded_as_it_is(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/v1/skills/skill_1/versions/latest").mock(
            return_value=httpx2.Response(200, json={"id": "skillver_1", "version": "1759178010641129"})
        )

        await call_client(
            sync,
            spans,
            lambda client: client.beta.skills.versions.retrieve("latest", skill_id="skill_1"),
            _strict_response_validation=False,
        )

        # The attribute has what the path has, not the ID of the version that the API resolved it to.
        span = spans.one("anthropic.skills.versions.retrieve")
        assert resource_ids(span) == {"anthropic.skill.id": "skill_1", "anthropic.skill.version.id": "latest"}
        assert attributes(span)["url.path"] == "/v1/skills/skill_1/versions/latest"

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_a_failed_request_for_a_malformed_id_has_the_id_and_the_path(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        not_found = {"type": "error", "error": {"type": "not_found_error", "message": "Not found"}}
        respx_mock.get("/v1/files/not%20an%20id").mock(return_value=httpx2.Response(404, json=not_found))

        with pytest.raises(APIStatusError):
            await call_client(sync, spans, lambda client: client.beta.files.retrieve_metadata("not an id"))

        span = spans.one("anthropic.files.retrieve_metadata")
        assert span.status.status_code == StatusCode.ERROR
        assert attributes(span)["error.type"] == "not_found_error"
        assert resource_ids(span) == {"anthropic.file.id": "not an id"}
        assert attributes(span)["http.route"] == "/v1/files/{file_id}"
        assert url_attributes(span) == {
            "url.scheme": "http",
            "url.path": "/v1/files/not%20an%20id",
            "url.full": f"{base_url}/v1/files/not%20an%20id",
        }

    @pytest.mark.parametrize("raw", [False, True], ids=["parsed", "raw"])
    @pytest.mark.respx(base_url=base_url)
    def test_create_has_the_id_of_what_it_created(self, raw: bool, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/sessions").mock(return_value=httpx2.Response(200, json={"id": "sesn_1"}))
        client = make_client(spans, _strict_response_validation=False)
        sessions: Any = client.beta.sessions.with_raw_response if raw else client.beta.sessions

        sessions.create(agent="agent_1", environment_id="env_1")

        # The created Session, besides the Agent and the environment that a Session's create starts its span with.
        assert resource_ids(spans.one("anthropic.sessions.create")) == {
            "anthropic.session.id": "sesn_1",
            "gen_ai.agent.id": "agent_1",
            "anthropic.session.environment.id": "env_1",
        }

    @SYNC_AND_ASYNC
    @pytest.mark.parametrize("traces", [True, False], ids=["spans_on", "spans_off"])
    @pytest.mark.respx(base_url=base_url)
    async def test_session_create_sends_an_agent_without_an_id_for_the_api_to_reject(
        self, traces: bool, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        route = respx_mock.post("/v1/sessions").mock(return_value=httpx2.Response(200, json={"id": "sesn_1"}))
        agents: list[Any] = [{"type": "agent", "version": 1}, {"type": "agent", "id": "agent_2"}, 7]

        make: Callable[..., Any] = make_client if sync else make_async_client
        client = make(spans, open_telemetry=spans.option(traces=traces), _strict_response_validation=False)

        for agent in agents:
            created = client.beta.sessions.create(agent=agent, environment_id="env_1")
            if not sync:
                await created

        # The SDK sends what it is given, and reads the span's attributes from it only when there is a span.
        assert [json.loads(request.content)["agent"] for request in requests(route)] == agents
        agent_ids = [attributes(span).get("gen_ai.agent.id") for span in spans.named("anthropic.sessions.create")]
        assert agent_ids == ([None, "agent_2", None] if traces else [])

    @pytest.mark.parametrize("body", [{}, {"id": None}, {"id": 7}], ids=str)
    @pytest.mark.respx(base_url=base_url)
    def test_create_without_an_id_in_its_response(
        self, body: dict[str, Any], spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/sessions").mock(return_value=httpx2.Response(200, json=body))
        client = make_client(spans, _strict_response_validation=False)

        client.beta.sessions.create(agent="agent_1", environment_id="env_1")

        span = spans.one("anthropic.sessions.create")
        assert span.status.status_code == StatusCode.OK
        assert "anthropic.session.id" not in attributes(span)

    @pytest.mark.respx(base_url=base_url)
    def test_failed_create_has_no_id(self, spans: Spans, respx_mock: MockRouter) -> None:
        error = {"type": "error", "error": {"type": "invalid_request_error", "message": "no", "id": "err_1"}, "id": "x"}
        respx_mock.post("/v1/sessions").mock(return_value=httpx2.Response(400, json=error))
        client = make_client(spans)

        with pytest.raises(APIStatusError):
            client.beta.sessions.create(agent="agent_1", environment_id="env_1")

        span = spans.one("anthropic.sessions.create")
        assert span.status.status_code == StatusCode.ERROR
        # The Agent and the environment are in the request, so a failed call has them too.
        assert resource_ids(span) == {"gen_ai.agent.id": "agent_1", "anthropic.session.environment.id": "env_1"}
        assert "gen_ai.agent.name" not in attributes(span)
        assert "gen_ai.request.model" not in attributes(span)

    @pytest.mark.parametrize(
        "agent",
        [
            "agent_1",
            {"type": "agent", "id": "agent_1", "version": 2},
            {"type": "agent_with_overrides", "id": "agent_1", "model": {"id": "claude-override"}},
        ],
        ids=["id", "agent", "agent_with_overrides"],
    )
    @pytest.mark.parametrize("raw", [False, True], ids=["parsed", "raw"])
    @pytest.mark.respx(base_url=base_url)
    def test_session_create_has_its_agent_model_and_environment(
        self, raw: bool, agent: Any, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/sessions").mock(return_value=httpx2.Response(200, json=SESSION))
        client = make_client(spans, _strict_response_validation=False)
        sessions: Any = client.beta.sessions.with_raw_response if raw else client.beta.sessions

        sessions.create(agent=agent, environment_id="env_1")

        created = attributes(spans.one("anthropic.sessions.create"))
        assert created["gen_ai.agent.id"] == "agent_1"
        assert created["anthropic.session.environment.id"] == "env_1"
        # The name and the model are those the Session resolved, not the request's overrides.
        assert created["gen_ai.agent.name"] == "Researcher"
        assert created["gen_ai.request.model"] == "claude-test"

    @pytest.mark.respx(base_url=base_url)
    def test_session_create_starts_its_span_with_the_agent_and_environment(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/sessions").mock(return_value=httpx2.Response(200, json=SESSION))
        sampler = StartAttributes()
        provider = TracerProvider(sampler=sampler)
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry={"tracer_provider": provider})

        client.beta.sessions.create(agent={"type": "agent", "id": "agent_1"}, environment_id="env_1")

        assert sampler.started == [
            (
                "anthropic.sessions.create",
                {
                    "server.address": "127.0.0.1",
                    "server.port": 4010,
                    "http.request.method": "POST",
                    "http.route": "/v1/sessions",
                    "gen_ai.provider.name": "anthropic",
                    "gen_ai.agent.id": "agent_1",
                    "anthropic.session.environment.id": "env_1",
                },
            )
        ]

    @pytest.mark.respx(base_url=base_url)
    async def test_async_session_create_has_its_agent_model_and_environment(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/sessions").mock(return_value=httpx2.Response(200, json=SESSION))
        client = make_async_client(spans, _strict_response_validation=False)

        await client.beta.sessions.create(agent={"type": "agent", "id": "agent_1"}, environment_id="env_1")

        created = attributes(spans.one("anthropic.sessions.create"))
        assert created["gen_ai.agent.id"] == "agent_1"
        assert created["anthropic.session.environment.id"] == "env_1"
        assert created["gen_ai.agent.name"] == "Researcher"
        assert created["gen_ai.request.model"] == "claude-test"

    @pytest.mark.respx(base_url=base_url)
    def test_other_sessions_methods_do_not_have_the_agent_model_or_environment(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/v1/sessions/sesn_1").mock(return_value=httpx2.Response(200, json=SESSION))
        respx_mock.post("/v1/sessions/sesn_1").mock(return_value=httpx2.Response(200, json=SESSION))
        respx_mock.get("/v1/sessions").mock(return_value=httpx2.Response(200, json={"data": [SESSION]}))
        client = make_client(spans, _strict_response_validation=False)

        client.beta.sessions.retrieve("sesn_1")
        client.beta.sessions.update("sesn_1", title="Research")
        client.beta.sessions.list()

        for name in ("anthropic.sessions.retrieve", "anthropic.sessions.update", "anthropic.sessions.list"):
            span = attributes(spans.one(name))
            assert "gen_ai.agent.id" not in span
            assert "gen_ai.agent.name" not in span
            assert "gen_ai.request.model" not in span
            assert "anthropic.session.environment.id" not in span

    @pytest.mark.respx(base_url=base_url)
    def test_delete_has_the_id_of_what_it_deletes(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.delete("/v1/sessions/sesn_1").mock(return_value=httpx2.Response(200, json={"id": "sesn_1"}))
        respx_mock.delete("/v1/sessions/sesn_2").mock(return_value=httpx2.Response(404, json={}))
        client = make_client(spans, _strict_response_validation=False)

        client.beta.sessions.delete("sesn_1")
        with pytest.raises(APIStatusError):
            client.beta.sessions.delete("sesn_2")

        deleted, failed = spans.named("anthropic.sessions.delete")
        assert resource_ids(deleted) == {"anthropic.session.id": "sesn_1"}
        # The ID is in the path, so a failed call has it too.
        assert failed.status.status_code == StatusCode.ERROR
        assert resource_ids(failed) == {"anthropic.session.id": "sesn_2"}

    @pytest.mark.respx(base_url=base_url)
    def test_method_that_creates_several_objects_has_only_the_ids_in_its_path(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        sent = {"data": [{"id": "sevt_1", "type": "user.message"}, {"id": "sevt_2", "type": "user.message"}]}
        respx_mock.post("/v1/sessions/sesn_1/events").mock(return_value=httpx2.Response(200, json=sent))
        client = make_client(spans, _strict_response_validation=False)

        client.beta.sessions.events.send(
            "sesn_1", events=[{"type": "user.message", "content": [{"type": "text", "text": "Hello"}]}]
        )

        assert resource_ids(spans.one("anthropic.sessions.events.send")) == {"anthropic.session.id": "sesn_1"}

    @pytest.mark.respx(base_url=base_url)
    def test_list_has_only_the_ids_in_its_path(self, spans: Spans, respx_mock: MockRouter) -> None:
        first = {"data": [{"id": "sthr_1", "type": "session_thread"}], "next_page": "page_2"}
        second = {"data": [{"id": "sthr_2", "type": "session_thread"}], "next_page": None}
        respx_mock.get("/v1/sessions/sesn_1/threads").mock(
            side_effect=[httpx2.Response(200, json=first), httpx2.Response(200, json=second)]
        )
        sessions = {"data": [{"id": "sesn_1"}], "next_page": None}
        respx_mock.get("/v1/sessions").mock(return_value=httpx2.Response(200, json=sessions))
        models: dict[str, Any] = {"data": [], "has_more": False, "first_id": None, "last_id": None}
        respx_mock.get("/v1/models").mock(return_value=httpx2.Response(200, json=models))
        client = make_client(spans, _strict_response_validation=False)

        assert [thread.id for thread in client.beta.sessions.threads.list("sesn_1")] == ["sthr_1", "sthr_2"]
        client.beta.sessions.list()
        client.models.list()

        # The request for a later page has its own span, with the same IDs.
        pages = spans.named("anthropic.sessions.threads.list")
        assert [resource_ids(page) for page in pages] == [{"anthropic.session.id": "sesn_1"}] * 2
        # No ID in the path, and none for the objects listed.
        assert resource_ids(spans.one("anthropic.sessions.list")) == {}
        assert resource_ids(spans.one("anthropic.models.list")) == {}

    @pytest.mark.respx(base_url=base_url)
    def test_event_stream_has_the_ids_in_its_path(self, spans: Spans, respx_mock: MockRouter) -> None:
        event = {"type": "session.status_running", "id": "sevt_1", "processed_at": "2026-01-01T00:00:00Z"}
        respx_mock.get("/v1/sessions/sesn_1/threads/sthr_1/stream").mock(
            return_value=httpx2.Response(200, content=sse([event]), headers={"content-type": "text/event-stream"})
        )
        client = make_client(spans)

        with client.beta.sessions.threads.events.stream("sthr_1", session_id="sesn_1") as stream:
            assert [item.type for item in stream] == ["session.status_running"]

        assert resource_ids(spans.one("anthropic.sessions.threads.events.stream")) == {
            "anthropic.session.id": "sesn_1",
            "anthropic.session.thread.id": "sthr_1",
            "gen_ai.conversation.id": "sthr_1",
        }

    @pytest.mark.respx(base_url=base_url)
    def test_agent_id_is_the_conventions_attribute(self, spans: Spans, respx_mock: MockRouter) -> None:
        versions: dict[str, Any] = {"data": [], "next_page": None}
        respx_mock.post("/v1/agents").mock(return_value=httpx2.Response(200, json={"id": "agent_1"}))
        respx_mock.get("/v1/agents/agent_1").mock(return_value=httpx2.Response(200, json={"id": "agent_1"}))
        respx_mock.get("/v1/agents/agent_1/versions").mock(return_value=httpx2.Response(200, json=versions))
        client = make_client(spans, _strict_response_validation=False)

        client.beta.agents.create(model="claude-test", name="Helper")
        client.beta.agents.retrieve("agent_1")
        client.beta.agents.versions.list("agent_1")

        # An Agent's ID has a `gen_ai.*` attribute, which replaces `anthropic.agent.id`.
        for name in ("anthropic.agents.create", "anthropic.agents.retrieve", "anthropic.agents.versions.list"):
            assert resource_ids(spans.one(name)) == {"gen_ai.agent.id": "agent_1"}

    @pytest.mark.parametrize("call", RESOURCE_CALLS, ids=[call[4] for call in RESOURCE_CALLS])
    @pytest.mark.respx(base_url=base_url)
    def test_each_resource(self, call: ResourceCall, spans: Spans, respx_mock: MockRouter) -> None:
        invoke, method, path, body, name, ids = call
        respx_mock.route(method=method, path=path).mock(return_value=httpx2.Response(200, json=body))

        invoke(make_client(spans, _strict_response_validation=False))

        assert resource_ids(spans.one(name)) == ids
        assert_http_attributes(spans.one(name), method, path)

    @pytest.mark.parametrize("call", RESOURCE_CALLS, ids=[call[4] for call in RESOURCE_CALLS])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_each_resource(self, call: ResourceCall, spans: Spans, respx_mock: MockRouter) -> None:
        invoke, method, path, body, name, ids = call
        respx_mock.route(method=method, path=path).mock(return_value=httpx2.Response(200, json=body))

        await invoke(make_async_client(spans, _strict_response_validation=False))

        assert resource_ids(spans.one(name)) == ids
        assert_http_attributes(spans.one(name), method, path)

    @pytest.mark.parametrize("call", RESOURCE_CALLS, ids=[call[4] for call in RESOURCE_CALLS])
    @pytest.mark.respx(base_url=base_url)
    def test_each_resource_failed(self, call: ResourceCall, spans: Spans, respx_mock: MockRouter) -> None:
        invoke, method, path, body, name, ids = call
        respx_mock.route(method=method, path=path).mock(return_value=httpx2.Response(404, json=body))

        with pytest.raises(APIStatusError):
            invoke(make_client(spans))

        # A failed call has the IDs in its path, which the method sent, and not the ID of an object it would have created.
        in_path = {key: value for key, value in ids.items() if f"/{value}" in path}
        assert resource_ids(spans.one(name)) == in_path
        assert_http_attributes(spans.one(name), method, path)

    @pytest.mark.parametrize("call", RESOURCE_LISTS, ids=[call[3] for call in RESOURCE_LISTS])
    @pytest.mark.respx(base_url=base_url)
    def test_each_kind_of_page(self, call: ResourceList, spans: Spans, respx_mock: MockRouter) -> None:
        invoke, path, pages, name, ids, later_query = call
        respx_mock.get(path).mock(side_effect=[httpx2.Response(200, json=page) for page in pages])

        assert len(list(invoke(make_client(spans, _strict_response_validation=False)))) == 2

        # The request for a later page has the IDs in the path too, and none for the objects listed.
        assert [resource_ids(page) for page in spans.named(name)] == [ids, ids]
        first, later = spans.named(name)
        assert_http_attributes(later, "GET", path)
        # The cursor of a later page is a parameter that the endpoint defines, and the span has it unless it is content.
        assert "url.query" not in attributes(first)
        assert attributes(later).get("url.query") == later_query

    @pytest.mark.parametrize("call", RESOURCE_LISTS, ids=[call[3] for call in RESOURCE_LISTS])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_each_kind_of_page(self, call: ResourceList, spans: Spans, respx_mock: MockRouter) -> None:
        invoke, path, pages, name, ids, later_query = call
        respx_mock.get(path).mock(side_effect=[httpx2.Response(200, json=page) for page in pages])

        items = [item async for item in invoke(make_async_client(spans, _strict_response_validation=False))]

        assert len(items) == 2
        assert [resource_ids(page) for page in spans.named(name)] == [ids, ids]
        first, later = spans.named(name)
        assert_http_attributes(later, "GET", path)
        assert "url.query" not in attributes(first)
        assert attributes(later).get("url.query") == later_query

    @pytest.mark.parametrize("body", [{}, {"user_id": None}, {"id": "member_1"}], ids=str)
    @pytest.mark.respx(base_url=base_url)
    def test_add_without_the_named_field_in_its_response(
        self, body: dict[str, Any], spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/organizations/workspaces/wrkspc_1/members").mock(
            return_value=httpx2.Response(200, json=body)
        )
        client = make_client(spans, _strict_response_validation=False)

        client.beta.organization.workspaces.members.add("wrkspc_1", user_id="user_1", workspace_role="workspace_user")

        # The user's ID in the request's body is not in its path, so only the response gives it.
        span = spans.one("anthropic.organization.workspaces.members.add")
        assert span.status.status_code == StatusCode.OK
        assert resource_ids(span) == {"anthropic.organization.workspace.id": "wrkspc_1"}


def without(value: dict[str, Any], *keys: str) -> dict[str, Any]:
    return {key: item for key, item in value.items() if key not in keys}


# Message bodies that do not match the declared types, as a gateway or a compatible endpoint can return them.
MALFORMED_MESSAGES: dict[str, dict[str, Any]] = {
    "usage absent": without(MESSAGE, "usage"),
    "usage null": {**MESSAGE, "usage": None},
    "token count as a string": {**MESSAGE, "usage": {**MESSAGE["usage"], "input_tokens": "12"}},
    "empty output_tokens_details": {**MESSAGE, "usage": {**MESSAGE["usage"], "output_tokens_details": {}}},
    "no id or model": without(MESSAGE, "id", "model"),
}


def malformed_stream_events(message: dict[str, Any]) -> list[dict[str, Any]]:
    events = stream_events()
    events[0] = {"type": "message_start", "message": {**message, "content": [], "stop_reason": None}}
    return events


@pytest.mark.parametrize("content_mode", ["metadata_only", "content"])
@pytest.mark.parametrize("message", MALFORMED_MESSAGES.values(), ids=MALFORMED_MESSAGES.keys())
class TestMalformedResponses:
    """A response that the span cannot read still gives the application its result: recording it
    raises nothing, and the span ends, with the attributes that could be read.
    """

    def ended(self, spans: Spans, content_mode: str, *, output: bool = True) -> ReadableSpan:
        span = spans.one("anthropic.messages.create")
        assert span.end_time is not None
        assert span.status.status_code != StatusCode.ERROR
        assert attributes(span)["gen_ai.request.model"] == "claude-test"
        # What the span cannot read of the response does not cost it the content.
        assert ("gen_ai.input.messages" in attributes(span)) == (content_mode == "content")
        assert ("gen_ai.output.messages" in attributes(span)) == (content_mode == "content" and output)
        return span

    @pytest.mark.respx(base_url=base_url)
    def test_create(self, message: dict[str, Any], content_mode: str, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=message))
        client = make_client(
            spans, open_telemetry=spans.option(traces={"content_mode": content_mode}), _strict_response_validation=False
        )

        assert create(client).content[0].text == "Hi there"

        span = self.ended(spans, content_mode)
        # The span keeps what it could read before the field that it could not.
        assert attributes(span).get("gen_ai.response.id") == message.get("id")
        assert attributes(span)["anthropic.message.stop_reason"] == "end_turn"

    @pytest.mark.respx(base_url=base_url)
    async def test_async_create(
        self, message: dict[str, Any], content_mode: str, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=message))
        client = make_async_client(
            spans, open_telemetry=spans.option(traces={"content_mode": content_mode}), _strict_response_validation=False
        )

        assert (await create(client)).content[0].text == "Hi there"

        self.ended(spans, content_mode)

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response(
        self, message: dict[str, Any], content_mode: str, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=message))
        client = make_client(
            spans, open_telemetry=spans.option(traces={"content_mode": content_mode}), _strict_response_validation=False
        )

        resource: Any = client.messages.with_raw_response
        raw = resource.create(**REQUEST)

        assert raw.parse().content[0].text == "Hi there"
        self.ended(spans, content_mode)

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @pytest.mark.respx(base_url=base_url)
    def test_stream_read_without_the_stream_helper(
        self, beta: bool, message: dict[str, Any], content_mode: str, spans: Spans, respx_mock: MockRouter
    ) -> None:
        events = malformed_stream_events(message)
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events))
        client = make_client(
            spans, open_telemetry=spans.option(traces={"content_mode": content_mode}), _strict_response_validation=False
        )

        read = [event.type for event in messages_resource(client, beta=beta).create(**REQUEST, stream=True)]

        assert read == [event["type"] for event in events]
        self.ended(spans, content_mode, output=False)

    @pytest.mark.respx(base_url=base_url)
    async def test_async_stream_read_without_the_stream_helper(
        self, message: dict[str, Any], content_mode: str, spans: Spans, respx_mock: MockRouter
    ) -> None:
        events = malformed_stream_events(message)
        respx_mock.post("/v1/messages").mock(return_value=stream_response(events))
        client = make_async_client(
            spans, open_telemetry=spans.option(traces={"content_mode": content_mode}), _strict_response_validation=False
        )

        read = [event.type async for event in await client.messages.create(**REQUEST, stream=True)]

        assert read == [event["type"] for event in events]
        self.ended(spans, content_mode, output=False)

    @pytest.mark.respx(base_url=base_url)
    def test_stream_helper(
        self, message: dict[str, Any], content_mode: str, spans: Spans, respx_mock: MockRouter
    ) -> None:
        if message.get("usage") is None:
            pytest.skip("the stream helper itself cannot accumulate a Message without usage")
        respx_mock.post("/v1/messages").mock(return_value=stream_response(malformed_stream_events(message)))
        client = make_client(
            spans, open_telemetry=spans.option(traces={"content_mode": content_mode}), _strict_response_validation=False
        )

        with client.messages.stream(**REQUEST) as stream:
            assert stream.get_final_text() == "Hi there"

        self.ended(spans, content_mode)


class TestMalformedCountsAndBatches:
    @pytest.mark.parametrize("body", [{}, {"input_tokens": None}, {"input_tokens": "12"}], ids=str)
    @pytest.mark.parametrize("raw", [False, True], ids=["parsed", "raw"])
    @pytest.mark.respx(base_url=base_url)
    def test_count_tokens(self, body: dict[str, Any], raw: bool, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages/count_tokens").mock(return_value=httpx2.Response(200, json=body))
        client = make_client(spans, _strict_response_validation=False)
        resource: Any = client.messages.with_raw_response if raw else client.messages

        assert resource.count_tokens(messages=[{"role": "user", "content": "Hello"}], model="claude-test") is not None

        span = spans.one("anthropic.messages.count_tokens")
        assert span.end_time is not None
        assert span.status.status_code != StatusCode.ERROR

    @pytest.mark.parametrize("body", [{}, {"id": None}, {"id": 7}], ids=str)
    @pytest.mark.parametrize("raw", [False, True], ids=["parsed", "raw"])
    @pytest.mark.respx(base_url=base_url)
    def test_batch_create(self, body: dict[str, Any], raw: bool, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages/batches").mock(return_value=httpx2.Response(200, json=body))
        client = make_client(spans, _strict_response_validation=False)
        resource: Any = client.messages.batches.with_raw_response if raw else client.messages.batches

        assert resource.create(requests=[]) is not None

        span = spans.one("anthropic.messages.batches.create")
        assert span.end_time is not None
        assert span.status.status_code != StatusCode.ERROR


class FailingProcessor(SpanProcessor):
    """A span processor that raises when a span starts, or else when one ends."""

    def __init__(self, failure: str) -> None:
        self.failure = failure

    @override
    def on_start(self, span: SdkSpan, parent_context: context.Context | None = None) -> None:
        if self.failure == "on_start":
            raise RuntimeError("cannot start a span")

    @override
    def on_end(self, span: ReadableSpan) -> None:
        if self.failure == "on_end":
            raise RuntimeError("cannot end a span")


class FailingSampler(sampling.Sampler):
    @override
    def should_sample(self, *args: Any, **kwargs: Any) -> sampling.SamplingResult:
        raise RuntimeError("cannot sample a span")

    @override
    def get_description(self) -> str:
        return "failing"


class FailingPropagator(TextMapPropagator):
    @override
    def extract(self, carrier: Any, context: Context | None = None, getter: Any = None) -> Context:
        raise RuntimeError("cannot extract a trace context")

    @override
    def inject(self, carrier: Any, context: Context | None = None, setter: Any = None) -> None:
        raise RuntimeError("cannot inject a trace context")

    @property
    @override
    def fields(self) -> set[str]:
        return set()


def failing_tracing(failure: str) -> OpenTelemetryOptions:
    """An `open_telemetry` option whose tracer provider fails every span at `failure`."""
    if failure == "sampler":
        return {"tracer_provider": TracerProvider(sampler=FailingSampler())}
    provider = TracerProvider()
    provider.add_span_processor(FailingProcessor(failure))
    return {"tracer_provider": provider}


TRACING_FAILURES = pytest.mark.parametrize("failure", ["sampler", "on_start", "on_end"])


async def read_events(sync: bool, stream: Any) -> list[str]:
    if sync:
        return [event.type for event in stream]
    return [event.type async for event in stream]


async def final_text(sync: bool, spans: Spans, **options: Any) -> str:
    """The text that the stream helper of a client of `spans` accumulates."""
    if sync:
        with make_client(spans, **options).messages.stream(**REQUEST) as stream:
            return stream.get_final_text()
    async with make_async_client(spans, **options).messages.stream(**REQUEST) as async_stream:
        return await async_stream.get_final_text()


class TestTracingFailures:
    """Tracing that fails leaves an API call as it is without tracing: its result, its error and its requests."""

    @TRACING_FAILURES
    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_the_call_returns_its_result_from_one_request(
        self, sync: bool, failure: str, spans: Spans, respx_mock: MockRouter
    ) -> None:
        route = respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))

        message = await call_client(sync, spans, create, open_telemetry=failing_tracing(failure), max_retries=2)

        assert message.id == "msg_1"
        assert route.call_count == 1

    @TRACING_FAILURES
    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_the_call_raises_the_error_of_the_api_after_its_retries(
        self, sync: bool, failure: str, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        error = {"type": "error", "error": {"type": "api_error", "message": "Internal server error"}}
        route = respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(500, json=error))
        monkeypatch.setattr(_base_client.BaseClient, "_calculate_retry_timeout", no_wait)

        with pytest.raises(InternalServerError):
            await call_client(sync, spans, create, open_telemetry=failing_tracing(failure), max_retries=2)

        assert route.call_count == 3

    @TRACING_FAILURES
    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_a_stream_gives_every_event(
        self, sync: bool, failure: str, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[stream_response() for _ in range(3)])
        options = failing_tracing(failure)

        stream = await call_client(sync, spans, lambda client: create(client, stream=True), open_telemetry=options)

        assert await read_events(sync, stream) == [event["type"] for event in stream_events()]
        assert await final_text(sync, spans, open_telemetry=options) == "Hi there"

        # An application that stops reading closes the stream, which ends the span too.
        stream = await call_client(sync, spans, lambda client: create(client, stream=True), open_telemetry=options)
        if sync:
            assert next(stream).type == "message_start"
            stream.close()
        else:
            assert (await stream.__anext__()).type == "message_start"
            await stream.close()

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_a_url_that_cannot_be_recorded_leaves_the_call_as_it_is(
        self, sync: bool, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        route = respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))

        def fail(*_args: object, **_kwargs: object) -> None:
            raise RuntimeError("cannot record")

        monkeypatch.setattr("anthropic._tracing.set_url_attributes", fail)

        message = await call_client(sync, spans, create, max_retries=2)

        assert message.id == "msg_1"
        assert route.call_count == 1
        span = spans.one("anthropic.messages.create")
        assert span.status.status_code == StatusCode.OK
        assert url_attributes(span) == {}

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_a_failing_propagator_sends_the_request_without_a_trace_context(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        route = respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))
        propagator = propagate.get_global_textmap()
        propagate.set_global_textmap(FailingPropagator())

        try:
            message = await call_client(sync, spans, create)
        finally:
            propagate.set_global_textmap(propagator)

        assert message.id == "msg_1"
        [request] = requests(route)
        assert "traceparent" not in request.headers
        assert spans.one("anthropic.messages.create").status.status_code == StatusCode.OK

    def test_a_propagator_that_is_not_installed_fails_neither_the_import_nor_a_call(self) -> None:
        """In a subprocess, because `opentelemetry.propagate` reads `OTEL_PROPAGATORS` once, when it is imported."""
        script = "\n".join(
            [
                "import httpx2",
                "from opentelemetry.sdk.trace import TracerProvider",
                "from anthropic import Anthropic",
                f"message = {MESSAGE!r}",
                "transport = httpx2.MockTransport(lambda request: httpx2.Response(200, json=message))",
                "client = Anthropic(",
                "    api_key='key',",
                "    http_client=httpx2.Client(transport=transport),",
                "    open_telemetry={'tracer_provider': TracerProvider()},",
                ")",
                f"print(client.messages.create(**{REQUEST!r}).id)",
            ]
        )

        process = subprocess.run(
            [sys.executable, "-c", script],
            env={**os.environ, "OTEL_PROPAGATORS": "not-installed"},
            capture_output=True,
            text=True,
        )

        assert process.returncode == 0, process.stderr
        assert process.stdout.strip() == "msg_1"

    @pytest.mark.parametrize("beta", [False, True], ids=["stable", "beta"])
    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_batch_create_without_requests_reaches_the_api(
        self, sync: bool, beta: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        error = {"type": "error", "error": {"type": "invalid_request_error", "message": "requests: Field required"}}
        route = respx_mock.post("/v1/messages/batches").mock(return_value=httpx2.Response(400, json=error))

        def create_batch(client: Any) -> Any:
            return (client.beta.messages.batches if beta else client.messages.batches).create(requests=None)

        with pytest.raises(BadRequestError):
            await call_client(sync, spans, create_batch)

        [request] = requests(route)
        assert json.loads(request.content) == {"requests": None}
        span = spans.one("anthropic.messages.batches.create")
        assert "anthropic.message.batch.request_count" not in attributes(span)
        assert attributes(span)["error.type"] == "invalid_request_error"

    @SYNC_AND_ASYNC
    @pytest.mark.usefixtures("unloadable_global_tracer_provider")
    @pytest.mark.respx(base_url=base_url)
    async def test_global_tracer_provider_that_cannot_be_loaded_leaves_the_client_without_spans(
        self, sync: bool, spans: Spans, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        route = respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))

        with caplog.at_level(logging.DEBUG, logger="anthropic._tracing"):
            client: Any = (Anthropic if sync else AsyncAnthropic)(base_url=base_url, api_key="key")
            enabled = client.with_options(open_telemetry={"traces": True})
            for called in (client, client.with_options(max_retries=0), client.copy(), enabled, enabled.copy()):
                assert called.open_telemetry["traces"]["enabled"] is True
                assert (await call(called)).id == "msg_1"

        assert route.call_count == 5
        assert not any("traceparent" in request.headers for request in requests(route))
        assert spans.finished == ()
        logged = [record for record in caplog.records if "global OpenTelemetry tracer provider" in record.message]
        assert [record.levelno for record in logged] == [logging.DEBUG]

        # A provider that the client is given is used whatever the global one does.
        await call(client.with_options(open_telemetry=spans.option()))
        assert len(spans.named("anthropic.messages.create")) == 1

    @pytest.mark.usefixtures("unloadable_global_tracer_provider")
    @pytest.mark.respx()
    async def test_global_tracer_provider_that_cannot_be_loaded_leaves_platform_clients_without_spans(
        self, spans: Spans, respx_mock: MockRouter, caplog: pytest.LogCaptureFixture
    ) -> None:
        route = respx_mock.post().mock(return_value=httpx2.Response(200, json=MESSAGE))

        with caplog.at_level(logging.DEBUG, logger="anthropic._tracing"):
            clients = platform_clients(None)
            for client in clients:
                for called in (client, client.with_options(max_retries=0), client.copy()):
                    assert (await call(called)).id == "msg_1"

        assert any("global OpenTelemetry tracer provider" in record.message for record in caplog.records)
        assert route.call_count == 3 * len(clients)
        assert not any("traceparent" in request.headers for request in requests(route))
        assert spans.finished == ()

    @SYNC_AND_ASYNC
    @pytest.mark.respx(base_url=base_url)
    async def test_tracer_provider_that_gives_no_tracer_leaves_the_client_without_spans(
        self, sync: bool, respx_mock: MockRouter
    ) -> None:
        route = respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=MESSAGE))

        class NoTracers(TracerProvider):
            @override
            def get_tracer(self, *args: Any, **kwargs: Any) -> trace.Tracer:
                raise StopIteration

        option: OpenTelemetryOptions = {"tracer_provider": NoTracers()}
        client: Any = (Anthropic if sync else AsyncAnthropic)(base_url=base_url, api_key="key", open_telemetry=option)
        for called in (client, client.with_options(max_retries=0), client.copy(open_telemetry=option)):
            assert (await call(called)).id == "msg_1"

        assert not any("traceparent" in request.headers for request in requests(route))

    @pytest.mark.parametrize("how", ["option", "variable"])
    @SYNC_AND_ASYNC
    @pytest.mark.respx()
    async def test_disabled_spans_call_nothing_of_opentelemetry(
        self, sync: bool, how: str, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        route = respx_mock.post().mock(return_value=httpx2.Response(200, json=MESSAGE))
        called_names: list[str] = []
        await close_what_earlier_tests_left_suspended()

        def refuse(name: str) -> Callable[..., Any]:
            def function(*_args: object, **_kwargs: object) -> Any:
                called_names.append(name)
                raise AssertionError(f"`opentelemetry.trace.{name}` was called")

            return function

        for name in ("get_tracer_provider", "get_tracer", "get_current_span", "use_span", "set_span_in_context"):
            monkeypatch.setattr(trace, name, refuse(name))
        ask_for_global_tracer_provider_again()
        option: OpenTelemetryClientOption = False if how == "option" else None

        try:
            with update_env(ANTHROPIC_OPEN_TELEMETRY="true" if how == "option" else "false"):
                cls: Any = Anthropic if sync else AsyncAnthropic
                clients = [cls(base_url=base_url, api_key="key", open_telemetry=option), *platform_clients(option)]
                for client in clients:
                    for called in (client, client.with_options(max_retries=0), client.copy()):
                        assert called.open_telemetry["traces"]["enabled"] is False
                        assert (await call(called)).id == "msg_1"
        finally:
            ask_for_global_tracer_provider_again()

        assert route.call_count == 3 * len(clients)
        assert called_names == []


async def close_what_earlier_tests_left_suspended() -> None:
    """Closes the generators that earlier tests of this process walked away from, such as a tool runner's.

    Python closes one when it frees it, which can be during a later test, and a tool runner that closes calls
    OpenTelemetry.
    """
    while True:
        gc.collect()
        # The event loop closes an asynchronous generator in a task, which it starts on its next turn.
        await asyncio.sleep(0)
        closing = asyncio.all_tasks() - {asyncio.current_task()}
        if not closing:
            return
        await asyncio.wait(closing)


def ask_for_global_tracer_provider_again() -> None:
    """Makes the SDK forget whether OpenTelemetry could load its global tracer provider, which it asks once a process."""
    cast(Any, global_tracer_provider_loads).cache_clear()


@pytest.fixture
def unloadable_global_tracer_provider(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Makes OpenTelemetry fail to load its global tracer provider, as when the environment names one that is not installed."""
    monkeypatch.setenv("OTEL_PYTHON_TRACER_PROVIDER", "tracer_provider_that_is_not_installed")
    # Another test of this process may have set the global provider, which OpenTelemetry then loads no other for.
    monkeypatch.setattr(trace, "_TRACER_PROVIDER", None)
    ask_for_global_tracer_provider_again()
    yield
    ask_for_global_tracer_provider_again()


# Tripwires. Each compares a list that the tracing code was written from with the generated type that it came from,
# and asserts no behavior. When one fails, decide what the spans do with the new member, change the code that the
# message names if they record it, and then add the member to the set that says so.


def union_members(tp: Any) -> list[Any]:
    """The classes of a union, a list of them, or one class, however nested or annotated."""
    origin = get_origin(tp)
    if origin in (Annotated, Required, NotRequired):
        return union_members(get_args(tp)[0])
    if origin in (Union, UnionType, list, Iterable, Sequence):
        return [member for arg in get_args(tp) for member in union_members(arg)]
    return [tp] if isinstance(tp, type) and (is_typeddict(tp) or issubclass(tp, pydantic.BaseModel)) else []


def field_types(cls: Any) -> dict[str, Any]:
    if issubclass(cls, pydantic.BaseModel):
        return {name: field.annotation for name, field in get_model_fields(cls).items()}
    return get_type_hints(cls, include_extras=True)


def literal_values(tp: Any) -> set[str]:
    if get_origin(tp) in (Annotated, Required, NotRequired):
        return literal_values(get_args(tp)[0])
    return set(get_args(tp)) if get_origin(tp) is Literal else set()


def type_names(tp: Any) -> set[str]:
    """The `type` of each member of a union."""
    return {name for member in union_members(tp) for name in literal_values(field_types(member).get("type"))}


def type_names_under(tp: Any, *, stop_at: Collection[str], seen: set[Any] | None = None) -> set[str]:
    """The `type` of each member of a union and of everything in their fields, except inside a `stop_at` type."""
    seen = set() if seen is None else seen
    names: set[str] = set()
    for member in union_members(tp):
        if member in seen:
            continue
        seen.add(member)
        fields = field_types(member)
        own = literal_values(fields.get("type"))
        names |= own
        if not own & set(stop_at):
            for field in fields.values():
                names |= type_names_under(field, stop_at=stop_at, seen=seen)
    return names


def lists_in(tp: Any) -> list[Any]:
    """The list types among the members of a union."""
    origin = get_origin(tp)
    if origin in (Annotated, Required, NotRequired):
        return lists_in(get_args(tp)[0])
    if origin in (Union, UnionType):
        return [found for arg in get_args(tp) for found in lists_in(arg)]
    return [tp] if origin in (list, Iterable, Sequence) else []


def result_blocks(*unions: Any) -> list[Any]:
    """The result blocks of server tools and MCP tools in the unions of content blocks."""
    return [
        member
        for union in unions
        for member in union_members(union)
        if any(name.endswith("_tool_result") and name != "tool_result" for name in type_names(member))
    ]


USAGE_FIELDS_RECORDED = {
    "cache_creation",
    "cache_creation_input_tokens",
    "cache_read_input_tokens",
    "input_tokens",
    "output_tokens",
    "output_tokens_details",
    "service_tier",
}
USAGE_FIELDS_WITHOUT_AN_ATTRIBUTE = {"inference_geo", "server_tool_use", "speed"}


@pytest.mark.parametrize(
    ("usage", "recorded", "without_an_attribute"),
    [
        (Usage, USAGE_FIELDS_RECORDED, USAGE_FIELDS_WITHOUT_AN_ATTRIBUTE),
        (
            BetaUsage,
            USAGE_FIELDS_RECORDED | {"iterations"},
            USAGE_FIELDS_WITHOUT_AN_ATTRIBUTE | {"fallback_credit"},
        ),
        (CacheCreation, {"ephemeral_1h_input_tokens", "ephemeral_5m_input_tokens"}, set[str]()),
        (BetaCacheCreation, {"ephemeral_1h_input_tokens", "ephemeral_5m_input_tokens"}, set[str]()),
        (OutputTokensDetails, {"thinking_tokens"}, set[str]()),
        (BetaOutputTokensDetails, {"thinking_tokens"}, set[str]()),
    ],
    ids=lambda value: getattr(value, "__name__", ""),
)
def test_usage_fields_are_all_recorded_or_left_out(
    usage: type[pydantic.BaseModel], recorded: set[str], without_an_attribute: set[str]
) -> None:
    assert set(get_model_fields(usage)) == recorded | without_an_attribute, (
        f"`{usage.__name__}` has changed. If the spans have an attribute for the new field, record it in "
        "`set_message_attributes` (src/anthropic/lib/_tracing/_response.py). Then list it in this test."
    )


@pytest.mark.skipif(PYDANTIC_V1, reason="reads the fields of pydantic v2 models")
def test_usage_iteration_types_are_all_recorded_or_left_out() -> None:
    compactions = {"compaction"}
    in_the_totals = {"message", "advisor_message", "fallback_message"}

    assert type_names(field_types(BetaUsage)["iterations"]) == compactions | in_the_totals, (
        "`BetaUsage.iterations` has a new type of entry. `set_message_attributes` "
        "(src/anthropic/lib/_tracing/_response.py) records only the `compaction` entries, whose tokens the usage's "
        "totals leave out. Record the new entries there if the totals leave them out too. Then list the type here."
    )


BLOCK_TYPES_WITH_CONTENT = {"text", "thinking", "tool_use", "server_tool_use", "tool_result"}
BLOCK_TYPES_OF_RESULTS = {
    "bash_code_execution_tool_result",
    "code_execution_tool_result",
    "text_editor_code_execution_tool_result",
    "tool_search_tool_result",
    "web_fetch_tool_result",
    "web_search_tool_result",
}
BLOCK_TYPES_WITH_ONLY_THEIR_TYPE = {"container_upload", "document", "image", "redacted_thinking", "search_result"}


@pytest.mark.skipif(PYDANTIC_V1, reason="reads the fields of pydantic v2 models")
@pytest.mark.parametrize(
    ("blocks", "expected"),
    [
        (
            (ContentBlock, ContentBlockParam),
            BLOCK_TYPES_WITH_CONTENT | BLOCK_TYPES_OF_RESULTS | BLOCK_TYPES_WITH_ONLY_THEIR_TYPE,
        ),
        (
            (BetaContentBlock, BetaContentBlockParam),
            BLOCK_TYPES_WITH_CONTENT
            | {"mcp_tool_use"}
            | BLOCK_TYPES_OF_RESULTS
            | {"advisor_tool_result", "mcp_tool_result"}
            | BLOCK_TYPES_WITH_ONLY_THEIR_TYPE
            | {"compaction", "fallback", "mcp_tool_listing", "tool_addition", "tool_removal"},
        ),
    ],
    ids=["stable", "beta"],
)
def test_message_block_types_are_all_a_part_with_content_or_with_only_their_type(
    blocks: tuple[Any, ...], expected: set[str]
) -> None:
    assert set().union(*(type_names(union) for union in blocks)) == expected, (
        "A message can have a new type of content block. `block_part` (src/anthropic/lib/_tracing/_content.py) makes "
        "a part with only its `type` of a block that it does not know, and a `tool_call_response` part of one whose "
        "type ends with `_tool_result`. Give the new block a part with content there if the spans should have its "
        "content. Then list its type in this test."
    )


@pytest.mark.skipif(PYDANTIC_V1, reason="reads the fields of pydantic v2 models")
@pytest.mark.parametrize("tool_result", [ToolResultBlockParam, BetaToolResultBlockParam], ids=["stable", "beta"])
def test_tool_result_block_types_all_keep_their_fields_or_only_their_type(tool_result: Any) -> None:
    keep_their_fields = {"text", "search_result"}
    keep_only_their_type = {"browser_state", "document", "image", "tool_reference"}

    assert type_names(field_types(tool_result)["content"]) == keep_their_fields | keep_only_their_type, (
        "A tool result can have a new type of content block. `tool_result_content` "
        "(src/anthropic/lib/_tracing/_content.py) keeps only the `type` of a block that it does not know. Keep the "
        "new block's fields there if the spans should have them. Then list its type in this test."
    )


@pytest.mark.skipif(PYDANTIC_V1, reason="reads the fields of pydantic v2 models")
@pytest.mark.parametrize(
    ("blocks", "keep_their_fields"),
    [
        ((ContentBlock, ContentBlockParam), {"web_search_result"}),
        ((BetaContentBlock, BetaContentBlockParam), {"web_search_result", "text"}),
    ],
    ids=["stable", "beta"],
)
def test_result_block_list_types_all_keep_their_fields_or_only_their_type(
    blocks: tuple[Any, ...], keep_their_fields: set[str]
) -> None:
    in_lists: set[str] = set()
    for block in result_blocks(*blocks):
        for items in lists_in(field_types(block)["content"]):
            in_lists |= type_names(items)

    assert in_lists == keep_their_fields, (
        "The `content` of a server tool's or an MCP tool's result block can be a list of a new type of block. "
        "`result_block_content` (src/anthropic/lib/_tracing/_content.py) keeps only the `type` of a block in a list "
        "that it does not know. Keep the new block's fields there if the spans should have them. Then list its type "
        "in this test."
    )


RESULT_CONTENT_TYPES_KEPT = {
    "bash_code_execution_output",
    "bash_code_execution_result",
    "bash_code_execution_tool_result_error",
    "code_execution_output",
    "code_execution_result",
    "code_execution_tool_result_error",
    "encrypted_code_execution_result",
    "ephemeral",
    "text_editor_code_execution_create_result",
    "text_editor_code_execution_str_replace_result",
    "text_editor_code_execution_tool_result_error",
    "text_editor_code_execution_view_result",
    "tool_reference",
    "tool_search_tool_result_error",
    "tool_search_tool_search_result",
    "web_fetch_result",
    "web_fetch_tool_result_error",
    "web_search_result",
    "web_search_tool_result_error",
}
RESULT_CONTENT_TYPES_WITHOUT_THEIR_DATA = {"document", "image"}


@pytest.mark.skipif(PYDANTIC_V1, reason="reads the fields of pydantic v2 models")
@pytest.mark.parametrize(
    ("blocks", "kept"),
    [
        ((ContentBlock, ContentBlockParam), RESULT_CONTENT_TYPES_KEPT),
        (
            (BetaContentBlock, BetaContentBlockParam),
            RESULT_CONTENT_TYPES_KEPT
            | {
                "advisor_redacted_result",
                "advisor_result",
                "advisor_tool_result_error",
                "char_location",
                "content_block_location",
                "page_location",
                "search_result_location",
                "text",
                "web_search_result_location",
            },
        ),
    ],
    ids=["stable", "beta"],
)
def test_types_in_result_blocks_are_all_kept_or_lose_their_data(blocks: tuple[Any, ...], kept: set[str]) -> None:
    in_results: set[str] = set()
    for block in result_blocks(*blocks):
        in_results |= type_names_under(
            field_types(block)["content"], stop_at=RESULT_CONTENT_TYPES_WITHOUT_THEIR_DATA, seen=set()
        )

    assert in_results - RESULT_CONTENT_TYPES_WITHOUT_THEIR_DATA == kept, (
        "The result block of a server tool or an MCP tool can hold a new type of object. `without_data` "
        "(src/anthropic/lib/_tracing/_content.py) keeps every field of an object, except `encrypted_` fields, the "
        "data of an image or a document, and the file data of a `text_editor_code_execution_view_result`. Leave out "
        "the new object's data there if it is large or binary. Then list its type in this test."
    )


@pytest.mark.skipif(PYDANTIC_V1, reason="reads the fields of pydantic v2 models")
@pytest.mark.parametrize(
    "view_result",
    [
        TextEditorCodeExecutionViewResultBlock,
        TextEditorCodeExecutionViewResultBlockParam,
        BetaTextEditorCodeExecutionViewResultBlock,
        BetaTextEditorCodeExecutionViewResultBlockParam,
    ],
    ids=lambda value: getattr(value, "__name__", ""),
)
def test_view_result_file_types_all_keep_or_lose_their_content(view_result: Any) -> None:
    keep_their_content = {"text"}
    lose_their_content = {"image", "pdf"}

    assert literal_values(field_types(view_result)["file_type"]) == keep_their_content | lose_their_content, (
        "A `text_editor_code_execution_view_result` can have a new `file_type`. `without_data` "
        "(src/anthropic/lib/_tracing/_content.py) leaves out the content of an `image` and a `pdf` file. Leave out "
        "the new one's too if it is binary. Then list it in this test."
    )


@pytest.mark.skipif(PYDANTIC_V1, reason="reads the fields of pydantic v2 models")
@pytest.mark.parametrize("events", [RawMessageStreamEvent, BetaRawMessageStreamEvent], ids=["stable", "beta"])
def test_stream_event_types_are_all_handled_or_passed_over(events: Any) -> None:
    handled = {"message_start", "content_block_start", "content_block_delta", "message_delta", "message_stop"}
    passed_over = {"content_block_stop"}

    assert type_names(events) == handled | passed_over, (
        "A stream of a Message can have a new type of event. `StreamedMessage.item` "
        "(src/anthropic/lib/_tracing/_streaming.py) passes over an event that it does not know. Handle the new event "
        "there if the span should have what it carries. Then list its type in this test."
    )
