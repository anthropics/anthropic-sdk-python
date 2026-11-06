from typing import Optional

from ...._models import BaseModel
from .beta_telemetry_destination_content_mode import BetaTelemetryDestinationContentMode

__all__ = ["BetaTelemetryDestinationTraces"]


class BetaTelemetryDestinationTraces(BaseModel):
    """A telemetry destination's settings for the traces it receives."""

    content_mode: BetaTelemetryDestinationContentMode
    """What the exported spans contain."""

    enabled: bool
    """Whether the destination receives traces.

    A destination whose `enabled` is false keeps its other settings.
    """

    endpoint_url: Optional[str] = None
    """
    The full URL that the API posts traces to, exactly as registered, or `null` if
    the destination doesn't have one.

    When it is `null`, the API posts traces to `endpoint_url` with `/v1/traces`
    appended.
    """

    max_content_bytes: Optional[int] = None
    """
    The most bytes of content that one exported span can contain, or `null` if only
    the API's maximum applies.

    Content means model prompts and responses, and tool inputs and outputs. The API
    shortens longer content to this size before it delivers the span. A destination
    whose `content_mode` is `metadata_only` keeps this value. It applies once
    `content_mode` is `content`.
    """
