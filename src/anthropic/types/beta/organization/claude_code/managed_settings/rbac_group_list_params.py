from __future__ import annotations

from typing import List, Optional
from typing_extensions import TypedDict

from .....anthropic_beta_param import AnthropicBetaParam

__all__ = ["RBACGroupListParams"]


class RBACGroupListParams(TypedDict, total=False):
    limit: int
    """Number of items to return per page.

    Defaults to `20`. Ranges from `1` to `100`.
    """

    page: Optional[str]
    """Optionally set to the `next_page` token from the previous response."""

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send
    `ce-claude-code-managed-settings-2026-10-06` in this header.
    """
