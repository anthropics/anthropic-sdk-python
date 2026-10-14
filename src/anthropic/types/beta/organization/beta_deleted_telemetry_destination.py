from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaDeletedTelemetryDestination"]


class BetaDeletedTelemetryDestination(BaseModel):
    """Confirmation that a destination was deleted."""

    id: str
    """ID of the deleted destination (`tdst_...`)."""

    type: Literal["telemetry_destination_deleted"]
