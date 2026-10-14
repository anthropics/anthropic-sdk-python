"""OpenTelemetry tracing of the client's API calls.

An "API call" is one invocation of an SDK method, with every retry and the reading of the stream it
returns. Each has one `CLIENT` span, the "call span". An "attempt" is one HTTP request within it. The
SDK emits no span per attempt, and sends the call span's trace context with each unless `propagation` is off.
"""

from __future__ import annotations

import os
import logging
from typing import cast
from datetime import timedelta
from dataclasses import dataclass
from urllib.parse import unquote
from collections.abc import Mapping, Callable, Iterator, Collection, AsyncIterator, AsyncGenerator
from typing_extensions import Literal, Protocol, override

import httpx2
from opentelemetry import trace
from opentelemetry.trace import Span, Status, Tracer, SpanKind, StatusCode
from opentelemetry.context import Context
from opentelemetry.util.types import AttributeValue

from ._types import (
    OpenTelemetryTraces,
    OpenTelemetryOptions,
    OpenTelemetryClientOption,
    ResolvedOpenTelemetryOptions,
)
from ._utils import lru_cache
from ._models import FinalRequestOptions
from ._streaming import Stream, AsyncStream
from ._exceptions import APIStatusError, APITimeoutError, APIConnectionError, APIResponseValidationError

log: logging.Logger = logging.getLogger(__name__)

INSTRUMENTATION_SCOPE = "com.anthropic.sdk.python"

# Copied from `opentelemetry.semconv`, which is not a dependency of this SDK.
ERROR_TYPE = "error.type"
HTTP_REQUEST_METHOD = "http.request.method"
HTTP_REQUEST_RESEND_COUNT = "http.request.resend_count"
HTTP_RESPONSE_STATUS_CODE = "http.response.status_code"
HTTP_ROUTE = "http.route"
SERVER_ADDRESS = "server.address"
SERVER_PORT = "server.port"
URL_FULL = "url.full"
URL_PATH = "url.path"
URL_QUERY = "url.query"
URL_SCHEME = "url.scheme"

CONVERSATION_ID = "gen_ai.conversation.id"
SESSION_THREAD_ID = "anthropic.session.thread.id"

DEFAULT_MAX_CONTENT_BYTES = 750_000
"""The default `traces.max_content_bytes`."""


def resolve_open_telemetry(option: OpenTelemetryClientOption) -> ResolvedOpenTelemetryOptions:
    """`option` with `propagation` and every field of its `traces`.

    The environment variables are for a client that is given no option, `None`: `env_open_telemetry` makes its option
    from them. An option that is given is complete, even `{}`: `propagation`, or a field of `traces`, that it leaves out
    has the default, whatever the environment says.

    `False` is short for `{"traces": False}`. A client resolves the option that it is given once, when it is
    constructed, and a copy of it that is given no other option has the resolved one. So a later change to the
    environment does not reach a client that exists, nor those copies.

    A `max_content_bytes` below 1 is not valid: in `option` it is the default, and in the environment it is ignored.
    """
    options: OpenTelemetryOptions
    if option is None:
        options = env_open_telemetry()
    elif option is False:
        options = {"traces": False}
    else:
        options = option
    traces = traces_of(options)

    enabled = traces.get("enabled")
    max_content_bytes = traces.get("max_content_bytes")
    propagation = options.get("propagation")

    resolved: ResolvedOpenTelemetryOptions = {
        "propagation": True if propagation is None else propagation,
        "traces": {
            "enabled": True if enabled is None else enabled,
            "content_mode": traces.get("content_mode") or "metadata_only",
            "max_content_bytes": (
                DEFAULT_MAX_CONTENT_BYTES if max_content_bytes is None or max_content_bytes < 1 else max_content_bytes
            ),
        },
    }
    if (tracer_provider := options.get("tracer_provider")) is not None:
        resolved["tracer_provider"] = tracer_provider
    if (conversation_id := options.get("conversation_id")) is not None:
        resolved["conversation_id"] = conversation_id
    return resolved


