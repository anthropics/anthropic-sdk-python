from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaPluginTargetOrganizationMember"]


class BetaPluginTargetOrganizationMember(BaseModel):
    type: Literal["organization_member"]
    """One member of the organization."""

    user_id: str
    """The member's User ID."""
