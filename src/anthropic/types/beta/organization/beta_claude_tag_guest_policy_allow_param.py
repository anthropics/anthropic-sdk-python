from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaClaudeTagGuestPolicyAllowParam"]


class BetaClaudeTagGuestPolicyAllowParam(TypedDict, total=False):
    """Claude answers in the channel."""

    type: Required[Literal["allow"]]
