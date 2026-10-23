from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from .....anthropic_beta_param import AnthropicBetaParam

__all__ = ["TargetListParams"]


class TargetListParams(TypedDict, total=False):
    limit: int
    """Number of items to return per page, between 1 and 100. Defaults to 20."""

    page: str
    """Opaque cursor from a previous response's `next_page`."""

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send
    `experimental-claude-tag-2026-10-21` in this header.
    """
