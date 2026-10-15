from typing import Optional

from ...._models import BaseModel

__all__ = ["BetaAnalyticsPluginCoworkMetrics"]


class BetaAnalyticsPluginCoworkMetrics(BaseModel):
    """Cowork activity metrics for a single plugin on a given day."""

    distinct_session_plugin_used_count: Optional[int] = None
    """Number of distinct Cowork sessions in which the plugin was invoked.

    Null on aggregated rows where a distinct count cannot be computed.
    """
