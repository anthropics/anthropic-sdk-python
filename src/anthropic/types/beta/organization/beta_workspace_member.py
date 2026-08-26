# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel
from .beta_workspace_role import BetaWorkspaceRole

__all__ = ["BetaWorkspaceMember"]


class BetaWorkspaceMember(BaseModel):
    type: Literal["workspace_member"]
    """Object type.

    For Workspace Members, this is always `"workspace_member"`.
    """

    user_id: str
    """ID of the User."""

    workspace_id: str
    """ID of the Workspace."""

    workspace_role: BetaWorkspaceRole
    """Role of the Workspace Member."""
