from ...._models import BaseModel
from .beta_analytics_tool_actions import BetaAnalyticsToolActions
from .beta_analytics_core_code_metrics import BetaAnalyticsCoreCodeMetrics

__all__ = ["BetaAnalyticsClaudeCodeMetrics"]


class BetaAnalyticsClaudeCodeMetrics(BaseModel):
    """Claude Code activity metrics for a single user on a given day."""

    core_metrics: BetaAnalyticsCoreCodeMetrics
    """Core Claude Code activity metrics for a single user on a given day."""

    tool_actions: BetaAnalyticsToolActions
    """Per-tool accepted/rejected counts for Claude Code file modification tools."""
