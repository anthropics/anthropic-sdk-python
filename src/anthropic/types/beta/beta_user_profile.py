from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_user_profile_trust_grant import BetaUserProfileTrustGrant
from .beta_user_profile_external_user_details import BetaUserProfileExternalUserDetails

__all__ = ["BetaUserProfile"]


class BetaUserProfile(BaseModel):
    id: str
    """Unique identifier for this user profile, prefixed `uprof_`."""

    created_at: datetime
    """A timestamp in RFC 3339 format"""

    metadata: Dict[str, str]
    """Arbitrary key-value metadata.

    Maximum 16 pairs, keys up to 64 chars, values up to 512 chars.
    """

    trust_grants: Dict[str, BetaUserProfileTrustGrant]
    """Trust grants for this profile, keyed by grant name.

    Key omitted when no grant is active or in flight.
    """

    type: Literal["user_profile"]
    """Object type. Always `user_profile`."""

    updated_at: datetime
    """A timestamp in RFC 3339 format"""

    access_type: Optional[Literal["application", "passthrough"]] = None
    """How the platform uses the API on behalf of the entity this profile represents.

    `application`: the platform sells a product that uses the API behind the scenes,
    and the profile represents an individual end-user of that product.
    `passthrough`: the platform resells raw inference, and the profile identifies
    the resold-to company.
    """

    external_id: Optional[str] = None
    """Platform's own identifier for this user.

    Not enforced unique. Present under the `user-profiles-2026-03-24` and
    `user-profiles-2026-08-18` beta headers; under `user-profiles-2026-09-04` the
    value is `external_user_details.reference_id`.
    """

    external_user_details: Optional[BetaUserProfileExternalUserDetails] = None
    """Details about the entity this profile represents, as the platform states them.

    Anthropic does not verify them. Every field is present, `null` until the
    platform supplies a value.
    """

    external_user_onboarded_at: Optional[datetime] = None
    """A timestamp in RFC 3339 format"""

    name: Optional[str] = None
    """Real-world name of the entity this profile represents (company or individual).

    For a company the platform resells Claude access to (`access_type`
    `passthrough`) this is that company's name.
    """
