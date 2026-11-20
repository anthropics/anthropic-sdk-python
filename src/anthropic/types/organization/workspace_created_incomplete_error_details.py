from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["WorkspaceCreatedIncompleteErrorDetails"]


class WorkspaceCreatedIncompleteErrorDetails(BaseModel):
    """
    The Workspace was created, but some of what the request asked for did not take effect, or may not have. Don't send the create again. The error's `message` says what to do with the Workspace at `workspace_id`.
    """

    error_code: Literal["workspace_created_incomplete"]

    workspace_id: str
    """ID of the Workspace the request created."""
