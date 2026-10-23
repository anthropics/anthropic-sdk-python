from typing import Union
from typing_extensions import Annotated, TypeAlias

from ...._models import UnionDiscriminator
from .beta_claude_tag_guest_policy_allow import BetaClaudeTagGuestPolicyAllow
from .beta_claude_tag_guest_policy_restrict import BetaClaudeTagGuestPolicyRestrict
from .beta_claude_tag_guest_policy_channel_only import BetaClaudeTagGuestPolicyChannelOnly

__all__ = ["BetaClaudeTagGuestPolicy"]

BetaClaudeTagGuestPolicy: TypeAlias = Annotated[
    Union[BetaClaudeTagGuestPolicyAllow, BetaClaudeTagGuestPolicyRestrict, BetaClaudeTagGuestPolicyChannelOnly],
    UnionDiscriminator("type"),
]
