from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .workspace_role import WorkspaceRole

__all__ = ["ServiceAccountWorkspaceMember"]


class ServiceAccountWorkspaceMember(BaseModel):
    created_by_actor_id: Optional[str] = None
    """Tagged ID (`user_...`/`svac_...`) of the actor who created this membership."""

    implicit: Optional[bool] = None
    """
    True when this is the implicit default-workspace membership every service
    account has when no explicit membership exists. Implicit memberships have role
    `workspace_user` and cannot be removed.
    """

    service_account_id: str
    """Tagged service account ID (`svac_...`)."""

    type: Literal["service_account_workspace_member"]

    workspace_id: str
    """Tagged workspace ID (`wrkspc_...`)."""

    workspace_role: WorkspaceRole
    """Role of the service account in this workspace.

    Service accounts cannot hold the `workspace_billing` role.
    """
