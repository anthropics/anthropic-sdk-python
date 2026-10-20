from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["UserProfileActionURL"]


class UserProfileActionURL(BaseModel):
    """A URL to give to the person who takes the requested action."""

    expires_at: datetime
    """When the URL stops working, in RFC 3339 format."""

    type: Literal["user_profile_action_url"]
    """Object type. Always `user_profile_action_url`."""

    url: str
    """The URL to give to the person who takes the action.

    Anyone who holds it can open it until `expires_at`.
    """
