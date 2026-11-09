from typing_extensions import Literal

from ..._models import BaseModel
from .workspace_role import WorkspaceRole

__all__ = ["WorkspaceMember"]


class WorkspaceMember(BaseModel):
    type: Literal["workspace_member"]
    """Object type.

    For Workspace Members, this is always `"workspace_member"`.
    """

    user_id: str
    """ID of the User."""

    workspace_id: str
    """ID of the Workspace."""

    workspace_role: WorkspaceRole
    """Role of the Workspace Member."""
