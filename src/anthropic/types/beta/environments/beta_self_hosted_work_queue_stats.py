from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaSelfHostedWorkQueueStats"]


class BetaSelfHostedWorkQueueStats(BaseModel):
    """Statistics about the work queue for an environment."""

    depth: int
    """Number of work items waiting to be picked up"""

    oldest_queued_at: Optional[str] = None
    """
    RFC 3339 timestamp of oldest item in the work stream (includes both queued and
    pending items), null if stream empty
    """

    pending: int
    """Number of work items being processed (polled but not acknowledged)"""

    type: Literal["work_queue_stats"]
    """The type of object"""

    workers_polling: Optional[int] = None
    """Number of workers that have polled for work in the last 30 seconds.

    Requires worker_id to be sent with poll requests.
    """
