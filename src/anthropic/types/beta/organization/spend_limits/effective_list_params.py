from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, TypedDict

from ....._types import SequenceNotStr

__all__ = ["EffectiveListParams"]


class EffectiveListParams(TypedDict, total=False):
    limit: int
    """Maximum number of members per page.

    A member's period rows never split across pages, so a page may carry more rows
    than this. Defaults to `20`.
    """

    page: Optional[str]
    """Opaque cursor from a previous response's `next_page` field."""

    period: Optional[List[Literal["daily", "monthly", "weekly"]]]
    """Restrict the report to these limit periods.

    Omit to return one row per period each member resolves a spend limit for.
    """

    user_ids: Optional[SequenceNotStr[str]]
    """Restrict the report to these members, by tagged user ID (`user_...`).

    At most 100 entries.
    """
