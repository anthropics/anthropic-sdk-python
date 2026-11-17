from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["UserProfileNotBillableErrorDetails"]


class UserProfileNotBillableErrorDetails(BaseModel):
    """The caller is not allowed to bill the user profile that the request names.

    The response gives no more specific error code and does not say what the reason is.
    """

    error_code: Literal["user_profile_not_billable"]
