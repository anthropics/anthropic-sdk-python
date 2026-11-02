from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["APIKeyWorkspaceScope"]


class APIKeyWorkspaceScope(BaseModel):
    type: Literal["workspace"]
    """Scope type. Always `"workspace"`: the API key belongs to one Workspace."""

    workspace_id: str
    """
    ID of the Workspace the API key belongs to, including when it is the
    organization's default Workspace.
    """
