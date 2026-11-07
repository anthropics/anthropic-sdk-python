from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsSessionDeletedEvent"]


class BetaManagedAgentsSessionDeletedEvent(BaseModel):
    """Emitted when a session has been deleted.

    Terminates any active event stream — no further events will be emitted for this session.
    """

    id: str
    """Unique identifier for this event."""

    processed_at: datetime
    """Timestamp when the session was deleted."""

    type: Literal["session.deleted"]
