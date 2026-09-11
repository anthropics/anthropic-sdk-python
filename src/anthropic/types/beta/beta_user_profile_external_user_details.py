from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaUserProfileExternalUserDetails"]


class BetaUserProfileExternalUserDetails(BaseModel):
    """Details about the entity this profile represents, as the platform states them.

    Anthropic does not verify them. Every field is present, `null` until the platform supplies a value.
    """

    account_status: Optional[Literal["active", "suspended", "blocked"]] = None
    """
    The status of the entity's account on the platform, as the platform states it:
    `active`; `suspended`, when the platform has restricted the account and may
    restore it; or `blocked`, when the platform has barred it. It records the
    platform's decision only; the statuses in `trust_grants` are Anthropic's and do
    not follow it.
    """

    country: Optional[str] = None
    """
    The country the platform associates with the entity, as an ISO 3166-1 alpha-2
    code. `null` until the platform supplies one.
    """

    email_hash: Optional[str] = None
    """The platform-computed hash of the entity's email address.

    `null` until the platform supplies one.
    """

    entity_type: Optional[Literal["individual", "business", "non_profit", "government"]] = None
    """
    What kind of entity the profile represents, as the platform states it:
    `individual`, `business`, `non_profit` or `government`.
    """

    name_hash: Optional[str] = None
    """The platform-computed hash of the entity's name.

    `null` until the platform supplies one.
    """

    onboarded_at: Optional[datetime] = None
    """A timestamp in RFC 3339 format"""

    reference_id: Optional[str] = None
    """The platform's own reference for the entity.

    `null` until the platform supplies one.
    """
