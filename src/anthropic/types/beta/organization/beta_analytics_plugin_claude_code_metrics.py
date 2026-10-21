from typing import Optional

from ...._models import BaseModel

__all__ = ["BetaAnalyticsPluginClaudeCodeMetrics"]


class BetaAnalyticsPluginClaudeCodeMetrics(BaseModel):
    """Claude Code activity metrics for a single plugin on a given day."""

    distinct_session_plugin_used_count: Optional[int] = None
    """Number of distinct Claude Code sessions in which the plugin was invoked.

    Null on aggregated rows where a distinct count cannot be computed.
    """