def env_open_telemetry() -> OpenTelemetryOptions:
    """The option that the environment variables make, for a client that is given no `open_telemetry` option.

    It has only what a variable changes from the default. Nothing else reads these variables.
    """
    traces: OpenTelemetryTraces = {}
    if os.environ.get("ANTHROPIC_OPEN_TELEMETRY", "").lower() == "false":
        traces["enabled"] = False
    if os.environ.get("ANTHROPIC_OPEN_TELEMETRY_TRACES_CONTENT_MODE", "").lower() == "content":
        traces["content_mode"] = "content"
    if (max_content_bytes := env_max_content_bytes()) is not None:
        traces["max_content_bytes"] = max_content_bytes

    options: OpenTelemetryOptions = {"traces": traces}
    if os.environ.get("ANTHROPIC_OPEN_TELEMETRY_PROPAGATION", "").lower() == "false":
        options["propagation"] = False
    return options


def env_max_content_bytes() -> int | None:
    """The `max_content_bytes` that the environment sets, or `None` when its value is not valid.

    A valid value is ASCII decimal digits, with or without whitespace around them, that make a number of at least 1.
    """
    value = os.environ.get("ANTHROPIC_OPEN_TELEMETRY_TRACES_MAX_CONTENT_BYTES", "").strip()
    if not (value.isascii() and value.isdigit()):
        return None
    try:
        number = int(value)
    except ValueError:
        # `int` refuses a number of thousands of digits.
        return None
    return number if number >= 1 else None


def traces_of(options: OpenTelemetryOptions) -> OpenTelemetryTraces:
    """A copy of the `traces` of `options` as a dict. `True` and `False` are short for `enabled`."""
    traces = options.get("traces")
    if isinstance(traces, bool):
        return {"enabled": traces}
    # The resolved type is `OpenTelemetryTraces` with every field required, which no `TypedDict` can derive.
    return {**cast(OpenTelemetryTraces, traces or {})}


def get_tracer(
    options: ResolvedOpenTelemetryOptions, version: str, *, scope: str = INSTRUMENTATION_SCOPE
) -> Tracer | None:
    """The tracer for a client with the resolved `options`, or `None` when the client has no spans.

    A client has none when its spans are disabled, which calls nothing of OpenTelemetry, and when OpenTelemetry
    cannot give a tracer, as when `OTEL_PYTHON_TRACER_PROVIDER` names a provider that is not installed. Never raises.
    """
    if not options["traces"]["enabled"]:
        return None
    tracer_provider = options.get("tracer_provider")
    if tracer_provider is None and not global_tracer_provider_loads():
        return None
    try:
        return trace.get_tracer(scope, version, tracer_provider=tracer_provider)
    except Exception:
        log.debug("Could not get an OpenTelemetry tracer, so the client has no spans", exc_info=True)
        return None


@lru_cache(maxsize=None)
def global_tracer_provider_loads() -> bool:
    """Whether OpenTelemetry can give its global tracer provider, which a client without a `tracer_provider` uses.

    Asked once: OpenTelemetry loads the provider that the environment names again, and logs the failure again,
    each time that it is asked after a failure.
    """
    try:
        trace.get_tracer_provider()
    except Exception:
        log.debug(
            "Could not load the global OpenTelemetry tracer provider, so clients without a `tracer_provider` have no spans",
            exc_info=True,
        )
        return False
    return True


@dataclass(frozen=True)
class ApiCallResult:
    """The result of an API call, as far as the call got."""

    options: FinalRequestOptions

    start_time: int
    """When the call started, in nanoseconds since the epoch. A span cannot report its own start time."""

    response: httpx2.Response | None = None

    data: object = None
    """What the call returns to the application: the parsed body, a stream, or the raw response."""

    error: BaseException | None = None

    cast_to: object = None

    resend_count: int = 0
    """How many times the SDK sent the call's request again, as a retry or a fallback."""

    @property
    def final_attempt(self) -> httpx2.Response | None:
        """The response of the call's final attempt, which the error of a failed call carries."""
        if self.response is None and isinstance(self.error, (APIStatusError, APIResponseValidationError)):
            return self.error.response
        return self.response


