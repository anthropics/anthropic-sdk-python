from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaURLImageSourceParam"]


class BetaURLImageSourceParam(TypedDict, total=False):
    type: Required[Literal["url"]]

    url: Required[str]
