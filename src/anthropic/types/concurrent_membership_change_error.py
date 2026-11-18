from typing_extensions import Literal

from .._exceptions import ConflictError
from .concurrent_membership_change_error_details import ConcurrentMembershipChangeErrorDetails

__all__ = ["ConcurrentMembershipChangeError"]


class ConcurrentMembershipChangeError(ConflictError):
    """Another change to the organization's members is in progress.

    Retry the request once it completes.
    """

    error_code: Literal["concurrent_membership_change"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: ConcurrentMembershipChangeErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
