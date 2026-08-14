from __future__ import annotations

import os
import re
import json
from typing import Any, Protocol, cast
from pathlib import Path
from unittest import mock
from typing_extensions import override

import httpx
import pytest
from respx import MockRouter

from anthropic import (
    Stream,
    CallNext,
    Anthropic,
    APIRequest,
    Middleware,
    APIResponse,
    AsyncCallNext,
    AsyncAnthropic,
    RetryableError,
    AnthropicVertex,
    BadRequestError,
    AnthropicBedrock,
    AsyncAPIResponse,
    APIConnectionError,
    AsyncAnthropicVertex,
    AsyncAnthropicBedrock,
    AnthropicBedrockMantle,
    AsyncAnthropicBedrockMantle,
)
from anthropic._models import FinalRequestOptions
from anthropic.lib.aws import AnthropicAWS, AsyncAnthropicAWS
from anthropic._response import BinaryAPIResponse, AsyncBinaryAPIResponse, StreamedBinaryAPIResponse
from anthropic.lib.foundry import AnthropicFoundry, AsyncAnthropicFoundry
from anthropic.types.message import Message
from anthropic._legacy_response import LegacyAPIResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")
api_key = "my-anthropic-api-key"


class MockRequestCall(Protocol):
    request: httpx.Request


def _low_retry_timeout(*_args: Any, **_kwargs: Any) -> float:
    return 0.1


def make_sync_client(**kwargs: Any) -> Anthropic:
    return Anthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True, **kwargs)


def make_async_client(**kwargs: Any) -> AsyncAnthropic:
    return AsyncAnthropic(base_url=base_url, api_key=api_key, _strict_response_validation=True, **kwargs)


def message_body(*, model: str = "claude-opus-4-6") -> dict[str, Any]:
    return {
        "id": "msg_013Zva2CMHLNnXjNJJKqJ2EF",
        "type": "message",
        "role": "assistant",
        "model": model,
        "content": [{"type": "text", "text": "Hello!"}],
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "usage": {"input_tokens": 10, "output_tokens": 5},
    }


def error_body(*, type: str, message: str) -> dict[str, Any]:
    return {"type": "error", "error": {"type": type, "message": message}}


def request_body(call: MockRequestCall) -> dict[str, Any]:
    return cast("dict[str, Any]", json.loads(call.request.content))


def middleware_request_body(request: APIRequest) -> dict[str, Any]:
    body = request.json
    assert isinstance(body, dict)
    return cast("dict[str, Any]", body)


class RecordingMiddleware(Middleware):
    def __init__(self, name: str = "middleware", events: "list[str] | None" = None) -> None:
        self.name = name
        self.events = events if events is not None else []
        self.requests: list[APIRequest] = []
        self.results: list[Any] = []

    @override
    def handle(self, request: APIRequest, call_next: CallNext) -> Any:
        self.requests.append(request)
        self.events.append(f"{self.name}:enter")
        result = call_next(request)
        self.events.append(f"{self.name}:exit")
        self.results.append(result)
        return result

    @override
    async def handle_async(self, request: APIRequest, call_next: AsyncCallNext) -> Any:
        self.requests.append(request)
        self.events.append(f"{self.name}:enter")
        result = await call_next(request)
        self.events.append(f"{self.name}:exit")
        self.results.append(result)
        return result


class MutateBody(Middleware):
    def __init__(self, **changes: object) -> None:
        self.changes = changes

    def _mutate(self, request: APIRequest) -> APIRequest:
        body = request.json
        assert isinstance(body, dict)
        return request.copy(body={**cast("dict[str, object]", body), **self.changes})

    @override
    def handle(self, request: APIRequest, call_next: CallNext) -> Any:
        return call_next(self._mutate(request))

    @override
    async def handle_async(self, request: APIRequest, call_next: AsyncCallNext) -> Any:
        return await call_next(self._mutate(request))


class ModelFallback(Middleware):
    def __init__(self, fallback_model: str) -> None:
        self.fallback_model = fallback_model

    def _fallback(self, request: APIRequest) -> APIRequest:
        body = request.json
        assert isinstance(body, dict)
        return request.copy(body={**cast("dict[str, object]", body), "model": self.fallback_model})

    @override
    def handle(self, request: APIRequest, call_next: CallNext) -> Any:
        response = call_next(request)
        if response.status_code == 529:
            return call_next(self._fallback(request))
        return response

    @override
    async def handle_async(self, request: APIRequest, call_next: AsyncCallNext) -> Any:
        response = await call_next(request)
        if response.status_code == 529:
            return await call_next(self._fallback(request))
        return response


class ShrinkMaxTokensOnTooLarge(Middleware):
    def __init__(self, max_tokens: int) -> None:
        self.max_tokens = max_tokens

    def _shrink(self, request: APIRequest) -> APIRequest:
        body = request.json
        assert isinstance(body, dict)
        return request.copy(body={**cast("dict[str, object]", body), "max_tokens": self.max_tokens})

    @override
    def handle(self, request: APIRequest, call_next: CallNext) -> Any:
        response = call_next(request)
        if response.status_code == 413:
            return call_next(self._shrink(request))
        return response

    @override
    async def handle_async(self, request: APIRequest, call_next: AsyncCallNext) -> Any:
        response = await call_next(request)
        if response.status_code == 413:
            return await call_next(self._shrink(request))
        return response


class ShortCircuit(Middleware):
    def __init__(self, message: Message) -> None:
        self.message = message
        self.requests: list[APIRequest] = []

    @override
    def handle(self, request: APIRequest, call_next: CallNext) -> Any:  # noqa: ARG002
        self.requests.append(request)
        return self.message

    @override
    async def handle_async(self, request: APIRequest, call_next: AsyncCallNext) -> Any:  # noqa: ARG002
        self.requests.append(request)
        return self.message


class AttemptRecorder(Middleware):
    """Records the `retries_taken` and response status of every attempt the chain runs for."""

    def __init__(self) -> None:
        self.attempts: list[int] = []
        self.statuses: list[int] = []
        self.errors: list[Exception] = []

    @override
    def handle(self, request: APIRequest, call_next: CallNext) -> Any:
        self.attempts.append(request.retries_taken)
        try:
            response = call_next(request)
        except Exception as err:
            self.errors.append(err)
            raise
        self.statuses.append(response.status_code)
        return response

    @override
    async def handle_async(self, request: APIRequest, call_next: AsyncCallNext) -> Any:
        self.attempts.append(request.retries_taken)
        try:
            response = await call_next(request)
        except Exception as err:
            self.errors.append(err)
            raise
        self.statuses.append(response.status_code)
        return response


class Boom(Exception):
    pass


class Exploding(Middleware):
    @override
    def handle(self, request: APIRequest, call_next: CallNext) -> Any:  # noqa: ARG002
        raise Boom("middleware failure")

    @override
    async def handle_async(self, request: APIRequest, call_next: AsyncCallNext) -> Any:  # noqa: ARG002
        raise Boom("middleware failure")


class SyncOnlyMiddleware(Middleware):
    @override
    def handle(self, request: APIRequest, call_next: CallNext) -> Any:
        return call_next(request)


class AsyncOnlyMiddleware(Middleware):
    @override
    async def handle_async(self, request: APIRequest, call_next: AsyncCallNext) -> Any:
        return await call_next(request)


class InspectResponse(Middleware):
    """Records the response wrapper returned by `call_next` and passes it through."""

    def __init__(self) -> None:
        self.responses: list[Any] = []

    @override
    def handle(self, request: APIRequest, call_next: CallNext) -> Any:
        response = call_next(request)
        self.responses.append(response)
        return response

    @override
    async def handle_async(self, request: APIRequest, call_next: AsyncCallNext) -> Any:
        response = await call_next(request)
        self.responses.append(response)
        return response


