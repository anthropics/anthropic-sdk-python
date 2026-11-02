from __future__ import annotations

import json
import asyncio
from typing import Any, cast
from collections.abc import Callable, Sequence
from typing_extensions import Final, override

import httpx2
import pytest
import pydantic
from respx import MockRouter
from opentelemetry import trace
from opentelemetry.trace import Span, SpanKind, StatusCode
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider, sampling
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from anthropic import Anthropic, AsyncAnthropic, RateLimitError, beta_tool, beta_async_tool
from anthropic._types import OpenTelemetryTraces, OpenTelemetryOptions
from anthropic._compat import PYDANTIC_V1
from anthropic._tracing import resolve_open_telemetry
from anthropic.lib.tools import (
    BetaToolRunner,
    BetaStreamingToolRunner,
    _beta_session_runner as session_runner_mod,
)
from anthropic._streaming import AsyncStream
from anthropic.types.beta import BetaToolParam, BetaTextBlockParam, BetaSearchResultBlockParam
from anthropic.lib._tracing import OpenTelemetryConfig
from anthropic.lib._tracing._utils import to_json
from anthropic.types.beta.sessions import BetaManagedAgentsSessionEvent, BetaManagedAgentsStreamSessionEvents
from anthropic.lib._tracing._content import CONTENT_LIMIT, fit_content, set_content_attributes
from anthropic.lib._tracing._attributes import AttributeName
from anthropic.lib.tools._beta_functions import BetaBuiltinFunctionTool
from anthropic.lib.tools._beta_session_runner import SessionToolRunner
from anthropic.types.beta.parsed_beta_message import ParsedBetaMessage
from anthropic.types.beta.beta_tool_result_block_param import Content as BetaContent

from .toolsets._stubs import EchoBrowserToolset, AsyncEchoBrowserToolset
from .test_session_runner import FakeAsyncEvents, _FakeTool, _tool_use, _FakeClient, _terminated, _custom_tool_use
from ...test_open_telemetry import TRACING_FAILURES, utf8_size, type_names, failing_tracing

base_url = "http://127.0.0.1:4010"

pytestmark = pytest.mark.skipif(PYDANTIC_V1, reason="tool runner not supported with pydantic v1")

USAGE = {"input_tokens": 3, "output_tokens": 4}
FINAL: dict[str, Any] = {
    "id": "msg_final",
    "type": "message",
    "role": "assistant",
    "model": "claude-test",
    "content": [{"type": "text", "text": "It is sunny."}],
    "stop_reason": "end_turn",
    "stop_sequence": None,
    "usage": USAGE,
}

CONTENT_ATTRIBUTES: Final = ("gen_ai.tool.call.arguments", "anthropic.tool_result.content")

COMPACTION: dict[str, Any] = {
    "id": "msg_compaction",
    "type": "message",
    "role": "assistant",
    "model": "claude-test",
    "content": [{"type": "compaction", "content": "Summary of the conversation so far."}],
    "stop_reason": "compaction",
    "stop_sequence": None,
    "usage": USAGE,
}


def tool_use_message(city: str = "SF") -> dict[str, Any]:
    return {
        "id": f"msg_{city}",
        "type": "message",
        "role": "assistant",
        "model": "claude-test",
        "content": [{"type": "tool_use", "id": f"toolu_{city}", "name": "get_weather", "input": {"city": city}}],
        "stop_reason": "tool_use",
        "stop_sequence": None,
        "usage": USAGE,
    }


def sse(message: dict[str, Any]) -> httpx2.Response:
    """`message` as the response of a streamed request."""
    start: dict[str, Any] = {**message, "content": [], "stop_reason": None}
    events: list[dict[str, Any]] = [{"type": "message_start", "message": start}]
    for index, block in enumerate(message["content"]):
        empty: dict[str, Any]
        delta: dict[str, Any]
        if block["type"] == "tool_use":
            empty = {**block, "input": {}}
            delta = {"type": "input_json_delta", "partial_json": json.dumps(block["input"])}
        elif block["type"] == "compaction":
            empty = {"type": "compaction", "content": None}
            delta = {"type": "compaction_delta", "content": block["content"]}
        else:
            empty = {"type": "text", "text": ""}
            delta = {"type": "text_delta", "text": block["text"]}
        events += [
            {"type": "content_block_start", "index": index, "content_block": empty},
            {"type": "content_block_delta", "index": index, "delta": delta},
            {"type": "content_block_stop", "index": index},
        ]
    events += [
        {"type": "message_delta", "delta": {"stop_reason": message["stop_reason"]}, "usage": USAGE},
        {"type": "message_stop"},
    ]
    body = b"".join(f"event: {e['type']}\ndata: {json.dumps(e)}\n\n".encode() for e in events)
    return httpx2.Response(200, content=body, headers={"content-type": "text/event-stream"})


class Spans:
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


def attributes(span: ReadableSpan) -> dict[str, Any]:
    return dict(span.attributes or {})


def span_id(span: ReadableSpan | Span) -> int:
    span_context = span.get_span_context()
    assert span_context is not None
    return span_context.span_id


def parent_id(span: ReadableSpan) -> int:
    assert span.parent is not None
    return span.parent.span_id


def get_weather(city: str) -> str:
    """The weather in a city.

    Args:
        city: The city.
    """
    if city == "Atlantis":
        raise ValueError("no such city")
    return json.dumps({"city": city, "weather": "sunny"})


async def async_get_weather(city: str) -> str:
    """The weather in a city.

    Args:
        city: The city.
    """
    if city == "Atlantis":
        raise ValueError("no such city")
    return json.dumps({"city": city, "weather": "sunny"})


def run(
    client: Anthropic, *, conversation_id: str | None = None, **kwargs: Any
) -> "BetaToolRunner[Any] | BetaStreamingToolRunner[Any]":
    if conversation_id is not None:
        client = client.with_options(open_telemetry={**client.open_telemetry, "conversation_id": conversation_id})
    return cast(
        "BetaToolRunner[Any] | BetaStreamingToolRunner[Any]",
        client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-test",
            # Made here, because tool functions need pydantic v2 and this module is collected under v1 too.
            tools=[beta_tool(get_weather)],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
            **kwargs,
        ),
    )


def async_run(client: AsyncAnthropic, **kwargs: Any) -> Any:
    return cast(Any, client.beta.messages).tool_runner(
        max_tokens=1024,
        model="claude-test",
        tools=[beta_async_tool(async_get_weather, name="get_weather")],
        messages=[{"role": "user", "content": "What is the weather in SF?"}],
        **kwargs,
    )


def instrument(monkeypatch: pytest.MonkeyPatch, spans: Spans, runner: object, method: str) -> None:
    """Runs `method` of the runner's class in a span named after it, as instrumentation that the SDK
    knows nothing about would: a patched library, or a callback that the application gave.
    """
    original = getattr(type(runner), method)
    tracer = spans.provider.get_tracer("other")

    def instrumented(*args: Any, **kwargs: Any) -> Any:
        with tracer.start_as_current_span(f"other.{method}"):
            return original(*args, **kwargs)

    monkeypatch.setattr(type(runner), method, instrumented)


