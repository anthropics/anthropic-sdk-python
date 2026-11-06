from typing import Optional

from ...._models import BaseModel
from .beta_claude_tag_guest_policy import BetaClaudeTagGuestPolicy

__all__ = ["BetaClaudeTagSettings"]


class BetaClaudeTagSettings(BaseModel):
    """Claude Tag settings.

    Without `include_inherited`, a setting that is null is not set on the settings level and is inherited. With it, `enabled` and `guest_policy` are never null, and `instructions`, `model` and `environment_id` are null when no settings level sets them.
    """

    enabled: Optional[bool] = None
    """Whether Claude is on. The nearest settings level that sets it decides."""

    environment_id: Optional[str] = None
    """
    The environment Claude's sessions run in, starting with `env_`, or the
    identifier of a self-hosted runner pool, starting with `ccpool_`. The nearest
    settings level that sets it decides.
    """

    guest_policy: Optional[BetaClaudeTagGuestPolicy] = None
    """What Claude does in a channel while a Slack guest is in it.

    The nearest settings level that sets it decides.
    """

    instructions: Optional[str] = None
    """Instructions for Claude.

    Instructions add up: the text of every settings level that sets it is joined,
    broadest first.
    """

    model: Optional[str] = None
    """The model Claude uses: a model identifier or the name of a model line.

    The nearest settings level that sets it decides. When none does, Claude uses the
    product's default model.
    """
