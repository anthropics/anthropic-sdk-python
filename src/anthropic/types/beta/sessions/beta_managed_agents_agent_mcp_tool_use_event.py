# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsAgentMCPToolUseEvent"]


class BetaManagedAgentsAgentMCPToolUseEvent(BaseModel):
    """Event emitted when the agent invokes a tool provided by an MCP server."""

    id: str
    """Unique identifier for this event."""

    input: Dict[str, object]
    """Input parameters for the tool call."""

    mcp_server_name: str
    """Name of the MCP server providing the tool."""

    name: str
    """Name of the MCP tool being used."""

    processed_at: datetime
    """A timestamp in RFC 3339 format"""

    type: Literal["agent.mcp_tool_use"]

    evaluated_permission: Optional[Literal["allow", "ask", "deny"]] = None
    """AgentEvaluatedPermission enum"""

    session_thread_id: Optional[str] = None
    """
    When set, this event was cross-posted from a subagent's thread to surface its
    permission request on the primary thread's stream. Empty on the thread's own
    events. Echo this on a `user.tool_confirmation` event to route the approval
    back.
    """
