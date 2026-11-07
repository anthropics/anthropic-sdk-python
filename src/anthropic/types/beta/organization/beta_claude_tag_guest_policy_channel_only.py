from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaClaudeTagGuestPolicyChannelOnly"]


class BetaClaudeTagGuestPolicyChannelOnly(BaseModel):
    """Claude answers with only the Bundles attached to the channel itself."""

    type: Literal["channel_only"]
