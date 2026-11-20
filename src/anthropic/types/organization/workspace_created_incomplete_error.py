from typing_extensions import Literal

from ..._exceptions import ServiceUnavailableError
from .workspace_created_incomplete_error_details import WorkspaceCreatedIncompleteErrorDetails

__all__ = ["WorkspaceCreatedIncompleteError"]


class WorkspaceCreatedIncompleteError(ServiceUnavailableError):
    """
    The Workspace was created, but some of what the request asked for did not take effect, or may not have. Don't send the create again. The error's `message` says what to do with the Workspace at `workspace_id`.
    """

    error_code: Literal["workspace_created_incomplete"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: WorkspaceCreatedIncompleteErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
