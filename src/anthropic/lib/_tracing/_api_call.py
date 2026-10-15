from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, cast
from collections.abc import Mapping

import httpx2
from opentelemetry import trace
from opentelemetry.util.types import AttributeValue

from ._utils import MessageCreateBody, get, as_dict
from ...types import Message, MessageTokensCount
from ..._types import Omit
from ..._utils import is_dict
from ._content import set_message_content
from ..._models import BaseModel
from ._response import as_model, set_response, response_data
from ..._tracing import (
    ApiCallResult,
    StreamObserver,
    end_api_call_span,
    end_api_call_span_when_body_ends,
)
from ._streaming import StreamedMessage
from ._attributes import RESPONSE_HEADER_ATTRIBUTES, AnthropicSpan, AttributeName, attributes
from ..._streaming import Stream, AsyncStream
from ...types.beta import BetaMessage, BetaMessageTokensCount, BetaManagedAgentsSession

if TYPE_CHECKING:
    from ..._base_client import BaseClient

__all__ = [
    "finish_api_call_span",
    "messages_create_request_attributes",
    "messages_count_tokens_request_attributes",
]

log: logging.Logger = logging.getLogger(__name__)


def finish_api_call_span(client: BaseClient[Any, Any], span: trace.Span, result: ApiCallResult) -> None:
    """Records the call's `result` on its span, and ends the span.

    The body of a stream or of an unread raw response keeps the span until the application has read,
    closed or dropped it. Anything else ends it now. Never raises.
    """
    try:
        observer = record_api_call(client, span, result)
        if result.response is not None:
            end_api_call_span_when_body_ends(span, result.response, result, observer)
            return
        end_api_call_span(span, result)
    except Exception:
        log.debug("Could not end the span of an API call", exc_info=True)


def record_api_call(client: BaseClient[Any, Any], span: trace.Span, result: ApiCallResult) -> StreamObserver | None:
    """Sets the `gen_ai.*` and `anthropic.*` attributes of the call. Never raises.

    Returns the observer that records a streamed Message as the application reads it, and `None` for any other result.
    """
    if not span.is_recording():
        return None
    try:
        set_response_header_attributes(span, result)
        set_created_id_attribute(span, result)
        # What to record follows from what the method says the call returns, which is also known when the call fails.
        returns: type[object] = result.cast_to if isinstance(result.cast_to, type) else object
        if issubclass(returns, (Message, BetaMessage)):
            return record_messages_create(client, span, result, returns)
        set_response_attributes(span, result, returns)
        return None
    except Exception:
        log.debug("Could not record the API call on its span", exc_info=True)
        return None


def set_response_header_attributes(span: AnthropicSpan, result: ApiCallResult) -> None:
    response = result.final_attempt
    if response is None:
        return
    for attribute, header in RESPONSE_HEADER_ATTRIBUTES:
        if value := response.headers.get(header):
            span.set_attribute(attribute, value)


def set_created_id_attribute(span: trace.Span, result: ApiCallResult) -> None:
    """Sets the ID of the object that the call created, which the body of a raw response has too."""
    created = result.options.span_created_id
    returns = result.cast_to
    if created is None or result.error is not None:
        return
    if not (isinstance(returns, type) and issubclass(returns, BaseModel)):
        return
    attribute, field = (created, "id") if isinstance(created, str) else created
    created_id: object = getattr(as_model(response_data(result), returns), field, None)
    if isinstance(created_id, str):
        span.set_attribute(attribute, created_id)


def set_response_attributes(span: AnthropicSpan, result: ApiCallResult, returns: type[object]) -> None:
    if issubclass(returns, (MessageTokensCount, BetaMessageTokensCount)):
        if (count := as_model(response_data(result), returns)) is not None:
            span.set_attribute("anthropic.message.count_tokens.input_tokens", count.input_tokens)
    # Other Sessions methods return a Session too, and only the span of the one that creates it, which names the
    # attribute of the created ID, has its Agent's name and model.
    if issubclass(returns, BetaManagedAgentsSession) and result.options.span_created_id is not None:
        if (session := as_model(response_data(result), BetaManagedAgentsSession)) is not None:
            span.set_attribute("gen_ai.agent.name", session.agent.name)
            span.set_attribute("gen_ai.request.model", session.agent.model.id)


