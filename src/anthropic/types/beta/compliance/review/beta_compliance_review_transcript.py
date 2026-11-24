from typing import Optional

from ....._models import BaseModel

__all__ = ["BetaComplianceReviewTranscript"]


class BetaComplianceReviewTranscript(BaseModel):
    """One flagged message of a review case."""

    item_id: str
    """The ID of the flagged message."""

    user_profile_id: Optional[str] = None
    """The ID of the user profile that the message belongs to.

    Null when the message belongs to none, or when the profile can no longer be
    looked up.
    """
