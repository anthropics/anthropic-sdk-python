from datetime import datetime
from typing_extensions import Literal

from ....._models import BaseModel
from ..beta_claude_tag_settings import BetaClaudeTagSettings
from ..beta_claude_tag_setting_sources import BetaClaudeTagSettingSources
from ..beta_claude_tag_slack_channel_identifiers import BetaClaudeTagSlackChannelIdentifiers

__all__ = ["BetaClaudeTagSlackChannel"]


class BetaClaudeTagSlackChannel(BaseModel):
    """
    A Slack channel set up for Claude Tag, with the settings it stores or, with `include_inherited`, the settings that apply in it.
    """

    id: str
    """The channel's identifier.

    Starts with `slch_`. It does not change for as long as the channel is set up,
    with one exception: a channel that is not configured gets a new one when
    claude.ai replaces its record, which happens only while the organization's
    read-only mode is off. A channel that is removed and set up again also has a new
    one. The old one keeps returning 404; look the channel up by its Slack
    identifiers for the new one.
    """

    created_at: datetime
    """Time the channel was set up, by whichever route.

    It does not change for as long as `id` does not.
    """

    settings: BetaClaudeTagSettings
    """What the channel itself stores or, with `include_inherited`, what applies in it.

    `sources` says which.
    """

    slack: BetaClaudeTagSlackChannelIdentifiers
    """Slack's own identifiers for the channel."""

    sources: BetaClaudeTagSettingSources
    """For each setting, the settings level its value in `settings` comes from."""

    type: Literal["slack_channel"]

    updated_at: datetime
    """Time Claude Tag's record of the channel last changed.

    It moves on every change to a setting, and can also move when something no
    response holds changes, so a later value says to read the channel again, not
    that a setting changed. Attaching or detaching a Bundle does not by itself move
    it.
    """
