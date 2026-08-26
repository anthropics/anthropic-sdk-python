# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..beta_workspace_role import BetaWorkspaceRole

__all__ = ["MemberUpdateParams"]


class MemberUpdateParams(TypedDict, total=False):
    workspace_id: Required[str]
    """ID of the Workspace."""

    workspace_role: Required[BetaWorkspaceRole]
    """New workspace role for the User."""
