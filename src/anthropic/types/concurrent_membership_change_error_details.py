from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ConcurrentMembershipChangeErrorDetails"]


class ConcurrentMembershipChangeErrorDetails(BaseModel):
    """Another change to the organization's members is in progress.

    Retry the request once it completes.
    """

    error_code: Literal["concurrent_membership_change"]
