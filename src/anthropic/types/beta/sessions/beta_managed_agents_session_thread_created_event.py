# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsSessionThreadCreatedEvent"]


class BetaManagedAgentsSessionThreadCreatedEvent(BaseModel):
    """Emitted when a subagent is spawned as a new thread.

    Written to the parent thread's output stream so clients observing the session see child creation.
    """

    id: str
    """Unique identifier for this event."""

    agent_name: str
    """Name of the callable agent the thread runs."""

    processed_at: datetime
    """A timestamp in RFC 3339 format"""

    session_thread_id: str
    """Public `sthr_` ID of the newly created thread."""

    type: Literal["session.thread_created"]
