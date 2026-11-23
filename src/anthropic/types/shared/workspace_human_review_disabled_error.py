from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .workspace_human_review_disabled_error_details import WorkspaceHumanReviewDisabledErrorDetails

__all__ = ["WorkspaceHumanReviewDisabledError"]


class WorkspaceHumanReviewDisabledError(BadRequestError):
    """
    The request's Workspace has Human Review turned off, and this operation is not available there. Use a Workspace with Human Review on.
    """

    error_code: Literal["workspace_human_review_disabled"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: WorkspaceHumanReviewDisabledErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
