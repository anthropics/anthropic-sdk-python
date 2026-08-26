# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ......_models import BaseModel

__all__ = ["WorkspaceRemoveResponse"]


class WorkspaceRemoveResponse(BaseModel):
    federation_rule_id: str
    """Tagged ID of the federation rule."""

    type: Literal["federation_rule_workspace_deleted"]

    workspace_id: str
    """Tagged ID of the workspace named in the delete request. Removal is idempotent."""
