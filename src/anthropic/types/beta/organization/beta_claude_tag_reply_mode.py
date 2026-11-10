from typing import Union
from typing_extensions import Annotated, TypeAlias

from ...._models import UnionDiscriminator
from .beta_claude_tag_reply_mode_thread import BetaClaudeTagReplyModeThread
from .beta_claude_tag_reply_mode_automatic import BetaClaudeTagReplyModeAutomatic
from .beta_claude_tag_reply_mode_always_awake import BetaClaudeTagReplyModeAlwaysAwake
from .beta_claude_tag_reply_mode_mention_only import BetaClaudeTagReplyModeMentionOnly

__all__ = ["BetaClaudeTagReplyMode"]

BetaClaudeTagReplyMode: TypeAlias = Annotated[
    Union[
        BetaClaudeTagReplyModeAutomatic,
        BetaClaudeTagReplyModeMentionOnly,
        BetaClaudeTagReplyModeAlwaysAwake,
        BetaClaudeTagReplyModeThread,
    ],
    UnionDiscriminator("type"),
]
