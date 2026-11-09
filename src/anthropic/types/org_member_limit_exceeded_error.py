from typing_extensions import Literal

from .._exceptions import BadRequestError
from .org_member_limit_exceeded_error_details import OrgMemberLimitExceededErrorDetails

__all__ = ["OrgMemberLimitExceededError"]


class OrgMemberLimitExceededError(BadRequestError):
    """The organization has reached the member limit that Anthropic set for it.

    Pending invites count toward the limit.
    """

    error_code: Literal["org_member_limit_exceeded"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: OrgMemberLimitExceededErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
