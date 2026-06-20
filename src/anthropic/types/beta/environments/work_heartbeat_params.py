# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo
from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["WorkHeartbeatParams"]


class WorkHeartbeatParams(TypedDict, total=False):
    environment_id: Required[str]

    desired_ttl_seconds: Optional[int]
    """Desired TTL in seconds"""

    expected_last_heartbeat: Optional[str]
    """Expected last_heartbeat for conditional update (optimistic concurrency).

    Use literal 'NO_HEARTBEAT' to claim an unclaimed lease (first heartbeat). For
    subsequent heartbeats, echo the server's previous last_heartbeat value exactly.
    Returns 412 Precondition Failed if the actual value doesn't match.
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
