# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_managed_agents_system_content_block import BetaManagedAgentsSystemContentBlock

__all__ = ["BetaManagedAgentsSystemMessageEvent"]


class BetaManagedAgentsSystemMessageEvent(BaseModel):
    """A mid-conversation system message event.

    Carries system-role content that is appended to the session as a `role: "system"` turn.
    """

    id: str
    """Unique identifier for this event."""

    content: List[BetaManagedAgentsSystemContentBlock]
    """System content blocks. Text-only."""

    type: Literal["system.message"]

    processed_at: Optional[datetime] = None
    """A timestamp in RFC 3339 format"""
