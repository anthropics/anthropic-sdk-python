from __future__ import annotations

import os
from typing import Any, cast
from urllib.parse import unquote
from collections.abc import Callable, Iterator
from typing_extensions import override

import httpx2
import pytest
from opentelemetry import trace, propagate
from opentelemetry.trace import Span, Tracer, TraceFlags, SpanContext, TracerProvider, NonRecordingSpan
from opentelemetry.propagators.textmap import TextMapPropagator

from anthropic import Anthropic, AsyncAnthropic
from anthropic._types import OpenTelemetryClientOption, ResolvedOpenTelemetryOptions
from anthropic._tracing import global_tracer_provider_loads
from anthropic._base_client import make_request_options

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
api_key = "my-anthropic-api-key"

Client = Anthropic | AsyncAnthropic

ENV = "ANTHROPIC_OPEN_TELEMETRY"
PROPAGATION_ENV = f"{ENV}_PROPAGATION"
TRACEPARENT = "00-00000000000000000000000000000001-0000000000000001-01"


class RecordingSpan(NonRecordingSpan):
    """A span with a valid context, which records unless a sampler dropped it."""

    def __init__(self, attributes: Any, *, sampled: bool) -> None:
        flags = TraceFlags(TraceFlags.SAMPLED if sampled else TraceFlags.DEFAULT)
        super().__init__(SpanContext(trace_id=1, span_id=1, is_remote=False, trace_flags=flags))
        self.attributes: dict[str, Any] = dict(attributes or {})
        self.sampled = sampled
        self.ended = False

    @override
    def is_recording(self) -> bool:
        return self.sampled and not self.ended

    @override
    def set_attribute(self, key: str, value: Any) -> None:
        self.attributes[key] = value

    @override
    def end(self, end_time: int | None = None) -> None:
        self.ended = True


