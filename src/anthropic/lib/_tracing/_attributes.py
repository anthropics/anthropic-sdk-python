from __future__ import annotations

from collections.abc import Mapping
from typing_extensions import Literal, Protocol

from opentelemetry.util.types import AttributeValue

from ..._utils import is_list

__all__ = ["AttributeName", "AnthropicSpan", "attributes", "count"]

AttributeName = Literal[
    "gen_ai.agent.id",
    "gen_ai.conversation.id",
    "gen_ai.input.messages",
    "gen_ai.operation.name",
    "gen_ai.output.messages",
    "gen_ai.output.type",
    "gen_ai.provider.name",
    "gen_ai.request.model",
    "gen_ai.request.stop_sequences",
    "gen_ai.response.time_to_first_chunk",
    "gen_ai.system_instructions",
    "gen_ai.tool.call.arguments",
    "gen_ai.tool.call.id",
    "gen_ai.tool.description",
    "gen_ai.tool.name",
    "gen_ai.tool.type",
    "gen_ai.usage.input_tokens",
    "anthropic.content.truncated",
    "anthropic.environment.id",
    "anthropic.environment.work.id",
    "anthropic.message.batch.request_count",
    "anthropic.session.id",
    "anthropic.session.thread.id",
    "anthropic.tool_result.content",
    "anthropic.toolset.name",
    "anthropic.usage.compaction.input_tokens",
    "anthropic.usage.compaction.output_tokens",
]


class AnthropicSpan(Protocol):
    """An OpenTelemetry span that takes only an `AttributeName`, so that a misspelled attribute is a type error."""

    def set_attribute(self, key: AttributeName, value: AttributeValue) -> None: ...


def attributes(values: Mapping[AttributeName, AttributeValue | None]) -> dict[str, AttributeValue]:
    """The attributes to start a span with: `values` without those that are `None`."""
    return {key: value for key, value in values.items() if value is not None}


def count(value: object) -> int | None:
    """How many items the list `value` has, and `None` for anything else, such as a list that the request lacks."""
    return len(value) if is_list(value) else None
