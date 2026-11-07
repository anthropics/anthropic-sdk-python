from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaUserProfileTrustGrant"]


class BetaUserProfileTrustGrant(BaseModel):
    """
    The status of one trust grant on a user profile, listed in the profile's `trust_grants` map under the grant's name.
    """

    status: Literal["active", "pending", "rejected"]
    """Status of the trust grant."""
