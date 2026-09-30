from typing import Optional

from ...._models import BaseModel

__all__ = ["BetaAnalyticsConnectorChatMetrics"]


class BetaAnalyticsConnectorChatMetrics(BaseModel):
    """Claude.ai activity metrics for a single connector on a given day."""

    distinct_conversation_connector_used_count: Optional[int] = None
    """Number of distinct conversations in which the connector was used.

    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """
