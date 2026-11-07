from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaThreadCreateParams"]


class BetaThreadCreateParams(TypedDict, total=False):
    """Start holding conversation state under this response's ``id``."""

    type: Required[Literal["create"]]
