from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["MemberAddParams"]


class MemberAddParams(TypedDict, total=False):
    user_id: Required[str]
    """ID of the User."""
