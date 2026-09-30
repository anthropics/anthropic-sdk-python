from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..no_billing_workspace_role import NoBillingWorkspaceRole

__all__ = ["ServiceAccountAddParams"]


class ServiceAccountAddParams(TypedDict, total=False):
    service_account_id: Required[str]
    """Tagged service account ID to add."""

    workspace_role: Required[NoBillingWorkspaceRole]
    """Role to assign to the service account in this workspace."""
