from __future__ import annotations

import time
import logging
from typing import TypeVar, cast

from ...types import Message
from ..._utils import is_dict
from ..._models import BaseModel, construct_type_unchecked
from ..._tracing import ApiCallResult
from ..._response import BaseAPIResponse
from ._attributes import AnthropicSpan
from ...types.beta import BetaUsage, BetaMessage

__all__ = ["response_data", "as_model", "set_response", "set_time_to_first_chunk"]

_ModelT = TypeVar("_ModelT", bound=BaseModel)

log: logging.Logger = logging.getLogger(__name__)


def response_data(result: ApiCallResult) -> object:
    """What an API call's response gave: the parsed body or the stream, or the decoded body of a raw response.

    `.with_streaming_response` has not read its body, so that gives `None`.
    """
    data = result.data
    if isinstance(data, BaseAPIResponse):
        raw = cast("BaseAPIResponse[object]", data)
        return json_body(raw) if raw.http_response.is_closed else None
    return data


def json_body(raw: BaseAPIResponse[object]) -> object:
    response = raw.http_response
    media_type = response.headers.get("content-type", "").split(";")[0].strip().lower()
    if media_type != "application/json":
        return None
    try:
        return response.json()
    except Exception:
        log.debug("Could not decode the response body for its span", exc_info=True)
        return None


def as_model(data: object, model: type[_ModelT], *, without: str | None = None) -> _ModelT | None:
    """`data` as a `model`: itself when it is one, and the `model` built from it when it is a decoded body.

    The list in the body's `without` field is left out, because building a Message's content costs far
    more than the rest.
    """
    if isinstance(data, model):
        return data
    if not is_dict(data):
        return None
    body: dict[object, object] = {**data, without: []} if without is not None else data
    return construct_type_unchecked(type_=model, value=body)


def set_time_to_first_chunk(span: AnthropicSpan, start_time: int) -> None:
    span.set_attribute("gen_ai.response.time_to_first_chunk", (time.time_ns() - start_time) / 1e9)


def set_response(span: AnthropicSpan, message: Message | BetaMessage, *, complete: bool) -> None:
    """Sets the attributes that come from a Message.

    The stop reason and the output usage need `complete`: a streamed Message has them from its `message_delta`.

    Never raises: nothing validates a response against its type unless the client is told to, so a
    field can be missing or of another type.
    """
    try:
        set_message_attributes(span, message, complete=complete)
    except Exception:
        log.debug("Could not record the response on its span", exc_info=True)


def set_message_attributes(span: AnthropicSpan, message: Message | BetaMessage, *, complete: bool) -> None:
    span.set_attribute("gen_ai.response.id", message.id)
    span.set_attribute("gen_ai.response.model", message.model)
    if complete and message.stop_reason is not None:
        span.set_attribute("anthropic.message.stop_reason", message.stop_reason)

    usage = message.usage
    cached = (usage.cache_read_input_tokens or 0) + (usage.cache_creation_input_tokens or 0)
    span.set_attribute("gen_ai.usage.input_tokens", usage.input_tokens + cached)
    if usage.cache_creation_input_tokens is not None:
        span.set_attribute("gen_ai.usage.cache_write.input_tokens", usage.cache_creation_input_tokens)
    if usage.cache_read_input_tokens is not None:
        span.set_attribute("gen_ai.usage.cache_read.input_tokens", usage.cache_read_input_tokens)
    if usage.cache_creation is not None:
        span.set_attribute(
            "anthropic.usage.cache_creation.ephemeral_5m_input_tokens", usage.cache_creation.ephemeral_5m_input_tokens
        )
        span.set_attribute(
            "anthropic.usage.cache_creation.ephemeral_1h_input_tokens", usage.cache_creation.ephemeral_1h_input_tokens
        )
    if usage.service_tier is not None:
        span.set_attribute("anthropic.response.service_tier", usage.service_tier)
    if not complete:
        return

    span.set_attribute("gen_ai.usage.output_tokens", usage.output_tokens)
    if usage.output_tokens_details is not None:
        span.set_attribute("gen_ai.usage.reasoning.output_tokens", usage.output_tokens_details.thinking_tokens)

    # Only the beta usage has the iterations. The usage above leaves out the tokens of their compactions.
    if not isinstance(usage, BetaUsage) or not usage.iterations:
        return
    compactions = [entry for entry in usage.iterations if entry.type == "compaction"]
    if not compactions:
        return
    cached = sum(entry.cache_read_input_tokens + entry.cache_creation_input_tokens for entry in compactions)
    span.set_attribute(
        "anthropic.usage.compaction.input_tokens", sum(entry.input_tokens for entry in compactions) + cached
    )
    span.set_attribute("anthropic.usage.compaction.output_tokens", sum(entry.output_tokens for entry in compactions))
