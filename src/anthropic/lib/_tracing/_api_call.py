from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, cast

import httpx2
from opentelemetry import trace
from opentelemetry.util.types import AttributeValue

from ._utils import MessageCreateBody, get, as_dict
from ...types import Message
from ._content import set_message_content
from ._response import set_usage_sums
from ..._tracing import (
    ApiCallResult,
    StreamObserver,
    response_data,
    end_api_call_span,
    set_created_id_attribute,
    end_api_call_span_when_body_ends,
)
from ._streaming import StreamedMessage
from ._attributes import attributes
from ..._streaming import Stream, AsyncStream
from ...types.beta import BetaMessage

if TYPE_CHECKING:
    from ..._base_client import BaseClient

__all__ = [
    "finish_api_call_span",
    "messages_create_request_attributes",
    "sessions_create_request_attributes",
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
    """Sets the attributes of the call that are not read off its request or its response as they are. Never raises.

    Returns the observer that records a streamed Message as the application reads it, and `None` for any other result.
    """
    if not span.is_recording():
        return None
    try:
        set_created_id_attribute(span, result)
        # What to record follows from what the method says the call returns, which is also known when the call fails.
        returns: type[object] = result.cast_to if isinstance(result.cast_to, type) else object
        if issubclass(returns, (Message, BetaMessage)):
            return record_messages_create(client, span, result, returns)
        return None
    except Exception:
        log.debug("Could not record the API call on its span", exc_info=True)
        return None


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
            span_name=result.options.span_name,
            request_headers=request_headers,
            content=content,
            max_content_bytes=client._otel.max_content_bytes,
            start_time=result.start_time,
        )

    set_usage_sums(span, data, complete=True, iterations=issubclass(returns, BetaMessage))
    if content:
        set_message_content(span, body, get(data, "content"), limit=client._otel.max_content_bytes)
    return None


def messages_create_request_attributes(body: object) -> dict[str, AttributeValue]:
    """What the span of a `messages.create` call starts with that is not a field of the request's `body` as it is.

    Read when the span starts, and never from a request whose client has no spans. Never raises.
    """
    # `output_format` is the deprecated form of `output_config.format`.
    output_formats = (get(get(body, "output_config"), "format"), get(body, "output_format"))
    json_output = any(get(output_format, "type") == "json_schema" for output_format in output_formats)
    return attributes({"gen_ai.output.type": "json" if json_output else None})


def sessions_create_request_attributes(body: object) -> dict[str, AttributeValue]:
    """What the span of a `sessions.create` call starts with that is not a field of the request's `body` as it is.

    Read when the span starts, and never from a request whose client has no spans. Never raises.
    """
    agent = get(body, "agent")
    return attributes({"gen_ai.agent.id": agent if isinstance(agent, str) else get(agent, "id")})
