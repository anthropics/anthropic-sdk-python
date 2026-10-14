from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaTelemetryDestinationStateEnabled"]


class BetaTelemetryDestinationStateEnabled(BaseModel):
    """The telemetry destination receives the spans of the workspaces that it covers."""

    type: Literal["enabled"]
