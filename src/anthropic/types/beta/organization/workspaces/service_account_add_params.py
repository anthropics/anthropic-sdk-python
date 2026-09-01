# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from ....anthropic_beta_param import AnthropicBetaParam
from ..beta_no_billing_workspace_role import BetaNoBillingWorkspaceRole

__all__ = ["ServiceAccountAddParams"]


class ServiceAccountAddParams(TypedDict, total=False):
    service_account_id: Required[str]
    """Tagged service account ID to add."""

    workspace_role: Required[BetaNoBillingWorkspaceRole]
    """Role to assign to the service account in this workspace."""

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""
