from typing import Optional
from datetime import date

from ..._models import BaseModel
from .analytics_user import AnalyticsUser
from .analytics_chat_metrics import AnalyticsChatMetrics
from .analytics_cowork_metrics import AnalyticsCoworkMetrics
from .analytics_design_metrics import AnalyticsDesignMetrics
from .analytics_office_metrics import AnalyticsOfficeMetrics
from .analytics_science_metrics import AnalyticsScienceMetrics
from .analytics_claude_tag_metrics import AnalyticsClaudeTagMetrics
from .analytics_claude_code_metrics import AnalyticsClaudeCodeMetrics
from .analytics_chat_cowork_unified_metrics import AnalyticsChatCoworkUnifiedMetrics

__all__ = ["AnalyticsUserActivity"]


class AnalyticsUserActivity(BaseModel):
    """Per-user activity data for a given day."""

    chat_metrics: AnalyticsChatMetrics
    """Claude.ai activity metrics for a single user on a given day."""

    claude_code_metrics: AnalyticsClaudeCodeMetrics
    """Claude Code activity metrics for a single user on a given day."""

    cowork_metrics: AnalyticsCoworkMetrics
    """Cowork activity metrics for a single user on a given day."""

    design_metrics: AnalyticsDesignMetrics
    """Claude Design activity metrics for a single user on a given day."""

    distinct_user_count: Optional[int] = None
    """Number of distinct active users represented by this row.

    Only set for grouped rollups (`group_by[]`); null for per-user rows. In
    date-range mode, recomputed as an exact distinct count of the group's active
    members over the requested window, never a sum of per-day values.
    """

    office_metrics: AnalyticsOfficeMetrics
    """
    Office Agent activity metrics for a single user on a given day, broken out by
    Office product.
    """

    science_metrics: AnalyticsScienceMetrics
    """Claude Science activity metrics for a single user on a given day."""

    user: Optional[AnalyticsUser] = None
    """The user this row describes. Null on rows aggregated across users."""

    web_search_count: int
    """Number of web searches performed"""

    chat_cowork_unified_metrics: Optional[AnalyticsChatCoworkUnifiedMetrics] = None
    """
    Activity recorded while the member had Chat and Cowork unified (Cowork's
    features inside claude.ai chat) turned on, split into `chat` (chat activity) and
    `sessions` (Cowork activity). Omitted from the response where Chat and Cowork
    unified is not available.
    """

    claude_tag_metrics: Optional[AnalyticsClaudeTagMetrics] = None
    """Claude Tag activity in Slack by a user who has linked a Claude account.

    Activity by Slack users who have not linked an account appears only in the
    `/summaries` Claude Tag counts, so these rows do not add up to those counts.
    Omitted from the response on deployments that do not offer Claude Tag reporting.
    """

    last_activity_date: Optional[date] = None
    """
    Most recent UTC day (YYYY-MM-DD) on which the user had any counted activity,
    within the requested window: equal to the requested `date` in single-day mode,
    and to the latest active day from `starting_date` (inclusive) to `ending_date`
    (exclusive) in date-range rollup mode — never a day earlier than the window
    start. On filtered requests (`filter[]`) only days matching the filter count:
    with `filter[]=rbac_group_id:{id}` it is the last day the user was active while
    a member of that group, consistent with the row's other metrics. On grouped
    (`group_by[]`) rows it is the latest day any member of the group was active (the
    requested `date` in single-day mode). Omitted from the response while
    last-activity reporting is not enabled for this organization.
    """

    rbac_group_id: Optional[str] = None
    """
    Tagged RBAC group identifier (`rbac_group_...`), matching the spend-limits API
    spelling. Present only when the request grouped by `rbac_group_id`.
    """

    rbac_group_name: Optional[str] = None
    """
    Resolved RBAC group display name, alongside `rbac_group_id` when name resolution
    is available. Null if the group has been deleted or its name could not be
    resolved; `rbac_group_id` remains the stable key.
    """
