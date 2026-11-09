from typing_extensions import Literal

from .._exceptions import BadRequestError
from .user_profile_not_found_error_details import UserProfileNotFoundErrorDetails

__all__ = ["UserProfileNotFoundError"]


class UserProfileNotFoundError(BadRequestError):
    """
    The request depends on a user profile that does not exist in the organization or is no longer active. The request either names this user profile by ID, or names a resource, such as an External Key, that is bound to it.
    """

    error_code: Literal["user_profile_not_found"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: UserProfileNotFoundErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
