# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsSessionThreadStatusRunningEvent"]


class BetaManagedAgentsSessionThreadStatusRunningEvent(BaseModel):
    """A session thread has begun executing.

    Emitted on the thread's own stream and cross-posted to the primary stream for child threads.
    """

    id: str
    """Unique identifier for this event."""

    agent_name: str
    """Name of the agent the thread runs."""

    processed_at: datetime
    """A timestamp in RFC 3339 format"""

    session_thread_id: str
    """Public sthr\\__ ID of the thread that started running."""

    type: Literal["session.thread_status_running"]