class RecordingTracer(Tracer):
    def __init__(self, provider: RecordingProvider) -> None:
        self.provider = provider

    @override
    def start_span(self, name: str, *args: Any, **kwargs: Any) -> Span:
        span = RecordingSpan(kwargs.get("attributes"), sampled=self.provider.sampled)
        self.provider.spans.append(span)
        return span

    @override
    def start_as_current_span(self, name: str, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("A client starts its spans with `start_span`")


class RecordingProvider(TracerProvider):
    def __init__(self, *, sampled: bool = True) -> None:
        self.spans: list[RecordingSpan] = []
        self.sampled = sampled
        self.tracers = 0

    @override
    def get_tracer(self, *args: Any, **kwargs: Any) -> Tracer:
        self.tracers += 1
        return RecordingTracer(self)


class CountingPropagator(TextMapPropagator):
    def __init__(self) -> None:
        self.injected = 0

    @override
    def extract(self, carrier: Any, context: Any = None, getter: Any = None) -> Any:
        return context

    @override
    def inject(self, carrier: Any, context: Any = None, setter: Any = None) -> None:
        self.injected += 1
        carrier["traceparent"] = TRACEPARENT

    @property
    @override
    def fields(self) -> set[str]:
        return {"traceparent"}


class Server:
    """Answers a call, after one retry if `retried`.

    Records each request, and the context of the span that was current while the HTTP client sent it.
    """

    def __init__(self, *, retried: bool = False) -> None:
        self.retried = retried
        self.requests: list[httpx2.Request] = []
        self.current_spans: list[SpanContext] = []

    def __call__(self, request: httpx2.Request) -> httpx2.Response:
        self.requests.append(request)
        self.current_spans.append(trace.get_current_span().get_span_context())
        if self.retried and len(self.requests) == 1:
            return httpx2.Response(500, headers={"retry-after-ms": "1"}, json={})
        return httpx2.Response(200, json={})

    @property
    def traceparents(self) -> list[str | None]:
        return [request.headers.get("traceparent") for request in self.requests]


NewClient = Callable[..., Client]


@pytest.fixture(params=[Anthropic, AsyncAnthropic], ids=["sync", "async"])
def new_client(request: pytest.FixtureRequest) -> NewClient:
    """Constructs a client, which reads the environment. One that is given a `server` sends its requests there."""

    def new(server: Server | None = None, open_telemetry: OpenTelemetryClientOption = None) -> Client:
        http_client: Any = None
        if server is not None:
            http_client_class = httpx2.Client if request.param is Anthropic else httpx2.AsyncClient
            http_client = http_client_class(transport=httpx2.MockTransport(server))
        return cast(
            Client,
            request.param(
                base_url=base_url,
                api_key=api_key,
                _strict_response_validation=True,
                http_client=http_client,
                open_telemetry=open_telemetry,
                max_retries=1,
            ),
        )

    return new


async def call(client: Client, **options: Any) -> None:
    """Makes a request the way an SDK method does, which names its span."""
    request_options = make_request_options(span_name="test", **options)
    if isinstance(client, Anthropic):
        client.get("/foo", cast_to=httpx2.Response, options=request_options)
    else:
        await client.get("/foo", cast_to=httpx2.Response, options=request_options)


@pytest.fixture
def propagator() -> Iterator[CountingPropagator]:
    registered = propagate.get_global_textmap()
    propagator = CountingPropagator()
    propagate.set_global_textmap(propagator)
    yield propagator
    propagate.set_global_textmap(registered)


@pytest.mark.parametrize(
    ("content_mode", "endpoint_content_params", "query", "recorded"),
    [
        pytest.param("content", (), {"email": "a@example.com"}, "email=a@example.com", id="content"),
        pytest.param("metadata_only", (), {"email": "a@example.com"}, None, id="metadata_only"),
        pytest.param("content", ("filter",), {"filter": "open"}, "filter=open", id="content-on-the-endpoint"),
        pytest.param("metadata_only", ("filter",), {"filter": "open"}, None, id="metadata_only-on-the-endpoint"),
        pytest.param("metadata_only", (), {"filter": "open"}, "filter=open", id="metadata_only-on-another-endpoint"),
    ],
)
async def test_content_mode_decides_whether_a_content_query_is_recorded(
    new_client: NewClient,
    monkeypatch: pytest.MonkeyPatch,
    content_mode: str,
    endpoint_content_params: tuple[str, ...],
    query: dict[str, str],
    recorded: str | None,
) -> None:
    # The package's own parameters that are content wherever they are a parameter depend on its config.
    monkeypatch.setattr("anthropic._tracing.CONTENT_QUERY_PARAMS", frozenset({"email"}))
    provider = RecordingProvider()
    client = new_client(
        Server(), open_telemetry={"tracer_provider": provider, "traces": {"content_mode": content_mode}}
    )

    await call(client, query=query, span_content_query_params=endpoint_content_params)

    (span,) = provider.spans
    assert span.ended
    url_query = span.attributes.get("url.query")
    assert (None if url_query is None else unquote(url_query)) == recorded


async def test_each_request_carries_the_trace_context(new_client: NewClient, propagator: CountingPropagator) -> None:
    server = Server(retried=True)
    client = new_client(server, open_telemetry={"tracer_provider": RecordingProvider()})

    await call(client)

    assert client.open_telemetry["propagation"] is True
    assert server.traceparents == [TRACEPARENT, TRACEPARENT]
    assert propagator.injected > 0


async def test_propagation_off_changes_only_the_headers(new_client: NewClient, propagator: CountingPropagator) -> None:
    server = Server(retried=True)
    provider = RecordingProvider()
    client = new_client(server, open_telemetry={"tracer_provider": provider, "propagation": False})

    await call(client, extra_headers={"traceparent": "own"})

    assert client.open_telemetry["propagation"] is False
    assert server.traceparents == ["own", "own"]
    assert propagator.injected == 0
    (span,) = provider.spans
    assert span.ended


async def test_propagation_off_keeps_a_dropped_span_current(
    new_client: NewClient, propagator: CountingPropagator
) -> None:
    """A span that a sampler dropped stays the parent of the spans of an instrumented HTTP client."""
    server = Server(retried=True)
    provider = RecordingProvider(sampled=False)
    client = new_client(server, open_telemetry={"tracer_provider": provider, "propagation": False})

    await call(client)

    assert server.traceparents == [None, None]
    assert propagator.injected == 0
    (span,) = provider.spans
    context = span.get_span_context()
    assert context.is_valid and not context.trace_flags.sampled
    assert server.current_spans == [context, context]


async def test_propagation_off_drops_a_span_without_a_valid_context(
    new_client: NewClient, propagator: CountingPropagator
) -> None:
    """Such a span is only there to be propagated."""
    server = Server(retried=True)
    client = new_client(server, open_telemetry={"propagation": False})

    await call(client)

    assert server.traceparents == [None, None]
    assert propagator.injected == 0
    assert [context.is_valid for context in server.current_spans] == [False, False]


@pytest.mark.parametrize(
    ("env", "option", "propagation"),
    [
        pytest.param("FALSE", None, False, id="false-in-any-case"),
        pytest.param("0", None, True, id="only-false"),
        pytest.param("false", {"propagation": True}, True, id="option-over-env"),
        pytest.param("false", {}, True, id="empty-option-over-env"),
    ],
)
async def test_propagation_env(
    new_client: NewClient,
    propagator: CountingPropagator,
    monkeypatch: pytest.MonkeyPatch,
    env: str,
    option: OpenTelemetryClientOption,
    propagation: bool,
) -> None:
    monkeypatch.setenv(PROPAGATION_ENV, env)
    server = Server(retried=True)
    client = new_client(server, open_telemetry=option)

    await call(client)

    assert client.open_telemetry["propagation"] is propagation
    assert server.traceparents == ([TRACEPARENT, TRACEPARENT] if propagation else [None, None])
    assert (propagator.injected > 0) is propagation


def test_copy_keeps_propagation(new_client: NewClient) -> None:
    client = new_client(open_telemetry={"propagation": False})

    assert client.with_options(max_retries=0).open_telemetry["propagation"] is False


DEFAULTS: ResolvedOpenTelemetryOptions = {
    "propagation": True,
    "traces": {"enabled": True, "content_mode": "metadata_only", "max_content_bytes": 750_000},
}
OFF: ResolvedOpenTelemetryOptions = {**DEFAULTS, "traces": {**DEFAULTS["traces"], "enabled": False}}
FROM_ENV: ResolvedOpenTelemetryOptions = {
    "propagation": False,
    "traces": {"enabled": False, "content_mode": "content", "max_content_bytes": 300},
}


@pytest.fixture
def every_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Sets every variable to something other than the default."""
    monkeypatch.setenv(ENV, "false")
    monkeypatch.setenv(PROPAGATION_ENV, "false")
    monkeypatch.setenv(f"{ENV}_TRACES_CONTENT_MODE", "content")
    monkeypatch.setenv(f"{ENV}_TRACES_MAX_CONTENT_BYTES", "300")


@pytest.mark.usefixtures("every_env")
def test_client_without_an_option_reads_every_env(new_client: NewClient) -> None:
    client = new_client()

    assert client.open_telemetry == FROM_ENV
    assert client.with_options(max_retries=0).open_telemetry == FROM_ENV
    assert client.with_options(open_telemetry=None).open_telemetry == FROM_ENV
    assert client.copy().open_telemetry == FROM_ENV


@pytest.mark.usefixtures("every_env")
@pytest.mark.parametrize(
    ("option", "resolved"),
    [
        pytest.param({}, DEFAULTS, id="empty"),
        pytest.param(False, OFF, id="false"),
        pytest.param({"traces": True}, DEFAULTS, id="traces-true"),
        pytest.param({"traces": {"content_mode": "metadata_only"}}, DEFAULTS, id="one-field"),
    ],
)
def test_client_with_an_option_reads_no_env(
    new_client: NewClient, option: OpenTelemetryClientOption, resolved: ResolvedOpenTelemetryOptions
) -> None:
    assert new_client(open_telemetry=option).open_telemetry == resolved
    assert new_client().with_options(open_telemetry=option).open_telemetry == resolved


@pytest.fixture
def tracer_provider_that_is_not_installed(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """A job can inherit an `OTEL_PYTHON_TRACER_PROVIDER` that names a provider its environment lacks.

    OpenTelemetry then raises each time it is asked for the global provider.
    """
    monkeypatch.setenv("OTEL_PYTHON_TRACER_PROVIDER", "tracer_provider_that_is_not_installed")
    try:
        trace.get_tracer_provider()
    except Exception:
        pass
    else:
        pytest.fail("A tracer provider is registered, so OpenTelemetry does not load the one that the variable names")
    # The package asks for the global provider once per process.
    forget = cast(Any, global_tracer_provider_loads).cache_clear
    forget()
    yield
    forget()


@pytest.mark.usefixtures("tracer_provider_that_is_not_installed")
async def test_tracer_provider_that_is_not_installed_leaves_a_client_without_spans(new_client: NewClient) -> None:
    server = Server()
    client = new_client(server)

    for called in (client, client.with_options(max_retries=0), client.copy()):
        assert called.open_telemetry["traces"]["enabled"] is True
        await call(called)

    assert server.traceparents == [None, None, None]


@pytest.mark.usefixtures("tracer_provider_that_is_not_installed")
async def test_given_tracer_provider_is_asked_at_the_first_call(new_client: NewClient) -> None:
    """Whatever the registered provider does."""
    provider = RecordingProvider()
    client = new_client(Server()).with_options(open_telemetry={"tracer_provider": provider})
    assert provider.tracers == 0

    await call(client)

    assert provider.tracers == 1
