from typing import Optional

from ..._models import BaseModel

__all__ = ["AnalyticsPluginChatCoworkUnifiedMetrics"]


class AnalyticsPluginChatCoworkUnifiedMetrics(BaseModel):
    """
    A plugin's use in Cowork sessions recorded while members had Chat
    and Cowork unified turned on.
    """

    distinct_session_plugin_used_count: Optional[int] = None
    """
    Same measure as `cowork_metrics.distinct_session_plugin_used_count`, for
    activity recorded while members had Chat and Cowork unified turned on. Null on
    aggregated rows where a distinct count cannot be computed.
    """
