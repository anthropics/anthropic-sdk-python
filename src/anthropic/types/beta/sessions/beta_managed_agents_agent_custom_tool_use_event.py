from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsAgentCustomToolUseEvent"]


class BetaManagedAgentsAgentCustomToolUseEvent(BaseModel):
    """Event emitted when the agent calls a custom tool.

    The session goes idle until the client sends a `user.custom_tool_result` event with the result.
    """

    id: str
    """Unique identifier for this event."""

    input: Dict[str, object]
    """Input parameters for the tool call."""

    name: str
    """Name of the custom tool being called."""

    processed_at: datetime
    """A timestamp in RFC 3339 format"""

    type: Literal["agent.custom_tool_use"]

    session_thread_id: Optional[str] = None
    """
    When set, this event was cross-posted from a subagent's thread to surface its
    custom tool use on the primary thread's stream. Empty on the thread's own
    events. Informational only: the server routes the matching
    `user.custom_tool_result` by `custom_tool_use_id`, so clients do not send it
    back.
    """
