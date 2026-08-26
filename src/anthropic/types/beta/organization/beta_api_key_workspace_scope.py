# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAPIKeyWorkspaceScope"]


class BetaAPIKeyWorkspaceScope(BaseModel):
    type: Literal["workspace"]
    """Scope type. Always `"workspace"`: the API key belongs to one Workspace."""

    workspace_id: str
    """ID of the Workspace the API key belongs to.

    Unlike the deprecated top-level `workspace_id`, this is the Workspace's real ID
    even for the organization's default Workspace.
    """
