from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["WorkspaceMemberLimitExceededErrorDetails"]


class WorkspaceMemberLimitExceededErrorDetails(BaseModel):
    """The workspace has reached the member limit that Anthropic set for it."""

    error_code: Literal["workspace_member_limit_exceeded"]
