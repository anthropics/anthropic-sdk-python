from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .workspace_api_key_limit_exceeded_error_details import WorkspaceAPIKeyLimitExceededErrorDetails

__all__ = ["WorkspaceAPIKeyLimitExceededError"]


class WorkspaceAPIKeyLimitExceededError(BadRequestError):
    """The workspace has reached its limit of active API keys."""

    error_code: Literal["workspace_api_key_limit_exceeded"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: WorkspaceAPIKeyLimitExceededErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
