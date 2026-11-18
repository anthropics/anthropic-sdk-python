from ..._models import BaseModel

__all__ = ["AnalyticsLinesOfCode"]


class AnalyticsLinesOfCode(BaseModel):
    """Lines of code added and removed via Claude Code."""

    added_count: int
    """Lines of code added"""

    removed_count: int
    """Lines of code removed"""
