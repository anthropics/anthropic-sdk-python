from ...._models import BaseModel

__all__ = ["BetaAnalyticsToolActionCounts"]


class BetaAnalyticsToolActionCounts(BaseModel):
    """Accepted/rejected counts for a single Claude Code tool type."""

    accepted_count: int
    """Number of tool proposals accepted"""

    rejected_count: int
    """Number of tool proposals rejected"""
