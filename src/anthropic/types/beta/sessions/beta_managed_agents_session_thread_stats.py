# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsSessionThreadStats"]


class BetaManagedAgentsSessionThreadStats(BaseModel):
    """Timing statistics for a session thread."""

    active_seconds: Optional[float] = None
    """Cumulative time in seconds the thread spent actively running.

    Excludes idle time.
    """

    duration_seconds: Optional[float] = None
    """Elapsed time since thread creation in seconds.

    For archived threads, frozen at the final update.
    """

    startup_seconds: Optional[float] = None
    """Time in seconds for the thread to begin running.

    Zero for child threads, which start immediately.
    """
