from typing import Optional
from datetime import datetime

from ...._models import BaseModel

__all__ = ["BetaAnalyticsSingleDayActivitySummary"]


class BetaAnalyticsSingleDayActivitySummary(BaseModel):
    """Per-day entry in the /summaries response."""

    assigned_seat_count: Optional[int] = None
    """Number of seats currently assigned to members.

    Null when the response is scoped to an RBAC group — seat assignment is org-wide
    and has no per-group analogue.
    """

    cowork_daily_active_user_count: int
    """Number of users with Cowork activity on the requested day"""

    cowork_monthly_active_user_count: int
    """Number of users with Cowork activity in the 30-day rolling window"""

    cowork_weekly_active_user_count: int
    """Number of users with Cowork activity in the 7-day rolling window"""

    daily_active_user_count: int
    """Number of users with token consumption on the requested day"""

    daily_adoption_rate: Optional[float] = None
    """
    Percentage of assigned seats with activity on the requested day
    (`DAU / assigned_seat_count * 100`). Null when the response is scoped to an RBAC
    group.
    """

    ending_at: datetime
    """End of the aggregation period (exclusive), UTC midnight in RFC 3339 format (e.g.

    `2026-01-16T00:00:00Z`).
    """

    monthly_active_user_count: int
    """Number of users with token consumption in the 30-day rolling window"""

    monthly_adoption_rate: Optional[float] = None
    """
    Percentage of assigned seats with activity in the 30-day rolling window
    (`MAU / assigned_seat_count * 100`). Null when the response is scoped to an RBAC
    group.
    """

    pending_invite_count: Optional[int] = None
    """Number of pending invitations to join the organization.

    Null when the response is scoped to an RBAC group.
    """

    starting_at: datetime
    """
    Start of the aggregation period (inclusive), UTC midnight in RFC 3339 format
    (e.g. `2026-01-15T00:00:00Z`).
    """

    weekly_active_user_count: int
    """Number of users with token consumption in the 7-day rolling window"""

    weekly_adoption_rate: Optional[float] = None
    """
    Percentage of assigned seats with activity in the 7-day rolling window
    (`WAU / assigned_seat_count * 100`). Null when the response is scoped to an RBAC
    group.
    """

    chat_daily_active_user_count: Optional[int] = None
    """Number of users with claude.ai (chat) activity on the requested day.

    Omitted from the response while the per-product breakdown is not enabled for
    this organization.
    """

    chat_monthly_active_user_count: Optional[int] = None
    """Number of users with claude.ai (chat) activity in the 30-day rolling window.

    Omitted from the response while the per-product breakdown is not enabled for
    this organization.
    """

    chat_weekly_active_user_count: Optional[int] = None
    """Number of users with claude.ai (chat) activity in the 7-day rolling window.

    Omitted from the response while the per-product breakdown is not enabled for
    this organization.
    """

    claude_code_daily_active_user_count: Optional[int] = None
    """Number of users with Claude Code activity on the requested day.

    Omitted from the response while the per-product breakdown is not enabled for
    this organization.
    """

    claude_code_monthly_active_user_count: Optional[int] = None
    """Number of users with Claude Code activity in the 30-day rolling window.

    Omitted from the response while the per-product breakdown is not enabled for
    this organization.
    """

    claude_code_weekly_active_user_count: Optional[int] = None
    """Number of users with Claude Code activity in the 7-day rolling window.

    Omitted from the response while the per-product breakdown is not enabled for
    this organization.
    """

    claude_design_daily_active_user_count: Optional[int] = None
    """Number of users with Claude Design activity on the requested day.

    Omitted from the response while the per-product breakdown is not enabled for
    this organization.
    """

    claude_design_monthly_active_user_count: Optional[int] = None
    """Number of users with Claude Design activity in the 30-day rolling window.

    Omitted from the response while the per-product breakdown is not enabled for
    this organization.
    """

    claude_design_weekly_active_user_count: Optional[int] = None
    """Number of users with Claude Design activity in the 7-day rolling window.

    Omitted from the response while the per-product breakdown is not enabled for
    this organization.
    """

    office_agent_daily_active_user_count: Optional[int] = None
    """Number of users with Claude in Office activity on the requested day.

    Omitted from the response while the per-product breakdown is not enabled for
    this organization.
    """

    office_agent_monthly_active_user_count: Optional[int] = None
    """Number of users with Claude in Office activity in the 30-day rolling window.

    Omitted from the response while the per-product breakdown is not enabled for
    this organization.
    """

    office_agent_weekly_active_user_count: Optional[int] = None
    """Number of users with Claude in Office activity in the 7-day rolling window.

    Omitted from the response while the per-product breakdown is not enabled for
    this organization.
    """

    science_daily_active_user_count: Optional[int] = None
    """Number of users with Claude Science activity on the requested day.

    Omitted from the response while the per-product breakdown is not enabled for
    this organization.
    """

    science_entitled_user_count: Optional[int] = None
    """
    Number of users with a Claude Science seat entitlement (per-seat RBAC) at the
    time of the daily snapshot. The funnel top; independent of the org-level Claude
    Science toggle. Null when the response is scoped to an RBAC group — entitlement
    is org-wide and has no per-group analogue. Omitted from the response while the
    per-product breakdown is not enabled for this organization.
    """

    science_monthly_active_user_count: Optional[int] = None
    """Number of users with Claude Science activity in the 30-day rolling window.

    Omitted from the response while the per-product breakdown is not enabled for
    this organization.
    """

    science_weekly_active_user_count: Optional[int] = None
    """Number of users with Claude Science activity in the 7-day rolling window.

    Omitted from the response while the per-product breakdown is not enabled for
    this organization.
    """
