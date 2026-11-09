from typing import Optional

from ...._models import BaseModel

__all__ = ["BetaAnalyticsConnectorCoworkMetrics"]


class BetaAnalyticsConnectorCoworkMetrics(BaseModel):
    """Cowork activity metrics for a single connector on a given day."""

    distinct_session_connector_used_count: Optional[int] = None
    """Number of distinct Cowork sessions in which the connector was used.

    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """
