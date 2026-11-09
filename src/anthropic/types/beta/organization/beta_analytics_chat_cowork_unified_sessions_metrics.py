from typing import Optional

from ...._models import BaseModel

__all__ = ["BetaAnalyticsChatCoworkUnifiedSessionsMetrics"]


class BetaAnalyticsChatCoworkUnifiedSessionsMetrics(BaseModel):
    """
    Cowork session activity recorded while members had Chat and Cowork
    unified turned on.
    """

    action_count: int
    """
    Same measure as `cowork_metrics.action_count`, for activity recorded while
    members had Chat and Cowork unified turned on.
    """

    artifacts_created_count: int
    """
    Same measure as `cowork_metrics.artifacts_created_count`, for activity recorded
    while members had Chat and Cowork unified turned on. Exact in date-range mode: a
    creation belongs to exactly one day, so the per-day counts never overlap and
    their sum over the window is the exact count of distinct creations in it.
    """

    connectors_used_count: int
    """
    Same measure as `cowork_metrics.connectors_used_count`, for activity recorded
    while members had Chat and Cowork unified turned on.
    """

    dispatch_turn_count: int
    """
    Same measure as `cowork_metrics.dispatch_turn_count`, for activity recorded
    while members had Chat and Cowork unified turned on.
    """

    distinct_connectors_used_count: Optional[int] = None
    """
    Same measure as `cowork_metrics.distinct_connectors_used_count`, for activity
    recorded while members had Chat and Cowork unified turned on. Approximate (HLL,
    typical error <2%) in date-range mode. Null on aggregated rows where a distinct
    count cannot be computed.
    """

    distinct_plugins_used_count: Optional[int] = None
    """
    Same measure as `cowork_metrics.distinct_plugins_used_count`, for activity
    recorded while members had Chat and Cowork unified turned on. Approximate (HLL,
    typical error <2%) in date-range mode. Null on aggregated rows where a distinct
    count cannot be computed.
    """

    distinct_session_count: Optional[int] = None
    """
    Same measure as `cowork_metrics.distinct_session_count`, for activity recorded
    while members had Chat and Cowork unified turned on. Approximate (HLL, typical
    error <2%) in date-range mode. Null on aggregated rows where a distinct count
    cannot be computed.
    """

    distinct_skills_used_count: Optional[int] = None
    """
    Same measure as `cowork_metrics.distinct_skills_used_count`, for activity
    recorded while members had Chat and Cowork unified turned on. Approximate (HLL,
    typical error <2%) in date-range mode. Null on aggregated rows where a distinct
    count cannot be computed.
    """

    edit_tool_count: Optional[int] = None
    """
    Same measure as `cowork_metrics.edit_tool_count`, for activity recorded while
    members had Chat and Cowork unified turned on.
    """

    file_edit_count: Optional[int] = None
    """
    Same measure as `cowork_metrics.file_edit_count`, for activity recorded while
    members had Chat and Cowork unified turned on.
    """

    message_count: int
    """
    Same measure as `cowork_metrics.message_count`, for activity recorded while
    members had Chat and Cowork unified turned on.
    """

    multi_edit_tool_count: Optional[int] = None
    """
    Same measure as `cowork_metrics.multi_edit_tool_count`, for activity recorded
    while members had Chat and Cowork unified turned on. Claude no longer has a
    multi-edit tool, so expect 0 when not null; each edit is now a separate Edit
    tool call, counted in `edit_tool_count` and `file_edit_count`.
    """

    notebook_edit_tool_count: Optional[int] = None
    """
    Same measure as `cowork_metrics.notebook_edit_tool_count`, for activity recorded
    while members had Chat and Cowork unified turned on.
    """

    plugins_used_count: Optional[int] = None
    """
    Same measure as `cowork_metrics.plugins_used_count`, for activity recorded while
    members had Chat and Cowork unified turned on.
    """

    sessions_with_file_edits_count: Optional[int] = None
    """
    Same measure as `cowork_metrics.sessions_with_file_edits_count`, for activity
    recorded while members had Chat and Cowork unified turned on. Approximate (HLL,
    typical error <2%) in date-range mode. Null on aggregated rows where a distinct
    count cannot be computed.
    """

    skills_used_count: int
    """
    Same measure as `cowork_metrics.skills_used_count`, for activity recorded while
    members had Chat and Cowork unified turned on.
    """

    write_tool_count: Optional[int] = None
    """
    Same measure as `cowork_metrics.write_tool_count`, for activity recorded while
    members had Chat and Cowork unified turned on.
    """
