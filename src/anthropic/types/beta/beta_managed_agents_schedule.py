# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsSchedule"]


class BetaManagedAgentsSchedule(BaseModel):
    """5-field POSIX cron schedule with computed runtime timestamps."""

    expression: str
    """
    5-field POSIX cron expression: minute hour day-of-month month day-of-week (e.g.,
    "0 9 \\** \\** 1-5" for weekdays at 9am). Day-of-week is 0-7 where 0 and 7 both mean
    Sunday. Extended cron syntax - seconds or year fields, and the special
    characters L, W, #, and ? - is not supported, nor are predefined shortcuts
    (@daily).
    """

    timezone: str
    """IANA timezone identifier (e.g., "America/Los_Angeles", "UTC")."""

    type: Literal["cron"]

    last_run_at: Optional[datetime] = None
    """A timestamp in RFC 3339 format"""

    upcoming_runs_at: Optional[List[datetime]] = None
    """Up to 5 timestamps of upcoming cron occurrences.

    Non-empty for active and paused deployments (reflects what the schedule would do
    if unpaused); empty once the deployment is archived (`archived_at` set). Each
    fire is offset by a small per-schedule jitter, so a run will actually start at
    or shortly after its listed time.
    """
