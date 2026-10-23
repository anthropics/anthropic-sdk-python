from typing_extensions import Literal

from ...._models import BaseModel
from .beta_claude_tag_slack_channel_identifiers import BetaClaudeTagSlackChannelIdentifiers

__all__ = ["BetaClaudeTagSlackGridChannelSettingSource"]


class BetaClaudeTagSlackGridChannelSettingSource(BaseModel):
    """
    The value comes from the addressed channel as it is set up under another workspace of its Enterprise Grid: a channel shared across the Grid keeps one Slack channel identifier in every workspace that sees it.
    """

    slack: BetaClaudeTagSlackChannelIdentifiers
    """Slack's own identifiers for the channel under that other workspace."""

    type: Literal["slack_grid_channel"]
