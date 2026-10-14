from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaDeletedTelemetryDestinationWorkspace"]


class BetaDeletedTelemetryDestinationWorkspace(BaseModel):
    """Confirmation that a workspace was removed from a destination's list."""

    telemetry_destination_id: str
    """ID of the telemetry destination (`tdst_...`)."""

    type: Literal["telemetry_destination_workspace_deleted"]

    workspace_id: str
    """ID of the workspace that was removed (`wrkspc_...`)."""
