from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..no_billing_workspace_role import NoBillingWorkspaceRole

__all__ = ["MemberAddParams"]


class MemberAddParams(TypedDict, total=False):
    user_id: Required[str]
    """ID of the User."""

    workspace_role: Required[NoBillingWorkspaceRole]
    """Role of the new Workspace Member. Cannot be `workspace_billing`."""
