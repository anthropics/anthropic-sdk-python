from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_claude_tag_reply_mode_thread_param import BetaClaudeTagReplyModeThreadParam
from .beta_claude_tag_reply_mode_automatic_param import BetaClaudeTagReplyModeAutomaticParam
from .beta_claude_tag_reply_mode_always_awake_param import BetaClaudeTagReplyModeAlwaysAwakeParam
from .beta_claude_tag_reply_mode_mention_only_param import BetaClaudeTagReplyModeMentionOnlyParam

__all__ = ["BetaClaudeTagReplyModeParam"]

BetaClaudeTagReplyModeParam: TypeAlias = Union[
    BetaClaudeTagReplyModeAutomaticParam,
    BetaClaudeTagReplyModeMentionOnlyParam,
    BetaClaudeTagReplyModeAlwaysAwakeParam,
    BetaClaudeTagReplyModeThreadParam,
]
