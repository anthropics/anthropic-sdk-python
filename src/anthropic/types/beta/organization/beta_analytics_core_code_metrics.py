from typing import Optional

from ...._models import BaseModel
from .beta_analytics_lines_of_code import BetaAnalyticsLinesOfCode

__all__ = ["BetaAnalyticsCoreCodeMetrics"]


class BetaAnalyticsCoreCodeMetrics(BaseModel):
    """Core Claude Code activity metrics for a single user on a given day."""

    artifacts_created_count: int
    """
    Number of artifacts created in Claude Code sessions: an artifact counts once, on
    the day a session first saves it. Counted from 2026-08-17; 0 on earlier days.
    Exact in date-range mode: a creation belongs to exactly one day, so the per-day
    counts never overlap and their sum over the window is the exact count of
    distinct creations in it.
    """

    commit_count: int
    """Number of commits made via Claude Code"""

    distinct_session_count: Optional[int] = None
    """Number of distinct Claude Code sessions.

    On aggregated rows and in date-range mode: summed per-day distinct counts. A
    session essentially never spans a UTC day, so the sum is in practice the true
    distinct count.
    """

    lines_of_code: BetaAnalyticsLinesOfCode
    """Lines of code added and removed via Claude Code."""

    pull_request_count: int
    """Number of pull requests created via Claude Code"""
