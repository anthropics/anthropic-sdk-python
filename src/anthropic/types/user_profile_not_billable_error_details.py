from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["UserProfileNotBillableErrorDetails"]


class UserProfileNotBillableErrorDetails(BaseModel):
    """The request's user profile cannot be billed.

    The response gives no more specific error code and does not say what the reason is.
    """

    error_code: Literal["user_profile_not_billable"]
