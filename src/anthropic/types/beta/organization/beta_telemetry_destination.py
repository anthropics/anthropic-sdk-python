from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_telemetry_destination_state import BetaTelemetryDestinationState
from .beta_telemetry_destination_traces import BetaTelemetryDestinationTraces
from .beta_telemetry_destination_workspaces import BetaTelemetryDestinationWorkspaces
from .beta_telemetry_destination_delivery_health import BetaTelemetryDestinationDeliveryHealth

__all__ = ["BetaTelemetryDestination"]


class BetaTelemetryDestination(BaseModel):
    """
    An OpenTelemetry destination: an OTLP/HTTP endpoint, the request headers sent with every delivery to it, what the exported spans contain, and which workspaces it covers. A destination belongs to an organization. A workspace's spans go to every enabled destination that covers it.
    """

    id: str
    """The unique ID of the destination (`tdst_...`)."""

    created_at: datetime
    """Time the destination was created."""

    delivery_health: BetaTelemetryDestinationDeliveryHealth
    """The most recent delivery results for this destination."""

    display_name: Optional[str] = None
    """Human-readable name for the destination. Null when none was set."""

    endpoint_url: str
    """The base URL of the destination's OTLP/HTTP endpoint, exactly as registered.

    The API appends the per-signal path, such as `/v1/traces`, on delivery, unless
    `traces.endpoint_url` is set.
    """

    header_names: List[str]
    """Names of the registered request headers.

    Header values are write-only and are never returned.
    """

    state: BetaTelemetryDestinationState
    """Whether the destination receives deliveries."""

    traces: BetaTelemetryDestinationTraces
    """The destination's settings for the traces it receives."""

    type: Literal["telemetry_destination"]

    updated_at: datetime
    """Time of the last change to the destination's configuration or state.

    Changes to `delivery_health` don't change it.

    An update that sets a header value always changes it, even when the value is the
    same as before. Adding or removing a single workspace on the destination's list
    doesn't change it. An update that changes the list does.
    """

    workspaces: BetaTelemetryDestinationWorkspaces
    """Which of the organization's workspaces the destination covers."""
