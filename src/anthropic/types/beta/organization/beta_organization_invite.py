# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from ..beta_organization_role import BetaOrganizationRole

__all__ = ["BetaOrganizationInvite"]


class BetaOrganizationInvite(BaseModel):
    id: str
    """ID of the Invite."""

    accepted_at: Optional[datetime] = None
    """RFC 3339 datetime string indicating when the Invite was accepted, or null."""

    email: str
    """Email of the User being invited."""

    expires_at: datetime
    """RFC 3339 datetime string indicating when the Invite expires."""

    invited_at: datetime
    """RFC 3339 datetime string indicating when the Invite was created."""

    rbac_group_ids: List[str]
    """
    RBAC group IDs recorded on the Invite (Claude Enterprise organizations), to be
    assigned to the User when the Invite is accepted. `[]` when none.
    """

    role: BetaOrganizationRole
    """Organization role of the User."""

    status: Literal["accepted", "deleted", "expired", "pending"]
    """Status of the Invite."""

    type: Literal["invite"]
    """Object type.

    For Invites, this is always `"invite"`.
    """
