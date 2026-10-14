from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaTelemetryDestinationWorkspacesExclude"]


class BetaTelemetryDestinationWorkspacesExclude(BaseModel):
    """
    The destination covers every workspace of the organization except the workspaces on its list. A workspace created later is covered until it is added to the list.
    """

    type: Literal["exclude"]