def record_messages_create(
    client: BaseClient[Any, Any],
    span: trace.Span,
    result: ApiCallResult,
    returns: type[Message] | type[BetaMessage],
) -> StreamObserver | None:
    """Records the response of a `messages.create` call, and in content mode the request's messages too.

    A streamed Message is recorded from its events as the application reads them, by the observer that is returned.
    """
    body = cast(MessageCreateBody, as_dict(result.options.json_data) or {})
    content = client._otel.records_content
    data = response_data(result)
    response = result.response
    streams = isinstance(result.data, (Stream, AsyncStream))
    # A raw response of a streaming request has no stream until the application parses it.
    if response is not None and (streams or (get(body, "stream") is True and not response.is_closed)):
        try:
            request_headers = response.request.headers
        except RuntimeError:
            # A response that a middleware made has a request only if the middleware set one.
            request_headers = httpx2.Headers()
        return StreamedMessage(
            span,
            body,
            request_headers=request_headers,
            content=content,
            max_content_bytes=client._otel.max_content_bytes,
            start_time=result.start_time,
        )

    message = as_model(data, returns, without="content")
    if message is not None:
        set_response(span, message, complete=True)
    if content:
        # The body of a raw response holds the content that its model leaves out.
        output = data.get("content") if is_dict(data) else message.content if message is not None else None
        set_message_content(span, body, output, limit=client._otel.max_content_bytes)
    return None


def messages_create_request_attributes(
    client: BaseClient[Any, Any], body: object, extra_headers: Mapping[str, object] | None
) -> dict[str, AttributeValue]:
    """The attributes that the span of a `messages.create` call starts with, from the request's `body` and headers.

    Empty when `client` has no spans. Never raises.
    """
    if client._tracer is None:
        return {}
    values: dict[AttributeName, AttributeValue | None] = {}
    try:
        values["gen_ai.operation.name"] = "chat"
        values["gen_ai.request.model"] = get(body, "model")
        values["gen_ai.request.max_tokens"] = get(body, "max_tokens")
        if (temperature := get(body, "temperature")) is not None:
            values["gen_ai.request.temperature"] = float(temperature)
        if (top_p := get(body, "top_p")) is not None:
            values["gen_ai.request.top_p"] = float(top_p)
        values["gen_ai.request.top_k"] = get(body, "top_k")
        if get(body, "stream") is True:
            values["gen_ai.request.stream"] = True
        values["gen_ai.request.reasoning.level"] = get(get(body, "output_config"), "effort")
        # `output_format` is the deprecated form of `output_config.format`.
        output_formats = (get(get(body, "output_config"), "format"), get(body, "output_format"))
        if any(get(output_format, "type") == "json_schema" for output_format in output_formats):
            values["gen_ai.output.type"] = "json"
        values["anthropic.request.service_tier"] = get(body, "service_tier")
        thinking = get(body, "thinking")
        values["anthropic.thinking.type"] = get(thinking, "type")
        values["anthropic.thinking.budget_tokens"] = get(thinking, "budget_tokens")
        beta_header = request_header(client, extra_headers, "anthropic-beta") or ""
        betas = [beta.strip() for beta in beta_header.split(",") if beta.strip()]
        if betas:
            values["anthropic.beta"] = betas
    except Exception:
        log.debug("Could not read the request for its span", exc_info=True)
    return attributes(values)


def messages_count_tokens_request_attributes(client: BaseClient[Any, Any], body: object) -> dict[str, AttributeValue]:
    """The attributes that the span of a `messages.count_tokens` call starts with. Empty when `client` has no spans."""
    if client._tracer is None:
        return {}
    model = get(body, "model")
    return attributes({"gen_ai.request.model": model if isinstance(model, str) else None})


def sessions_create_request_attributes(body: object) -> dict[str, AttributeValue]:
    """The attributes that the span of a `sessions.create` call starts with, from the request's `body`.

    Read when the span starts, and never from a request whose client has no spans. Never raises.
    """
    agent = get(body, "agent")
    return attributes(
        {
            "gen_ai.agent.id": agent if isinstance(agent, str) else get(agent, "id"),
            "anthropic.session.environment.id": get(body, "environment_id"),
        }
    )


def request_header(client: BaseClient[Any, Any], extra_headers: Mapping[str, object] | None, name: str) -> str | None:
    """The value that the call's attempts send for the header `name`: the call's own, or else the client's default."""
    value: str | None = None
    layers: list[Mapping[str, object]] = [client.default_headers, extra_headers or {}]
    for layer in layers:
        for key, header in layer.items():
            if key.lower() == name:
                value = None if isinstance(header, Omit) else str(header)
    return value
