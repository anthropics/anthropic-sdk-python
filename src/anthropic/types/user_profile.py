from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .user_profile_programs import UserProfilePrograms
from .user_profile_access_type import UserProfileAccessType
from .user_profile_enforcement_action import UserProfileEnforcementAction
from .user_profile_enforcement_status import UserProfileEnforcementStatus
from .user_profile_external_user_details import UserProfileExternalUserDetails

__all__ = ["UserProfile"]


class UserProfile(BaseModel):
    """
    A record of an entity that the platform serves through the API, such as an end-user of the platform's product or a company that the platform resells Claude access to.

    A Messages, Message Batches or token counting request can send a profile's `id` in the `anthropic-user-profile-id` header to attribute the request to that entity.
    """

    id: str
    """Unique identifier for this user profile, prefixed `uprof_`."""

    access_type: UserProfileAccessType
    """
    How the platform uses the API for this entity: `application` (default) or
    `passthrough`. Absent under the legacy `user-profiles-2026-03-24` beta header.
    """

    created_at: datetime
    """When this user profile was created, in RFC 3339 format."""

    enforcement_actions: List[UserProfileEnforcementAction]
    """The enforcement actions open on this profile; empty when none is open.

    Absent under the `user-profiles-2026-09-04` and earlier beta headers.
    """

    enforcement_status: UserProfileEnforcementStatus
    """
    Anthropic's enforcement status of this profile, from its open enforcement
    actions and any identity check under review, by the first rule that applies:
    `banned` while any open action is a `ban`; `pending` while a restriction that an
    identity check can clear is open, the end user has submitted that check,
    Anthropic's review of it has not ended, and no open action's `reason` is
    `account_compromise`; `restricted` while any action is open; `unrestricted`
    while none is. Absent under the `user-profiles-2026-09-04` and earlier beta
    headers.
    """

    external_user_details: UserProfileExternalUserDetails
    """
    Details about the entity this profile represents, as the platform states them;
    not verified by Anthropic. Every field is present, `null` until the platform
    supplies a value. Absent under the legacy `user-profiles-2026-03-24` and
    `user-profiles-2026-08-18` beta headers, which serve `reference_id` as the
    top-level `external_id` and, under `user-profiles-2026-08-18`, `onboarded_at` as
    `external_user_onboarded_at`.
    """

    metadata: Dict[str, str]
    """Arbitrary key-value metadata.

    Maximum 16 pairs, keys up to 64 chars, values up to 512 chars.
    """

    name: Optional[str] = None
    """Real-world name of the entity this profile represents (company or individual).

    For a company the platform resells Claude access to (`access_type`
    `passthrough`) this is that company's name. `null` until the platform supplies
    one.
    """

    programs: UserProfilePrograms
    """
    The profile's standing in each Anthropic program, such as the Cyber Verification
    Program. Present when the request sends no user-profiles beta header; absent
    under the `user-profiles-2026-09-04` and earlier beta headers, which serve
    `trust_grants` instead.
    """

    type: Literal["user_profile"]
    """Object type. Always `user_profile`."""

    updated_at: datetime
    """When this user profile was last modified, in RFC 3339 format.

    It normally also updates shortly after Anthropic gives the profile an approval
    or withdraws one. Other changes to the statuses that Anthropic reports do not
    always update it, so read the status itself rather than watching this timestamp.
    """
