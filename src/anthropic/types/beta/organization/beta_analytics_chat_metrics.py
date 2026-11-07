from typing import Optional

from ...._models import BaseModel

__all__ = ["BetaAnalyticsChatMetrics"]


class BetaAnalyticsChatMetrics(BaseModel):
    """Claude.ai activity metrics for a single user on a given day."""

    connectors_used_count: int
    """Number of MCP connector invocations."""

    distinct_artifacts_created_count: int
    """Number of distinct artifacts created.

    Exact in date-range mode: a creation belongs to exactly one day, so the per-day
    counts never overlap and their sum over the window is the exact count of
    distinct creations in it.
    """

    distinct_connectors_used_count: Optional[int] = None
    """Distinct claude.ai connectors this user used.

    Excludes calls whose connector could not be identified and all calls from
    organizations with zero data retention. Approximate (HLL, typical error <2%) in
    date-range mode. Null on aggregated rows where a distinct count cannot be
    computed.
    """

    distinct_conversation_count: Optional[int] = None
    """Number of distinct conversations the user participated in.

    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """

    distinct_files_uploaded_count: Optional[int] = None
    """Number of distinct files uploaded.

    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """

    distinct_projects_created_count: int
    """Number of distinct projects created.

    Exact in date-range mode: a creation belongs to exactly one day, so the per-day
    counts never overlap and their sum over the window is the exact count of
    distinct creations in it.
    """

    distinct_projects_used_count: Optional[int] = None
    """Number of distinct projects used.

    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """

    distinct_shared_artifacts_viewed_count: Optional[int] = None
    """Number of distinct shared artifacts the user viewed.

    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """

    distinct_skills_used_count: Optional[int] = None
    """Number of distinct skills used.

    Approximate (HLL, typical error <2%) in date-range mode. Null on aggregated rows
    where a distinct count cannot be computed.
    """

    message_count: int
    """Number of messages sent"""

    shared_conversations_viewed_count: int
    """Number of times the user opened a shared conversation in a project"""

    thinking_message_count: int
    """Number of messages that used extended thinking"""
