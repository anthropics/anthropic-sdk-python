from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["WorkspaceAddParams"]


class WorkspaceAddParams(TypedDict, total=False):
    workspace_id: Required[str]
    """Tagged ID of the workspace to enable this rule for."""
