from __future__ import annotations

from typing import List, Optional
from typing_extensions import TypedDict

from ....._types import SequenceNotStr
from .beta_spend_limit_increase_request_status import BetaSpendLimitIncreaseRequestStatus

__all__ = ["IncreaseRequestListParams"]


class IncreaseRequestListParams(TypedDict, total=False):
    actor_ids: Optional[SequenceNotStr[str]]
    """Filter by requester, as `user_...` tagged IDs."""

    limit: int

    page: Optional[str]
    """Opaque cursor from a previous response's `next_page`."""

    status: Optional[List[BetaSpendLimitIncreaseRequestStatus]]
    """Filter by status. Omit to return all."""
