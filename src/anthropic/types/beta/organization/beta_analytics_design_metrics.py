from typing import Optional

from ...._models import BaseModel

__all__ = ["BetaAnalyticsDesignMetrics"]


class BetaAnalyticsDesignMetrics(BaseModel):
    """Claude Design activity metrics for a single user on a given day."""

    distinct_projects_created_count: int
    """Number of distinct Claude Design projects created.

    Exact in date-range mode: a creation belongs to exactly one day, so the per-day
    counts never overlap and their sum over the window is the exact count of
    distinct creations in it.
    """

    distinct_projects_used_count: Optional[int] = None
    """Number of distinct Claude Design projects the user worked in.

    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """

    distinct_session_count: Optional[int] = None
    """Number of distinct Claude Design sessions.

    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """

    message_count: int
    """Number of messages sent in Claude Design sessions"""
