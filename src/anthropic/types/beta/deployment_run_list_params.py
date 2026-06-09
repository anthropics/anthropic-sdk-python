# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo
from ..anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_trigger_type import BetaManagedAgentsTriggerType

__all__ = ["DeploymentRunListParams"]


class DeploymentRunListParams(TypedDict, total=False):
    created_at_gt: Annotated[Union[str, datetime], PropertyInfo(alias="created_at[gt]", format="iso8601")]
    """Return runs created strictly after this time (exclusive)."""

    created_at_gte: Annotated[Union[str, datetime], PropertyInfo(alias="created_at[gte]", format="iso8601")]
    """Return runs created at or after this time (inclusive)."""

    created_at_lt: Annotated[Union[str, datetime], PropertyInfo(alias="created_at[lt]", format="iso8601")]
    """Return runs created strictly before this time (exclusive)."""

    created_at_lte: Annotated[Union[str, datetime], PropertyInfo(alias="created_at[lte]", format="iso8601")]
    """Return runs created at or before this time (inclusive)."""

    deployment_id: str
    """Filter to a specific deployment.

    Omit to list across all deployments in the workspace. Filtering by a
    non-existent deployment_id returns 200 with empty data.
    """

    has_error: bool
    """
    Filter: true for runs with non-null error, false for runs with non-null
    session_id. Omit for all.
    """

    limit: int
    """Maximum results per page. Default 20, maximum 1000."""

    page: str
    """Opaque pagination cursor.

    Pass next_page from the previous response. Invalid or expired cursors
    return 400.
    """

    trigger_type: BetaManagedAgentsTriggerType
    """Filter runs by what triggered them. Omit to return all runs."""

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