@dataclass
class ApiCall:
    """An API call that has a call span, while the call runs."""

    span: Span

    start_time: int
    """When the call started, in nanoseconds since the epoch."""

    records_content: bool = False
    """Whether the call's span may have content, as the client's content mode says."""

    propagation: bool = True
    """Whether the call's requests carry the trace context of its span, as the client's `propagation` says."""

    requests_sent: int = 0
    """How many requests the SDK has sent for the call: the first, and each retry and fallback."""

    def sending(self, request: httpx2.Request, options: FinalRequestOptions) -> None:
        """Counts `request`, which the SDK is about to send, and records the URL of the call's first request."""
        self.requests_sent += 1
        if self.requests_sent != 1:
            return
        try:
            set_url_attributes(
                self.span,
                request.url,
                options.span_query_params,
                options.span_content_query_params,
                content=self.records_content,
            )
        except Exception:
            log.debug("Could not record the URL of an API call on its span", exc_info=True)

    def result(
        self,
        options: FinalRequestOptions,
        *,
        response: httpx2.Response | None = None,
        data: object = None,
        error: BaseException | None = None,
        cast_to: object = None,
    ) -> ApiCallResult:
        """The result of the call, as far as the call has got."""
        return ApiCallResult(
            options,
            self.start_time,
            response=response,
            data=data,
            error=error,
            cast_to=cast_to,
            resend_count=max(self.requests_sent - 1, 0),
        )


def start_api_call_span(
    tracer: Tracer,
    base_url: httpx2.URL,
    options: FinalRequestOptions,
    attributes: Mapping[str, AttributeValue],
    *,
    propagation: bool = True,
) -> Span | None:
    """Starts the call span of the API call that the prepared `options` describe.

    Returns `None` for a request that no SDK method made, which has no span name, and for a span
    that neither records nor propagates a trace context. Without `propagation`, a valid span context
    counts as propagated: instrumentation of the HTTP client makes its spans children of the call span.
    Never raises: a span that cannot start is `None` too, and the call goes on without one.
    """
    if not options.span_name:
        return None
    try:
        method_attributes = options.span_attributes or {}
        if callable(method_attributes):
            method_attributes = method_attributes(options.json_data)
        span = tracer.start_span(
            options.span_name,
            kind=SpanKind.CLIENT,
            attributes={
                **server_attributes(base_url),
                **request_attributes(options),
                # Before `attributes`, whose conversation ID is the one that the application set.
                **conversation_attributes(method_attributes),
                **attributes,
                **method_attributes,
            },
        )
        if not span.is_recording() and not (trace_headers(span) if propagation else span.get_span_context().is_valid):
            return None
        return span
    except Exception:
        log.debug("Could not start the span of an API call", exc_info=True)
        return None


def inject_trace_headers(span: Span, headers: httpx2.Headers) -> None:
    """Writes the trace context of `span` into `headers`, in place of any already there."""
    for key, value in trace_headers(span).items():
        headers[key] = value


def remove_trace_headers(span: Span, headers: httpx2.Headers) -> None:
    """Removes what `inject_trace_headers` sets, so that no signature covers a value that is replaced later."""
    for key in trace_headers(span):
        if key in headers:
            del headers[key]


def end_api_call_span(span: Span, result: ApiCallResult) -> None:
    """Ends the call span with the call's `result`. A span that already ended is left alone."""
    if not span.is_recording():
        return
    set_response_status_code(span, result)
    set_resend_count(span, result)
    if result.error is not None:
        set_error_status(span, result.error)
    else:
        span.set_status(Status(StatusCode.OK))
    span.end()


