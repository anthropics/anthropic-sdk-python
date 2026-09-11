from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaPlainTextSourceParam"]


class BetaPlainTextSourceParam(TypedDict, total=False):
    data: Required[str]

    media_type: Required[Literal["text/plain"]]

    type: Required[Literal["text"]]
