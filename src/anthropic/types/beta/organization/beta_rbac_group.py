from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaRBACGroup"]


class BetaRBACGroup(BaseModel):
    id: str
    """ID of the RBAC Group."""

    created_at: datetime
    """RFC 3339 timestamp of when the RBAC Group was created."""

    name: str
    """Name of the RBAC Group. Not uniqueness-enforced."""

    role_ids: Optional[List[str]] = None
    """RBAC Role IDs attached to this RBAC Group.

    Role attachment is managed in the admin settings and is read-only on this API.
    `null` means role data was temporarily unavailable — retry to distinguish from
    an empty list.
    """

    source_type: Literal["direct", "scim"]
    """
    How the RBAC Group was created: `"direct"` for groups created directly (for
    example, in the organization's admin settings), `"scim"` for groups provisioned
    by the identity provider.
    """

    type: Literal["rbac_group"]
    """Object type.

    For RBAC Groups, this is always `"rbac_group"`.
    """

    updated_at: datetime
    """RFC 3339 timestamp of when the RBAC Group was last updated."""
