from typing_extensions import Literal

from .._exceptions import PermissionDeniedError
from .user_profile_not_billable_error_details import UserProfileNotBillableErrorDetails

__all__ = ["UserProfileNotBillableError"]


class UserProfileNotBillableError(PermissionDeniedError):
    """The request's user profile cannot be billed.

    The response gives no more specific error code and does not say what the reason is.
    """

    error_code: Literal["user_profile_not_billable"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: UserProfileNotBillableErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
