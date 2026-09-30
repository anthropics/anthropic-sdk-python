from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..workspace_role import WorkspaceRole

__all__ = ["MemberUpdateParams"]


class MemberUpdateParams(TypedDict, total=False):
    workspace_id: Required[str]
    """ID of the Workspace."""

    workspace_role: Required[WorkspaceRole]
    """New workspace role for the User."""
