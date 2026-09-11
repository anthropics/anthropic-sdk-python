from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["BetaUserProfileExternalUserDetailsParams"]


class BetaUserProfileExternalUserDetailsParams(TypedDict, total=False):
    account_status: Optional[Literal["active", "suspended", "blocked"]]
    """
    The status of the entity's account on the platform, as the platform states it:
    `active`; `suspended`, when the platform has restricted the account and may
    restore it; or `blocked`, when the platform has barred it. It records the
    platform's decision only; the statuses in `trust_grants` are Anthropic's and do
    not follow it.
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
    What kind of entity the profile represents, as the platform states it:
    `individual`, `business`, `non_profit` or `government`.
    """

    name_hash: Optional[str]
    """A hash of the entity's name, computed by the platform.

    Anthropic treats it as an opaque string and does not prescribe the hash
    function. 1 to 255 characters.
    """

    onboarded_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """A timestamp in RFC 3339 format"""

    reference_id: Optional[str]
    """
    The platform's own reference for the entity, for example the key of the
    end-user's row in the platform's database. Not interpreted by Anthropic and not
    enforced unique. 1 to 255 characters.
    """
