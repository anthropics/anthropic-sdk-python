from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaClaudeTagGuestPolicyRestrict"]


class BetaClaudeTagGuestPolicyRestrict(BaseModel):
    """Claude does not answer in the channel."""

    type: Literal["restrict"]
