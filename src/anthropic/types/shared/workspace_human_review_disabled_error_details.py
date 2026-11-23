from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["WorkspaceHumanReviewDisabledErrorDetails"]


class WorkspaceHumanReviewDisabledErrorDetails(BaseModel):
    """
    The request's Workspace has Human Review turned off, and this operation is not available there. Use a Workspace with Human Review on.
    """

    error_code: Literal["workspace_human_review_disabled"]
