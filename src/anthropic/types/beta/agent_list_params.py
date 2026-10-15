from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import TypedDict

from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["AgentListParams"]


class AgentListParams(TypedDict, total=False):
    created_at_gte: Union[str, datetime]
    """Return agents created at or after this time (inclusive)."""

    created_at_lte: Union[str, datetime]
    """Return agents created at or before this time (inclusive)."""

    include_archived: bool
    """Include archived agents in results. Defaults to false."""

    limit: int
    """Maximum results per page. Default 20, maximum 100."""

    page: str
    """Opaque pagination cursor from a previous response."""

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
