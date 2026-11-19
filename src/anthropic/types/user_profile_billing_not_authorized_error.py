from typing_extensions import Literal

from .._exceptions import PermissionDeniedError
from .user_profile_billing_not_authorized_error_details import UserProfileBillingNotAuthorizedErrorDetails

__all__ = ["UserProfileBillingNotAuthorizedError"]


class UserProfileBillingNotAuthorizedError(PermissionDeniedError):
    """
    The customer that the request's user profile represents has not authorized the caller to bill them, or the authorization that the request's credential uses has ended. The response does not say which applies.
    """

    error_code: Literal["user_profile_billing_not_authorized"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: UserProfileBillingNotAuthorizedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
