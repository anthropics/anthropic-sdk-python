from datetime import datetime

from ....._models import BaseModel
from .beta_analytics_usage_group import BetaAnalyticsUsageGroup
from .beta_analytics_usage_metrics import BetaAnalyticsUsageMetrics

__all__ = ["BetaAnalyticsUsageItem"]


class BetaAnalyticsUsageItem(BaseModel):
    ending_at: datetime
    """
    End of the period this row covers (exclusive), as an RFC 3339 UTC timestamp: the
    end of the row's time bucket when a time-bucket width is set; otherwise the
    requested `ending_at` (or, when omitted, the earlier of now and `starting_at`
    plus 31 days) rounded down to the hour, because without a time bucket the report
    covers whole hours.
    """

    group: BetaAnalyticsUsageGroup
    """The dimension values this row's usage is broken out by."""

    starting_at: datetime
    """
    Start of the period this row covers (inclusive), as an RFC 3339 UTC timestamp:
    the start of the row's time bucket when a time-bucket width is set, otherwise
    the requested `starting_at` rounded down to the hour.
    """

    usage: BetaAnalyticsUsageMetrics
    """Token usage for this row."""
