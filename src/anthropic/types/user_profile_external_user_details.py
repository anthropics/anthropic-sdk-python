from typing import Optional
from datetime import datetime

from .._models import BaseModel
from .user_profile_external_user_entity_type import UserProfileExternalUserEntityType
from .user_profile_external_user_account_status import UserProfileExternalUserAccountStatus

__all__ = ["UserProfileExternalUserDetails"]


class UserProfileExternalUserDetails(BaseModel):
    """Details about the entity this profile represents, as the platform states them.

    Anthropic does not verify them. Every field is present, `null` until the platform supplies a value.
    """

    account_status: Optional[UserProfileExternalUserAccountStatus] = None
    """
    The status of the entity's account on the platform: `active`, `suspended` or
    `blocked`. `null` until the platform supplies one.
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

    entity_type: Optional[UserProfileExternalUserEntityType] = None
    """
    What kind of entity the profile represents: `individual`, `business`,
    `non_profit` or `government`. `null` until the platform supplies one.
    """

    name_hash: Optional[str] = None
    """The platform-computed hash of the entity's name.

    `null` until the platform supplies one.
    """

    onboarded_at: Optional[datetime] = None
    """
    When the entity opened its account with the platform, as stated by the platform,
    in RFC 3339 format (UTC). `null` until the platform supplies one.
    """

    reference_id: Optional[str] = None
    """The platform's own reference for the entity.

    `null` until the platform supplies one.
    """
