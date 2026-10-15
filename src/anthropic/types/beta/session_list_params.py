from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import Literal, TypedDict

from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["SessionListParams"]


class SessionListParams(TypedDict, total=False):
    agent_id: str
    """Filter sessions created with this agent ID."""

    agent_version: int
    """Filter by agent version. Only applies when `agent_id` is also set."""

    created_at_gt: Union[str, datetime]
    """Return sessions created after this time (exclusive)."""

    created_at_gte: Union[str, datetime]
    """Return sessions created at or after this time (inclusive)."""

    created_at_lt: Union[str, datetime]
    """Return sessions created before this time (exclusive)."""

    created_at_lte: Union[str, datetime]
    """Return sessions created at or before this time (inclusive)."""

    deployment_id: str
    """Filter sessions created by this deployment ID."""

    include_archived: bool
    """When true, includes archived sessions. Default: false (exclude archived)."""

    limit: int
    """Maximum number of results to return."""

    memory_store_id: str
    """
    Filter sessions whose resources contain a `memory_store` with this memory store
    ID.
    """

    order: Literal["asc", "desc"]
    """Sort direction for results, ordered by `created_at`.

    Defaults to `desc` (newest first).
    """

    page: str
    """Opaque pagination cursor from a previous response."""

    statuses: List[Literal["rescheduling", "running", "idle", "terminated"]]
    """Filter by session status.

    Repeat the parameter to match any of multiple statuses.
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
