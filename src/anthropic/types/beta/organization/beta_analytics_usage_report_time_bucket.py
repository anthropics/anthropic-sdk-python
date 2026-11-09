from typing import List
from datetime import datetime

from ...._models import BaseModel
from .beta_analytics_usage_bucketed_result import BetaAnalyticsUsageBucketedResult

__all__ = ["BetaAnalyticsUsageReportTimeBucket"]


class BetaAnalyticsUsageReportTimeBucket(BaseModel):
    ending_at: datetime
    """End of the time bucket (exclusive) in RFC 3339 format."""

    results: List[BetaAnalyticsUsageBucketedResult]
    """Rows for this time bucket.

    Empty when the bucket has no data; otherwise a single combined row when
    `group_by[]` is omitted, or one row per group (subject to the per-bucket group
    cap described on the `group_by[]` parameter).
    """

    starting_at: datetime
    """Start of the time bucket (inclusive) in RFC 3339 format."""