def slow_stream_closes(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Makes closing a response stream wait, as closing a connection does, and lists each close as it
    starts and finishes.
    """
    close = AsyncStream[Any].close
    closes: list[str] = []

    async def slow_close(stream: AsyncStream[Any]) -> None:
        closes.append("started")
        for _ in range(3):
            await asyncio.sleep(0)
        await close(stream)
        closes.append("finished")

    monkeypatch.setattr(AsyncStream, "close", slow_close)
    return closes


RUNNER_MODES: Final = pytest.mark.parametrize(
    "mode",
    [{}, {"stream": True}, {"stream": True, "run_tools_eagerly": True}],
    ids=["whole", "streamed", "eager"],
)


def member_calls(*calls: tuple[str, str, str | None]) -> dict[str, Any]:
    """A reply with one `tool_use` for each call, which is its id, its name and its `toolset_name`, if it has one."""
    reply = tool_use_message()
    reply["content"] = [
        {"type": "tool_use", "id": id, "name": name, "input": {"step": step}}
        | ({} if toolset_name is None else {"toolset_name": toolset_name})
        for step, (id, name, toolset_name) in enumerate(calls)
    ]
    return reply


async def run_with_a_browser_toolset(
    sync: bool,
    respx_mock: MockRouter,
    reply: dict[str, Any],
    *,
    open_telemetry: OpenTelemetryOptions,
    mode: dict[str, Any],
    at_the_end_of_each_reply: Callable[[], None] = lambda: None,
) -> Any:
    """Runs the loop of a tool runner that has a browser toolset on `reply` and then `FINAL`, and returns the route.

    A streamed reply is read to its end, and `at_the_end_of_each_reply` is called on its `message_stop` event.
    """
    stream = mode.get("stream", False)
    route = respx_mock.post("/v1/messages").mock(
        side_effect=[sse(message) if stream else httpx2.Response(200, json=message) for message in (reply, FINAL)]
    )
    options: dict[str, Any] = {"base_url": base_url, "api_key": "key", "open_telemetry": open_telemetry}
    params: dict[str, Any] = {
        "max_tokens": 1024,
        "model": "claude-test",
        "messages": [{"role": "user", "content": "Open the page."}],
        **mode,
    }
    if sync:
        for item in cast(Any, Anthropic(**options).beta.messages).tool_runner(tools=[EchoBrowserToolset()], **params):
            for event in item if stream else ():
                if event.type == "message_stop":
                    at_the_end_of_each_reply()
    else:
        runner = cast(Any, AsyncAnthropic(**options).beta.messages).tool_runner(
            tools=[AsyncEchoBrowserToolset()], **params
        )
        async for item in runner:
            if stream:
                async for event in item:
                    if event.type == "message_stop":
                        at_the_end_of_each_reply()
    return route


def tool_spans(spans: Spans) -> list[ReadableSpan]:
    return [span for span in spans.finished if attributes(span).get("gen_ai.operation.name") == "execute_tool"]


class TestToolRunnerSpans:
    @pytest.mark.respx(base_url=base_url)
    def test_tool_runner_and_tool_spans(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())

        tracer = spans.provider.get_tracer("app")
        with tracer.start_as_current_span("app") as app:
            run(client, conversation_id="conv_1").until_done()

        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.kind == SpanKind.INTERNAL
        assert tool_runner_span.status.status_code == StatusCode.OK
        assert parent_id(tool_runner_span) == span_id(app)
        assert attributes(tool_runner_span) == {
            "gen_ai.operation.name": "invoke_agent",
            "gen_ai.provider.name": "anthropic",
            "gen_ai.request.model": "claude-test",
            "gen_ai.conversation.id": "conv_1",
        }

        calls = spans.named("anthropic.messages.create")
        assert len(calls) == 2
        for call in calls:
            assert parent_id(call) == span_id(tool_runner_span)
            assert attributes(call)["gen_ai.conversation.id"] == "conv_1"
        # Each request has its own response's stop reason; the tool runner span, above, has none.
        assert [attributes(call)["anthropic.message.stop_reason"] for call in calls] == ["tool_use", "end_turn"]

        tool = spans.one("anthropic.custom_tool_use get_weather")
        assert tool.kind == SpanKind.INTERNAL
        assert tool.status.status_code == StatusCode.OK
        assert parent_id(tool) == span_id(tool_runner_span)
        assert attributes(tool) == {
            "gen_ai.operation.name": "execute_tool",
            "gen_ai.provider.name": "anthropic",
            "gen_ai.tool.name": "get_weather",
            # The description is metadata, so the span has it without content mode.
            "gen_ai.tool.description": "The weather in a city.",
            "gen_ai.tool.call.id": "toolu_SF",
            "gen_ai.conversation.id": "conv_1",
            "gen_ai.tool.type": "function",
        }
        assert calls[0].end_time <= tool.start_time <= tool.end_time <= calls[1].start_time  # type: ignore[operator]

    @pytest.mark.respx(base_url=base_url)
    def test_tool_error(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message("Atlantis")), httpx2.Response(200, json=FINAL)]
        )
        client = Anthropic(
            base_url=base_url, api_key="key", open_telemetry=spans.option(traces={"content_mode": "content"})
        )

        run(client).until_done()

        tool = spans.one("anthropic.custom_tool_use get_weather")
        assert tool.status.status_code == StatusCode.ERROR
        assert attributes(tool)["error.type"] == "tool_error"
        assert json.loads(attributes(tool)["gen_ai.tool.call.arguments"]) == {"city": "Atlantis"}
        # The content of the error result that the runner made of the tool's exception.
        assert json.loads(attributes(tool)["anthropic.tool_result.content"]) == [
            {"type": "text", "text": "ValueError('no such city')"}
        ]
        assert "gen_ai.tool.call.result" not in attributes(tool)
        assert spans.one("anthropic.messages.tool_runner").status.status_code == StatusCode.OK

    @pytest.mark.respx(base_url=base_url)
    def test_tool_result_content(self, spans: Spans, respx_mock: MockRouter) -> None:
        text: BetaTextBlockParam = {
            "type": "text",
            "text": "It is sunny.",
            "citations": [
                {
                    "type": "char_location",
                    "cited_text": "sunny",
                    "document_index": 0,
                    "document_title": "Weather",
                    "start_char_index": 0,
                    "end_char_index": 5,
                },
                {
                    "type": "web_search_result_location",
                    "cited_text": "sunny",
                    "encrypted_index": "encrypted_0",
                    "title": "Weather",
                    "url": "https://example.com/weather",
                },
            ],
            "cache_control": {"type": "ephemeral"},
        }
        search_result: BetaSearchResultBlockParam = {
            "type": "search_result",
            "source": "https://example.com/weather",
            "title": "Weather",
            "content": [{"type": "text", "text": "sunny"}],
            "citations": {"enabled": True},
        }

        def blocks(city: str) -> list[BetaContent]:
            image: BetaContent = {"type": "image", "source": {"type": "url", "url": f"https://example.com/{city}.png"}}
            return [text, search_result, image]

        def nothing(city: str) -> Any:
            return None if city else ""

        client = Anthropic(
            base_url=base_url, api_key="key", open_telemetry=spans.option(traces={"content_mode": "content"})
        )
        for function in (get_weather, blocks, nothing):
            respx_mock.post("/v1/messages").mock(
                side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
            )
            client.beta.messages.tool_runner(
                max_tokens=1024,
                model="claude-test",
                tools=[beta_tool(function, name="get_weather")],
                messages=[{"role": "user", "content": "What is the weather in SF?"}],
            ).until_done()

        string, listed, none = spans.named("anthropic.custom_tool_use get_weather")
        assert json.loads(attributes(string)["anthropic.tool_result.content"]) == [
            {"type": "text", "text": '{"city": "SF", "weather": "sunny"}'}
        ]
        # A text block and a search result keep all of their fields but one whose name starts with `encrypted_`. Any
        # other block is its type, with no prefix.
        char_location, web_search_result_location = text.get("citations") or []
        assert json.loads(attributes(listed)["anthropic.tool_result.content"]) == [
            {
                **text,
                "citations": [
                    char_location,
                    {key: value for key, value in web_search_result_location.items() if key != "encrypted_index"},
                ],
            },
            search_result,
            {"type": "image"},
        ]
        assert "encrypted_0" not in attributes(listed)["anthropic.tool_result.content"]
        assert json.loads(attributes(none)["anthropic.tool_result.content"]) == []
        for tool_span in (string, listed, none):
            assert "gen_ai.tool.call.result" not in attributes(tool_span)

    @pytest.mark.parametrize("returned", [None, []], ids=["none", "empty_list"])
    @pytest.mark.respx(base_url=base_url)
    def test_tool_result_without_content_has_an_empty_list(
        self, returned: object, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )

        cities: list[str] = []

        def get_weather(city: str) -> Any:
            cities.append(city)
            return returned

        client = Anthropic(
            base_url=base_url, api_key="key", open_telemetry=spans.option(traces={"content_mode": "content"})
        )
        client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-test",
            tools=[beta_tool(get_weather)],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        ).until_done()

        # The JSON of a list, as it is with content, and neither `null` nor an object.
        tool = spans.one("anthropic.custom_tool_use get_weather")
        assert cities == ["SF"]
        assert tool.status.status_code == StatusCode.OK
        assert attributes(tool)["anthropic.tool_result.content"] == "[]"

    @pytest.mark.parametrize("returned", [None, []], ids=["none", "empty_list"])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_tool_result_without_content_has_an_empty_list(
        self, returned: object, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )

        cities: list[str] = []

        async def get_weather(city: str) -> Any:
            cities.append(city)
            return returned

        client = AsyncAnthropic(
            base_url=base_url, api_key="key", open_telemetry=spans.option(traces={"content_mode": "content"})
        )
        await client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-test",
            tools=[beta_async_tool(get_weather)],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        ).until_done()

        tool = spans.one("anthropic.custom_tool_use get_weather")
        assert cities == ["SF"]
        assert tool.status.status_code == StatusCode.OK
        assert attributes(tool)["anthropic.tool_result.content"] == "[]"

    @pytest.mark.respx(base_url=base_url)
    def test_tool_result_content_loses_its_last_blocks_over_the_content_limit(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        half = "x" * (CONTENT_LIMIT // 2)

        def blocks(city: str) -> list[BetaContent]:
            texts = [city + half, half, "last"]
            return [{"type": "text", "text": text} for text in texts]

        def string(city: str) -> str:
            return city + half + half

        content = Anthropic(
            base_url=base_url, api_key="key", open_telemetry=spans.option(traces={"content_mode": "content"})
        )
        metadata = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        for client, function in ((content, blocks), (content, string), (content, get_weather), (metadata, string)):
            respx_mock.post("/v1/messages").mock(
                side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
            )
            client.beta.messages.tool_runner(
                max_tokens=1024,
                model="claude-test",
                tools=[beta_tool(function, name="get_weather")],
                messages=[{"role": "user", "content": "What is the weather in SF?"}],
            ).until_done()

        listed, single, under, off = spans.named("anthropic.custom_tool_use get_weather")
        # The second block does not fit beside the first, so it goes, and so does the one after it, which would fit.
        assert json.loads(attributes(listed)["anthropic.tool_result.content"]) == [
            {"type": "text", "text": "SF" + half}
        ]
        # A string is one block, so the list is left empty.
        assert json.loads(attributes(single)["anthropic.tool_result.content"]) == []
        for tool in (listed, single):
            assert attributes(tool)["anthropic.content.truncated"] is True
            arguments, result = (attributes(tool)[name] for name in CONTENT_ATTRIBUTES)
            assert json.loads(arguments) == {"city": "SF"}
            assert utf8_size(arguments + result) <= CONTENT_LIMIT
        assert json.loads(attributes(under)["anthropic.tool_result.content"]) == [
            {"type": "text", "text": '{"city": "SF", "weather": "sunny"}'}
        ]
        assert "anthropic.content.truncated" not in attributes(under)
        for name in (*CONTENT_ATTRIBUTES, "anthropic.content.truncated"):
            assert name not in attributes(off)

    @pytest.mark.respx(base_url=base_url)
    def test_tool_result_content_is_within_the_clients_max_content_bytes(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        def blocks(city: str) -> list[BetaContent]:
            texts = [city + "x" * 100, "y" * 100, "last"]
            return [{"type": "text", "text": text} for text in texts]

        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        traces: OpenTelemetryTraces = {"content_mode": "content", "max_content_bytes": 200}
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option(traces=traces))

        client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-test",
            tools=[beta_tool(blocks, name="get_weather")],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        ).until_done()

        tool = spans.one("anthropic.custom_tool_use get_weather")
        arguments, result = (attributes(tool)[name] for name in CONTENT_ATTRIBUTES)
        assert json.loads(result) == [{"type": "text", "text": "SF" + "x" * 100}]
        assert attributes(tool)["anthropic.content.truncated"] is True
        assert utf8_size(arguments + result) <= 200 < CONTENT_LIMIT

    @pytest.mark.parametrize(
        ("limit", "arguments", "result", "expected_arguments", "expected", "sizes"),
        [
            # Blocks go from the end, the last one first, whole. The arguments fit, so they stay whole and count.
            pytest.param(
                152,
                {"city": "Paris"},
                [
                    {"type": "text", "text": "first 111111111111111111111111111111"},
                    {"type": "text", "text": "second 222222222222222222222222222222"},
                    {"type": "image"},
                    {"type": "text", "text": "fourth 444444444444444444444444444444"},
                ],
                {"city": "Paris"},
                [
                    {"type": "text", "text": "first 111111111111111111111111111111"},
                    {"type": "text", "text": "second 222222222222222222222222222222"},
                ],
                (222, 142),
                id="tool_span_blocks_go_from_the_end",
            ),
            # The arguments exceed the limit by themselves: they go whole, and the result has the whole limit.
            pytest.param(
                100,
                {"text": "w" * 150},
                [{"type": "text", "text": "ok"}],
                None,
                [{"type": "text", "text": "ok"}],
                (190, 29),
                id="tool_span_arguments_alone_over_the_bound",
            ),
        ],
    )
    def test_size_bound_cases_of_a_tool_span(
        self,
        spans: Spans,
        limit: int,
        arguments: dict[str, Any],
        result: list[Any],
        expected_arguments: "dict[str, Any] | None",
        expected: list[Any],
        sizes: "tuple[int, int]",
    ) -> None:
        arguments_name, result_name = CONTENT_ATTRIBUTES
        given: dict[AttributeName, Any] = {arguments_name: arguments, result_name: result}
        span = spans.provider.get_tracer("test").start_span("anthropic.custom_tool_use f")
        assert isinstance(span, ReadableSpan)

        assert sum(utf8_size(to_json(value)) for value in given.values()) == sizes[0]

        set_content_attributes(span, given, limit=limit)

        # `None` for the arguments says that the span has none.
        values = {name: attributes(span)[name] for name in CONTENT_ATTRIBUTES if name in attributes(span)}
        assert {key: json.loads(value) for key, value in values.items()} == {
            key: value
            for key, value in ((arguments_name, expected_arguments), (result_name, expected))
            if value is not None
        }
        assert attributes(span)["anthropic.content.truncated"] is True
        assert sum(map(utf8_size, values.values())) == sizes[1]

    def test_tool_arguments_exactly_at_the_bound_stay_and_one_over_are_removed_whole(self) -> None:
        arguments_name, result_name = CONTENT_ATTRIBUTES
        arguments = {"text": "w" * 89}
        result = [{"type": "text", "text": "ok"}]
        assert len(to_json(arguments)) == 100

        # They leave no room for any block, so the list is emptied, and the values stay over the limit.
        assert fit_content({arguments_name: arguments, result_name: result}, 100) == (
            {arguments_name: to_json(arguments), result_name: "[]"},
            True,
        )
        assert fit_content({arguments_name: arguments, result_name: result}, 99) == (
            {result_name: to_json(result)},
            True,
        )
        # A run that was interrupted has no result, and one whose arguments fit is not marked.
        assert fit_content({arguments_name: arguments, result_name: None}, 100) == (
            {arguments_name: to_json(arguments)},
            False,
        )
        assert fit_content({arguments_name: arguments, result_name: None}, 99) == ({}, True)

    # The second city has one character of two bytes, so its arguments are 17 characters and 18 bytes.
    @pytest.mark.parametrize(("city", "size"), [("SF", 13), ("Z\u00fcrich", 18)], ids=["ascii", "multibyte"])
    @pytest.mark.respx(base_url=base_url)
    def test_tool_arguments_alone_over_the_bound_are_removed_whole(
        self, city: str, size: int, spans: Spans, respx_mock: MockRouter
    ) -> None:
        def get_weather(city: str) -> str:
            return "sunny in " + city

        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message(city)), httpx2.Response(200, json=FINAL)] * 2
        )
        assert utf8_size(to_json({"city": city})) == size
        for max_content_bytes in (size, size - 1):
            traces: OpenTelemetryTraces = {"content_mode": "content", "max_content_bytes": max_content_bytes}
            client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option(traces=traces))
            client.beta.messages.tool_runner(
                max_tokens=1024,
                model="claude-test",
                tools=[beta_tool(get_weather)],
                messages=[{"role": "user", "content": "What is the weather in SF?"}],
            ).until_done()

        arguments_name, result_name = CONTENT_ATTRIBUTES
        at_the_bound, one_over = spans.named("anthropic.custom_tool_use get_weather")
        assert json.loads(attributes(at_the_bound)[arguments_name]) == {"city": city}
        assert arguments_name not in attributes(one_over)
        for tool in (at_the_bound, one_over):
            # The result does not fit either way: the emptied list stays.
            assert attributes(tool)[result_name] == "[]"
            assert attributes(tool)["anthropic.content.truncated"] is True

    @pytest.mark.parametrize(("city", "size"), [("SF", 13), ("Z\u00fcrich", 18)], ids=["ascii", "multibyte"])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_tool_arguments_alone_over_the_bound_are_removed_whole(
        self, city: str, size: int, spans: Spans, respx_mock: MockRouter
    ) -> None:
        async def get_weather(city: str) -> str:
            return "sunny in " + city

        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message(city)), httpx2.Response(200, json=FINAL)] * 2
        )
        assert utf8_size(to_json({"city": city})) == size
        for max_content_bytes in (size, size - 1):
            traces: OpenTelemetryTraces = {"content_mode": "content", "max_content_bytes": max_content_bytes}
            client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option(traces=traces))
            await client.beta.messages.tool_runner(
                max_tokens=1024,
                model="claude-test",
                tools=[beta_async_tool(get_weather)],
                messages=[{"role": "user", "content": "What is the weather in SF?"}],
            ).until_done()

        arguments_name, result_name = CONTENT_ATTRIBUTES
        at_the_bound, one_over = spans.named("anthropic.custom_tool_use get_weather")
        assert json.loads(attributes(at_the_bound)[arguments_name]) == {"city": city}
        assert arguments_name not in attributes(one_over)
        for tool in (at_the_bound, one_over):
            assert attributes(tool)[result_name] == "[]"
            assert attributes(tool)["anthropic.content.truncated"] is True

    @pytest.mark.respx(base_url=base_url)
    def test_tool_content_that_json_cannot_hold_is_not_recorded(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = Anthropic(
            base_url=base_url, api_key="key", open_telemetry=spans.option(traces={"content_mode": "content"})
        )
        circular: dict[str, Any] = {}
        circular["self"] = circular

        def get_weather(city: str) -> Any:
            return [{"type": "text", "text": circular, "city": city}]

        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-test",
            tools=[beta_tool(get_weather)],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        )
        for _ in runner:
            # The circular result cannot be sent either, so only the first turn runs.
            break
        runner.generate_tool_call_response()

        tool = spans.one("anthropic.custom_tool_use get_weather")
        assert tool.status.status_code == StatusCode.OK
        assert "anthropic.tool_result.content" not in attributes(tool)

    @pytest.mark.respx(base_url=base_url)
    def test_content_is_off_by_default(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())

        run(client).until_done()

        tool = spans.one("anthropic.custom_tool_use get_weather")
        assert "gen_ai.tool.call.arguments" not in attributes(tool)
        assert "anthropic.tool_result.content" not in attributes(tool)
        assert attributes(tool)["gen_ai.tool.description"] == "The weather in a city."
        # The application set no conversation ID, and a Messages tool runner has no Session.
        for name in ("gen_ai.conversation.id", "anthropic.session.id", "anthropic.session.thread.id"):
            assert name not in attributes(tool)
        for call in spans.named("anthropic.messages.create"):
            assert "gen_ai.conversation.id" not in attributes(call)

    @pytest.mark.respx(base_url=base_url)
    def test_tool_that_the_application_runs_between_items_has_the_conversation_id(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        runner = run(client, conversation_id="conv_1")

        next(runner)
        # The runner executes the tool here, outside its loop's own code.
        assert runner.generate_tool_call_response() is not None
        assert attributes(spans.one("anthropic.custom_tool_use get_weather"))["gen_ai.conversation.id"] == "conv_1"
        runner.until_done()

        # The loop uses that result, so the tool ran once.
        assert len(spans.named("anthropic.custom_tool_use get_weather")) == 1

    @pytest.mark.respx(base_url=base_url)
    def test_tool_that_the_application_runs_is_a_child_of_the_applications_span(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        runner = run(client)

        next(runner)
        # The tool runner span is open here, but it is not current in the application's code.
        with spans.provider.get_tracer("app").start_as_current_span("app") as app:
            assert runner.generate_tool_call_response() is not None
        runner.until_done()

        assert parent_id(spans.one("anthropic.custom_tool_use get_weather")) == span_id(app)

    @pytest.mark.respx(base_url=base_url)
    def test_tool_that_the_application_runs_with_no_current_span_is_a_root_span(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        runner = run(client)

        next(runner)
        assert runner.generate_tool_call_response() is not None
        runner.until_done()

        assert spans.one("anthropic.custom_tool_use get_weather").parent is None

    @pytest.mark.respx(base_url=base_url)
    async def test_tool_that_the_application_runs_on_an_async_runner_is_a_child_of_the_applications_span(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        runner = async_run(client)

        async for _ in runner:
            break
        with spans.provider.get_tracer("app").start_as_current_span("app") as app:
            assert await runner.generate_tool_call_response() is not None
        await runner.until_done()
        await runner.close()

        assert parent_id(spans.one("anthropic.custom_tool_use get_weather")) == span_id(app)

    @pytest.mark.respx(base_url=base_url)
    def test_tool_description(self, spans: Spans, respx_mock: MockRouter) -> None:
        def undocumented(city: str) -> str:
            return f"sunny in {city}"

        class GetWeather(BetaBuiltinFunctionTool):
            @override
            def to_dict(self) -> BetaToolParam:
                return {"name": "get_weather", "description": "From the definition", "input_schema": {"type": "object"}}

            @override
            def call(self, input: object) -> str:
                return f"sunny: {input}"

        tools: list[Any] = [
            # The description that the application gave, not the function's docstring.
            beta_tool(get_weather, description="Given by the application"),
            # Neither a description nor a docstring.
            beta_tool(undocumented, name="get_weather"),
            # A tool that is its own definition.
            GetWeather(),
        ]
        client = Anthropic(
            base_url=base_url, api_key="key", open_telemetry=spans.option(traces={"content_mode": "content"})
        )
        for tool in tools:
            respx_mock.post("/v1/messages").mock(
                side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
            )
            client.beta.messages.tool_runner(
                max_tokens=1024,
                model="claude-test",
                tools=[tool],
                messages=[{"role": "user", "content": "What is the weather in SF?"}],
            ).until_done()

        given, none, defined = spans.named("anthropic.custom_tool_use get_weather")
        assert attributes(given)["gen_ai.tool.description"] == "Given by the application"
        assert "gen_ai.tool.description" not in attributes(none)
        assert attributes(defined)["gen_ai.tool.description"] == "From the definition"

    @pytest.mark.respx(base_url=base_url)
    def test_failed_call_ends_the_loop_with_its_error(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx2.Response(
                429, json={"type": "error", "error": {"type": "rate_limit_error", "message": "slow down"}}
            )
        )
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option(), max_retries=0)

        with pytest.raises(RateLimitError):
            run(client).until_done()

        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.ERROR
        assert attributes(tool_runner_span)["error.type"] == "rate_limit_error"
        assert attributes(spans.one("anthropic.messages.create"))["error.type"] == "rate_limit_error"

    @pytest.mark.respx(base_url=base_url)
    def test_failed_streamed_call_ends_the_loop_with_its_error(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx2.Response(
                429, json={"type": "error", "error": {"type": "rate_limit_error", "message": "slow down"}}
            )
        )
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option(), max_retries=0)

        # The request is sent when the loop opens the stream, before the application reads it.
        with pytest.raises(RateLimitError):
            for stream in run(client, stream=True):
                for _ in stream:
                    pass

        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.ERROR
        assert attributes(tool_runner_span)["error.type"] == "rate_limit_error"
        assert attributes(spans.one("anthropic.messages.create"))["error.type"] == "rate_limit_error"

    @pytest.mark.respx(base_url=base_url)
    def test_resuming_after_a_break_continues_the_span(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())

        runner = run(client)
        for _ in runner:
            break
        assert spans.named("anthropic.messages.tool_runner") == []
        assert runner.until_done().id == "msg_final"
        # Closing a runner that is done has no effect.
        runner.close()

        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.OK
        assert len(spans.named("anthropic.messages.create")) == 2
        assert parent_id(spans.one("anthropic.custom_tool_use get_weather")) == span_id(tool_runner_span)

    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_closing_the_runner_ends_the_span_unset(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())

        runner = run(client)
        for _ in runner:
            break
        runner.close()

        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.UNSET
        assert "error.type" not in attributes(tool_runner_span)
        assert spans.named("anthropic.custom_tool_use get_weather") == []
        assert list(runner) == []
        assert runner.until_done().id == "msg_SF"
        assert len(spans.named("anthropic.messages.create")) == 1

    @pytest.mark.respx(base_url=base_url)
    def test_output_type_is_json_when_the_runner_sets_a_json_output_format(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        weather: dict[str, Any] = {**FINAL, "content": [{"type": "text", "text": '{"weather": "sunny"}'}]}
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                httpx2.Response(200, json=tool_use_message()),
                httpx2.Response(200, json=FINAL),
                httpx2.Response(200, json=FINAL),
                httpx2.Response(200, json=weather),
                httpx2.Response(200, json=FINAL),
            ]
        )
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        schema: dict[str, object] = {"type": "object", "properties": {"weather": {"type": "string"}}}

        run(client, output_config={"format": {"type": "json_schema", "schema": schema}}).until_done()
        run(client).until_done()

        with_format, without = spans.named("anthropic.messages.tool_runner")
        assert attributes(with_format)["gen_ai.output.type"] == "json"
        assert "gen_ai.output.type" not in attributes(without)
        # Each request of the loop sets the format, so each of its spans has the attribute too.
        calls = [span for span in spans.named("anthropic.messages.create") if parent_id(span) == span_id(with_format)]
        assert [attributes(call)["gen_ai.output.type"] for call in calls] == ["json", "json"]

        class Weather(pydantic.BaseModel):
            weather: str

        # The deprecated `output_format` of the runner is a type.
        assert run(client, output_format=Weather).until_done().parsed_output == Weather(weather="sunny")
        assert attributes(spans.named("anthropic.messages.tool_runner")[2])["gen_ai.output.type"] == "json"

        run(client, output_config={"format": {"type": "other"}}).until_done()
        assert "gen_ai.output.type" not in attributes(spans.named("anthropic.messages.tool_runner")[3])

    @pytest.mark.respx(base_url=base_url)
    def test_tool_runner_span_has_its_attributes_from_its_start(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx2.Response(200, json=FINAL))
        started: dict[str, Any] = {}

        class Recording(sampling.Sampler):
            """Keeps the attributes that each span starts with, which is all that a sampler is given."""

            @override
            def should_sample(self, *args: Any, **kwargs: Any) -> sampling.SamplingResult:
                name, attributes = kwargs.get("name", args[2] if len(args) > 2 else None), kwargs.get("attributes")
                started[str(name)] = dict(attributes or (args[4] if len(args) > 4 else None) or {})
                return sampling.ALWAYS_ON.should_sample(*args, **kwargs)

            @override
            def get_description(self) -> str:
                return "recording"

        provider = TracerProvider(sampler=Recording())
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry={"tracer_provider": provider})
        schema: dict[str, object] = {"type": "object", "properties": {"weather": {"type": "string"}}}

        run(
            client,
            output_config={"format": {"type": "json_schema", "schema": schema}},
            conversation_id="conv_1",
        ).until_done()

        assert started["anthropic.messages.tool_runner"] == {
            "gen_ai.operation.name": "invoke_agent",
            "gen_ai.provider.name": "anthropic",
            "gen_ai.request.model": "claude-test",
            "gen_ai.conversation.id": "conv_1",
            "gen_ai.output.type": "json",
        }

    @pytest.mark.respx(base_url=base_url)
    def test_spans_that_a_tool_starts_are_children_of_its_tool_span(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        tracer = spans.provider.get_tracer("app")

        def get_weather(city: str) -> str:
            with tracer.start_as_current_span("app.lookup"):
                return city

        client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-test",
            tools=[beta_tool(get_weather)],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        ).until_done()

        tool = spans.one("anthropic.custom_tool_use get_weather")
        assert parent_id(spans.one("app.lookup")) == span_id(tool)
        assert parent_id(tool) == span_id(spans.one("anthropic.messages.tool_runner"))
        assert not trace.get_current_span().get_span_context().is_valid

    @pytest.mark.respx(base_url=base_url)
    async def test_spans_that_an_async_tool_starts_are_children_of_its_tool_span(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        tracer = spans.provider.get_tracer("app")

        async def get_weather(city: str) -> str:
            with tracer.start_as_current_span("app.lookup"):
                await asyncio.sleep(0)
                return city

        await (
            cast(Any, client.beta.messages)
            .tool_runner(
                max_tokens=1024,
                model="claude-test",
                tools=[beta_async_tool(get_weather)],
                messages=[{"role": "user", "content": "What is the weather in SF?"}],
            )
            .until_done()
        )

        tool = spans.one("anthropic.custom_tool_use get_weather")
        assert parent_id(spans.one("app.lookup")) == span_id(tool)
        assert not trace.get_current_span().get_span_context().is_valid

    @pytest.mark.respx(base_url=base_url)
    def test_closing_the_runner_from_a_tool_stops_the_loop(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())

        def get_weather(city: str) -> str:
            runner.close()
            return city

        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-test",
            tools=[beta_tool(get_weather)],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        )
        assert [message.id for message in runner] == ["msg_SF"]

        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.UNSET
        assert spans.one("anthropic.custom_tool_use get_weather").status.status_code == StatusCode.OK
        assert len(spans.named("anthropic.messages.create")) == 1

    @pytest.mark.respx(base_url=base_url)
    async def test_resuming_after_an_async_break_continues_the_span(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())

        runner = async_run(client)
        async for _ in runner:
            break
        assert (await runner.until_done()).id == "msg_final"
        await runner.close()

        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.OK
        assert len(spans.named("anthropic.messages.create")) == 2

    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_closing_the_async_runner_ends_the_span_unset(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())

        runner = async_run(client)
        async for _ in runner:
            break
        await runner.close()

        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.UNSET
        assert "error.type" not in attributes(tool_runner_span)
        assert spans.named("anthropic.custom_tool_use get_weather") == []
        assert [item async for item in runner] == []
        assert len(spans.named("anthropic.messages.create")) == 1

    @pytest.mark.respx(base_url=base_url)
    async def test_closing_the_async_runner_while_it_works_stops_the_loop(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())

        async def get_weather(city: str) -> str:
            # The loop is running here, as it is for another task that closes the runner during a request.
            await runner.close()
            return city

        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-test",
            tools=[beta_async_tool(get_weather)],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        )
        assert [message.id async for message in runner] == ["msg_SF"]

        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.UNSET
        assert len(spans.named("anthropic.messages.create")) == 1

    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_closing_the_async_streaming_runner_from_another_task_ends_its_loop(
        self, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse(tool_use_message()), sse(FINAL)])
        closes = slow_stream_closes(monkeypatch)
        client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        runner = async_run(client, stream=True)
        in_body = asyncio.Event()
        closing = asyncio.Event()

        async def drive() -> int:
            items = 0
            async for _ in runner:
                items += 1
                in_body.set()
                await closing.wait()
            return items

        driver = asyncio.ensure_future(drive())
        await in_body.wait()
        close = asyncio.ensure_future(runner.close())
        # The close is now waiting for the stream to close, and the driver asks for the next item meanwhile.
        await asyncio.sleep(0)
        assert closes == ["started"]
        closing.set()

        assert await driver == 1
        await close
        assert closes == ["started", "finished"]
        assert [item async for item in runner] == []
        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.UNSET
        assert "error.type" not in attributes(tool_runner_span)
        assert len(spans.named("anthropic.messages.create")) == 1

    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_closing_the_async_streaming_runner_twice_at_once_closes_it_once(
        self, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse(tool_use_message()), sse(FINAL)])
        closes = slow_stream_closes(monkeypatch)
        client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        runner = async_run(client, stream=True)

        async for _ in runner:
            break
        await asyncio.gather(runner.close(), runner.close())

        assert closes == ["started", "finished"]
        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.UNSET
        assert len(spans.named("anthropic.messages.create")) == 1

    @pytest.mark.respx(base_url=base_url)
    def test_a_compaction_request_is_a_child_of_the_tool_runner_span(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        # The response to a compaction request has its tokens in an entry of `usage.iterations` only.
        compaction = {
            "type": "compaction",
            "input_tokens": 100,
            "output_tokens": 20,
            "cache_read_input_tokens": 10,
            "cache_creation_input_tokens": 5,
        }
        usage = {"input_tokens": 0, "output_tokens": 0, "iterations": [compaction]}
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                httpx2.Response(200, json=tool_use_message()),
                httpx2.Response(200, json={**COMPACTION, "usage": usage}),
                httpx2.Response(200, json=FINAL),
            ]
        )
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())

        runner = run(client, conversation_id="conv_1")
        stop_reasons: list[Any] = []
        for message in runner:
            assert isinstance(message, ParsedBetaMessage)
            stop_reasons.append(message.stop_reason)
            if message.stop_reason == "tool_use":
                runner.compact_before_next_turn()

        assert stop_reasons == ["tool_use", "compaction", "end_turn"]
        assert "compaction" in json.loads(cast(Any, respx_mock.calls[1]).request.content)
        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.OK
        calls = spans.named("anthropic.messages.create")
        assert len(calls) == 3
        for call in calls:
            assert parent_id(call) == span_id(tool_runner_span)
            assert attributes(call)["gen_ai.conversation.id"] == "conv_1"
        # Only the span of the compaction request has the tokens of the compaction.
        assert [attributes(call).get("anthropic.usage.compaction.input_tokens") for call in calls] == [None, 115, None]
        assert [attributes(call).get("anthropic.usage.compaction.output_tokens") for call in calls] == [None, 20, None]
        assert attributes(calls[1])["gen_ai.usage.input_tokens"] == 0
        assert attributes(calls[1])["gen_ai.usage.output_tokens"] == 0

    @pytest.mark.parametrize("stream", [False, True], ids=["messages", "streams"])
    @pytest.mark.respx(base_url=base_url)
    def test_all_of_the_runners_code_runs_in_the_tool_runner_span(
        self, stream: bool, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        bodies = [tool_use_message(), COMPACTION, FINAL]
        respx_mock.post("/v1/messages").mock(
            side_effect=[sse(body) if stream else httpx2.Response(200, json=body) for body in bodies]
        )
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        runner = run(client, stream=stream)
        # What the runner does between two items, other than send requests and run tools.
        instrument(monkeypatch, spans, runner, "_append_tool_results")
        instrument(monkeypatch, spans, runner, "_register_compaction_response")
        tracer = spans.provider.get_tracer("app")

        # The application resumes the runner from a context of its own each time.
        steps = 0
        while True:
            with tracer.start_as_current_span(f"app.step_{steps}") as app:
                try:
                    next(runner)
                except StopIteration:
                    break
                finally:
                    assert trace.get_current_span() is app
                if steps == 0:
                    runner.compact_before_next_turn()
            steps += 1
        assert steps == 3

        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.OK
        assert parent_id(tool_runner_span) == span_id(spans.one("app.step_0"))
        for name in ("other._append_tool_results", "other._register_compaction_response"):
            assert parent_id(spans.one(name)) == span_id(tool_runner_span)
        assert [parent_id(call) for call in spans.named("anthropic.messages.create")] == [span_id(tool_runner_span)] * 3
        assert parent_id(spans.one("anthropic.custom_tool_use get_weather")) == span_id(tool_runner_span)

    @pytest.mark.parametrize("stream", [False, True], ids=["messages", "streams"])
    @pytest.mark.respx(base_url=base_url)
    async def test_all_of_the_async_runners_code_runs_in_the_tool_runner_span(
        self, stream: bool, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        bodies = [tool_use_message(), COMPACTION, FINAL]
        respx_mock.post("/v1/messages").mock(
            side_effect=[sse(body) if stream else httpx2.Response(200, json=body) for body in bodies]
        )
        client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        runner = async_run(client, stream=stream)
        instrument(monkeypatch, spans, runner, "_append_tool_results")
        instrument(monkeypatch, spans, runner, "_register_compaction_response")
        tracer = spans.provider.get_tracer("app")

        async def step(number: int) -> bool:
            with tracer.start_as_current_span(f"app.step_{number}") as app:
                try:
                    await runner.__anext__()
                except StopAsyncIteration:
                    return False
                finally:
                    assert trace.get_current_span() is app
                if number == 0:
                    runner.compact_before_next_turn()
                return True

        # Each step runs in a task of its own, so in a context of its own.
        steps = 0
        while await asyncio.create_task(step(steps)):
            steps += 1
        assert steps == 3

        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.OK
        assert parent_id(tool_runner_span) == span_id(spans.one("app.step_0"))
        for name in ("other._append_tool_results", "other._register_compaction_response"):
            assert parent_id(spans.one(name)) == span_id(tool_runner_span)
        assert [parent_id(call) for call in spans.named("anthropic.messages.create")] == [span_id(tool_runner_span)] * 3
        assert parent_id(spans.one("anthropic.custom_tool_use get_weather")) == span_id(tool_runner_span)
        assert not trace.get_current_span().get_span_context().is_valid

    @pytest.mark.respx(base_url=base_url)
    def test_the_applications_code_between_items_keeps_its_own_context(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse(tool_use_message()), sse(FINAL)])
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        tracer = spans.provider.get_tracer("app")

        with tracer.start_as_current_span("app") as app:
            for stream in run(client, stream=True):
                assert not isinstance(stream, ParsedBetaMessage)
                # The tool runner span is open here, and it is not the current one.
                assert trace.get_current_span() is app
                with tracer.start_as_current_span("app.handle"):
                    stream.until_done()

        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert [parent_id(handled) for handled in spans.named("app.handle")] == [span_id(app)] * 2
        assert all(handled.end_time <= tool_runner_span.end_time for handled in spans.named("app.handle"))  # type: ignore[operator]

    @pytest.mark.respx(base_url=base_url)
    def test_async_runners_that_are_open_when_the_event_loop_ends_have_no_status(
        self, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse(tool_use_message()) for _ in range(8)])
        slow_stream_closes(monkeypatch)

        async def leave_runners_open() -> list[Any]:
            client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
            runners = [async_run(client, stream=True) for _ in range(8)]
            for runner in runners:
                async for _ in runner:
                    break
            return runners

        # At its end the event loop closes every open generator at once, those inside a runner too, in any order.
        runners = asyncio.run(leave_runners_open())

        statuses = [span.status.status_code for span in spans.named("anthropic.messages.tool_runner")]
        assert statuses == [StatusCode.UNSET] * len(runners)

    @pytest.mark.respx(base_url=base_url)
    async def test_closing_the_async_streaming_runner_during_a_compaction_closes_its_stream(
        self, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # The close leaves the compaction response unread, so any body will do for it.
        respx_mock.post("/v1/messages").mock(side_effect=[sse(tool_use_message()), sse(FINAL)])
        closes = slow_stream_closes(monkeypatch)
        client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        runner = async_run(client, stream=True)

        items = 0
        async for _ in runner:
            items += 1
            if items == 2:
                break
            runner.compact_before_next_turn()
        assert "compaction" in json.loads(cast(Any, respx_mock.calls[1]).request.content)
        assert closes == ["started", "finished"]
        await runner.close()

        # The stream of the compaction request is closed when `close()` returns, before the tool runner span ends.
        assert closes == ["started", "finished", "started", "finished"]
        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.UNSET
        calls = spans.named("anthropic.messages.create")
        assert len(calls) == 2
        assert all(parent_id(call) == span_id(tool_runner_span) for call in calls)
        assert all(call.end_time <= tool_runner_span.end_time for call in calls)  # type: ignore[operator]

    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_canceling_a_tool_run_leaves_its_span_and_the_tool_runner_span_unset(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = AsyncAnthropic(
            base_url=base_url, api_key="key", open_telemetry=spans.option(traces={"content_mode": "content"})
        )
        started = asyncio.Event()

        async def get_weather(city: str) -> str:
            # The application cancels the task that drives the loop while the tool is running.
            started.set()
            await asyncio.sleep(60)
            return city

        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-test",
            tools=[beta_async_tool(get_weather)],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        )
        task = asyncio.ensure_future(runner.until_done())
        await started.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

        # A cancellation is the application stopping the run, which is no failure of the tool or the loop.
        tool = spans.one("anthropic.custom_tool_use get_weather")
        assert tool.status.status_code == StatusCode.UNSET
        assert "error.type" not in attributes(tool)
        # The runner made no result of the run.
        assert json.loads(attributes(tool)["gen_ai.tool.call.arguments"]) == {"city": "SF"}
        assert "anthropic.tool_result.content" not in attributes(tool)
        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.UNSET
        assert "error.type" not in attributes(tool_runner_span)
        assert len(spans.named("anthropic.messages.create")) == 1

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_runner(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(side_effect=[sse(tool_use_message()), sse(FINAL)])
        client = Anthropic(
            base_url=base_url, api_key="key", open_telemetry=spans.option(traces={"content_mode": "content"})
        )

        for stream in run(client, stream=True):
            assert not isinstance(stream, ParsedBetaMessage)
            for _ in stream:
                pass

        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.OK
        calls = spans.named("anthropic.messages.create")
        assert len(calls) == 2
        assert all(parent_id(call) == span_id(tool_runner_span) for call in calls)
        assert all(call.status.status_code == StatusCode.OK for call in calls)
        # The runner streams with the stream helper, whose snapshot gives each call's output content.
        assert [json.loads(attributes(call)["gen_ai.output.messages"])[0]["parts"] for call in calls] == [
            [{"type": "tool_call", "id": "toolu_SF", "name": "get_weather", "arguments": {"city": "SF"}}],
            [{"type": "text", "content": "It is sunny."}],
        ]
        tool = spans.one("anthropic.custom_tool_use get_weather")
        assert parent_id(tool) == span_id(tool_runner_span)

    @pytest.mark.parametrize("city", ["SF", "Atlantis"])
    @pytest.mark.respx(base_url=base_url)
    def test_tool_that_runs_while_the_reply_streams_has_its_span(
        self, spans: Spans, respx_mock: MockRouter, city: str
    ) -> None:
        route = respx_mock.post("/v1/messages").mock(side_effect=[sse(tool_use_message(city)), sse(FINAL)])
        client = Anthropic(
            base_url=base_url, api_key="key", open_telemetry=spans.option(traces={"content_mode": "content"})
        )

        tool_spans_at_the_end_of_each_reply: list[int] = []
        tracer = spans.provider.get_tracer("app")
        with tracer.start_as_current_span("app"):
            for stream in run(client, stream=True, run_tools_eagerly=True):
                assert not isinstance(stream, ParsedBetaMessage)
                for event in stream:
                    if event.type == "message_stop":
                        tool_spans_at_the_end_of_each_reply.append(
                            len(spans.named("anthropic.custom_tool_use get_weather"))
                        )

        # The tool ran, in its span, before the application had read the whole reply that called it, and the
        # result that the runner kept from that run did not start a second span when it sent the result.
        assert tool_spans_at_the_end_of_each_reply == [1, 1]
        tool = spans.one("anthropic.custom_tool_use get_weather")
        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        # The runner ran the tool, so the span is a child of its span, not of the span that the application read from.
        assert parent_id(tool) == span_id(tool_runner_span)
        assert attributes(tool)["gen_ai.tool.call.id"] == f"toolu_{city}"
        assert json.loads(attributes(tool)["gen_ai.tool.call.arguments"]) == {"city": city}
        if city == "Atlantis":
            assert tool.status.status_code == StatusCode.ERROR
            assert attributes(tool)["error.type"] == "tool_error"
        else:
            assert tool.status.status_code == StatusCode.OK
            assert "error.type" not in attributes(tool)
        assert tool_runner_span.status.status_code == StatusCode.OK
        sent = json.loads(route.calls.last.request.content)["messages"][-1]["content"]
        assert [block["tool_use_id"] for block in sent] == [f"toolu_{city}"]

    @pytest.mark.parametrize("city", ["SF", "Atlantis"])
    @pytest.mark.respx(base_url=base_url)
    async def test_async_tool_that_runs_while_the_reply_streams_has_its_span(
        self, spans: Spans, respx_mock: MockRouter, city: str
    ) -> None:
        route = respx_mock.post("/v1/messages").mock(side_effect=[sse(tool_use_message(city)), sse(FINAL)])
        client = AsyncAnthropic(
            base_url=base_url, api_key="key", open_telemetry=spans.option(traces={"content_mode": "content"})
        )

        tool_spans_at_the_end_of_each_reply: list[int] = []
        tracer = spans.provider.get_tracer("app")
        with tracer.start_as_current_span("app"):
            async for stream in async_run(client, stream=True, run_tools_eagerly=True):
                async for event in stream:
                    if event.type == "message_stop":
                        tool_spans_at_the_end_of_each_reply.append(
                            len(spans.named("anthropic.custom_tool_use get_weather"))
                        )

        assert tool_spans_at_the_end_of_each_reply == [1, 1]
        tool = spans.one("anthropic.custom_tool_use get_weather")
        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert parent_id(tool) == span_id(tool_runner_span)
        assert attributes(tool)["gen_ai.tool.call.id"] == f"toolu_{city}"
        assert json.loads(attributes(tool)["gen_ai.tool.call.arguments"]) == {"city": city}
        if city == "Atlantis":
            assert tool.status.status_code == StatusCode.ERROR
            assert attributes(tool)["error.type"] == "tool_error"
        else:
            assert tool.status.status_code == StatusCode.OK
            assert "error.type" not in attributes(tool)
        assert tool_runner_span.status.status_code == StatusCode.OK
        sent = json.loads(route.calls.last.request.content)["messages"][-1]["content"]
        assert [block["tool_use_id"] for block in sent] == [f"toolu_{city}"]

    @pytest.mark.respx(base_url=base_url)
    def test_tool_call_that_the_application_holds_has_one_span_when_it_runs(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        reply = tool_use_message()
        reply["content"].append({"type": "tool_use", "id": "toolu_LA", "name": "get_weather", "input": {"city": "LA"}})
        respx_mock.post("/v1/messages").mock(side_effect=[sse(reply), sse(FINAL)])
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        runner = run(client, stream=True, run_tools_eagerly=True)
        assert isinstance(runner, BetaStreamingToolRunner)

        calls_with_a_span_at_the_end_of_each_reply: list[list[str]] = []
        for stream in runner:
            for event in stream:
                if event.type == "content_block_start" and event.content_block.type == "tool_use":
                    if event.content_block.id == "toolu_LA":
                        runner.defer_tool_call(event.content_block)
            calls_with_a_span_at_the_end_of_each_reply.append(
                [
                    attributes(tool)["gen_ai.tool.call.id"]
                    for tool in spans.named("anthropic.custom_tool_use get_weather")
                ]
            )

        # The held call ran after the application was done with the reply, and each call has one span.
        assert calls_with_a_span_at_the_end_of_each_reply == [["toolu_SF"], ["toolu_SF", "toolu_LA"]]
        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        tools = spans.named("anthropic.custom_tool_use get_weather")
        assert all(parent_id(tool) == span_id(tool_runner_span) for tool in tools)

    @pytest.mark.respx(base_url=base_url)
    async def test_tool_call_that_the_application_holds_on_an_async_runner_has_one_span_when_it_runs(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        reply = tool_use_message()
        reply["content"].append({"type": "tool_use", "id": "toolu_LA", "name": "get_weather", "input": {"city": "LA"}})
        respx_mock.post("/v1/messages").mock(side_effect=[sse(reply), sse(FINAL)])
        client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
        runner = async_run(client, stream=True, run_tools_eagerly=True)

        calls_with_a_span_at_the_end_of_each_reply: list[list[str]] = []
        async for stream in runner:
            async for event in stream:
                if event.type == "content_block_start" and event.content_block.type == "tool_use":
                    if event.content_block.id == "toolu_LA":
                        runner.defer_tool_call(event.content_block)
            calls_with_a_span_at_the_end_of_each_reply.append(
                [
                    attributes(tool)["gen_ai.tool.call.id"]
                    for tool in spans.named("anthropic.custom_tool_use get_weather")
                ]
            )

        assert calls_with_a_span_at_the_end_of_each_reply == [["toolu_SF"], ["toolu_SF", "toolu_LA"]]
        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        tools = spans.named("anthropic.custom_tool_use get_weather")
        assert all(parent_id(tool) == span_id(tool_runner_span) for tool in tools)

    @pytest.mark.parametrize("reader", ["application", "until_done", "loop"])
    @pytest.mark.respx(base_url=base_url)
    def test_closing_the_runner_from_a_tool_that_runs_while_the_reply_streams_stops_the_loop(
        self, spans: Spans, respx_mock: MockRouter, reader: str
    ) -> None:
        reply = tool_use_message()
        reply["content"].append({"type": "tool_use", "id": "toolu_LA", "name": "get_weather", "input": {"city": "LA"}})
        respx_mock.post("/v1/messages").mock(side_effect=[sse(reply), sse(FINAL)])
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())

        cities: list[str] = []

        def get_weather(city: str) -> str:
            cities.append(city)
            runner.close()
            return city

        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-test",
            tools=[beta_tool(get_weather)],
            messages=[{"role": "user", "content": "What is the weather in SF and in LA?"}],
            stream=True,
            run_tools_eagerly=True,
        )
        # The tool runs inside a read of the reply, by the application or by the loop, which the close must not break:
        # it closes nothing while the tool runs, and the loop stops at its next step, as it does for any other tool.
        events: list[str] = []
        streams = 0
        if reader == "until_done":
            assert runner.until_done().id == "msg_SF"
        else:
            for stream in runner:
                streams += 1
                if reader == "application":
                    events = [event.type for event in stream]
            assert streams == 1
        if reader == "application":
            assert events[-1] == "message_stop"

        assert cities == ["SF", "LA"]
        assert list(runner) == []
        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.UNSET
        assert "error.type" not in attributes(tool_runner_span)
        tools = spans.named("anthropic.custom_tool_use get_weather")
        assert [attributes(tool)["gen_ai.tool.call.id"] for tool in tools] == ["toolu_SF", "toolu_LA"]
        assert all(tool.status.status_code == StatusCode.OK for tool in tools)
        assert all(parent_id(tool) == span_id(tool_runner_span) for tool in tools)
        # The close ended nothing while a tool ran, so the runner's span outlasted the tools' spans.
        assert all(tool.end_time <= tool_runner_span.end_time for tool in tools)  # type: ignore[operator]
        assert len(spans.named("anthropic.messages.create")) == 1

    @pytest.mark.parametrize("reader", ["application", "until_done", "loop"])
    @pytest.mark.respx(base_url=base_url)
    async def test_closing_the_async_runner_from_a_tool_that_runs_while_the_reply_streams_stops_the_loop(
        self, spans: Spans, respx_mock: MockRouter, reader: str
    ) -> None:
        reply = tool_use_message()
        reply["content"].append({"type": "tool_use", "id": "toolu_LA", "name": "get_weather", "input": {"city": "LA"}})
        respx_mock.post("/v1/messages").mock(side_effect=[sse(reply), sse(FINAL)])
        client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())

        cities: list[str] = []

        async def get_weather(city: str) -> str:
            cities.append(city)
            await runner.close()
            return city

        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-test",
            tools=[beta_async_tool(get_weather)],
            messages=[{"role": "user", "content": "What is the weather in SF and in LA?"}],
            stream=True,
            run_tools_eagerly=True,
        )
        events: list[str] = []
        streams = 0
        if reader == "until_done":
            assert (await runner.until_done()).id == "msg_SF"
        else:
            async for stream in runner:
                streams += 1
                if reader == "application":
                    events = [event.type async for event in stream]
            assert streams == 1
        if reader == "application":
            assert events[-1] == "message_stop"

        assert cities == ["SF", "LA"]
        assert [item async for item in runner] == []
        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.UNSET
        assert "error.type" not in attributes(tool_runner_span)
        tools = spans.named("anthropic.custom_tool_use get_weather")
        assert [attributes(tool)["gen_ai.tool.call.id"] for tool in tools] == ["toolu_SF", "toolu_LA"]
        assert all(tool.status.status_code == StatusCode.OK for tool in tools)
        assert all(parent_id(tool) == span_id(tool_runner_span) for tool in tools)
        # The close ended nothing while a tool ran, so the runner's span outlasted the tools' spans.
        assert all(tool.end_time <= tool_runner_span.end_time for tool in tools)  # type: ignore[operator]
        assert len(spans.named("anthropic.messages.create")) == 1

    @pytest.mark.parametrize("reader", ["application", "until_done", "loop"])
    @pytest.mark.respx(base_url=base_url)
    def test_closing_the_runner_from_a_toolset_member_that_runs_while_the_reply_streams_stops_the_loop(
        self, spans: Spans, respx_mock: MockRouter, reader: str
    ) -> None:
        reply = member_calls(("toolu_1", "navigate", "browser"), ("toolu_2", "screenshot", "browser"))
        respx_mock.post("/v1/messages").mock(side_effect=[sse(reply), sse(FINAL)])
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())

        class ClosingToolset(EchoBrowserToolset):
            @override
            def call(self, context: Any, name: str, input: object) -> Any:
                runner.close()
                return super().call(context, name, input)

        toolset = ClosingToolset()
        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-test",
            tools=[toolset],
            messages=[{"role": "user", "content": "Open the page."}],
            stream=True,
            run_tools_eagerly=True,
        )
        # As for a tool, the close closes nothing while the member runs inside a read of the reply.
        events: list[str] = []
        streams = 0
        if reader == "until_done":
            assert runner.until_done().id == "msg_SF"
        else:
            for stream in runner:
                streams += 1
                if reader == "application":
                    events = [event.type for event in stream]
            assert streams == 1
        if reader == "application":
            assert events[-1] == "message_stop"

        assert [name for name, _ in toolset.calls] == ["navigate", "screenshot"]
        assert list(runner) == []
        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.UNSET
        assert [attributes(tool)["gen_ai.tool.call.id"] for tool in tool_spans(spans)] == ["toolu_1", "toolu_2"]
        assert all(tool.status.status_code == StatusCode.OK for tool in tool_spans(spans))
        assert all(parent_id(tool) == span_id(tool_runner_span) for tool in tool_spans(spans))
        # The close ended nothing while a member ran, so the runner's span outlasted the members' spans.
        assert all(tool.end_time <= tool_runner_span.end_time for tool in tool_spans(spans))  # type: ignore[operator]
        assert len(spans.named("anthropic.messages.create")) == 1

    @pytest.mark.parametrize("reader", ["application", "until_done", "loop"])
    @pytest.mark.respx(base_url=base_url)
    async def test_closing_the_async_runner_from_a_toolset_member_that_runs_while_the_reply_streams_stops_the_loop(
        self, spans: Spans, respx_mock: MockRouter, reader: str
    ) -> None:
        reply = member_calls(("toolu_1", "navigate", "browser"), ("toolu_2", "screenshot", "browser"))
        respx_mock.post("/v1/messages").mock(side_effect=[sse(reply), sse(FINAL)])
        client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())

        class ClosingToolset(AsyncEchoBrowserToolset):
            @override
            async def call(self, context: Any, name: str, input: object) -> Any:
                await runner.close()
                return await super().call(context, name, input)

        toolset = ClosingToolset()
        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-test",
            tools=[toolset],
            messages=[{"role": "user", "content": "Open the page."}],
            stream=True,
            run_tools_eagerly=True,
        )
        events: list[str] = []
        streams = 0
        if reader == "until_done":
            assert (await runner.until_done()).id == "msg_SF"
        else:
            async for stream in runner:
                streams += 1
                if reader == "application":
                    events = [event.type async for event in stream]
            assert streams == 1
        if reader == "application":
            assert events[-1] == "message_stop"

        assert [name for name, _ in toolset.calls] == ["navigate", "screenshot"]
        assert [item async for item in runner] == []
        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.UNSET
        assert [attributes(tool)["gen_ai.tool.call.id"] for tool in tool_spans(spans)] == ["toolu_1", "toolu_2"]
        assert all(tool.status.status_code == StatusCode.OK for tool in tool_spans(spans))
        assert all(parent_id(tool) == span_id(tool_runner_span) for tool in tool_spans(spans))
        # The close ended nothing while a member ran, so the runner's span outlasted the members' spans.
        assert all(tool.end_time <= tool_runner_span.end_time for tool in tool_spans(spans))  # type: ignore[operator]
        assert len(spans.named("anthropic.messages.create")) == 1

    @pytest.mark.respx(base_url=base_url)
    async def test_async_runner(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())

        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-test",
            tools=[beta_async_tool(async_get_weather, name="get_weather")],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        )
        await runner.until_done()

        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.OK
        tool = spans.one("anthropic.custom_tool_use get_weather")
        assert tool.status.status_code == StatusCode.OK
        assert parent_id(tool) == span_id(tool_runner_span)
        assert len(spans.named("anthropic.messages.create")) == 2

    @pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
    @pytest.mark.respx(base_url=base_url)
    async def test_only_the_api_calls_of_a_tool_runner_have_http_and_url_attributes(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )

        if sync:
            run(Anthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())).until_done()
        else:
            await async_run(
                AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())
            ).until_done()

        http = {
            (span.name, span.kind): sorted(
                key for key in attributes(span) if key.startswith(("http.", "url.", "server."))
            )
            for span in spans.finished
        }
        assert http == {
            ("anthropic.messages.tool_runner", SpanKind.INTERNAL): [],
            ("anthropic.custom_tool_use get_weather", SpanKind.INTERNAL): [],
            ("anthropic.messages.create", SpanKind.CLIENT): [
                "http.request.method",
                "http.response.status_code",
                "http.route",
                "server.address",
                "server.port",
                "url.full",
                "url.path",
                "url.scheme",
            ],
        }

    @pytest.mark.respx(base_url=base_url)
    async def test_a_tool_the_mcp_helper_made_runs_in_an_mcp_tool_use_span(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        mcp_types = pytest.importorskip("mcp.types")
        from anthropic.lib.tools.mcp import async_mcp_tool

        class MCPClient:
            async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
                return mcp_types.CallToolResult(
                    content=[mcp_types.TextContent(type="text", text=f"{name}{arguments}: sunny")]
                )

        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())

        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-test",
            tools=[
                async_mcp_tool(
                    mcp_types.Tool(
                        name="get_weather",
                        description="The weather, from the MCP server.",
                        inputSchema={"type": "object", "properties": {}},
                    ),
                    cast(Any, MCPClient()),
                )
            ],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        )
        await runner.until_done()

        tool = spans.one("anthropic.mcp_tool_use get_weather")
        assert tool.kind == SpanKind.INTERNAL
        assert tool.status.status_code == StatusCode.OK
        assert parent_id(tool) == span_id(spans.one("anthropic.messages.tool_runner"))
        assert attributes(tool) == {
            "gen_ai.operation.name": "execute_tool",
            "gen_ai.provider.name": "anthropic",
            "gen_ai.tool.name": "get_weather",
            "gen_ai.tool.description": "The weather, from the MCP server.",
            "gen_ai.tool.call.id": "toolu_SF",
            "gen_ai.tool.type": "function",
        }
        assert spans.named("anthropic.custom_tool_use get_weather") == []

    @pytest.mark.respx(base_url=base_url)
    async def test_a_tool_the_mcp_helper_made_without_a_description_has_none(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        mcp_types = pytest.importorskip("mcp.types")
        from anthropic.lib.tools.mcp import async_mcp_tool

        class MCPClient:
            async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
                return mcp_types.CallToolResult(
                    content=[mcp_types.TextContent(type="text", text=f"{name}{arguments}: sunny")]
                )

        respx_mock.post("/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option())

        runner = client.beta.messages.tool_runner(
            max_tokens=1024,
            model="claude-test",
            tools=[
                async_mcp_tool(
                    mcp_types.Tool(name="get_weather", inputSchema={"type": "object", "properties": {}}),
                    cast(Any, MCPClient()),
                )
            ],
            messages=[{"role": "user", "content": "What is the weather in SF?"}],
        )
        await runner.until_done()

        assert "gen_ai.tool.description" not in attributes(spans.one("anthropic.mcp_tool_use get_weather"))

    @RUNNER_MODES
    @pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
    @pytest.mark.respx(base_url=base_url)
    async def test_toolset_member_that_the_runner_runs_has_a_tool_span(
        self, sync: bool, mode: dict[str, Any], spans: Spans, respx_mock: MockRouter
    ) -> None:
        route = await run_with_a_browser_toolset(
            sync,
            respx_mock,
            member_calls(("toolu_1", "navigate", "browser"), ("toolu_2", "screenshot", "browser")),
            open_telemetry=spans.option(conversation_id="conv_1"),
            mode=mode,
        )

        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert tool_runner_span.status.status_code == StatusCode.OK
        # Each member call that the toolset ran has one span, in the model's order.
        assert [span.name for span in tool_spans(spans)] == [
            "anthropic.custom_tool_use navigate",
            "anthropic.custom_tool_use screenshot",
        ]
        for tool, name, call_id in zip(
            tool_spans(spans), ("navigate", "screenshot"), ("toolu_1", "toolu_2"), strict=True
        ):
            assert tool.kind == SpanKind.INTERNAL
            assert tool.status.status_code == StatusCode.OK
            assert parent_id(tool) == span_id(tool_runner_span)
            # A toolset has no description, and the call's input and result are content.
            assert attributes(tool) == {
                "gen_ai.operation.name": "execute_tool",
                "gen_ai.provider.name": "anthropic",
                "gen_ai.tool.name": name,
                "anthropic.toolset.name": "browser",
                "gen_ai.tool.call.id": call_id,
                "gen_ai.conversation.id": "conv_1",
                "gen_ai.tool.type": "function",
            }
        # The spans are of the runs whose results the runner sent, and tracing made no request of its own.
        assert route.call_count == 2
        sent = json.loads(route.calls.last.request.content)["messages"][-1]["content"]
        assert [(block["tool_use_id"], block["content"]) for block in sent] == [
            ("toolu_1", 'navigate:{"step": 0}'),
            ("toolu_2", 'screenshot:{"step": 1}'),
        ]

    @pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
    @pytest.mark.respx(base_url=base_url)
    async def test_toolset_member_that_runs_while_the_reply_streams_has_its_span(
        self, sync: bool, spans: Spans, respx_mock: MockRouter
    ) -> None:
        tool_spans_at_the_end_of_each_reply: list[int] = []
        with spans.provider.get_tracer("app").start_as_current_span("app"):
            await run_with_a_browser_toolset(
                sync,
                respx_mock,
                member_calls(("toolu_1", "navigate", "browser"), ("toolu_2", "screenshot", "browser")),
                open_telemetry=spans.option(),
                mode={"stream": True, "run_tools_eagerly": True},
                at_the_end_of_each_reply=lambda: tool_spans_at_the_end_of_each_reply.append(len(tool_spans(spans))),
            )

        # Both members ran, each in its span, before the application had read the whole reply that called them, and
        # the results that the runner kept from those runs did not start more spans when it sent them.
        assert tool_spans_at_the_end_of_each_reply == [2, 2]
        # The runner ran the members, so their spans are children of its span, not of the span that the application
        # read the reply from.
        tool_runner_span = spans.one("anthropic.messages.tool_runner")
        assert [parent_id(tool) for tool in tool_spans(spans)] == [span_id(tool_runner_span)] * 2
        assert [attributes(tool)["gen_ai.tool.call.id"] for tool in tool_spans(spans)] == ["toolu_1", "toolu_2"]

    @RUNNER_MODES
    @pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
    @pytest.mark.respx(base_url=base_url)
    async def test_toolset_member_that_fails_has_a_tool_error_and_the_members_it_stops_have_no_span(
        self, sync: bool, mode: dict[str, Any], spans: Spans, respx_mock: MockRouter
    ) -> None:
        route = await run_with_a_browser_toolset(
            sync,
            respx_mock,
            member_calls(("toolu_1", "boom", "browser"), ("toolu_2", "navigate", "browser")),
            open_telemetry=spans.option(traces={"content_mode": "content"}),
            mode=mode,
        )

        [tool] = tool_spans(spans)
        assert tool.name == "anthropic.custom_tool_use boom"
        assert tool.status.status_code == StatusCode.ERROR
        assert attributes(tool)["error.type"] == "tool_error"
        assert attributes(tool)["gen_ai.tool.call.id"] == "toolu_1"
        assert json.loads(attributes(tool)["gen_ai.tool.call.arguments"]) == {"step": 0}
        # The content of the error result that the toolset made of the member's error.
        assert json.loads(attributes(tool)["anthropic.tool_result.content"]) == [
            {"type": "text", "text": "member refused"}
        ]
        assert spans.one("anthropic.messages.tool_runner").status.status_code == StatusCode.OK
        # The runner answered the later member without running it, so that call has no span.
        sent = json.loads(route.calls.last.request.content)["messages"][-1]["content"]
        assert [(block["tool_use_id"], block["is_error"]) for block in sent] == [("toolu_1", True), ("toolu_2", True)]
        assert sent[1]["content"] == "Not executed: an earlier action in this turn failed."

    @RUNNER_MODES
    @pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
    @pytest.mark.respx(base_url=base_url)
    async def test_toolset_call_that_no_toolset_of_the_runner_runs_has_no_span(
        self, sync: bool, mode: dict[str, Any], spans: Spans, respx_mock: MockRouter
    ) -> None:
        with pytest.warns(UserWarning, match="Toolset 'computer' .* not found in tool runner"):
            route = await run_with_a_browser_toolset(
                sync,
                respx_mock,
                # A member of a toolset that the runner doesn't have, and a call named like its toolset.
                member_calls(("toolu_1", "screenshot", "computer"), ("toolu_2", "browser", None)),
                open_telemetry=spans.option(),
                mode=mode,
            )

        assert tool_spans(spans) == []
        assert spans.one("anthropic.messages.tool_runner").status.status_code == StatusCode.OK
        sent = json.loads(route.calls.last.request.content)["messages"][-1]["content"]
        assert [(block["tool_use_id"], block["is_error"]) for block in sent] == [("toolu_1", True), ("toolu_2", True)]

    @TRACING_FAILURES
    @pytest.mark.parametrize("stream", [False, True], ids=["whole", "streamed"])
    @pytest.mark.parametrize("sync", [True, False], ids=["sync", "async"])
    @pytest.mark.respx(base_url=base_url)
    async def test_tracing_that_fails_leaves_the_tool_runner_as_it_is(
        self, sync: bool, stream: bool, failure: str, respx_mock: MockRouter
    ) -> None:
        replies = [tool_use_message(), FINAL]
        route = respx_mock.post("/v1/messages").mock(
            side_effect=[sse(reply) if stream else httpx2.Response(200, json=reply) for reply in replies]
        )
        options: dict[str, Any] = {"base_url": base_url, "api_key": "key", "open_telemetry": failing_tracing(failure)}

        if sync:
            message = run(Anthropic(**options), stream=stream).until_done()
        else:
            message = await async_run(AsyncAnthropic(**options), stream=stream).until_done()

        assert message.id == "msg_final"
        assert route.call_count == 2
        # The second request has the result of the tool, which ran.
        [tool_result] = json.loads(route.calls.last.request.content)["messages"][-1]["content"]
        assert tool_result["tool_use_id"] == "toolu_SF"
        assert json.loads(tool_result["content"]) == {"city": "SF", "weather": "sunny"}

    def test_no_spans_without_a_tracer(self, spans: Spans, respx_mock: MockRouter) -> None:
        respx_mock.post(f"{base_url}/v1/messages").mock(
            side_effect=[httpx2.Response(200, json=tool_use_message()), httpx2.Response(200, json=FINAL)]
        )
        client = Anthropic(base_url=base_url, api_key="key", open_telemetry=False)

        assert run(client).until_done().id == "msg_final"
        assert spans.finished == ()


def session_event(type: str, id: str, **fields: Any) -> dict[str, Any]:
    return {"type": type, "id": id, "processed_at": "2026-01-01T00:00:00Z", **fields}


PRIMARY_THREAD_RUNS: Final = [
    session_event("session.status_running", "sevt_1"),
    session_event("session.thread_status_running", "sevt_2", session_thread_id="sthr_primary", agent_name="assistant"),
    session_event("user.message", "sevt_3", content=[{"type": "text", "text": "Hello"}]),
]
TERMINATED: Final = session_event("session.status_terminated", "sevt_9")


async def echo(x: int = 0) -> str:
    """Gives `x` back."""
    return str(x)


def session_api(
    respx_mock: MockRouter,
    spans: Spans,
    *,
    history: list[dict[str, Any]] | None,
    live: list[dict[str, Any]],
    **options: Any,
) -> AsyncAnthropic:
    """A client for the session `sesn_1`, whose event history is `history` and whose event stream gives `live`.

    Reading the history fails when `history` is `None`.
    """
    body = b"".join(f"event: {event['type']}\ndata: {json.dumps(event)}\n\n".encode() for event in live)
    respx_mock.get("/v1/sessions/sesn_1/events/stream").mock(
        return_value=httpx2.Response(200, content=body, headers={"content-type": "text/event-stream"})
    )
    respx_mock.get("/v1/sessions/sesn_1/events").mock(
        return_value=httpx2.Response(400, json={"type": "error", "error": {"type": "invalid_request_error"}})
        if history is None
        else httpx2.Response(200, json={"data": history, "next_page": None})
    )
    respx_mock.post("/v1/sessions/sesn_1/events").mock(return_value=httpx2.Response(200, json={"data": []}))
    return AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option(**options))


class TestSessionToolRunnerSpans:
    async def test_tool_span(self, spans: Spans, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(session_runner_mod, "_scoped_client", lambda client, _key: client)  # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]

        async def echo(input: dict[str, Any]) -> str:
            return f"got {input.get('x')}"

        async def weather(_input: dict[str, Any]) -> str:
            return "sunny"

        member = _tool_use("sevt_1", "echo", {"x": 42})
        cast(Any, member).toolset_name = "computer"
        events = FakeAsyncEvents(
            stream_events=[
                member,
                _custom_tool_use("sevt_2", "get_weather", {}, session_thread_id="sthr_1"),
                _terminated(),
            ]
        )
        client = _FakeClient(events)
        cast(Any, client)._tracer = spans.provider.get_tracer("com.anthropic.sdk.python")
        cast(Any, client)._otel = OpenTelemetryConfig(
            resolve_open_telemetry({"traces": {"content_mode": "content"}, "conversation_id": "c"}),
            provider_name="anthropic",
        )

        tracer = spans.provider.get_tracer("app")
        with tracer.start_as_current_span("app") as app:
            runner = SessionToolRunner(
                cast(Any, client),
                "sesn_1",
                tools=cast(Any, [_FakeTool("echo", echo), _FakeTool("get_weather", weather)]),
                max_idle=None,
            )
            items = [item async for item in runner]

        assert len(items) == 2
        # An agent-toolset tool (`agent.tool_use`) runs in an anthropic.tool_use span, an
        # application-defined tool (`agent.custom_tool_use`) in an anthropic.custom_tool_use span.
        custom = spans.one("anthropic.custom_tool_use get_weather")
        assert custom.status.status_code == StatusCode.OK
        assert attributes(custom)["gen_ai.tool.call.id"] == "sevt_2"
        tool = spans.one("anthropic.tool_use echo")
        assert tool.kind == SpanKind.INTERNAL
        assert tool.status.status_code == StatusCode.OK
        assert parent_id(tool) == span_id(app)
        assert attributes(tool)["gen_ai.tool.call.id"] == "sevt_1"
        assert json.loads(attributes(tool)["gen_ai.tool.call.arguments"]) == {"x": 42}
        # The content of the `user.tool_result` event, and of the `user.custom_tool_result` event.
        assert json.loads(attributes(tool)["anthropic.tool_result.content"]) == [{"type": "text", "text": "got 42"}]
        assert json.loads(attributes(custom)["anthropic.tool_result.content"]) == [{"type": "text", "text": "sunny"}]
        # Both have the conversation ID that the application set, which comes before an event's thread, and the
        # runner's Session. Only the event of a thread other than the primary one names its thread.
        for span in (custom, tool):
            assert "gen_ai.tool.call.result" not in attributes(span)
            assert attributes(span)["gen_ai.conversation.id"] == "c"
            assert attributes(span)["anthropic.session.id"] == "sesn_1"
        assert attributes(custom)["anthropic.session.thread.id"] == "sthr_1"
        assert "anthropic.session.thread.id" not in attributes(tool)
        # Only the event that has a `toolset_name` gives its span one.
        assert attributes(tool)["anthropic.toolset.name"] == "computer"
        assert "anthropic.toolset.name" not in attributes(custom)
        # Neither stand-in tool has a description.
        assert "gen_ai.tool.description" not in attributes(custom)
        assert "gen_ai.tool.description" not in attributes(tool)
        assert spans.named("anthropic.messages.tool_runner") == []
        assert events.stream_headers == [None]

    @TRACING_FAILURES
    async def test_tracing_that_fails_leaves_the_runner_as_it_is(
        self, failure: str, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(session_runner_mod, "_scoped_client", lambda client, _key: client)  # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]

        async def echo(input: dict[str, Any]) -> str:
            return f"got {input.get('x')}"

        events = FakeAsyncEvents(stream_events=[_tool_use("sevt_1", "echo", {"x": 42}), _terminated()])
        client = _FakeClient(events)
        provider = failing_tracing(failure).get("tracer_provider")
        assert provider is not None
        cast(Any, client)._tracer = provider.get_tracer("com.anthropic.sdk.python")
        cast(Any, client)._otel = OpenTelemetryConfig(
            resolve_open_telemetry({"traces": {"content_mode": "content"}}), provider_name="anthropic"
        )

        runner = SessionToolRunner(
            cast(Any, client), "sesn_1", tools=cast(Any, [_FakeTool("echo", echo)]), max_idle=None
        )
        [item] = [item async for item in runner]

        assert item.is_error is False
        [sent] = events.send_calls
        assert sent["events"][0]["content"] == [{"type": "text", "text": "got 42"}]

    async def test_block_sent_as_its_json_is_recorded_by_its_type(
        self, spans: Spans, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(session_runner_mod, "_scoped_client", lambda client, _key: client)  # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]

        browser_state = {
            "type": "browser_state",
            "screenshot": {"type": "base64", "media_type": "image/png", "data": "aGVsbG8="},
            "encrypted_content": "encrypted_0",
        }
        tool_reference = {"type": "tool_reference", "tool_name": "get_weather"}

        async def browse(_input: dict[str, Any]) -> list[dict[str, Any]]:
            return [{"type": "text", "text": "Opened the page."}, browser_state, tool_reference]

        events = FakeAsyncEvents(stream_events=[_custom_tool_use("sevt_1", "browse", {}), _terminated()])
        client = _FakeClient(events)
        cast(Any, client)._tracer = spans.provider.get_tracer("com.anthropic.sdk.python")
        cast(Any, client)._otel = OpenTelemetryConfig(
            resolve_open_telemetry({"traces": {"content_mode": "content"}}), provider_name="anthropic"
        )

        runner = SessionToolRunner(
            cast(Any, client), "sesn_1", tools=cast(Any, [_FakeTool("browse", browse)]), max_idle=None
        )
        (item,) = [item async for item in runner]

        # The result event cannot hold these blocks, so it has each as the text of its JSON.
        result = {
            "type": "user.custom_tool_result",
            "custom_tool_use_id": "sevt_1",
            "is_error": False,
            "content": [
                {"type": "text", "text": "Opened the page."},
                {"type": "text", "text": json.dumps(browser_state)},
                {"type": "text", "text": json.dumps(tool_reference)},
            ],
        }
        assert [call["events"] for call in events.send_calls] == [[result]]
        assert item.result == result
        # A span keeps a text block whole, so it has these blocks by their own types, not as their JSON.
        content = attributes(spans.one("anthropic.custom_tool_use browse"))["anthropic.tool_result.content"]
        assert json.loads(content) == [
            {"type": "text", "text": "Opened the page."},
            {"type": "browser_state"},
            {"type": "tool_reference"},
        ]
        assert "aGVsbG8=" not in content
        assert "encrypted_0" not in content

    async def test_conversation_id_is_the_events_thread_when_the_application_set_none(
        self, spans: Spans, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(session_runner_mod, "_scoped_client", lambda client, _key: client)  # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]

        async def echo(_input: dict[str, Any]) -> str:
            return "ok"

        events = FakeAsyncEvents(
            stream_events=[
                _tool_use("sevt_1", "echo", {}),
                _custom_tool_use("sevt_2", "get_weather", {}, session_thread_id="sthr_1"),
                _terminated(),
            ]
        )
        client = _FakeClient(events)
        cast(Any, client)._tracer = spans.provider.get_tracer("com.anthropic.sdk.python")
        cast(Any, client)._otel = OpenTelemetryConfig(
            resolve_open_telemetry({"traces": {"content_mode": "metadata_only"}}), provider_name="anthropic"
        )

        runner = SessionToolRunner(
            cast(Any, client),
            "sesn_1",
            tools=cast(Any, [_FakeTool("echo", echo), _FakeTool("get_weather", echo)]),
            max_idle=None,
        )
        assert len([item async for item in runner]) == 2

        # The platform's spans have the thread ID as their conversation ID.
        in_thread = spans.one("anthropic.custom_tool_use get_weather")
        assert attributes(in_thread)["gen_ai.conversation.id"] == "sthr_1"
        assert attributes(in_thread)["anthropic.session.thread.id"] == "sthr_1"
        # An event of the primary thread names no thread, and the Session's ID is no conversation ID.
        primary = spans.one("anthropic.tool_use echo")
        assert "gen_ai.conversation.id" not in attributes(primary)
        assert attributes(primary)["anthropic.session.id"] == "sesn_1"

    @pytest.mark.respx(base_url=base_url)
    async def test_request_that_sends_a_tools_result_has_the_tools_conversation_id(
        self, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(session_runner_mod, "_scoped_client", lambda client, _key: client)  # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
        respx_mock.post("/v1/sessions/sesn_1/events").mock(return_value=httpx2.Response(200, json={"data": []}))

        async def echo(_input: dict[str, Any]) -> str:
            return "ok"

        async def sends(**options: Any) -> list[ReadableSpan]:
            """The spans of the requests that send the result of a tool call of the primary thread, and then of
            one of the thread `sthr_1`. The client sends them; the events that the runner reads are stand-ins.
            """
            events = FakeAsyncEvents(
                stream_events=[
                    _tool_use("sevt_1", "echo", {}),
                    _custom_tool_use("sevt_2", "get_weather", {}, session_thread_id="sthr_1"),
                    _terminated(),
                ]
            )
            client = AsyncAnthropic(base_url=base_url, api_key="key", open_telemetry=spans.option(**options))
            monkeypatch.setattr(client.beta.sessions.events, "stream", events.stream)
            monkeypatch.setattr(client.beta.sessions.events, "list", events.list)
            spans.exporter.clear()
            runner = SessionToolRunner(
                client,
                "sesn_1",
                tools=cast(Any, [_FakeTool("echo", echo), _FakeTool("get_weather", echo)]),
                max_idle=None,
            )
            assert [item.posted async for item in runner] == [True, True]
            return spans.named("anthropic.sessions.events.send")

        # The application set no conversation ID: the request has the thread ID, as the tool's span has. An
        # event of the primary thread names no thread.
        primary, in_thread = await sends()
        assert "gen_ai.conversation.id" not in attributes(primary)
        assert attributes(in_thread)["gen_ai.conversation.id"] == "sthr_1"
        assert attributes(spans.one("anthropic.custom_tool_use get_weather"))["gen_ai.conversation.id"] == "sthr_1"

        # The conversation ID that the application set comes before an event's thread.
        for send in await sends(conversation_id="c"):
            assert attributes(send)["gen_ai.conversation.id"] == "c"

    @pytest.mark.respx(base_url=base_url)
    @pytest.mark.parametrize("status_events_in", ["history", "live_stream"])
    async def test_primary_threads_tool_has_the_thread_id_that_the_sessions_log_gives(
        self, spans: Spans, respx_mock: MockRouter, status_events_in: str
    ) -> None:
        # What the platform writes when a session first runs, before the first tool call of its primary thread.
        log = [*PRIMARY_THREAD_RUNS, session_event("agent.custom_tool_use", "sevt_4", name="echo", input={"x": 1})]
        history = log if status_events_in == "history" else []
        live = [TERMINATED] if status_events_in == "history" else [*log, TERMINATED]
        client = session_api(respx_mock, spans, history=history, live=live)

        runner = client.beta.sessions.events.tool_runner("sesn_1", tools=[beta_async_tool(echo)], max_idle=None)
        assert [item.posted async for item in runner] == [True]

        tool = spans.one("anthropic.custom_tool_use echo")
        assert attributes(tool)["gen_ai.conversation.id"] == "sthr_primary"
        assert attributes(spans.one("anthropic.sessions.events.send"))["gen_ai.conversation.id"] == "sthr_primary"
        # The event names no thread, so neither does its span.
        assert "anthropic.session.thread.id" not in attributes(tool)
        assert attributes(tool)["anthropic.session.id"] == "sesn_1"
        # Learning the thread costs no request: the runner reads the stream and the history, and sends the result.
        requests: list[httpx2.Request] = [call.request for call in cast(Any, respx_mock.calls)]
        assert [(request.method, request.url.path, request.url.query) for request in requests] == [
            ("GET", "/v1/sessions/sesn_1/events/stream", b""),
            ("GET", "/v1/sessions/sesn_1/events", b"limit=1000"),
            ("POST", "/v1/sessions/sesn_1/events", b""),
        ]

    @pytest.mark.respx(base_url=base_url)
    async def test_later_thread_events_do_not_replace_the_primary_thread(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        child = {"session_thread_id": "sthr_child", "agent_name": "researcher"}
        history = [
            *PRIMARY_THREAD_RUNS,
            session_event("session.thread_created", "sevt_4", **child),
            session_event("session.thread_status_running", "sevt_5", **child),
            session_event("agent.custom_tool_use", "sevt_6", name="echo", input={}, session_thread_id="sthr_child"),
        ]
        live = [
            session_event("session.thread_status_idle", "sevt_7", stop_reason={"type": "end_turn"}, **child),
            session_event("agent.custom_tool_use", "sevt_8", name="echo", input={}),
            TERMINATED,
        ]
        client = session_api(respx_mock, spans, history=history, live=live)

        runner = client.beta.sessions.events.tool_runner("sesn_1", tools=[beta_async_tool(echo)], max_idle=None)
        assert [item.tool_use_id async for item in runner] == ["sevt_6", "sevt_8"]

        in_child, in_primary = spans.named("anthropic.custom_tool_use echo")
        assert attributes(in_child)["gen_ai.conversation.id"] == "sthr_child"
        assert attributes(in_child)["anthropic.session.thread.id"] == "sthr_child"
        assert attributes(in_primary)["gen_ai.conversation.id"] == "sthr_primary"
        assert "anthropic.session.thread.id" not in attributes(in_primary)
        sends = spans.named("anthropic.sessions.events.send")
        assert [attributes(send)["gen_ai.conversation.id"] for send in sends] == ["sthr_child", "sthr_primary"]

    @pytest.mark.respx(base_url=base_url)
    async def test_request_that_sends_a_tools_result_has_the_environment_keys_credentials_alone(
        self, spans: Spans, respx_mock: MockRouter, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        # A custom header goes before a client's own credentials, and each new client reads these again.
        monkeypatch.setenv("ANTHROPIC_CUSTOM_HEADERS", "Authorization: Bearer env-secret\nX-Api-Key: env-api-key")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "env-account-key")
        history = [
            *PRIMARY_THREAD_RUNS,
            session_event("agent.custom_tool_use", "sevt_4", name="echo", input={}),
            session_event("agent.custom_tool_use", "sevt_5", name="echo", input={}, session_thread_id="sthr_child"),
        ]
        client = session_api(respx_mock, spans, history=history, live=[TERMINATED])

        runner = client.beta.sessions.events.tool_runner(
            "sesn_1", tools=[beta_async_tool(echo)], environment_key="env_key", max_idle=None
        )
        assert [item.posted async for item in runner] == [True, True]

        sends = spans.named("anthropic.sessions.events.send")
        assert [attributes(send)["gen_ai.conversation.id"] for send in sends] == ["sthr_primary", "sthr_child"]
        requests: list[httpx2.Request] = [call.request for call in cast(Any, respx_mock.calls)]
        assert [request.method for request in requests] == ["GET", "GET", "POST", "POST"]
        for request in requests:
            assert request.headers["authorization"] == "Bearer env_key"
            assert "x-api-key" not in request.headers

    @pytest.mark.parametrize("environment_key", [None, "env_key"], ids=["clients_credentials", "environment_key"])
    @pytest.mark.respx(base_url=base_url)
    async def test_client_that_sends_a_threads_results_has_the_clients_other_options(
        self, environment_key: str | None, spans: Spans, respx_mock: MockRouter
    ) -> None:
        history = [
            *PRIMARY_THREAD_RUNS,
            session_event("agent.custom_tool_use", "sevt_4", name="echo", input={}, session_thread_id="sthr_child"),
        ]
        traces: OpenTelemetryTraces = {"content_mode": "content", "max_content_bytes": 4096}
        client = session_api(respx_mock, spans, history=history, live=[TERMINATED], traces=traces)

        runner = client.beta.sessions.events.tool_runner(
            "sesn_1", tools=[beta_async_tool(echo)], environment_key=environment_key, max_idle=None
        )
        assert [item.posted async for item in runner] == [True]

        # The copy is given a whole option, which replaces the client's: the client's own with the thread's ID.
        sender: AsyncAnthropic = cast(Any, runner)._events_by_conversation["sthr_child"]._client
        assert sender is not client
        assert sender.open_telemetry == {**client.open_telemetry, "conversation_id": "sthr_child"}
        assert sender.open_telemetry.get("traces") == {"enabled": True, **traces}
        # Its span goes to the client's tracer provider.
        send = spans.one("anthropic.sessions.events.send")
        assert attributes(send)["gen_ai.conversation.id"] == "sthr_child"

    @pytest.mark.respx(base_url=base_url)
    async def test_applications_conversation_id_comes_before_the_primary_thread(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        history = [*PRIMARY_THREAD_RUNS, session_event("agent.custom_tool_use", "sevt_4", name="echo", input={})]
        client = session_api(respx_mock, spans, history=history, live=[TERMINATED], conversation_id="c")

        runner = client.beta.sessions.events.tool_runner("sesn_1", tools=[beta_async_tool(echo)], max_idle=None)
        assert [item.posted async for item in runner] == [True]

        assert attributes(spans.one("anthropic.custom_tool_use echo"))["gen_ai.conversation.id"] == "c"
        assert attributes(spans.one("anthropic.sessions.events.send"))["gen_ai.conversation.id"] == "c"

    @pytest.mark.respx(base_url=base_url)
    async def test_live_stream_alone_does_not_tell_the_primary_thread(
        self, spans: Spans, respx_mock: MockRouter
    ) -> None:
        # Without the history, the first thread event that the stream gives may be that of another thread.
        live = [
            session_event("session.thread_status_running", "sevt_5", session_thread_id="sthr_child", agent_name="a"),
            session_event("agent.custom_tool_use", "sevt_6", name="echo", input={}),
            TERMINATED,
        ]
        client = session_api(respx_mock, spans, history=None, live=live)

        runner = client.beta.sessions.events.tool_runner("sesn_1", tools=[beta_async_tool(echo)], max_idle=None)
        assert [item.posted async for item in runner] == [True]

        assert "gen_ai.conversation.id" not in attributes(spans.one("anthropic.custom_tool_use echo"))
        assert "gen_ai.conversation.id" not in attributes(spans.one("anthropic.sessions.events.send"))

    async def test_tool_description(self, spans: Spans, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(session_runner_mod, "_scoped_client", lambda client, _key: client)  # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]

        events = FakeAsyncEvents(
            stream_events=[
                _tool_use("sevt_1", "read", {"city": "SF"}),
                _custom_tool_use("sevt_2", "get_weather", {"city": "SF"}),
                _terminated(),
            ]
        )
        client = _FakeClient(events)
        cast(Any, client)._tracer = spans.provider.get_tracer("com.anthropic.sdk.python")
        cast(Any, client)._otel = OpenTelemetryConfig(
            resolve_open_telemetry({"traces": {"content_mode": "metadata_only"}}), provider_name="anthropic"
        )

        runner = SessionToolRunner(
            cast(Any, client),
            "sesn_1",
            tools=[
                beta_async_tool(async_get_weather, name="read", description="Reads the weather."),
                beta_async_tool(async_get_weather, name="get_weather"),
            ],
            max_idle=None,
        )
        assert len([item async for item in runner]) == 2

        # The description is metadata, so both spans have it without content mode.
        agent_tool = spans.one("anthropic.tool_use read")
        assert attributes(agent_tool)["gen_ai.tool.description"] == "Reads the weather."
        assert "gen_ai.tool.call.arguments" not in attributes(agent_tool)
        custom = spans.one("anthropic.custom_tool_use get_weather")
        assert attributes(custom)["gen_ai.tool.description"] == "The weather in a city."
        # The application set no conversation ID on this runner.
        assert "gen_ai.conversation.id" not in attributes(custom)
        assert attributes(custom)["anthropic.session.id"] == "sesn_1"


@pytest.mark.skipif(PYDANTIC_V1, reason="reads the fields of pydantic v2 models")
@pytest.mark.parametrize(
    "events", [BetaManagedAgentsSessionEvent, BetaManagedAgentsStreamSessionEvents], ids=["listed", "streamed"]
)
def test_thread_status_event_types_all_tell_the_primary_thread(events: Any) -> None:
    # A tripwire: it compares a hand-written list with the generated type, and asserts no behavior.
    tell_the_primary_thread = {
        "session.thread_status_running",
        "session.thread_status_idle",
        "session.thread_status_rescheduled",
        "session.thread_status_terminated",
    }

    assert {name for name in type_names(events) if name.startswith("session.thread_status_")} == (
        tell_the_primary_thread
    ), (
        "A Session's event log can have a new type of `session.thread_status_*` event. "
        "`SessionToolRunner._note_primary_thread` (src/anthropic/lib/tools/_beta_session_runner.py) takes the "
        "session's primary thread from the first such event of the log, and passes over a type that it does not "
        "know. Name the new type there. Then list it in this test."
    )
