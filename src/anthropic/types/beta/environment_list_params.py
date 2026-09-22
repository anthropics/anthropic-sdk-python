from __future__ import annotations

from typing import List, Optional
from typing_extensions import TypedDict

from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["EnvironmentListParams"]


class EnvironmentListParams(TypedDict, total=False):
    include_archived: bool
    """Include archived environments in the response"""

    limit: int
    """Maximum number of environments to return"""

    page: Optional[str]
    """Opaque cursor from previous response for pagination.

    Pass the `next_page` value from the previous response.
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
