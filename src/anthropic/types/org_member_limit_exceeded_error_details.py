from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["OrgMemberLimitExceededErrorDetails"]


class OrgMemberLimitExceededErrorDetails(BaseModel):
    """The organization has reached the member limit that Anthropic set for it.

    Pending invites count toward the limit.
    """

    error_code: Literal["org_member_limit_exceeded"]
