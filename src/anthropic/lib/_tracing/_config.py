from __future__ import annotations

from opentelemetry.util.types import AttributeValue

from ... import _tracing
from ..._types import ResolvedOpenTelemetryOptions
from ._attributes import attributes

__all__ = ["OpenTelemetryConfig"]


class OpenTelemetryConfig:
    """What a client's `open_telemetry` option says about its spans, once `resolve_open_telemetry` has resolved it."""

    def __init__(
        self, options: ResolvedOpenTelemetryOptions, *, provider_name: str, platform: str | None = None
    ) -> None:
        self.provider_name = provider_name
        self.conversation_id = options.get("conversation_id")
        self.max_content_bytes = options["traces"]["max_content_bytes"]
        self._content_mode = options["traces"]["content_mode"]
        self._platform = platform

    @property
    def records_content(self) -> bool:
        return self._content_mode == "content"

    @property
    def instrumentation_scope(self) -> str:
        """The scope of the client's tracer: the SDK's name, and for a platform client the platform after it."""
        if self._platform is None:
            return _tracing.INSTRUMENTATION_SCOPE
        return f"{_tracing.INSTRUMENTATION_SCOPE}.{self._platform}"

    def api_call_start_attributes(self) -> dict[str, AttributeValue]:
        """The attributes that the span of every API call starts with, so that a sampler sees them."""
        return attributes({"gen_ai.provider.name": self.provider_name, "gen_ai.conversation.id": self.conversation_id})
