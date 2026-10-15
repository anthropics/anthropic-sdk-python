from typing import Optional

from ...._models import BaseModel

__all__ = ["BetaAnalyticsOfficeProductMetrics"]


class BetaAnalyticsOfficeProductMetrics(BaseModel):
    """
    Office Agent activity metrics for a single user on a given day within one Office product.
    """

    connectors_used_count: int
    """Number of MCP connector invocations"""

    distinct_connectors_used_count: Optional[int] = None
    """Number of distinct MCP connectors used.

    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """

    distinct_session_count: Optional[int] = None
    """Number of distinct Office Agent sessions.

    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """

    distinct_skills_used_count: Optional[int] = None
    """Number of distinct skills used.

    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """

    message_count: int
    """Number of messages sent"""

    skills_used_count: int
    """Number of skill invocations"""
