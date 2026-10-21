from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAnalyticsUser"]


class BetaAnalyticsUser(BaseModel):
    """A user in the organization, identified by tagged id and email address."""

    id: str
    """Tagged user identifier (e.g. `user_...`)"""

    email_address: str
    """Email address of the user"""

    type: Literal["user"]
    """Object type. Always `user`."""
