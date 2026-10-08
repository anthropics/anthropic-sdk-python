from typing import Optional
from datetime import date

from ...._models import BaseModel
from .beta_analytics_user import BetaAnalyticsUser
from .beta_analytics_chat_metrics import BetaAnalyticsChatMetrics
from .beta_analytics_cowork_metrics import BetaAnalyticsCoworkMetrics
from .beta_analytics_design_metrics import BetaAnalyticsDesignMetrics
from .beta_analytics_office_metrics import BetaAnalyticsOfficeMetrics
from .beta_analytics_science_metrics import BetaAnalyticsScienceMetrics
from .beta_analytics_claude_code_metrics import BetaAnalyticsClaudeCodeMetrics
from .beta_analytics_chat_cowork_unified_chat_metrics import BetaAnalyticsChatCoworkUnifiedChatMetrics
from .beta_analytics_chat_cowork_unified_sessions_metrics import BetaAnalyticsChatCoworkUnifiedSessionsMetrics

__all__ = ["BetaAnalyticsUserActivity", "ChatCoworkUnifiedMetrics"]


class ChatCoworkUnifiedMetrics(BaseModel):
    """
    Activity recorded while the member had Chat and Cowork unified (Cowork's features inside claude.ai chat) turned on, split into `chat` (chat activity) and `sessions` (Cowork activity). Omitted from the response on deployments that do not offer Chat and Cowork unified.
    """

    chat: BetaAnalyticsChatCoworkUnifiedChatMetrics
    """Chat activity recorded while members had Chat and Cowork unified turned on."""

    sessions: BetaAnalyticsChatCoworkUnifiedSessionsMetrics
    """
    Cowork session activity recorded while members had Chat and Cowork unified
    turned on.
    """


class BetaAnalyticsUserActivity(BaseModel):
    """Per-user activity data for a given day."""

    chat_metrics: BetaAnalyticsChatMetrics
    """Claude.ai activity metrics for a single user on a given day."""

    claude_code_metrics: BetaAnalyticsClaudeCodeMetrics
    """Claude Code activity metrics for a single user on a given day."""

    cowork_metrics: BetaAnalyticsCoworkMetrics
    """Cowork activity metrics for a single user on a given day."""

    design_metrics: BetaAnalyticsDesignMetrics
    """Claude Design activity metrics for a single user on a given day."""

    office_metrics: BetaAnalyticsOfficeMetrics
    """
    Office Agent activity metrics for a single user on a given day, broken out by
    Office product.
    """

    science_metrics: BetaAnalyticsScienceMetrics
    """Claude Science activity metrics for a single user on a given day."""

    web_search_count: int
    """Number of web searches performed"""

    chat_cowork_unified_metrics: Optional[ChatCoworkUnifiedMetrics] = None
    """
    Activity recorded while the member had Chat and Cowork unified (Cowork's
    features inside claude.ai chat) turned on, split into `chat` (chat activity) and
    `sessions` (Cowork activity). Omitted from the response on deployments that do
    not offer Chat and Cowork unified.
    """

    distinct_user_count: Optional[int] = None
    """Number of distinct active users represented by this row.

    Only set for grouped rollups (`group_by[]`); null for per-user rows. In
    date-range mode, recomputed as an exact distinct count of the group's active
    members over the requested window, never a sum of per-day values.
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

    user: Optional[BetaAnalyticsUser] = None
    """The user this row describes. Null on rows aggregated across users."""
