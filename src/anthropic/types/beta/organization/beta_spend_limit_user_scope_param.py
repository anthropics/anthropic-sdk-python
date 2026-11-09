from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaSpendLimitUserScopeParam"]


class BetaSpendLimitUserScopeParam(TypedDict, total=False):
    """Scope selecting a single member of the organization."""

    type: Required[Literal["user"]]
    """Scope type. Always `user` for this scope."""

    user_id: Required[str]
    """Tagged ID of the member the spend limit applies to."""
