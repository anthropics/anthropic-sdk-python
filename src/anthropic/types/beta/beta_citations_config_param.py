from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["BetaCitationsConfigParam"]


class BetaCitationsConfigParam(TypedDict, total=False):
    enabled: bool