def end_api_call_span_when_body_ends(
    span: Span, response: httpx2.Response, result: ApiCallResult, observer: StreamObserver | None = None
) -> None:
    """Ends the call span when the application has read, closed or dropped the body of `response`.

    A body that was read before the call returned ends the span now, unless the call returns a stream,
    which has yet to give the application the events in that body.

    `observer` ends the span of a body that has an end event. Without one, a `StreamedBodyObserver` does.
    """
    if not span.is_recording():
        return
    if response.is_closed and not isinstance(result.data, (Stream, AsyncStream)):
        end_api_call_span(span, result)
        return
    set_response_status_code(span, result)
    set_resend_count(span, result)
    response.stream = span_ending_stream(response.stream, FirstEnd(observer or StreamedBodyObserver(span)))


StreamEnd = Literal["read", "closed", "failed"]
"""How the reading of a body ended. `closed` includes an application that stopped reading."""


class StreamObserver(Protocol):
    """Learns how the application reads the body of a response. No method raises."""

    def begin(self) -> None:
        """Called when a `Stream` or an `AsyncStream` starts to parse the body.

        Never called when the application reads the bytes itself.
        """
        ...

    def item(self, item: object, /) -> None: ...

    def end(self, how: StreamEnd, error: BaseException | None = None) -> None: ...


class StreamedBodyObserver:
    """Ends the call span of a body that has no end event."""

    def __init__(self, span: Span) -> None:
        self._span = span
        self._events = False

    def begin(self) -> None:
        self._events = True

    def item(self, item: object) -> None:
        pass

    def end(self, how: StreamEnd, error: BaseException | None = None) -> None:
        if error is not None:
            set_error_status(self._span, error)
        # Server-sent events without an end event are never read to the end, so only other bodies get `OK`.
        elif how == "read" and not self._events:
            self._span.set_status(Status(StatusCode.OK))
        self._span.end()


class FirstEnd:
    """Forwards every call to `inner` up to and including the first `end`, and drops the rest.

    Reading a body ends more than once: the stream and the body both report it, `httpx2` closes a body
    that it has read to the end, and a read can end or fail after another thread or task closed the body.
    """

    def __init__(self, observer: StreamObserver) -> None:
        self.inner = observer
        self._ended = False

    def begin(self) -> None:
        if not self._ended:
            self.inner.begin()

    def item(self, item: object) -> None:
        if not self._ended:
            self.inner.item(item)

    def end(self, how: StreamEnd, error: BaseException | None = None) -> None:
        if self._ended:
            return
        self._ended = True
        try:
            self.inner.end(how, error)
        except Exception:
            log.debug("Could not end the span of a response body", exc_info=True)


class SpanEndingStream(httpx2.SyncByteStream):
    """Wraps the body of a response, and reports to `stream_observer` how reading it ended.

    A `Stream` finds `stream_observer` here, on the body of its response.
    """

    def __init__(self, body: httpx2.SyncByteStream, observer: StreamObserver) -> None:
        self._body = body
        self.stream_observer = observer

    @property
    def elapsed(self) -> timedelta | None:
        """The `elapsed` of the wrapped body. `httpx2.Response.elapsed` reads it from `response.stream`."""
        return getattr(self._body, "elapsed", None)

    @override
    def __iter__(self) -> Iterator[bytes]:
        try:
            yield from self._body
            self.stream_observer.end("read")
        except Exception as err:
            self.stream_observer.end("failed", err)
            raise

    @override
    def close(self) -> None:
        self.stream_observer.end("closed")
        self._body.close()

    def __del__(self) -> None:
        # The application may drop the response without closing it, and without reading any of the body.
        self.stream_observer.end("closed")


