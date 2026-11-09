from typing import Optional

from ...._models import BaseModel

__all__ = ["BetaAnalyticsConnectorClaudeCodeMetrics"]


class BetaAnalyticsConnectorClaudeCodeMetrics(BaseModel):
    """Claude Code activity metrics for a single connector on a given day."""

    distinct_session_connector_used_count: Optional[int] = None
    """Number of distinct Claude Code sessions in which the connector was used.

    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """
