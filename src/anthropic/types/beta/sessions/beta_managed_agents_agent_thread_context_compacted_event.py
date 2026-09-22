from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsAgentThreadContextCompactedEvent"]


class BetaManagedAgentsAgentThreadContextCompactedEvent(BaseModel):
    """Indicates that context compaction (summarization) occurred during the session."""

    id: str
    """Unique identifier for this event."""

    processed_at: datetime
    """Timestamp when compaction was processed."""

    type: Literal["agent.thread_context_compacted"]
