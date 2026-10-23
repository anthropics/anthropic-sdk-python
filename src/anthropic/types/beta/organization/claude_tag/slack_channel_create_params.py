from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from ....anthropic_beta_param import AnthropicBetaParam
from ..beta_claude_tag_settings_create_param import BetaClaudeTagSettingsCreateParam
from ..beta_claude_tag_slack_channel_identifiers_param import BetaClaudeTagSlackChannelIdentifiersParam

__all__ = ["SlackChannelCreateParams"]


class SlackChannelCreateParams(TypedDict, total=False):
    slack: Required[BetaClaudeTagSlackChannelIdentifiersParam]
    """Slack's own identifiers for the channel to set up.

    The organization must own the workspace.
    """

    settings: BetaClaudeTagSettingsCreateParam
    """Settings to store on the channel, applied as Update Slack Channel applies them."""

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send
    `experimental-claude-tag-2026-10-21` in this header.
    """
