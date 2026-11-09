from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["WorkspaceAPIKeyLimitExceededErrorDetails"]


class WorkspaceAPIKeyLimitExceededErrorDetails(BaseModel):
    """The workspace has reached its limit of active API keys."""

    error_code: Literal["workspace_api_key_limit_exceeded"]
