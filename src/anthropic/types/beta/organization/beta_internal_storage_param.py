from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaInternalStorageParam"]


class BetaInternalStorageParam(TypedDict, total=False):
    """No External Storage for this purpose."""

    type: Required[Literal["internal"]]
