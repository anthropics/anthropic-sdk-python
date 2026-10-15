from typing import Optional

from ...._models import BaseModel

__all__ = ["BetaAnalyticsCoworkMetrics"]


class BetaAnalyticsCoworkMetrics(BaseModel):
    """Cowork activity metrics for a single user on a given day."""

    action_count: int
    """Number of tool actions completed in Cowork sessions"""

    artifacts_created_count: int
    """
    Number of artifacts created in Cowork sessions: an artifact counts once, on the
    day a session first saves it. Counted from 2026-08-17; 0 on earlier days. Exact
    in date-range mode: a creation belongs to exactly one day, so the per-day counts
    never overlap and their sum over the window is the exact count of distinct
    creations in it.
    """

    connectors_used_count: int
    """Total number of connector invocations in Cowork sessions"""

    dispatch_turn_count: int
    """Number of Dispatch (background agent) turns completed"""

    distinct_connectors_used_count: Optional[int] = None
    """Number of distinct connectors used in Cowork sessions.

    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """

    distinct_session_count: Optional[int] = None
    """Number of distinct Cowork sessions.

    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """

    distinct_skills_used_count: Optional[int] = None
    """Number of distinct skills used in Cowork sessions.

    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """

    message_count: int
    """Number of messages sent in Cowork sessions"""

    skills_used_count: int
    """Total number of skill invocations in Cowork sessions"""

    distinct_plugins_used_count: Optional[int] = None
    """Number of distinct plugins used in Cowork sessions.

    Null while Cowork plugin-use metrics are not enabled for this organization.
    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """

    edit_tool_count: Optional[int] = None
    """Number of successful Edit tool calls in Cowork sessions.

    Null while the file-edit metrics are not enabled for this organization.
    """

    file_edit_count: Optional[int] = None
    """
    Number of successful file-edit tool calls (Edit, MultiEdit, Write, NotebookEdit)
    in Cowork sessions. Null, never 0, while the file-edit metrics are not enabled
    for this organization.
    """

    multi_edit_tool_count: Optional[int] = None
    """Number of successful MultiEdit tool calls in Cowork sessions.

    Null while the file-edit metrics are not enabled for this organization.
    """

    notebook_edit_tool_count: Optional[int] = None
    """Number of successful NotebookEdit tool calls in Cowork sessions.

    Null while the file-edit metrics are not enabled for this organization.
    """

    plugins_used_count: Optional[int] = None
    """Total number of plugin invocations in Cowork sessions.

    Null while Cowork plugin-use metrics are not enabled for this organization.
    """

    sessions_with_file_edits_count: Optional[int] = None
    """
    Number of distinct Cowork sessions with at least one successful file-edit tool
    call. Null while the file-edit metrics are not enabled for this organization.
    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """

    write_tool_count: Optional[int] = None
    """Number of successful Write tool calls in Cowork sessions.

    Null while the file-edit metrics are not enabled for this organization.
    """
