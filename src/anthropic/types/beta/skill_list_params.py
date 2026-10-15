from __future__ import annotations

from typing import List, Optional
from typing_extensions import TypedDict

from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["SkillListParams"]


class SkillListParams(TypedDict, total=False):
    limit: int
    """Number of results to return per page.

    Ranges from `1` to `1000`. Defaults to `20`.
    """

    page: Optional[str]
    """Pagination token for fetching a specific page of results.

    Pass the value from a previous response's `next_page` field to get the next page
    of results.
    """

    source: Optional[str]
    """Filter skills by source.

    If provided, only skills from the specified source will be returned:

    - `"custom"`: only return user-created skills
    - `"anthropic"`: only return Anthropic-created skills
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
