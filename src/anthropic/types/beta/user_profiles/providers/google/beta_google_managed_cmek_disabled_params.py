from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaGoogleManagedCMEKDisabledParams"]


class BetaGoogleManagedCMEKDisabledParams(TypedDict, total=False):
    """Turns the control off and removes every region's key."""

    type: Required[Literal["disabled"]]
