from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaUnrestrictedNetworkParam"]


class BetaUnrestrictedNetworkParam(TypedDict, total=False):
    """Unrestricted network access."""

    type: Required[Literal["unrestricted"]]
    """Network policy type"""