class ParseInMiddleware(Middleware):
    """Parses the response inside the middleware before returning it."""

    def __init__(self) -> None:
        self.parsed: list[Any] = []

    @override
    def handle(self, request: APIRequest, call_next: CallNext) -> Any:
        response = call_next(request)
        self.parsed.append(response.parse())
        return response

    @override
    async def handle_async(self, request: APIRequest, call_next: AsyncCallNext) -> Any:
        response = await call_next(request)
        self.parsed.append(await response.parse())
        return response


class AsyncCallableMiddleware:
    """A middleware object that is a class instance with an async `__call__` method."""

    def __init__(self) -> None:
        self.requests: list[APIRequest] = []

    async def __call__(self, request: APIRequest, call_next: AsyncCallNext) -> Any:
        self.requests.append(request)
        return await call_next(request)


class SyncCallableMiddleware:
    """A middleware object that is a class instance with a sync `__call__` method."""

    def __init__(self) -> None:
        self.requests: list[APIRequest] = []

    def __call__(self, request: APIRequest, call_next: CallNext) -> Any:
        self.requests.append(request)
        return call_next(request)


class AsyncHandleMiddleware(Middleware):
    """Invalid middleware: defines the sync `handle()` hook as an async function."""

    @override
    async def handle(self, request: APIRequest, call_next: CallNext) -> Any:  # type: ignore[override]  # pyright: ignore[reportIncompatibleMethodOverride]
        return call_next(request)


class SyncHandleAsyncMiddleware(Middleware):
    """Invalid middleware: defines the async `handle_async()` hook as a plain function."""

    @override
    def handle_async(self, request: APIRequest, call_next: AsyncCallNext) -> Any:
        return call_next(request)


class RetryOnInternalServerError(Middleware):
    """Fallback middleware that retries the same request once on a 5xx error.

    Records the request headers observed before each `call_next(...)` invocation so
    that tests can assert that both invocations saw identical request state.
    """

    def __init__(self) -> None:
        self.headers_seen: list[dict[str, Any]] = []
        self.results: list[Any] = []

    @override
    def handle(self, request: APIRequest, call_next: CallNext) -> Any:
        self.headers_seen.append(dict(request.headers))
        result = call_next(request)
        if result.status_code >= 500:
            self.headers_seen.append(dict(request.headers))
            result = call_next(request)
        self.results.append(result)
        return result

    @override
    async def handle_async(self, request: APIRequest, call_next: AsyncCallNext) -> Any:
        self.headers_seen.append(dict(request.headers))
        result = await call_next(request)
        if result.status_code >= 500:
            self.headers_seen.append(dict(request.headers))
            result = await call_next(request)
        self.results.append(result)
        return result


def short_circuit_message(*, model: str = "claude-opus-4-6") -> Message:
    return Message.construct(**message_body(model=model))


def file_metadata_body() -> dict[str, Any]:
    return {
        "id": "file_123",
        "created_at": "2024-01-01T00:00:00Z",
        "filename": "upload.txt",
        "mime_type": "text/plain",
        "size_bytes": 13,
        "type": "file",
    }


class TestAPIRequest:
    def test_properties(self) -> None:
        options = FinalRequestOptions.construct(
            method="post",
            url="/v1/messages",
            json_data={"model": "claude-opus-4-6", "max_tokens": 16},
            headers={"x-foo": "bar"},
            params={"beta": "true"},
            max_retries=3,
            timeout=10.0,
        )
        request = APIRequest(options=options, cast_to=Message, stream=False, stream_cls=None)

        assert request.method == "post"
        assert request.url == "/v1/messages"
        assert request.json == {"model": "claude-opus-4-6", "max_tokens": 16}
        assert request.headers == {"x-foo": "bar"}
        assert request.query_params == {"beta": "true"}
        assert request.timeout == 10.0
        assert request.max_retries == 3
        assert request.cast_to is Message
        assert request.stream is False
        assert request.stream_cls is None
        assert request.options is options

    def test_headers_default_to_empty_mapping(self) -> None:
        options = FinalRequestOptions(method="get", url="/v1/models")
        request = APIRequest(options=options, cast_to=Message)
        assert request.headers == {}

    def test_copy_returns_new_instance_with_changes(self) -> None:
        options = FinalRequestOptions.construct(
            method="post",
            url="/v1/messages",
            json_data={"model": "claude-opus-4-6", "max_tokens": 16},
            max_retries=3,
        )
        request = APIRequest(options=options, cast_to=Message)

        copied = request.copy(body={"model": "claude-sonnet-4-5"}, headers={"x-trace-id": "123"})

        assert copied is not request
        assert copied.options is not request.options
        assert copied.json == {"model": "claude-sonnet-4-5"}
        assert copied.headers == {"x-trace-id": "123"}
        assert copied.method == "post"
        assert copied.url == "/v1/messages"
        assert copied.cast_to is Message
        assert copied.stream is False

        # the original request is untouched
        assert request.json == {"model": "claude-opus-4-6", "max_tokens": 16}
        assert request.headers == {}

    def test_retries_taken_defaults_to_zero_and_copy_preserves_it(self) -> None:
        options = FinalRequestOptions.construct(method="post", url="/v1/messages")
        request = APIRequest(options=options, cast_to=Message)
        assert request.retries_taken == 0

        attempt = APIRequest(options=options, cast_to=Message, retries_taken=2)
        assert attempt.copy(headers={"x-trace-id": "123"}).retries_taken == 2

    def test_copy_deep_copies_body(self) -> None:
        body: dict[str, Any] = {"model": "claude-opus-4-6", "messages": [{"role": "user", "content": "hi"}]}
        options = FinalRequestOptions.construct(method="post", url="/v1/messages", json_data=body)
        request = APIRequest(options=options, cast_to=Message)

        copied = request.copy()
        copied_body = copied.json
        assert isinstance(copied_body, dict)
        cast("dict[str, Any]", copied_body)["messages"][0]["content"] = "changed"

        assert request.json == {"model": "claude-opus-4-6", "messages": [{"role": "user", "content": "hi"}]}

    def test_copy_does_not_deep_copy_file_objects(self, tmp_path: Path) -> None:
        # file/IO objects cannot be deep-copied; `copy()` must carry them over by reference
        path = tmp_path / "upload.txt"
        path.write_bytes(b"file contents")

        with path.open("rb") as reader:
            options = FinalRequestOptions.construct(
                method="post",
                url="/v1/files?beta=true",
                json_data={"purpose": "test"},
                files=[("file", reader)],
            )
            request = APIRequest(options=options, cast_to=Message)

            copied = request.copy(headers={"x-trace-id": "123"})

            files = cast("list[tuple[str, Any]]", copied.options.files)
            assert files is not None
            assert files[0][1] is reader

            # mutating the copy must never affect the original request
            copied_body = copied.json
            assert isinstance(copied_body, dict)
            cast("dict[str, Any]", copied_body)["purpose"] = "changed"
            assert request.json == {"purpose": "test"}
            assert request.headers == {}

    def test_copy_header_mutations_do_not_affect_original(self) -> None:
        options = FinalRequestOptions.construct(
            method="post",
            url="/v1/messages",
            headers={"x-foo": "bar"},
            json_data={"model": "claude-opus-4-6"},
        )
        request = APIRequest(options=options, cast_to=Message)

        copied = request.copy()
        copied_headers = copied.options.headers
        assert isinstance(copied_headers, dict)
        cast("dict[str, str]", copied_headers)["x-added"] = "value"
        cast("dict[str, str]", copied_headers)["x-foo"] = "changed"

        assert request.headers == {"x-foo": "bar"}


