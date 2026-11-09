from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_managed_agents_agent_tool_evaluation import BetaManagedAgentsAgentToolEvaluation
from .beta_managed_agents_agent_evaluated_permission import BetaManagedAgentsAgentEvaluatedPermission

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
    """Timestamp when this event was processed."""

    type: Literal["agent.mcp_tool_use"]

    evaluated_permission: Optional[BetaManagedAgentsAgentEvaluatedPermission] = None
    """The evaluated permission policy for this tool invocation."""

    evaluation: Optional[BetaManagedAgentsAgentToolEvaluation] = None
    """
    Which resolved permission_policy produced evaluated_permission: always_allow,
    always_ask, or auto (with the server's per-invocation judgement). Absent only
    when the server refused the call before any policy applied (for example, the
    named tool is not enabled in the session); such a refusal has
    evaluated_permission deny. An event recorded before this field existed reads as
    the arm its evaluated_permission implies (always_allow for allow, always_ask for
    ask).
    """

    session_thread_id: Optional[str] = None
    """
    When set, this event was cross-posted from a subagent's thread to surface its
    permission request on the primary thread's stream. Empty on the thread's own
    events. Informational only: the server routes the matching
    `user.tool_confirmation` by `tool_use_id`, so clients do not send it back.
    """
