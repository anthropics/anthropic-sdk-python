from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .beta_claude_tag_guest_policy_param import BetaClaudeTagGuestPolicyParam

__all__ = ["BetaClaudeTagSettingsCreateParam"]


class BetaClaudeTagSettingsCreateParam(TypedDict, total=False):
    """The settings in a request that sets a Slack channel up.

    A setting left out is not set. A setting sent as null is cleared.
    """

    enabled: Optional[bool]
    """Whether Claude is on.

    `true` on a channel turns Claude on in it even when its workspace stores
    `false`. Null clears it.
    """

    environment_id: Optional[str]
    """
    The environment Claude's sessions run in: the identifier of an active
    environment of the organization, starting with `env_`. Null clears it.
    """

    guest_policy: Optional[BetaClaudeTagGuestPolicyParam]
    """What Claude does in a channel while a Slack guest is in it. Null clears it."""

    instructions: Optional[str]
    """
    Instructions for Claude, up to 8,192 characters after leading and trailing white
    space is trimmed. Null or blank text clears them.
    """

    model: Optional[str]
    """
    The model Claude uses: the identifier of a model, or the name of a model line,
    that the organization is entitled to for Claude Tag. Null clears it.
    """
