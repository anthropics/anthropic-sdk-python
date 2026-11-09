from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..no_billing_workspace_role import NoBillingWorkspaceRole

__all__ = ["WorkspaceAddParams"]


class WorkspaceAddParams(TypedDict, total=False):
    workspace_id: Required[str]
    """Tagged workspace ID to add the service account to."""

    workspace_role: Required[NoBillingWorkspaceRole]
    """Role to assign to the service account in this workspace."""