class AsyncSpanEndingStream(httpx2.AsyncByteStream):
    """Wraps the body of a response, and reports to `stream_observer` how reading it ended.

    An `AsyncStream` finds `stream_observer` here, on the body of its response.
    """

    def __init__(self, body: httpx2.AsyncByteStream, observer: StreamObserver) -> None:
        self._async_body = body
        self.stream_observer = observer

    @property
    def elapsed(self) -> timedelta | None:
        """The `elapsed` of the wrapped body. `httpx2.Response.elapsed` reads it from `response.stream`."""
        return getattr(self._async_body, "elapsed", None)

    @override
    async def __aiter__(self) -> AsyncIterator[bytes]:
        chunks = self._async_body.__aiter__()
        try:
            async for chunk in chunks:
                yield chunk
            self.stream_observer.end("read")
        except Exception as err:
            self.stream_observer.end("failed", err)
            raise
        finally:
            # Closes the generator of a body that was read in part, in the task that read it. Otherwise the event
            # loop closes it later, in a task of its own.
            if isinstance(chunks, AsyncGenerator):
                await chunks.aclose()

    @override
    async def aclose(self) -> None:
        self.stream_observer.end("closed")
        await self._async_body.aclose()

    def __del__(self) -> None:
        # The application may drop the response without closing it, and without reading any of the body.
        self.stream_observer.end("closed")


class SpanEndingByteStream(SpanEndingStream, AsyncSpanEndingStream):
    """Wraps a body that is a sync and an async one at once, as `httpx2.ByteStream` is.

    `body` and `async_body` are the same object, typed as each kind.
    """

    def __init__(
        self, body: httpx2.SyncByteStream, async_body: httpx2.AsyncByteStream, observer: StreamObserver
    ) -> None:
        SpanEndingStream.__init__(self, body, observer)
        AsyncSpanEndingStream.__init__(self, async_body, observer)


def span_ending_stream(
    body: httpx2.SyncByteStream | httpx2.AsyncByteStream, observer: StreamObserver
) -> httpx2.SyncByteStream | httpx2.AsyncByteStream:
    """The wrapper of the same kind as `body`, so that the checks of `httpx2.Response` on the kind still hold."""
    if not isinstance(body, httpx2.SyncByteStream):
        return AsyncSpanEndingStream(body, observer)
    if isinstance(body, httpx2.AsyncByteStream):
        return SpanEndingByteStream(body, body, observer)
    return SpanEndingStream(body, observer)


def set_response_status_code(span: Span, result: ApiCallResult) -> None:
    response = result.final_attempt
    if response is not None:
        span.set_attribute(HTTP_RESPONSE_STATUS_CODE, response.status_code)


def set_resend_count(span: Span, result: ApiCallResult) -> None:
    if result.resend_count:
        span.set_attribute(HTTP_REQUEST_RESEND_COUNT, result.resend_count)


def set_url_attributes(
    span: Span, url: httpx2.URL, query_params: Collection[str], content_query_params: Collection[str], *, content: bool
) -> None:
    """Sets the `url.*` attributes for a request to `url`. Of its query, they have only the `query_params`.

    A query that is content, and the full URL that has it, need `content`. One is content when it has one of the
    `CONTENT_QUERY_PARAMS` or of the `content_query_params`, which are content on the request's endpoint only.
    """
    path = url.raw_path.partition(b"?")[0].decode("ascii")
    query = defined_query(url.query.decode("ascii"), query_params)
    span.set_attribute(URL_SCHEME, url.scheme)
    span.set_attribute(URL_PATH, path)
    if is_content_query(query, content_query_params) and not content:
        return
    if query:
        span.set_attribute(URL_QUERY, query)
    # `netloc` has the port only when the URL names one that is not the scheme's default.
    full = f"{url.scheme}://{url.netloc.decode('ascii')}{path}"
    span.set_attribute(URL_FULL, f"{full}?{query}" if query else full)


def defined_query(query: str, names: Collection[str]) -> str:
    """The pairs of `query`, as sent, whose parameter is one of `names`, which an endpoint defines.

    A name is one of them when, percent-decoded, it is in `names` as it is, as `created_at[gte]` is for some
    endpoints, or when it ends in `[]`, as an array is sent, and the name before that is in `names`.
    """
    kept: list[str] = []
    for pair in query.split("&"):
        name = unquote(pair.partition("=")[0])
        if name in names or name.removesuffix("[]") in names:
            kept.append(pair)
    return "&".join(kept)


