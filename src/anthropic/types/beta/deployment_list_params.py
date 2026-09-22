from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import TypedDict

from ..anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_deployment_status import BetaManagedAgentsDeploymentStatus

__all__ = ["DeploymentListParams"]


class DeploymentListParams(TypedDict, total=False):
    agent_id: str
    """Filter by agent ID."""

    created_at_gte: Union[str, datetime]
    """Return deployments created at or after this time (inclusive)."""

    created_at_lte: Union[str, datetime]
    """Return deployments created at or before this time (inclusive)."""

    include_archived: bool
    """When true, includes archived deployments. Default: false (exclude archived)."""

    limit: int
    """Maximum results per page. Default 20, maximum 100."""

    page: str
    """Opaque pagination cursor."""

    status: BetaManagedAgentsDeploymentStatus
    """Filter by status: `active` or `paused`.

    Omit for both. To include archived deployments, use `include_archived` instead;
    the two cannot be combined.
    """

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
