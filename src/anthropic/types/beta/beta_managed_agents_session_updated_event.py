# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_managed_agents_session_agent import BetaManagedAgentsSessionAgent

__all__ = ["BetaManagedAgentsSessionUpdatedEvent"]


class BetaManagedAgentsSessionUpdatedEvent(BaseModel):
    """Emitted when an UpdateSession request changed at least one field.

    Carries only the fields that changed; absent fields were not part of the update. The new configuration applies from the next turn.
    """

    id: str
    """Unique identifier for this event."""

    processed_at: datetime
    """A timestamp in RFC 3339 format"""

    type: Literal["session.updated"]

    agent: Optional[BetaManagedAgentsSessionAgent] = None
    """Resolved `agent` definition for a `session`.

    Snapshot of the `agent` at `session` creation time.
    """

    metadata: Optional[Dict[str, str]] = None
    """The session's full metadata bag after the update.

    Present when the update set non-empty metadata; absent when metadata was
    unchanged or cleared to empty.
    """

    title: Optional[str] = None
    """The session's new title. Present only when the update changed it."""
