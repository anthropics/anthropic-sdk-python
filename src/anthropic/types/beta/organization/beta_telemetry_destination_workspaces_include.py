from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaTelemetryDestinationWorkspacesInclude"]


class BetaTelemetryDestinationWorkspacesInclude(BaseModel):
    """The destination covers the workspaces on its list, and no others."""

    type: Literal["include"]
