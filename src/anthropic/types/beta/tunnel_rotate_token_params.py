from __future__ import annotations

from typing import List, Optional
from typing_extensions import TypedDict

from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["TunnelRotateTokenParams"]


class TunnelRotateTokenParams(TypedDict, total=False):
    reason: Optional[str]
    """Optional free-text reason for the rotation, recorded for audit."""

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
