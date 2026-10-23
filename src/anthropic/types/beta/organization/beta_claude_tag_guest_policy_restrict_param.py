from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaClaudeTagGuestPolicyRestrictParam"]


class BetaClaudeTagGuestPolicyRestrictParam(TypedDict, total=False):
    """Claude does not answer in the channel."""

    type: Required[Literal["restrict"]]
