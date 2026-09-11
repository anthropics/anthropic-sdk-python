from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaUserProfileTrustGrant"]


class BetaUserProfileTrustGrant(BaseModel):
    status: Literal["active", "pending", "rejected"]
    """Status of the trust grant."""
