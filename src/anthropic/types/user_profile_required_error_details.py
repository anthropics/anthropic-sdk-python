from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["UserProfileRequiredErrorDetails"]


class UserProfileRequiredErrorDetails(BaseModel):
    """
    The request sets `billing_policy.bill_to` to `"user_profile"` but names no user profile. Name the profile to bill in the `anthropic-user-profile-id` header.
    """

    error_code: Literal["user_profile_required"]
