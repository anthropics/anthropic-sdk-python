from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .workspace_member_limit_exceeded_error_details import WorkspaceMemberLimitExceededErrorDetails

__all__ = ["WorkspaceMemberLimitExceededError"]


class WorkspaceMemberLimitExceededError(BadRequestError):
    """The workspace has reached the member limit that Anthropic set for it."""

    error_code: Literal["workspace_member_limit_exceeded"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: WorkspaceMemberLimitExceededErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
