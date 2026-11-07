from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .user_profile_enforcement_action_reason import UserProfileEnforcementActionReason
from .user_profile_enforcement_action_next_step import UserProfileEnforcementActionNextStep

__all__ = ["UserProfileEnforcementActionRestriction"]


class UserProfileEnforcementActionRestriction(BaseModel):
    """Anthropic has limited how it serves the end user until the action is resolved.

    The end user may still be served in part.
    """

    id: str
    """The action's ID (`enac_...`), stable while the action is open."""

    action: Optional[UserProfileEnforcementActionNextStep] = None
    """The next step on the action: `verify` or `null`.

    `verify`: the end user can clear it now by passing an identity check. `null`:
    there is nothing the end user can do now to clear it, including while Anthropic
    reviews an identity check the end user submitted.
    """

    expires_at: Optional[datetime] = None
    """
    When the action ends on its own, in RFC 3339 format; it stops showing once this
    time has passed. `null` when it has no end date, and always `null` when `reason`
    is `account_compromise`.
    """

    opened_at: datetime
    """When Anthropic opened the action, in RFC 3339 format."""

    reason: UserProfileEnforcementActionReason
    """
    Why Anthropic placed the limit: `unsupported_region`, `fraud_or_abuse`,
    `high_harm`, `usage_policy_violation`, `account_compromise` or `unspecified`.
    """

    type: Literal["restriction"]
