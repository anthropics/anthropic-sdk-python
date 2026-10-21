from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsSessionStatusRunningEvent"]


class BetaManagedAgentsSessionStatusRunningEvent(BaseModel):
    """Indicates the session is actively running and the agent is working."""

    id: str
    """Unique identifier for this event."""

    processed_at: datetime
    """Timestamp of status change."""

    type: Literal["session.status_running"]
