from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypedDict

__all__ = ["BetaUserProfileExternalUserDetailsParams"]


class BetaUserProfileExternalUserDetailsParams(TypedDict, total=False):
    account_status: Optional[Literal["active", "suspended", "blocked"]]
    """
    The status of the entity's account on the platform: `active`, `suspended` or
    `blocked`.

    - `active` - The platform has neither restricted nor barred the account of the
      entity that the user profile represents.
    - `suspended` - The platform has restricted the account of the entity that the
      user profile represents and may restore it.
    - `blocked` - The platform has barred the account of the entity that the user
      profile represents.
    """

    country: Optional[str]
    """
    The country of the entity (not of the platform), as the platform determines it:
    an ISO 3166-1 alpha-2 code in upper case, for example `US`. Only the form, two
    uppercase ASCII letters, is checked.
    """

    email_hash: Optional[str]
    """A hash of the entity's email address, computed by the platform.

    Anthropic treats it as an opaque string and does not prescribe the hash
    function. 1 to 255 characters.
    """

    entity_type: Optional[Literal["individual", "business", "non_profit", "government"]]
    """
    What kind of entity the profile represents: `individual`, `business`,
    `non_profit` or `government`.
    """

    name_hash: Optional[str]
    """A hash of the entity's name, computed by the platform.

    Anthropic treats it as an opaque string and does not prescribe the hash
    function. 1 to 255 characters.
    """

    onboarded_at: Union[str, datetime]
    """
    When the entity opened its account with the platform, in RFC 3339 format: for an
    `application` profile, when the end-user signed up; for a `passthrough` profile,
    when the company became the platform's customer. Must be a complete timestamp no
    more than 1 minute in the future.
    """

    reference_id: Optional[str]
    """
    The platform's own reference for the entity, for example the key of the
    end-user's row in the platform's database. Not interpreted by Anthropic and not
    enforced unique. 1 to 255 characters.
    """
