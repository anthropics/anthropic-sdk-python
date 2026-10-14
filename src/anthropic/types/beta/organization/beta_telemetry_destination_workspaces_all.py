from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaTelemetryDestinationWorkspacesAll"]


class BetaTelemetryDestinationWorkspacesAll(BaseModel):
    """
    The destination covers every workspace of the organization, including the default workspace, archived workspaces, and workspaces created later. It doesn't have a list.
    """

    type: Literal["all"]
