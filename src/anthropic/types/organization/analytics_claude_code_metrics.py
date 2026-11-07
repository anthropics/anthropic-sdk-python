from ..._models import BaseModel
from .analytics_tool_actions import AnalyticsToolActions
from .analytics_core_code_metrics import AnalyticsCoreCodeMetrics

__all__ = ["AnalyticsClaudeCodeMetrics"]


class AnalyticsClaudeCodeMetrics(BaseModel):
    """Claude Code activity metrics for a single user on a given day."""

    core_metrics: AnalyticsCoreCodeMetrics
    """Core Claude Code activity metrics for a single user on a given day."""

    tool_actions: AnalyticsToolActions
    """Per-tool accepted/rejected counts for Claude Code file modification tools."""
