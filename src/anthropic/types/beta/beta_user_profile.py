from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_user_profile_trust_grant import BetaUserProfileTrustGrant
from .beta_user_profile_external_user_details import BetaUserProfileExternalUserDetails

__all__ = ["BetaUserProfile"]


class BetaUserProfile(BaseModel):
    """
    A record of an entity that the platform serves through the API, such as an end-user of the platform's product or a company that the platform resells Claude access to.

    A Messages, Message Batches or token counting request can send a profile's `id` in the `anthropic-user-profile-id` header to attribute the request to that entity.
    """

    id: str
    """Unique identifier for this user profile, prefixed `uprof_`."""

    created_at: datetime
    """When this user profile was created, in RFC 3339 format."""

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

    trust_grants: Dict[str, BetaUserProfileTrustGrant]
    """Trust grants for this profile, keyed by grant name.

    Key omitted when no grant is active or in flight.
    """

    type: Literal["user_profile"]
    """Object type. Always `user_profile`."""

    updated_at: datetime
    """When this user profile was last modified, in RFC 3339 format.

    It normally also updates shortly after Anthropic gives the profile an approval
    or withdraws one. Other changes to the statuses that Anthropic reports do not
    always update it, so read the status itself rather than watching this timestamp.
    """

    access_type: Optional[Literal["application", "passthrough"]] = None
    """
    How the platform uses the API for this entity: `application` (default) or
    `passthrough`. Absent under the legacy `user-profiles-2026-03-24` beta header.

    - `application` - The user profile represents an individual end-user of a
      product that the platform builds on the API. New profiles get this value by
      default.
    - `passthrough` - The user profile represents a company that the platform
      resells Claude access to.
    """

    external_id: Optional[str] = None
    """Platform's own identifier for this user.

    Not enforced unique. Legacy field, present only under the
    `user-profiles-2026-03-24` and `user-profiles-2026-08-18` beta headers; without
    one of them, the value is `external_user_details.reference_id`.
    """

    external_user_details: Optional[BetaUserProfileExternalUserDetails] = None
    """
    Details about the entity this profile represents, as the platform states them;
    not verified by Anthropic. Every field is present, `null` until the platform
    supplies a value. Absent under the legacy `user-profiles-2026-03-24` and
    `user-profiles-2026-08-18` beta headers, which serve `reference_id` as the
    top-level `external_id` and, under `user-profiles-2026-08-18`, `onboarded_at` as
    `external_user_onboarded_at`.
    """

    external_user_onboarded_at: Optional[datetime] = None
    """
    When the entity this profile represents opened its account with the platform, as
    stated by the platform, in RFC 3339 format (UTC). `null` until the platform
    supplies one. Legacy field, present only under the `user-profiles-2026-08-18`
    beta header; without a legacy header, the value is
    `external_user_details.onboarded_at`.
    """
