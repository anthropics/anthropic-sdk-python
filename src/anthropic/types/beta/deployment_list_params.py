# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo
from ..anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_deployment_status import BetaManagedAgentsDeploymentStatus

__all__ = ["DeploymentListParams"]


class DeploymentListParams(TypedDict, total=False):
    agent_id: str
    """Filter by agent ID."""

    created_at_gte: Annotated[Union[str, datetime], PropertyInfo(alias="created_at[gte]", format="iso8601")]
    """Return deployments created at or after this time (inclusive)."""

    created_at_lte: Annotated[Union[str, datetime], PropertyInfo(alias="created_at[lte]", format="iso8601")]
    """Return deployments created at or before this time (inclusive)."""

    include_archived: bool
    """When true, includes archived deployments. Default: false (exclude archived)."""

    limit: int
    """Maximum results per page. Default 20, maximum 100."""

    page: str
    """Opaque pagination cursor."""

    status: BetaManagedAgentsDeploymentStatus
    """Filter by status: active or paused.

    Omit for both. To include archived deployments, use include_archived instead;
    the two cannot be combined.
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
