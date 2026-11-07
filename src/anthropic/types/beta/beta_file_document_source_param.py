from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaFileDocumentSourceParam"]


class BetaFileDocumentSourceParam(TypedDict, total=False):
    file_id: Required[str]

    type: Required[Literal["file"]]
