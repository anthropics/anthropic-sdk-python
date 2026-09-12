from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["CitationsConfigParam"]


class CitationsConfigParam(TypedDict, total=False):
    enabled: bool
