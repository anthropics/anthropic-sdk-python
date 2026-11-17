from typing_extensions import Literal

from .._exceptions import BadRequestError
from .user_profile_required_error_details import UserProfileRequiredErrorDetails

__all__ = ["UserProfileRequiredError"]


class UserProfileRequiredError(BadRequestError):
    """
    The request sets `billing_policy.bill_to` to `"user_profile"` but names no user profile. Name the profile to bill in the `anthropic-user-profile-id` header.
    """

    error_code: Literal["user_profile_required"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: UserProfileRequiredErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
