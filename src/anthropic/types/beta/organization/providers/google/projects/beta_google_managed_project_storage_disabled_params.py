from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaGoogleManagedProjectStorageDisabledParams"]


class BetaGoogleManagedProjectStorageDisabledParams(TypedDict, total=False):
    """Turns the control off and removes every region's bucket."""

    type: Required[Literal["disabled"]]
