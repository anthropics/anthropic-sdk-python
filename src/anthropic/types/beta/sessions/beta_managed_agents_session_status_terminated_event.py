from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsSessionStatusTerminatedEvent"]


class BetaManagedAgentsSessionStatusTerminatedEvent(BaseModel):
    """Indicates the session has terminated, either due to an error or completion."""

    id: str
    """Unique identifier for this event."""

    processed_at: datetime
    """Timestamp of status change."""

    type: Literal["session.status_terminated"]
