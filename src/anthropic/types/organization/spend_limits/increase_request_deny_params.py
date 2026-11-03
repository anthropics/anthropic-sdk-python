from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["IncreaseRequestDenyParams"]


class IncreaseRequestDenyParams(TypedDict, total=False):
    suppress_notification: bool
