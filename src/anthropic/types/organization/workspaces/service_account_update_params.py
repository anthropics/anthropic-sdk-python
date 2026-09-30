from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..no_billing_workspace_role import NoBillingWorkspaceRole

__all__ = ["ServiceAccountUpdateParams"]


class ServiceAccountUpdateParams(TypedDict, total=False):
    workspace_id: Required[str]
    """ID of the workspace."""

    workspace_role: Required[NoBillingWorkspaceRole]
    """New role for the service account in this workspace."""
