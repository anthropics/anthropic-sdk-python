from typing import List, Optional

from ...._models import BaseModel
from .beta_claude_tag_setting_source import BetaClaudeTagSettingSource

__all__ = ["BetaClaudeTagSettingSources"]


class BetaClaudeTagSettingSources(BaseModel):
    """For each setting, the settings level its value in `settings` comes from.

    Without `include_inherited`, a setting the channel or workspace stores has a source that names the channel or workspace itself, and one it does not store has null, or an empty list for `instructions`. With `include_inherited=true` no member is null: a value that no settings level sets has the source `default`.
    """

    enabled: Optional[BetaClaudeTagSettingSource] = None
    """The settings level `enabled` comes from."""

    environment_id: Optional[BetaClaudeTagSettingSource] = None
    """The settings level `environment_id` comes from."""

    guest_policy: Optional[BetaClaudeTagSettingSource] = None
    """The settings level `guest_policy` comes from."""

    instructions: List[BetaClaudeTagSettingSource]
    """
    Every settings level that contributes text to `instructions`, broadest first, in
    the order their text is joined. Empty when none does.
    """

    model: Optional[BetaClaudeTagSettingSource] = None
    """The settings level `model` comes from."""
