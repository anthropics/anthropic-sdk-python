from typing import Optional

from ...._models import BaseModel

__all__ = ["BetaAnalyticsScienceMetrics"]


class BetaAnalyticsScienceMetrics(BaseModel):
    """Claude Science activity metrics for a single user on a given day."""

    delegation_count: int
    """
    Number of delegations (handoffs to a specialized agent) in Claude Science
    sessions
    """

    distinct_session_count: Optional[int] = None
    """Number of distinct Claude Science sessions.

    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """

    message_count: int
    """Number of messages sent in Claude Science sessions"""

    remote_compute_job_count: int
    """Number of remote compute jobs launched from Claude Science sessions"""

    skills_used_count: int
    """Total number of skill invocations in Claude Science sessions"""
