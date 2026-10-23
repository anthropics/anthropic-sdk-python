from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from ....anthropic_beta_param import AnthropicBetaParam
from ..beta_claude_tag_settings_update_param import BetaClaudeTagSettingsUpdateParam

__all__ = ["SlackChannelUpdateParams"]


class SlackChannelUpdateParams(TypedDict, total=False):
    settings: Required[BetaClaudeTagSettingsUpdateParam]
    """The settings to change."""

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send
    `experimental-claude-tag-2026-10-21` in this header.
    """
