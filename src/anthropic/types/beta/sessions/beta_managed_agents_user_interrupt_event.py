# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsUserInterruptEvent"]


class BetaManagedAgentsUserInterruptEvent(BaseModel):
    """An interrupt event that pauses agent execution and returns control to the user."""

    id: str
    """Unique identifier for this event."""

    type: Literal["user.interrupt"]

    processed_at: Optional[datetime] = None
    """A timestamp in RFC 3339 format"""

    session_thread_id: Optional[str] = None
    """
    If absent, interrupts every non-archived thread in a multiagent session (or the
    primary alone in a single-agent session). If present, interrupts only the named
    thread.
    """
