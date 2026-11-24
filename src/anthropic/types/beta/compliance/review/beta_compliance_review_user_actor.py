from typing import Optional
from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaComplianceReviewUserActor"]


class BetaComplianceReviewUserActor(BaseModel):
    """A signed-in user."""

    email_address: Optional[str] = None
    """The user's email address.

    Set only for a current member of an organization that the API key can read.
    """

    type: Literal["user_actor"]

    user_id: str
    """The ID of the user (`user_...`)."""
