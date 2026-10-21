from typing import Optional

from ...._models import BaseModel

__all__ = ["BetaAnalyticsConnectorOfficeProductMetrics"]


class BetaAnalyticsConnectorOfficeProductMetrics(BaseModel):
    """
    Office Agent activity metrics for a single connector on a given day within one Office product.
    """

    distinct_session_connector_used_count: Optional[int] = None
    """Number of distinct Office Agent sessions in which the connector was used.

    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """
