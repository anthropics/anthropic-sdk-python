# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsScheduleParams"]


class BetaManagedAgentsScheduleParams(TypedDict, total=False):
    """5-field POSIX cron schedule.

    Literal wall-clock matching in the configured timezone.
    """

    expression: Required[str]
    """
    5-field POSIX cron expression: minute hour day-of-month month day-of-week (e.g.,
    "0 9 \\** \\** 1-5" for weekdays at 9am). Day-of-week is 0-7 where 0 and 7 both mean
    Sunday. Extended cron syntax - seconds or year fields, and the special
    characters L, W, #, and ? - is not supported, nor are predefined shortcuts
    (@daily).
    """

    timezone: Required[str]
    """Required.

    IANA timezone identifier (e.g., "America/Los_Angeles", "UTC"). Validated against
    the IANA timezone database.
    """

    type: Required[Literal["cron"]]
