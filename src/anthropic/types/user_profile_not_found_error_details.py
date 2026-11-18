from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["UserProfileNotFoundErrorDetails"]


class UserProfileNotFoundErrorDetails(BaseModel):
    """
    The request depends on a user profile that does not exist in the organization or is no longer active. The request either names this user profile by ID, or names a resource, such as an External Key, that is bound to it.
    """

    error_code: Literal["user_profile_not_found"]
