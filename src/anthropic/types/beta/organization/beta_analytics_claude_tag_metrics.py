from typing import Optional

from ...._models import BaseModel

__all__ = ["BetaAnalyticsClaudeTagMetrics"]


class BetaAnalyticsClaudeTagMetrics(BaseModel):
    """Claude Tag activity metrics for a single linked user on a given day."""

    active_day_count: Optional[int] = None
    """1 on a day the user was active in Claude Tag in Slack, otherwise 0.

    Summed over the window in date-range mode, so it is the number of active days;
    on grouped rows, the total of each member's active days. Null when Claude Tag
    data cannot be read for the request. Otherwise, 0 on a row filtered by project,
    and null on any other row when no covered day was measured.
    """

    active_message_count: Optional[int] = None
    """
    Number of the user's Slack messages that made them active: @-mentions, direct
    messages, group direct message asks, and thread posts Claude answered. Other
    messages are not counted. Null when Claude Tag data cannot be read for the
    request. Otherwise, 0 on a row filtered by project, and null on any other row
    when no covered day was measured.
    """
