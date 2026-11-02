from datetime import datetime
from typing_extensions import Literal

from ....._models import BaseModel
from ..beta_claude_tag_settings import BetaClaudeTagSettings
from ..beta_claude_tag_setting_sources import BetaClaudeTagSettingSources
from ..beta_claude_tag_slack_workspace_identifiers import BetaClaudeTagSlackWorkspaceIdentifiers

__all__ = ["BetaClaudeTagSlackWorkspace"]


class BetaClaudeTagSlackWorkspace(BaseModel):
    """
    A Slack workspace the organization has connected, itself or through its Slack Enterprise Grid, with the settings it stores or, with `include_inherited`, the settings that apply in it.
    """

    id: str
    """The workspace's identifier.

    Starts with `slws_`. It does not change for as long as the workspace is set up.
    A workspace that is removed and set up again has a new one, and the old one
    keeps returning 404; look the workspace up by its Slack identifier for the new
    one.
    """

    created_at: datetime
    """Time the workspace was set up, by whichever route.

    It does not change for as long as `id` does not.
    """

    settings: BetaClaudeTagSettings
    """
    What the workspace itself stores or, with `include_inherited`, what applies in
    it. `sources` says which.
    """

    slack: BetaClaudeTagSlackWorkspaceIdentifiers
    """Slack's own identifier for the workspace."""

    sources: BetaClaudeTagSettingSources
    """For each setting, the settings level its value in `settings` comes from."""

    type: Literal["slack_workspace"]

    updated_at: datetime
    """Time Claude Tag's record of the workspace last changed.

    It moves on every change to a setting, and can also move when something no
    response holds changes, so a later value says to read the workspace again, not
    that a setting changed. Attaching or detaching a Bundle does not by itself move
    it.
    """
