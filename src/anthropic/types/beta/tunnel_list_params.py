from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["TunnelListParams"]


class TunnelListParams(TypedDict, total=False):
    include_archived: bool
    """Whether to include archived tunnels in the results. Defaults to false."""

    limit: int
    """Maximum number of tunnels to return per page. Defaults to 20, maximum 1000."""

    page: str
    """Opaque pagination cursor from a previous `list_tunnels` response."""

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
