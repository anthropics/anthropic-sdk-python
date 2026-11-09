from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsSpanModelRequestStartEvent"]


class BetaManagedAgentsSpanModelRequestStartEvent(BaseModel):
    """Emitted when a model request is initiated by the agent."""

    id: str
    """Unique identifier for this event."""

    processed_at: datetime
    """Timestamp when the model request started."""

    type: Literal["span.model_request_start"]
