from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["UserProfileBillingNotAuthorizedErrorDetails"]


class UserProfileBillingNotAuthorizedErrorDetails(BaseModel):
    """
    The customer that the named user profile represents has not authorized the caller to bill them, or the authorization that the request's credential uses has ended. The response does not say which applies.
    """

    error_code: Literal["user_profile_billing_not_authorized"]