class TestDefaultMiddleware:
    def test_handle_is_passthrough(self) -> None:
        sentinel = object()
        request = APIRequest(options=FinalRequestOptions(method="post", url="/v1/messages"), cast_to=Message)
        seen: list[APIRequest] = []

        def handler(req: APIRequest) -> Any:
            seen.append(req)
            return sentinel

        assert Middleware().handle(request, handler) is sentinel
        assert seen == [request]

    async def test_handle_async_is_passthrough(self) -> None:
        sentinel = object()
        request = APIRequest(options=FinalRequestOptions(method="post", url="/v1/messages"), cast_to=Message)
        seen: list[APIRequest] = []

        async def handler(req: APIRequest) -> Any:
            seen.append(req)
            return sentinel

        assert await Middleware().handle_async(request, handler) is sentinel
        assert seen == [request]


class TestMiddlewareValidation:
    def test_sync_client_rejects_async_callable_object(self) -> None:
        with pytest.raises(TypeError, match="is an async function"):
            make_sync_client(middleware=[AsyncCallableMiddleware()])

    def test_async_client_accepts_async_callable_object(self) -> None:
        middleware = AsyncCallableMiddleware()
        client = make_async_client(middleware=[middleware])
        assert client._middleware == (middleware,)

    @pytest.mark.respx(base_url=base_url)
    async def test_async_callable_object_handles_requests(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        middleware = AsyncCallableMiddleware()
        client = make_async_client(middleware=[middleware])

        message = await client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert isinstance(message, Message)
        assert len(middleware.requests) == 1

    def test_async_client_rejects_sync_callable_object(self) -> None:
        with pytest.raises(TypeError, match="is not an async function"):
            make_async_client(middleware=[SyncCallableMiddleware()])

    def test_sync_client_accepts_sync_callable_object(self) -> None:
        middleware = SyncCallableMiddleware()
        client = make_sync_client(middleware=[middleware])
        assert client._middleware == (middleware,)

    @pytest.mark.respx(base_url=base_url)
    def test_sync_callable_object_handles_requests(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        middleware = SyncCallableMiddleware()
        client = make_sync_client(middleware=[middleware])

        message = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert isinstance(message, Message)
        assert len(middleware.requests) == 1

    def test_sync_client_rejects_non_callable(self) -> None:
        with pytest.raises(TypeError, match="is not callable"):
            make_sync_client(middleware=[cast(Any, object())])

    def test_async_client_rejects_non_callable(self) -> None:
        with pytest.raises(TypeError, match="is not callable"):
            make_async_client(middleware=[cast(Any, object())])

    def test_sync_client_rejects_async_handle_override(self) -> None:
        with pytest.raises(TypeError, match=r"defines `handle\(\)` as an async function"):
            make_sync_client(middleware=[AsyncHandleMiddleware()])

    def test_async_client_rejects_sync_handle_async_override(self) -> None:
        with pytest.raises(TypeError, match=r"defines `handle_async\(\)` as a sync function"):
            make_async_client(middleware=[SyncHandleAsyncMiddleware()])


class TestSyncMiddleware:
    @pytest.mark.respx(base_url=base_url)
    def test_middleware_sees_request_and_returns_response(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        recorder = RecordingMiddleware()
        client = make_sync_client(middleware=[recorder])

        message = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert isinstance(message, Message)
        assert message.id == "msg_013Zva2CMHLNnXjNJJKqJ2EF"

        assert len(recorder.requests) == 1
        request = recorder.requests[0]
        assert request.method == "post"
        assert request.url == "/v1/messages"
        assert request.cast_to is Message
        assert request.stream is False
        body = middleware_request_body(request)
        assert body["model"] == "claude-opus-4-6"
        assert body["max_tokens"] == 1024

        # the middleware itself saw the `APIResponse` wrapper; the value the caller
        # receives is parsed from that same response
        assert len(recorder.results) == 1
        response = recorder.results[0]
        assert isinstance(response, APIResponse)
        assert response.parse() is message

    @pytest.mark.respx(base_url=base_url)
    def test_middleware_ordering(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        events: list[str] = []
        outer = RecordingMiddleware("outer", events)
        inner = RecordingMiddleware("inner", events)
        client = make_sync_client(middleware=[outer, inner])

        client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert events == ["outer:enter", "inner:enter", "inner:exit", "outer:exit"]

    @pytest.mark.respx(base_url=base_url)
    def test_request_mutation_changes_outgoing_request(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        client = make_sync_client(middleware=[MutateBody(model="claude-sonnet-4-5", max_tokens=4096)])

        message = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )
        assert isinstance(message, Message)

        calls = cast("list[MockRequestCall]", respx_mock.calls)
        assert len(calls) == 1
        sent = request_body(calls[0])
        assert sent["model"] == "claude-sonnet-4-5"
        assert sent["max_tokens"] == 4096
        assert sent["messages"] == [{"role": "user", "content": "Hello"}]

    @pytest.mark.respx(base_url=base_url)
    def test_fallback_on_overloaded_error(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                httpx.Response(529, json=error_body(type="overloaded_error", message="Overloaded")),
                httpx.Response(200, json=message_body(model="claude-sonnet-4-5")),
            ]
        )

        client = make_sync_client(middleware=[ModelFallback("claude-sonnet-4-5")], max_retries=0)

        message = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert isinstance(message, Message)
        assert message.model == "claude-sonnet-4-5"

        calls = cast("list[MockRequestCall]", respx_mock.calls)
        assert len(calls) == 2
        assert request_body(calls[0])["model"] == "claude-opus-4-6"
        assert request_body(calls[1])["model"] == "claude-sonnet-4-5"

    @pytest.mark.respx(base_url=base_url)
    def test_retry_with_modified_params_on_request_too_large(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                httpx.Response(413, json=error_body(type="invalid_request_error", message="Request too large")),
                httpx.Response(200, json=message_body()),
            ]
        )

        client = make_sync_client(middleware=[ShrinkMaxTokensOnTooLarge(256)])

        message = client.messages.create(
            max_tokens=4096,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )
        assert isinstance(message, Message)

        calls = cast("list[MockRequestCall]", respx_mock.calls)
        assert len(calls) == 2
        assert request_body(calls[0])["max_tokens"] == 4096
        assert request_body(calls[1])["max_tokens"] == 256

    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_short_circuit_skips_http_request(self, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        cached = short_circuit_message(model="claude-cached")
        middleware = ShortCircuit(cached)
        client = make_sync_client(middleware=[middleware])

        message = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert message is cached
        assert len(middleware.requests) == 1
        assert route.call_count == 0

    @pytest.mark.respx(base_url=base_url)
    def test_functional_middleware(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        def add_trace_header(request: APIRequest, call_next: CallNext) -> Any:
            return call_next(request.copy(headers={**request.headers, "x-trace-id": "abc-123"}))

        client = make_sync_client(middleware=[add_trace_header])

        message = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )
        assert isinstance(message, Message)

        calls = cast("list[MockRequestCall]", respx_mock.calls)
        assert calls[0].request.headers["x-trace-id"] == "abc-123"

    @mock.patch("anthropic._base_client.BaseClient._calculate_retry_timeout", _low_retry_timeout)
    @pytest.mark.respx(base_url=base_url)
    def test_middleware_runs_per_attempt(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                httpx.Response(500),
                httpx.Response(500),
                httpx.Response(200, json=message_body()),
            ]
        )

        recorder = AttemptRecorder()
        client = make_sync_client(middleware=[recorder], max_retries=2)

        message = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert isinstance(message, Message)
        # the chain ran once per HTTP attempt, seeing each failure's response;
        # returning an error response keeps it on the SDK's retry path
        assert recorder.attempts == [0, 1, 2]
        assert recorder.statuses == [500, 500, 200]
        assert recorder.errors == []
        assert len(respx_mock.calls) == 3

    @mock.patch("anthropic._base_client.BaseClient._calculate_retry_timeout", _low_retry_timeout)
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_middleware_error_is_not_retried(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        recorder = AttemptRecorder()
        client = make_sync_client(middleware=[recorder, Exploding()], max_retries=2)

        with pytest.raises(Boom):
            client.messages.create(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Hello"}],
                model="claude-opus-4-6",
            )

        # the middleware's own error propagates immediately, without re-running the chain
        assert recorder.attempts == [0]
        assert len(respx_mock.calls) == 0

    @mock.patch("anthropic._base_client.BaseClient._calculate_retry_timeout", _low_retry_timeout)
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_retryable_error_is_retried_then_propagates(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        attempts: list[int] = []

        def give_up(request: APIRequest, call_next: CallNext) -> Any:  # noqa: ARG001
            attempts.append(request.retries_taken)
            raise RetryableError("try again")

        client = make_sync_client(middleware=[give_up], max_retries=2)

        with pytest.raises(RetryableError):
            client.messages.create(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Hello"}],
                model="claude-opus-4-6",
            )

        assert attempts == [0, 1, 2]
        assert len(respx_mock.calls) == 0

    @mock.patch("anthropic._base_client.BaseClient._calculate_retry_timeout", _low_retry_timeout)
    @pytest.mark.respx(base_url=base_url)
    def test_error_with_retryable_cause_is_retried(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                httpx.ConnectError("kaboom"),
                httpx.Response(200, json=message_body()),
            ]
        )

        def wrap_errors(request: APIRequest, call_next: CallNext) -> Any:
            try:
                return call_next(request)
            except APIConnectionError as err:
                # wrapping a retryable failure with `raise ... from` keeps it on the retry path
                raise Boom("wrapped") from err

        client = make_sync_client(middleware=[wrap_errors], max_retries=2)

        message = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert isinstance(message, Message)
        assert len(respx_mock.calls) == 2

    @mock.patch("anthropic._base_client.BaseClient._calculate_retry_timeout", _low_retry_timeout)
    @pytest.mark.respx(base_url=base_url)
    def test_returned_error_response_raises_typed_error_for_caller(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(400, json=error_body(type="invalid_request_error", message="bad request"))
        )

        recorder = AttemptRecorder()
        client = make_sync_client(middleware=[recorder], max_retries=2)

        with pytest.raises(BadRequestError):
            client.messages.create(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Hello"}],
                model="claude-opus-4-6",
            )

        # middleware saw the error response rather than an exception; the SDK
        # raised the typed error for the caller, without retrying the 400
        assert recorder.statuses == [400]
        assert recorder.errors == []
        assert len(respx_mock.calls) == 1

    @mock.patch("anthropic._base_client.BaseClient._calculate_retry_timeout", _low_retry_timeout)
    @pytest.mark.respx(base_url=base_url)
    def test_request_modifications_do_not_persist_across_attempts(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                httpx.Response(500),
                httpx.Response(200, json=message_body()),
            ]
        )

        def tag_attempt(request: APIRequest, call_next: CallNext) -> Any:
            # each attempt starts from the original request, not the previous attempt's copy
            assert "x-attempt" not in request.headers
            return call_next(request.copy(headers={**request.headers, "x-attempt": str(request.retries_taken)}))

        client = make_sync_client(middleware=[tag_attempt], max_retries=2)

        message = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert isinstance(message, Message)
        calls = cast("list[MockRequestCall]", respx_mock.calls)
        assert calls[0].request.headers["x-attempt"] == "0"
        assert calls[1].request.headers["x-attempt"] == "1"

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_flows_through_middleware(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, headers={"content-type": "text/event-stream"}, content=b"")
        )

        recorder = RecordingMiddleware()
        client = make_sync_client(middleware=[recorder])

        stream = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
            stream=True,
        )

        assert isinstance(stream, Stream)
        assert len(recorder.requests) == 1
        assert recorder.requests[0].stream is True
        assert recorder.requests[0].stream_cls is not None
        # the middleware sees the `APIResponse` wrapper, not the `Stream`
        assert isinstance(recorder.results[0], APIResponse)
        stream.close()

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_error_response_is_visible_to_middleware(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                httpx.Response(529, json=error_body(type="overloaded_error", message="Overloaded")),
                httpx.Response(200, headers={"content-type": "text/event-stream"}, content=b""),
            ]
        )

        client = make_sync_client(middleware=[ModelFallback("claude-sonnet-4-5")], max_retries=0)

        stream = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
            stream=True,
        )

        assert isinstance(stream, Stream)
        calls = cast("list[MockRequestCall]", respx_mock.calls)
        assert len(calls) == 2
        assert request_body(calls[1])["model"] == "claude-sonnet-4-5"
        stream.close()

    @pytest.mark.respx(base_url=base_url)
    def test_call_next_returns_api_response(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, json=message_body(), headers={"x-custom-header": "custom-value"})
        )

        middleware = InspectResponse()
        client = make_sync_client(middleware=[middleware])

        message = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert isinstance(message, Message)
        assert len(middleware.responses) == 1
        response = middleware.responses[0]
        assert isinstance(response, APIResponse)
        assert response.status_code == 200
        assert response.headers["x-custom-header"] == "custom-value"

    @pytest.mark.respx(base_url=base_url)
    def test_parse_in_middleware_shares_parse_cache(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        middleware = ParseInMiddleware()
        client = make_sync_client(middleware=[middleware])

        message = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        # the value parsed inside the middleware is the same object the caller receives
        assert isinstance(message, Message)
        assert middleware.parsed == [message]
        assert middleware.parsed[0] is message

    @pytest.mark.respx(base_url=base_url)
    def test_with_raw_response_flows_through_middleware(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        recorder = RecordingMiddleware()
        client = make_sync_client(middleware=[recorder])

        response = client.messages.with_raw_response.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert isinstance(response, LegacyAPIResponse)
        assert isinstance(response.parse(), Message)
        assert len(recorder.requests) == 1
        assert recorder.requests[0].url == "/v1/messages"

    @pytest.mark.respx(base_url=base_url)
    def test_with_raw_response_middleware_sees_api_response(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, json=message_body(), headers={"x-custom-header": "custom-value"})
        )

        middleware = InspectResponse()
        client = make_sync_client(middleware=[middleware])

        response = client.messages.with_raw_response.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        # the middleware itself saw a true `APIResponse`
        assert len(middleware.responses) == 1
        assert isinstance(middleware.responses[0], APIResponse)

        # the caller still receives the `LegacyAPIResponse` wrapper it expects
        assert isinstance(response, LegacyAPIResponse)
        assert response.status_code == 200
        assert response.headers["x-custom-header"] == "custom-value"
        message = response.parse()
        assert isinstance(message, Message)
        assert message.id == "msg_013Zva2CMHLNnXjNJJKqJ2EF"

    @pytest.mark.respx(base_url=base_url)
    def test_with_streaming_response_middleware_sees_api_response(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, json=message_body(), headers={"x-custom-header": "custom-value"})
        )

        middleware = InspectResponse()
        client = make_sync_client(middleware=[middleware])

        with client.messages.with_streaming_response.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        ) as response:
            # the middleware itself saw a true `APIResponse`
            assert len(middleware.responses) == 1
            assert isinstance(middleware.responses[0], APIResponse)

            # the caller still receives the `APIResponse` wrapper it expects
            assert isinstance(response, APIResponse)
            assert response.status_code == 200
            assert response.headers["x-custom-header"] == "custom-value"
            message = response.parse()
            assert isinstance(message, Message)
            assert message.id == "msg_013Zva2CMHLNnXjNJJKqJ2EF"

    @pytest.mark.respx(base_url=base_url)
    def test_response_wrapper_cast_to_is_returned_unparsed(self, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/files/file_id/content?beta=true").mock(
            return_value=httpx.Response(200, content=b"file contents")
        )

        recorder = RecordingMiddleware()
        client = make_sync_client(middleware=[recorder])

        # `download()` asks for the `BinaryAPIResponse` wrapper itself via `cast_to`;
        # the middleware chain must hand it back instead of parsing it
        file = client.beta.files.download(file_id="file_id")

        assert isinstance(file, BinaryAPIResponse)
        assert file.read() == b"file contents"
        assert len(recorder.requests) == 1

        # the middleware also saw the typed wrapper, not a generic `APIResponse`
        assert len(recorder.results) == 1
        assert isinstance(recorder.results[0], BinaryAPIResponse)
        assert recorder.results[0] is file

    @pytest.mark.respx(base_url=base_url)
    def test_fallback_retry_sees_identical_request_state(self, respx_mock: MockRouter) -> None:
        # use `with_streaming_response.download` as it relies on the internal cast_to
        # override header which the request pipeline consumes; a retrying middleware
        # must observe identical request state on every `call_next(...)` invocation
        respx_mock.get("/v1/files/file_id/content?beta=true").mock(
            side_effect=[
                httpx.Response(503, json=error_body(type="api_error", message="Service unavailable")),
                httpx.Response(200, json={"foo": "bar"}),
            ]
        )

        middleware = RetryOnInternalServerError()
        client = make_sync_client(middleware=[middleware], max_retries=0)

        with client.beta.files.with_streaming_response.download(file_id="file_id") as file:
            assert isinstance(file, StreamedBinaryAPIResponse)
            assert json.loads(file.read()) == {"foo": "bar"}

        calls = cast("list[MockRequestCall]", respx_mock.calls)
        assert len(calls) == 2

        # both invocations observed identical request state, including the
        # internal cast_to override header
        assert len(middleware.headers_seen) == 2
        assert middleware.headers_seen[0] == middleware.headers_seen[1]

        # and the successful retry produced the correctly-typed response
        assert len(middleware.results) == 1
        assert isinstance(middleware.results[0], StreamedBinaryAPIResponse)
        assert not isinstance(middleware.results[0], BinaryAPIResponse)

    @pytest.mark.respx(base_url=base_url)
    def test_middleware_ordering_across_sequential_requests(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        events: list[str] = []
        outer = RecordingMiddleware("outer", events)
        inner = RecordingMiddleware("inner", events)
        client = make_sync_client(middleware=[outer, inner])

        # the chain is built once at construction time and reused for every request
        chain = client._middleware_chain
        assert chain is not None

        for _ in range(3):
            client.messages.create(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Hello"}],
                model="claude-opus-4-6",
            )

        assert client._middleware_chain is chain
        assert events == ["outer:enter", "inner:enter", "inner:exit", "outer:exit"] * 3

    @pytest.mark.respx(base_url=base_url)
    def test_middleware_iterator_argument_runs_middleware(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        recorder = RecordingMiddleware()
        client = make_sync_client(middleware=iter([recorder]))

        assert client._middleware == (recorder,)

        message = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert isinstance(message, Message)
        assert len(recorder.requests) == 1

    @pytest.mark.respx(base_url=base_url)
    def test_file_upload_with_request_copying_middleware(self, respx_mock: MockRouter, tmp_path: Path) -> None:
        respx_mock.post("/v1/files?beta=true").mock(return_value=httpx.Response(200, json=file_metadata_body()))

        def add_trace_header(request: APIRequest, call_next: CallNext) -> Any:
            return call_next(request.copy(headers={**request.headers, "x-trace-id": "abc-123"}))

        client = make_sync_client(middleware=[add_trace_header])

        # uploading an open file handle must not crash when middleware copies the request
        path = tmp_path / "upload.txt"
        path.write_bytes(b"file contents")
        with path.open("rb") as f:
            file = client.beta.files.upload(file=f)

        assert file.id == "file_123"

        calls = cast("list[MockRequestCall]", respx_mock.calls)
        assert len(calls) == 1
        assert calls[0].request.headers["x-trace-id"] == "abc-123"

    def test_copy_inherits_replaces_and_clears_middleware(self) -> None:
        first = RecordingMiddleware("first")
        second = RecordingMiddleware("second")
        client = make_sync_client(middleware=[first])

        assert client._middleware == (first,)
        assert client.copy()._middleware == (first,)
        assert client.with_options(max_retries=7)._middleware == (first,)
        assert client.copy(middleware=[second])._middleware == (second,)
        assert client.copy(middleware=[])._middleware == ()
        assert client.copy(middleware=None)._middleware == ()

    def test_with_middleware_appends_without_mutating_original(self) -> None:
        first = RecordingMiddleware("first")
        second = RecordingMiddleware("second")
        third = RecordingMiddleware("third")
        client = make_sync_client(middleware=[first])

        derived = client.with_middleware(second, third)

        assert derived is not client
        assert derived._middleware == (first, second, third)
        assert client._middleware == (first,)

    def test_with_middleware_validates_like_the_constructor(self) -> None:
        client = make_sync_client()

        async def async_only(request: APIRequest, call_next: AsyncCallNext) -> Any:
            return await call_next(request)

        with pytest.raises(TypeError):
            client.with_middleware(async_only)

    @pytest.mark.respx(base_url=base_url)
    def test_with_middleware_client_runs_appended_middleware_innermost(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        events: list[str] = []
        outer = RecordingMiddleware("outer", events=events)
        extra = RecordingMiddleware("extra", events=events)
        client = make_sync_client(middleware=[outer])

        client.with_middleware(extra).messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        # the appended middleware runs inside the client's own middleware
        assert events == ["outer:enter", "extra:enter", "extra:exit", "outer:exit"]

        # the original client is unaffected by the derived client's calls
        events.clear()
        client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )
        assert events == ["outer:enter", "outer:exit"]

    @pytest.mark.respx(base_url=base_url)
    def test_with_options_client_runs_inherited_middleware(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        recorder = RecordingMiddleware()
        client = make_sync_client(middleware=[recorder])

        client.with_options(max_retries=0).messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert len(recorder.requests) == 1

    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    def test_middleware_exception_propagates(self, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        client = make_sync_client(middleware=[Exploding()])

        with pytest.raises(Boom, match="middleware failure"):
            client.messages.create(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Hello"}],
                model="claude-opus-4-6",
            )

        assert route.call_count == 0

    @pytest.mark.respx(base_url=base_url)
    def test_no_middleware_behavior_unchanged(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        client = make_sync_client()
        assert client._middleware == ()

        message = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )
        assert isinstance(message, Message)

    def test_construction_rejects_async_only_middleware(self) -> None:
        with pytest.raises(TypeError, match="does not implement `handle\\(\\)`"):
            make_sync_client(middleware=[AsyncOnlyMiddleware()])

    def test_construction_rejects_async_function(self) -> None:
        async def async_fn(request: APIRequest, call_next: AsyncCallNext) -> Any:
            return await call_next(request)

        with pytest.raises(TypeError, match="is an async function"):
            make_sync_client(middleware=[async_fn])

    def test_construction_accepts_sync_middleware(self) -> None:
        def sync_fn(request: APIRequest, call_next: CallNext) -> Any:
            return call_next(request)

        client = make_sync_client(middleware=[SyncOnlyMiddleware(), RecordingMiddleware(), sync_fn])
        assert len(client._middleware) == 3


class TestAsyncMiddleware:
    @pytest.mark.respx(base_url=base_url)
    async def test_middleware_sees_request_and_returns_response(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        recorder = RecordingMiddleware()
        client = make_async_client(middleware=[recorder])

        message = await client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert isinstance(message, Message)
        assert len(recorder.requests) == 1
        request = recorder.requests[0]
        assert request.method == "post"
        assert request.url == "/v1/messages"
        assert request.cast_to is Message
        assert request.stream is False
        assert middleware_request_body(request)["model"] == "claude-opus-4-6"

        # the middleware itself saw the `AsyncAPIResponse` wrapper; the value the
        # caller receives is parsed from that same response
        assert len(recorder.results) == 1
        response = recorder.results[0]
        assert isinstance(response, AsyncAPIResponse)
        assert await response.parse() is message

    @pytest.mark.respx(base_url=base_url)
    async def test_middleware_ordering(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        events: list[str] = []
        outer = RecordingMiddleware("outer", events)
        inner = RecordingMiddleware("inner", events)
        client = make_async_client(middleware=[outer, inner])

        await client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert events == ["outer:enter", "inner:enter", "inner:exit", "outer:exit"]

    @pytest.mark.respx(base_url=base_url)
    async def test_request_mutation_changes_outgoing_request(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        client = make_async_client(middleware=[MutateBody(model="claude-sonnet-4-5", max_tokens=4096)])

        message = await client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )
        assert isinstance(message, Message)

        calls = cast("list[MockRequestCall]", respx_mock.calls)
        assert len(calls) == 1
        sent = request_body(calls[0])
        assert sent["model"] == "claude-sonnet-4-5"
        assert sent["max_tokens"] == 4096

    @pytest.mark.respx(base_url=base_url)
    async def test_fallback_on_overloaded_error(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                httpx.Response(529, json=error_body(type="overloaded_error", message="Overloaded")),
                httpx.Response(200, json=message_body(model="claude-sonnet-4-5")),
            ]
        )

        client = make_async_client(middleware=[ModelFallback("claude-sonnet-4-5")], max_retries=0)

        message = await client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert isinstance(message, Message)
        assert message.model == "claude-sonnet-4-5"

        calls = cast("list[MockRequestCall]", respx_mock.calls)
        assert len(calls) == 2
        assert request_body(calls[0])["model"] == "claude-opus-4-6"
        assert request_body(calls[1])["model"] == "claude-sonnet-4-5"

    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_short_circuit_skips_http_request(self, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        cached = short_circuit_message(model="claude-cached")
        middleware = ShortCircuit(cached)
        client = make_async_client(middleware=[middleware])

        message = await client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert message is cached
        assert len(middleware.requests) == 1
        assert route.call_count == 0

    @pytest.mark.respx(base_url=base_url)
    async def test_functional_middleware(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        async def add_trace_header(request: APIRequest, call_next: AsyncCallNext) -> Any:
            return await call_next(request.copy(headers={**request.headers, "x-trace-id": "abc-123"}))

        client = make_async_client(middleware=[add_trace_header])

        message = await client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )
        assert isinstance(message, Message)

        calls = cast("list[MockRequestCall]", respx_mock.calls)
        assert calls[0].request.headers["x-trace-id"] == "abc-123"

    @pytest.mark.respx(base_url=base_url)
    async def test_call_next_returns_api_response(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, json=message_body(), headers={"x-custom-header": "custom-value"})
        )

        middleware = InspectResponse()
        client = make_async_client(middleware=[middleware])

        message = await client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert isinstance(message, Message)
        assert len(middleware.responses) == 1
        response = middleware.responses[0]
        assert isinstance(response, AsyncAPIResponse)
        assert response.status_code == 200
        assert response.headers["x-custom-header"] == "custom-value"

    @pytest.mark.respx(base_url=base_url)
    async def test_parse_in_middleware_shares_parse_cache(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        middleware = ParseInMiddleware()
        client = make_async_client(middleware=[middleware])

        message = await client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        # the value parsed inside the middleware is the same object the caller receives
        assert isinstance(message, Message)
        assert middleware.parsed == [message]
        assert middleware.parsed[0] is message

    @pytest.mark.respx(base_url=base_url)
    async def test_with_raw_response_flows_through_middleware(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        recorder = RecordingMiddleware()
        client = make_async_client(middleware=[recorder])

        response = await client.messages.with_raw_response.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert isinstance(response, LegacyAPIResponse)
        assert isinstance(response.parse(), Message)
        assert len(recorder.requests) == 1
        assert recorder.requests[0].url == "/v1/messages"

    @pytest.mark.respx(base_url=base_url)
    async def test_with_raw_response_middleware_sees_api_response(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, json=message_body(), headers={"x-custom-header": "custom-value"})
        )

        middleware = InspectResponse()
        client = make_async_client(middleware=[middleware])

        response = await client.messages.with_raw_response.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        # the middleware itself saw a true `AsyncAPIResponse`
        assert len(middleware.responses) == 1
        assert isinstance(middleware.responses[0], AsyncAPIResponse)

        # the caller still receives the `LegacyAPIResponse` wrapper it expects
        assert isinstance(response, LegacyAPIResponse)
        assert response.status_code == 200
        assert response.headers["x-custom-header"] == "custom-value"
        message = response.parse()
        assert isinstance(message, Message)
        assert message.id == "msg_013Zva2CMHLNnXjNJJKqJ2EF"

    @pytest.mark.respx(base_url=base_url)
    async def test_with_streaming_response_middleware_sees_api_response(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            return_value=httpx.Response(200, json=message_body(), headers={"x-custom-header": "custom-value"})
        )

        middleware = InspectResponse()
        client = make_async_client(middleware=[middleware])

        async with client.messages.with_streaming_response.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        ) as response:
            # the middleware itself saw a true `AsyncAPIResponse`
            assert len(middleware.responses) == 1
            assert isinstance(middleware.responses[0], AsyncAPIResponse)

            # the caller still receives the `AsyncAPIResponse` wrapper it expects
            assert isinstance(response, AsyncAPIResponse)
            assert response.status_code == 200
            assert response.headers["x-custom-header"] == "custom-value"
            message = await response.parse()
            assert isinstance(message, Message)
            assert message.id == "msg_013Zva2CMHLNnXjNJJKqJ2EF"

    @pytest.mark.respx(base_url=base_url)
    async def test_response_wrapper_cast_to_is_returned_unparsed(self, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/files/file_id/content?beta=true").mock(
            return_value=httpx.Response(200, content=b"file contents")
        )

        recorder = RecordingMiddleware()
        client = make_async_client(middleware=[recorder])

        # `download()` asks for the `AsyncBinaryAPIResponse` wrapper itself via `cast_to`;
        # the middleware chain must hand it back instead of parsing it
        file = await client.beta.files.download(file_id="file_id")

        assert isinstance(file, AsyncBinaryAPIResponse)
        assert await file.read() == b"file contents"
        assert len(recorder.requests) == 1

        # the middleware also saw the typed wrapper, not a generic `AsyncAPIResponse`
        assert len(recorder.results) == 1
        assert isinstance(recorder.results[0], AsyncBinaryAPIResponse)
        assert recorder.results[0] is file

    @pytest.mark.respx(base_url=base_url)
    async def test_fallback_retry_sees_identical_request_state(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                httpx.Response(503, json=error_body(type="api_error", message="Service unavailable")),
                httpx.Response(200, json=message_body()),
            ]
        )

        middleware = RetryOnInternalServerError()
        client = make_async_client(middleware=[middleware], max_retries=0)

        message = await client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )
        assert isinstance(message, Message)

        calls = cast("list[MockRequestCall]", respx_mock.calls)
        assert len(calls) == 2

        # both invocations observed identical request state
        assert len(middleware.headers_seen) == 2
        assert middleware.headers_seen[0] == middleware.headers_seen[1]

        # and both outgoing requests carried an identical body
        assert request_body(calls[0]) == request_body(calls[1])

    @pytest.mark.respx(base_url=base_url)
    async def test_middleware_ordering_across_sequential_requests(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        events: list[str] = []
        outer = RecordingMiddleware("outer", events)
        inner = RecordingMiddleware("inner", events)
        client = make_async_client(middleware=[outer, inner])

        # the chain is built once at construction time and reused for every request
        chain = client._middleware_chain
        assert chain is not None

        for _ in range(3):
            await client.messages.create(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Hello"}],
                model="claude-opus-4-6",
            )

        assert client._middleware_chain is chain
        assert events == ["outer:enter", "inner:enter", "inner:exit", "outer:exit"] * 3

    @pytest.mark.respx(base_url=base_url)
    async def test_middleware_iterator_argument_runs_middleware(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        recorder = RecordingMiddleware()
        client = make_async_client(middleware=iter([recorder]))

        assert client._middleware == (recorder,)

        message = await client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert isinstance(message, Message)
        assert len(recorder.requests) == 1

    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_middleware_exception_propagates(self, respx_mock: MockRouter) -> None:
        route = respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        client = make_async_client(middleware=[Exploding()])

        with pytest.raises(Boom, match="middleware failure"):
            await client.messages.create(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Hello"}],
                model="claude-opus-4-6",
            )

        assert route.call_count == 0

    @mock.patch("anthropic._base_client.BaseClient._calculate_retry_timeout", _low_retry_timeout)
    @pytest.mark.respx(base_url=base_url)
    async def test_middleware_runs_per_attempt(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(
            side_effect=[
                httpx.Response(500),
                httpx.Response(500),
                httpx.Response(200, json=message_body()),
            ]
        )

        recorder = AttemptRecorder()
        client = make_async_client(middleware=[recorder], max_retries=2)

        message = await client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert isinstance(message, Message)
        # the chain ran once per HTTP attempt, seeing each failure's response;
        # returning an error response keeps it on the SDK's retry path
        assert recorder.attempts == [0, 1, 2]
        assert recorder.statuses == [500, 500, 200]
        assert recorder.errors == []
        assert len(respx_mock.calls) == 3

    @mock.patch("anthropic._base_client.BaseClient._calculate_retry_timeout", _low_retry_timeout)
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_retryable_error_is_retried_then_propagates(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        attempts: list[int] = []

        async def give_up(request: APIRequest, call_next: AsyncCallNext) -> Any:  # noqa: ARG001
            attempts.append(request.retries_taken)
            raise RetryableError("try again")

        client = make_async_client(middleware=[give_up], max_retries=2)

        with pytest.raises(RetryableError):
            await client.messages.create(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Hello"}],
                model="claude-opus-4-6",
            )

        assert attempts == [0, 1, 2]
        assert len(respx_mock.calls) == 0

    @mock.patch("anthropic._base_client.BaseClient._calculate_retry_timeout", _low_retry_timeout)
    @pytest.mark.respx(base_url=base_url, assert_all_called=False)
    async def test_middleware_error_is_not_retried(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        recorder = AttemptRecorder()
        client = make_async_client(middleware=[recorder, Exploding()], max_retries=2)

        with pytest.raises(Boom):
            await client.messages.create(
                max_tokens=1024,
                messages=[{"role": "user", "content": "Hello"}],
                model="claude-opus-4-6",
            )

        # the middleware's own error propagates immediately, without re-running the chain
        assert recorder.attempts == [0]
        assert len(respx_mock.calls) == 0

    def test_copy_inherits_replaces_and_clears_middleware(self) -> None:
        first = RecordingMiddleware("first")
        second = RecordingMiddleware("second")
        client = make_async_client(middleware=[first])

        assert client._middleware == (first,)
        assert client.copy()._middleware == (first,)
        assert client.with_options(max_retries=7)._middleware == (first,)
        assert client.copy(middleware=[second])._middleware == (second,)
        assert client.copy(middleware=[])._middleware == ()
        assert client.copy(middleware=None)._middleware == ()

    @pytest.mark.respx(base_url=base_url)
    async def test_with_middleware_client_runs_appended_middleware_innermost(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        events: list[str] = []
        outer = RecordingMiddleware("outer", events=events)
        extra = RecordingMiddleware("extra", events=events)
        client = make_async_client(middleware=[outer])

        derived = client.with_middleware(extra)
        assert derived._middleware == (outer, extra)
        assert client._middleware == (outer,)

        await derived.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        # the appended middleware runs inside the client's own middleware
        assert events == ["outer:enter", "extra:enter", "extra:exit", "outer:exit"]

    @pytest.mark.respx(base_url=base_url)
    async def test_no_middleware_behavior_unchanged(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        client = make_async_client()
        assert client._middleware == ()

        message = await client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )
        assert isinstance(message, Message)

    def test_construction_rejects_sync_only_middleware(self) -> None:
        with pytest.raises(TypeError, match="does not implement `handle_async\\(\\)`"):
            make_async_client(middleware=[SyncOnlyMiddleware()])

    def test_construction_rejects_sync_function(self) -> None:
        def sync_fn(request: APIRequest, call_next: CallNext) -> Any:
            return call_next(request)

        with pytest.raises(TypeError, match="is not an async function"):
            make_async_client(middleware=[sync_fn])

    def test_construction_accepts_async_middleware(self) -> None:
        async def async_fn(request: APIRequest, call_next: AsyncCallNext) -> Any:
            return await call_next(request)

        client = make_async_client(middleware=[AsyncOnlyMiddleware(), RecordingMiddleware(), async_fn])
        assert len(client._middleware) == 3


class TestMiddlewareProperty:
    def test_exposes_configured_middleware(self) -> None:
        recorder = RecordingMiddleware()
        assert make_sync_client(middleware=[recorder]).middleware == (recorder,)
        assert make_sync_client().middleware == ()

    @pytest.mark.respx(base_url=base_url)
    def test_with_options_append_idiom(self, respx_mock: MockRouter) -> None:
        respx_mock.post("/v1/messages").mock(return_value=httpx.Response(200, json=message_body()))

        events: list[str] = []
        outer = RecordingMiddleware("outer", events)
        inner = RecordingMiddleware("inner", events)
        client = make_sync_client(middleware=[outer])

        derived = client.with_options(middleware=[*client.middleware, inner])
        message = derived.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )

        assert isinstance(message, Message)
        assert events == ["outer:enter", "inner:enter", "inner:exit", "outer:exit"]
        # the parent client is unchanged
        assert client.middleware == (outer,)


def make_bedrock_client(**kwargs: Any) -> AnthropicBedrock:
    return AnthropicBedrock(aws_region="us-east-1", api_key="aws-bearer-token", **kwargs)


def make_async_bedrock_client(**kwargs: Any) -> AsyncAnthropicBedrock:
    return AsyncAnthropicBedrock(aws_region="us-east-1", api_key="aws-bearer-token", **kwargs)


def make_vertex_client(**kwargs: Any) -> AnthropicVertex:
    return AnthropicVertex(region="region", project_id="project", access_token="my-access-token", **kwargs)


def make_async_vertex_client(**kwargs: Any) -> AsyncAnthropicVertex:
    return AsyncAnthropicVertex(region="region", project_id="project", access_token="my-access-token", **kwargs)


def make_mantle_client(**kwargs: Any) -> AnthropicBedrockMantle:
    return AnthropicBedrockMantle(aws_region="us-east-1", api_key="aws-bearer-token", **kwargs)


def make_async_mantle_client(**kwargs: Any) -> AsyncAnthropicBedrockMantle:
    return AsyncAnthropicBedrockMantle(aws_region="us-east-1", api_key="aws-bearer-token", **kwargs)


class TestLibClientMiddleware:
    bedrock_url = re.compile(r"https://bedrock-runtime\.us-east-1\.amazonaws\.com/model/.*/invoke")
    vertex_url = (
        "https://region-aiplatform.googleapis.com/v1"
        "/projects/project/locations/region/publishers/anthropic/models/claude-opus-4-6:rawPredict"
    )
    mantle_url = "https://bedrock-mantle.us-east-1.api.aws/anthropic/v1/messages"

    @pytest.mark.respx()
    def test_bedrock_middleware_sees_canonical_request(self, respx_mock: MockRouter) -> None:
        respx_mock.post(self.bedrock_url).mock(return_value=httpx.Response(200, json=message_body()))

        recorder = RecordingMiddleware()
        client = make_bedrock_client(middleware=[recorder])
        message = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )
        assert isinstance(message, Message)

        # the middleware sees the canonical request shape, before backend rewriting
        request = recorder.requests[0]
        assert request.url == "/v1/messages"
        assert middleware_request_body(request)["model"] == "claude-opus-4-6"

        # while the wire request hits the rewritten Bedrock URL with the model moved out of the body
        wire = cast("MockRequestCall", respx_mock.calls[0]).request
        assert wire.url.path == "/model/claude-opus-4-6/invoke"
        wire_body = json.loads(wire.content)
        assert "model" not in wire_body
        assert wire_body["anthropic_version"] == "bedrock-2023-05-31"

    @pytest.mark.respx()
    async def test_async_bedrock_middleware_sees_canonical_request(self, respx_mock: MockRouter) -> None:
        respx_mock.post(self.bedrock_url).mock(return_value=httpx.Response(200, json=message_body()))

        recorder = RecordingMiddleware()
        client = make_async_bedrock_client(middleware=[recorder])
        message = await client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )
        assert isinstance(message, Message)

        request = recorder.requests[0]
        assert request.url == "/v1/messages"
        assert middleware_request_body(request)["model"] == "claude-opus-4-6"

        wire = cast("MockRequestCall", respx_mock.calls[0]).request
        assert wire.url.path == "/model/claude-opus-4-6/invoke"

    @pytest.mark.respx()
    def test_vertex_middleware_sees_canonical_request(self, respx_mock: MockRouter) -> None:
        respx_mock.post(self.vertex_url).mock(return_value=httpx.Response(200, json=message_body()))

        recorder = RecordingMiddleware()
        client = make_vertex_client(middleware=[recorder])
        message = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )
        assert isinstance(message, Message)

        request = recorder.requests[0]
        assert request.url == "/v1/messages"
        assert middleware_request_body(request)["model"] == "claude-opus-4-6"

        wire = cast("MockRequestCall", respx_mock.calls[0]).request
        wire_body = json.loads(wire.content)
        assert "model" not in wire_body
        assert wire_body["anthropic_version"] == "vertex-2023-10-16"

    @pytest.mark.respx()
    async def test_async_vertex_middleware_sees_canonical_request(self, respx_mock: MockRouter) -> None:
        respx_mock.post(self.vertex_url).mock(return_value=httpx.Response(200, json=message_body()))

        recorder = RecordingMiddleware()
        client = make_async_vertex_client(middleware=[recorder])
        message = await client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )
        assert isinstance(message, Message)

        request = recorder.requests[0]
        assert request.url == "/v1/messages"
        assert middleware_request_body(request)["model"] == "claude-opus-4-6"

    @pytest.mark.respx()
    def test_mantle_middleware_sees_canonical_request(self, respx_mock: MockRouter) -> None:
        respx_mock.post(self.mantle_url).mock(return_value=httpx.Response(200, json=message_body()))

        recorder = RecordingMiddleware()
        client = make_mantle_client(middleware=[recorder])
        message = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )
        assert isinstance(message, Message)

        request = recorder.requests[0]
        assert request.url == "/v1/messages"
        assert middleware_request_body(request)["model"] == "claude-opus-4-6"

        wire = cast("MockRequestCall", respx_mock.calls[0]).request
        assert wire.url.path == "/anthropic/v1/messages"

    @pytest.mark.respx()
    async def test_async_mantle_middleware_sees_canonical_request(self, respx_mock: MockRouter) -> None:
        respx_mock.post(self.mantle_url).mock(return_value=httpx.Response(200, json=message_body()))

        recorder = RecordingMiddleware()
        client = make_async_mantle_client(middleware=[recorder])
        message = await client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )
        assert isinstance(message, Message)

        request = recorder.requests[0]
        assert request.url == "/v1/messages"
        assert middleware_request_body(request)["model"] == "claude-opus-4-6"

        wire = cast("MockRequestCall", respx_mock.calls[0]).request
        assert wire.url.path == "/anthropic/v1/messages"

    @pytest.mark.respx()
    def test_bedrock_fallback_middleware_retries_with_new_model(self, respx_mock: MockRouter) -> None:
        respx_mock.post(self.bedrock_url).mock(
            side_effect=[
                httpx.Response(529, json=error_body(type="overloaded_error", message="Overloaded")),
                httpx.Response(200, json=message_body(model="claude-sonnet-4-5")),
            ]
        )

        class ModelFallback(Middleware):
            @override
            def handle(self, request: APIRequest, call_next: CallNext) -> Any:
                response = call_next(request)
                if response.status_code != 529:
                    return response
                fallback = request.copy(
                    body={**middleware_request_body(request), "model": "claude-sonnet-4-5"},
                )
                return call_next(fallback)

        client = make_bedrock_client(middleware=[ModelFallback()], max_retries=0)
        message = client.messages.create(
            max_tokens=1024,
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-opus-4-6",
        )
        assert isinstance(message, Message)
        assert message.model == "claude-sonnet-4-5"

        # the fallback model is reflected in the rewritten URL of the second wire request
        first = cast("MockRequestCall", respx_mock.calls[0]).request
        second = cast("MockRequestCall", respx_mock.calls[1]).request
        assert first.url.path == "/model/claude-opus-4-6/invoke"
        assert second.url.path == "/model/claude-sonnet-4-5/invoke"

    def test_foundry_clients_accept_middleware(self) -> None:
        recorder = RecordingMiddleware()
        client = AnthropicFoundry(api_key=api_key, resource="resource", middleware=[recorder])
        assert client.middleware == (recorder,)
        async_client = AsyncAnthropicFoundry(api_key=api_key, resource="resource", middleware=[recorder])
        assert async_client.middleware == (recorder,)

    def test_lib_clients_copy_inherits_replaces_and_clears(self) -> None:
        recorder = RecordingMiddleware()
        clients = [
            make_bedrock_client(middleware=[recorder]),
            make_vertex_client(middleware=[recorder]),
            make_mantle_client(middleware=[recorder]),
            AnthropicFoundry(api_key=api_key, resource="resource", middleware=[recorder]),
            AnthropicAWS(skip_auth=True, base_url=base_url, middleware=[recorder]),
        ]
        for client in clients:
            assert client.middleware == (recorder,)
            assert client.copy().middleware == (recorder,)
            assert client.with_options(timeout=5).middleware == (recorder,)

            other = RecordingMiddleware()
            assert client.copy(middleware=[other]).middleware == (other,)
            assert client.copy(middleware=None).middleware == ()
            assert client.with_middleware(other).middleware == (recorder, other)
            assert client.middleware == (recorder,)

    def test_async_lib_clients_copy_inherits_replaces_and_clears(self) -> None:
        recorder = RecordingMiddleware()
        clients = [
            make_async_bedrock_client(middleware=[recorder]),
            make_async_vertex_client(middleware=[recorder]),
            make_async_mantle_client(middleware=[recorder]),
            AsyncAnthropicFoundry(api_key=api_key, resource="resource", middleware=[recorder]),
            AsyncAnthropicAWS(skip_auth=True, base_url=base_url, middleware=[recorder]),
        ]
        for client in clients:
            assert client.middleware == (recorder,)
            assert client.copy().middleware == (recorder,)
            assert client.with_options(timeout=5).middleware == (recorder,)

            other = RecordingMiddleware()
            assert client.copy(middleware=[other]).middleware == (other,)
            assert client.copy(middleware=None).middleware == ()
            assert client.with_middleware(other).middleware == (recorder, other)
            assert client.middleware == (recorder,)

    def test_lib_client_construction_validates_middleware(self) -> None:
        def sync_fn(request: APIRequest, call_next: CallNext) -> Any:
            return call_next(request)

        with pytest.raises(TypeError, match="is not an async function"):
            make_async_bedrock_client(middleware=[sync_fn])

        with pytest.raises(TypeError, match="is not an async function"):
            make_async_mantle_client(middleware=[sync_fn])

        async def async_fn(request: APIRequest, call_next: AsyncCallNext) -> Any:
            return await call_next(request)

        with pytest.raises(TypeError, match="is an async function"):
            make_vertex_client(middleware=[async_fn])

        with pytest.raises(TypeError, match="is an async function"):
            make_mantle_client(middleware=[async_fn])
