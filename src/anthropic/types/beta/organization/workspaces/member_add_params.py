# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..beta_no_billing_workspace_role import BetaNoBillingWorkspaceRole

__all__ = ["MemberAddParams"]


class MemberAddParams(TypedDict, total=False):
    user_id: Required[str]
    """ID of the User."""

    workspace_role: Required[BetaNoBillingWorkspaceRole]
    """Role of the new Workspace Member. Cannot be `workspace_billing`."""
