from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .user_profile_enforcement_action_reason import UserProfileEnforcementActionReason
from .user_profile_enforcement_action_next_step import UserProfileEnforcementActionNextStep

__all__ = ["UserProfileEnforcementActionBan"]


class UserProfileEnforcementActionBan(BaseModel):
    """
    Anthropic has stopped serving the end user where the ban applies and does not plan to serve them there again.
    """

    id: str
    """The action's ID (`enac_...`), stable while the action is open."""

    action: Optional[UserProfileEnforcementActionNextStep] = None
    """Always `null`: the end user cannot clear a ban."""

    expires_at: Optional[datetime] = None
    """Always `null`: a ban has no end date."""

    opened_at: datetime
    """When Anthropic opened the action, in RFC 3339 format."""

    reason: UserProfileEnforcementActionReason
    """
    Why Anthropic placed the limit: `unsupported_region`, `fraud_or_abuse`,
    `high_harm`, `usage_policy_violation`, `account_compromise` or `unspecified`.
    """

    type: Literal["ban"]
