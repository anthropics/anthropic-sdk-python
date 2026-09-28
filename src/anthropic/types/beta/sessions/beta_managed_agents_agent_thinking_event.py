from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsAgentThinkingEvent"]


class BetaManagedAgentsAgentThinkingEvent(BaseModel):
    """Indicates the agent is making forward progress via extended thinking.

    A progress signal, not a content carrier.
    """

    id: str
    """Unique identifier for this event."""

    processed_at: datetime
    """Timestamp when this thinking was produced."""

    type: Literal["agent.thinking"]
