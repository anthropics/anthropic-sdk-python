from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["DirectCallerParam"]


class DirectCallerParam(TypedDict, total=False):
    """Tool invocation directly from the model."""

    type: Required[Literal["direct"]]
