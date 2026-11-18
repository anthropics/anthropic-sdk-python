from __future__ import annotations

from typing import List, Optional
from typing_extensions import TypedDict

from ....anthropic_beta_param import AnthropicBetaParam

__all__ = ["BundleUpdateParams"]


class BundleUpdateParams(TypedDict, total=False):
    instructions: Optional[str]
    """
    Instructions for Claude, up to 10,000 bytes (UTF-8), added to the instructions
    of every session that can use the Bundle. Null or an empty string clears them.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send
    `experimental-claude-tag-2026-10-21` in this header.
    """
