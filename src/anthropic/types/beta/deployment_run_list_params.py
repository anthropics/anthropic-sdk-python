from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import TypedDict

from ..anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_trigger_type import BetaManagedAgentsTriggerType

__all__ = ["DeploymentRunListParams"]


class DeploymentRunListParams(TypedDict, total=False):
    created_at_gt: Union[str, datetime]
    """Return runs created strictly after this time (exclusive)."""

    created_at_gte: Union[str, datetime]
    """Return runs created at or after this time (inclusive)."""

    created_at_lt: Union[str, datetime]
    """Return runs created strictly before this time (exclusive)."""

    created_at_lte: Union[str, datetime]
    """Return runs created at or before this time (inclusive)."""

    deployment_id: str
    """Filter to a specific deployment.

    Omit to list across all deployments in the workspace. Filtering by a
    non-existent `deployment_id` returns 200 with empty data.
    """

    has_error: bool
    """
    Filter: true for runs with non-null `error`, false for runs with non-null
    `session_id`. Omit for all.
    """

    limit: int
    """Maximum results per page. Default 20, maximum 1000."""

    page: str
    """Opaque pagination cursor.

    Pass `next_page` from the previous response. Invalid or expired cursors
    return 400.
    """

    trigger_type: BetaManagedAgentsTriggerType
    """Filter runs by what triggered them. Omit to return all runs."""

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
