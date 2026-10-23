from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from .....anthropic_beta_param import AnthropicBetaParam
from .beta_claude_tag_bundle_target_create_param import BetaClaudeTagBundleTargetCreateParam

__all__ = ["TargetCreateParams"]


class TargetCreateParams(TypedDict, total=False):
    target: Required[BetaClaudeTagBundleTargetCreateParam]

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send
    `experimental-claude-tag-2026-10-21` in this header.
    """
