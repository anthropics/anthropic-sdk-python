from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaSpendLimitUserScope"]


class BetaSpendLimitUserScope(BaseModel):
    """Scope selecting a single member of the organization."""

    type: Literal["user"]
    """Scope type. Always `user` for this scope."""

    user_id: str
    """Tagged ID of the member the spend limit applies to."""
