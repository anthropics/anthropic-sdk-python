from __future__ import annotations

import time
import logging
from typing import cast
from collections.abc import Sequence

from ._utils import get
from ..._utils import is_dict, is_list
from ..._models import BaseModel
from ._attributes import AnthropicSpan

__all__ = ["FINAL_FROM_MESSAGE_DELTA", "without_message_delta_fields", "set_usage_sums", "set_time_to_first_chunk"]

log: logging.Logger = logging.getLogger(__name__)


def set_time_to_first_chunk(span: AnthropicSpan, start_time: int) -> None:
    span.set_attribute("gen_ai.response.time_to_first_chunk", (time.time_ns() - start_time) / 1e9)


FINAL_FROM_MESSAGE_DELTA: tuple[tuple[str, ...], ...] = (
    ("stop_reason",),
    ("usage", "output_tokens"),
    ("usage", "output_tokens_details"),
)
"""The paths in a streamed Message whose values are final only from its `message_delta` on.

`message_start` has placeholders for them, so the span of a stream that ended before `message_delta` records
nothing under them.
"""


def without_message_delta_fields(message: BaseModel) -> dict[str, object]:
    """The fields of the streamed `message` without what is under `FINAL_FROM_MESSAGE_DELTA`.

    Until that event the snapshot has what `message_start` put there, which is not the Message's own.
    """
    fields: dict[str, object] = dict(message)
    for path in FINAL_FROM_MESSAGE_DELTA:
        fields = without(fields, path)
    return fields


def set_usage_sums(span: AnthropicSpan, message: object, *, complete: bool, iterations: bool) -> None:
    """Sets the usage attributes that are sums of fields of `message`, a Message as a model or as a decoded body.

    The compaction sums need `complete`, because a streamed Message has its iterations from its `message_delta`,
    and `iterations`, because only the beta usage has them.

    Never raises: nothing validates a response against its type unless the client is told to, so a
    field can be missing or of another type.
    """
    try:
        usage = get(message, "usage")
        input_tokens = get(usage, "input_tokens")
        if isinstance(input_tokens, int):
            cached = tokens(usage, "cache_read_input_tokens") + tokens(usage, "cache_creation_input_tokens")
            span.set_attribute("gen_ai.usage.input_tokens", input_tokens + cached)
        if not (complete and iterations):
            return

        # The usage above leaves out the tokens of the compactions.
        entries = get(usage, "iterations")
        compactions = [entry for entry in entries if get(entry, "type") == "compaction"] if is_list(entries) else []
        if not compactions:
            return
        span.set_attribute(
            "anthropic.usage.compaction.input_tokens",
            sum(
                tokens(entry, "input_tokens")
                + tokens(entry, "cache_read_input_tokens")
                + tokens(entry, "cache_creation_input_tokens")
                for entry in compactions
            ),
        )
        span.set_attribute(
            "anthropic.usage.compaction.output_tokens", sum(tokens(entry, "output_tokens") for entry in compactions)
        )
    except Exception:
        log.debug("Could not record the usage of the response on its span", exc_info=True)


def tokens(usage: object, field: str) -> int:
    count = get(usage, field)
    return count if isinstance(count, int) else 0


def without(fields: dict[str, object], path: Sequence[str]) -> dict[str, object]:
    """`fields` without the value at `path`, as a copy that shares what the path does not go through."""
    name, *rest = path
    if name not in fields:
        return fields
    if not rest:
        return {key: value for key, value in fields.items() if key != name}
    value = fields[name]
    if isinstance(value, BaseModel) or is_dict(value):
        return {**fields, name: without(cast("dict[str, object]", dict(value)), rest)}
    return fields
