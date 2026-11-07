from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaClaudeTagGuestPolicyChannelOnlyParam"]


class BetaClaudeTagGuestPolicyChannelOnlyParam(TypedDict, total=False):
    """Claude answers with only the Bundles attached to the channel itself."""

    type: Required[Literal["channel_only"]]
