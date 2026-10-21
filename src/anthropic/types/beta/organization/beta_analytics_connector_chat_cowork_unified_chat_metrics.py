from typing import Optional

from ...._models import BaseModel

__all__ = ["BetaAnalyticsConnectorChatCoworkUnifiedChatMetrics"]


class BetaAnalyticsConnectorChatCoworkUnifiedChatMetrics(BaseModel):
    """
    A connector's use in chat conversations recorded while members had
    Chat and Cowork unified turned on.
    """

    distinct_conversation_connector_used_count: Optional[int] = None
    """
    Same measure as `chat_metrics.distinct_conversation_connector_used_count`, for
    activity recorded while members had Chat and Cowork unified turned on.
    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """
