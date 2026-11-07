from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaClaudeTagGuestPolicyAllow"]


class BetaClaudeTagGuestPolicyAllow(BaseModel):
    """Claude answers in the channel."""

    type: Literal["allow"]
