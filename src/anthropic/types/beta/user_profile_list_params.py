from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["UserProfileListParams"]


class UserProfileListParams(TypedDict, total=False):
    limit: int

    order: Literal["asc", "desc"]
    """ListOrder enum"""

    order_by: Literal["created_at", "name"]
    """
    Sort field for listing user profiles: `created_at` (default) or `name`
    (case-insensitive; profiles without a name sort last).
    """

    page: str

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
