from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["UserProfileCyberTier"]


class UserProfileCyberTier(BaseModel):
    """One tier of the Cyber Verification Program."""

    status: Literal["active", "inactive"]
    """`active` when the tier applies to the profile, otherwise `inactive`.

    The response does not say why a tier is `inactive`: it can be in review,
    declined, withdrawn, never applied for, or approved but not applied to this
    profile.
    """
