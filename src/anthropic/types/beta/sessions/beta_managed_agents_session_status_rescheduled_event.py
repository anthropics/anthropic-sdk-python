from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsSessionStatusRescheduledEvent"]


class BetaManagedAgentsSessionStatusRescheduledEvent(BaseModel):
    """
    Indicates the session is recovering from an error state and is rescheduled for execution.
    """

    id: str
    """Unique identifier for this event."""

    processed_at: datetime
    """Timestamp of status change."""

    type: Literal["session.status_rescheduled"]
