# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from ....anthropic_beta_param import AnthropicBetaParam
from ..beta_no_billing_workspace_role import BetaNoBillingWorkspaceRole

__all__ = ["ServiceAccountUpdateParams"]


class ServiceAccountUpdateParams(TypedDict, total=False):
    workspace_id: Required[str]
    """ID of the workspace."""

    workspace_role: Required[BetaNoBillingWorkspaceRole]
    """New role for the service account in this workspace."""

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
