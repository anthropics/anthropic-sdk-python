# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from ....anthropic_beta_param import AnthropicBetaParam
from ..beta_no_billing_workspace_role import BetaNoBillingWorkspaceRole

__all__ = ["WorkspaceAddParams"]


class WorkspaceAddParams(TypedDict, total=False):
    workspace_id: Required[str]
    """Tagged workspace ID to add the service account to."""

    workspace_role: Required[BetaNoBillingWorkspaceRole]
    """Role to assign to the service account in this workspace."""

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""
