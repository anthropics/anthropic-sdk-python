from typing import Optional

from ...._models import BaseModel

__all__ = ["BetaAnalyticsChatCoworkUnifiedChatMetrics"]


class BetaAnalyticsChatCoworkUnifiedChatMetrics(BaseModel):
    """
    Chat activity recorded while members had Chat and Cowork unified turned
    on.
    """

    connectors_used_count: int
    """
    Same measure as `chat_metrics.connectors_used_count`, for activity recorded
    while members had Chat and Cowork unified turned on.
    """

    distinct_artifacts_created_count: int
    """
    Same measure as `chat_metrics.distinct_artifacts_created_count`, for activity
    recorded while members had Chat and Cowork unified turned on. Exact in
    date-range mode: a creation belongs to exactly one day, so the per-day counts
    never overlap and their sum over the window is the exact count of distinct
    creations in it.
    """

    distinct_connectors_used_count: Optional[int] = None
    """
    Same measure as `chat_metrics.distinct_connectors_used_count`, for activity
    recorded while members had Chat and Cowork unified turned on. Approximate (HLL,
    typical error <2%) in date-range mode. Null on aggregated rows where a distinct
    count cannot be computed.
    """

    distinct_conversation_count: Optional[int] = None
    """
    Same measure as `chat_metrics.distinct_conversation_count`, for activity
    recorded while members had Chat and Cowork unified turned on. Approximate (HLL,
    typical error <2%) in date-range mode. Null on aggregated rows where a distinct
    count cannot be computed.
    """

    distinct_files_uploaded_count: Optional[int] = None
    """
    Same measure as `chat_metrics.distinct_files_uploaded_count`, for activity
    recorded while members had Chat and Cowork unified turned on. It counts uploaded
    files as well as files Claude created and images returned by Claude's tools,
    such as screenshots. Approximate (HLL, typical error <2%) in date-range mode.
    Null on aggregated rows where a distinct count cannot be computed.
    """

    distinct_projects_created_count: int
    """
    Same measure as `chat_metrics.distinct_projects_created_count`, for activity
    recorded while members had Chat and Cowork unified turned on. Exact in
    date-range mode: a creation belongs to exactly one day, so the per-day counts
    never overlap and their sum over the window is the exact count of distinct
    creations in it.
    """

    distinct_projects_used_count: Optional[int] = None
    """
    Same measure as `chat_metrics.distinct_projects_used_count`, for activity
    recorded while members had Chat and Cowork unified turned on. Approximate (HLL,
    typical error <2%) in date-range mode. Null on aggregated rows where a distinct
    count cannot be computed.
    """

    distinct_shared_artifacts_viewed_count: Optional[int] = None
    """Always null: shared-artifact views are not currently measured."""

    distinct_skills_used_count: Optional[int] = None
    """
    Same measure as `chat_metrics.distinct_skills_used_count`, for activity recorded
    while members had Chat and Cowork unified turned on. Approximate (HLL, typical
    error <2%) in date-range mode. Null on aggregated rows where a distinct count
    cannot be computed.
    """

    message_count: int
    """
    Same measure as `chat_metrics.message_count`, for activity recorded while
    members had Chat and Cowork unified turned on.
    """

    shared_conversations_viewed_count: int
    """
    Same measure as `chat_metrics.shared_conversations_viewed_count`, for activity
    recorded while members had Chat and Cowork unified turned on.
    """

    thinking_message_count: int
    """
    Same measure as `chat_metrics.thinking_message_count`, for activity recorded
    while members had Chat and Cowork unified turned on.
    """
