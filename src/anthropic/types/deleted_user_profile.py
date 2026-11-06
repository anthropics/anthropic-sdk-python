from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["DeletedUserProfile"]


class DeletedUserProfile(BaseModel):
    id: str
    """Identifier of the deleted user profile, prefixed `uprof_`."""

    type: Literal["user_profile_deleted"]
    """Object type. Always `user_profile_deleted`."""