CONTENT_QUERY_PARAMS = frozenset({"email", "path_prefix", "expected_content_sha256"})
"""The query parameters whose value is content: it filters like a search, or it comes from stored content."""


def is_content_query(query: str, content_names: Collection[str]) -> bool:
    """Whether `query`, as `defined_query` gives it, has one of the `CONTENT_QUERY_PARAMS` or of `content_names`.

    `content_names` has the parameters that are content on the request's endpoint only. A name is one of them
    by the rule of `defined_query`.
    """
    content_names = CONTENT_QUERY_PARAMS.union(content_names)
    names = (unquote(pair.partition("=")[0]) for pair in query.split("&"))
    return any(name in content_names or name.removesuffix("[]") in content_names for name in names)


def set_error_status(span: Span, error: BaseException, type: str | None = None) -> None:
    """Sets the `ERROR` status and `error.type`.

    Anything but an `Exception`, such as a `CancelledError`, is the application stopping the operation,
    which leaves the status unset.
    """
    if not isinstance(error, Exception):
        return
    span.set_status(Status(StatusCode.ERROR))
    span.set_attribute(ERROR_TYPE, type or error_type(error))


def error_type(error: BaseException) -> str:
    """The `error.type` of a failed operation: the type of the API's error envelope, or else the status code."""
    if isinstance(error, (APITimeoutError, httpx2.TimeoutException)):
        return "client_timeout_error"
    if isinstance(error, (APIConnectionError, httpx2.TransportError)):
        return "connection_error"
    if isinstance(error, APIStatusError):
        if error.type:
            return str(error.type)
        # An `error` event has the status of the response that opened its stream, which is no error.
        if error.status_code >= 400:
            return str(error.status_code)
    return "client_error"


def request_attributes(options: FinalRequestOptions) -> dict[str, AttributeValue]:
    """What every request of the call has in common. The call span starts with these, so that a sampler sees them."""
    attributes: dict[str, AttributeValue] = {HTTP_REQUEST_METHOD: options.method.upper()}
    if options.span_route is not None:
        attributes[HTTP_ROUTE] = options.span_route
    return attributes


def conversation_attributes(method_attributes: Mapping[str, AttributeValue]) -> dict[str, AttributeValue]:
    """The ID of the Session thread in the call's path as the conversation's ID: a Session thread is a conversation."""
    thread_id = method_attributes.get(SESSION_THREAD_ID)
    return {} if thread_id is None else {CONVERSATION_ID: thread_id}


def server_attributes(base_url: httpx2.URL) -> dict[str, AttributeValue]:
    return {SERVER_ADDRESS: base_url.host, SERVER_PORT: base_url.port or (80 if base_url.scheme == "http" else 443)}


def trace_headers(span: Span) -> dict[str, str]:
    """The headers that carry `span`'s trace context, from the propagator the application registered.

    Empty when the propagator cannot be loaded or fails. Never raises.
    """
    inject = trace_context_injector()
    if inject is None:
        return {}
    carrier: dict[str, str] = {}
    try:
        inject(carrier, trace.set_span_in_context(span))
    except Exception:
        log.debug("Could not write the trace context of a span into headers", exc_info=True)
        return {}
    return carrier


@lru_cache(maxsize=None)
def trace_context_injector() -> Callable[[dict[str, str], Context], None] | None:
    """`opentelemetry.propagate.inject`, or `None` when the propagators that the environment names cannot be loaded."""
    try:
        # Imported on first use: the module loads the propagators that `OTEL_PROPAGATORS` names when it is
        # imported, and raises for one that is not installed, which must not fail `import anthropic`.
        from opentelemetry.propagate import inject
    except Exception as err:
        log.warning("Could not load the OpenTelemetry propagators, so requests carry no trace context: %s", err)
        return None
    return inject
