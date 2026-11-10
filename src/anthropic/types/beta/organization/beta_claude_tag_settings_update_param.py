from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .beta_claude_tag_reply_mode_param import BetaClaudeTagReplyModeParam
from .beta_claude_tag_guest_policy_param import BetaClaudeTagGuestPolicyParam

__all__ = ["BetaClaudeTagSettingsUpdateParam"]


class BetaClaudeTagSettingsUpdateParam(TypedDict, total=False):
    """The settings to change.

    A setting left out is unchanged. A setting sent as null is cleared, so it is inherited.
    """

    enabled: Optional[bool]
    """Whether Claude is on.

    `true` on a channel turns Claude on in it even when its workspace stores
    `false`. Null clears it.
    """

    environment_id: Optional[str]
    """
    The environment Claude's sessions run in: the identifier of an active
    environment of the organization, starting with `env_`, or of a self-hosted
    runner pool of the organization that every member may use, starting with
    `ccpool_`. Null clears it.
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

    reply_mode: Optional[BetaClaudeTagReplyModeParam]
    """
    How Claude takes part in the channel: `automatic`, `mention_only`,
    `always_awake` or `thread`. Only a channel takes one: an update of a workspace
    that sends a value is refused, and one that sends null changes nothing. Null
    never clears it: sent to a channel that stores none it changes nothing, and sent
    to a channel that stores one it is refused, because a stored reply mode can be
    changed but never cleared; a caller that wants Claude's default behavior sends
    `automatic`.
    """
