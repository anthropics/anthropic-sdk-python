from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsWorkspaceArchivedRunErrorObject"]


class BetaManagedAgentsWorkspaceArchivedRunErrorObject(BaseModel):
    """The deployment's workspace was archived."""

    message: str
    """Human-readable error description."""

    type: Literal["workspace_archived_error"]
