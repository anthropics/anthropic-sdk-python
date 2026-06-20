# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsMCPEgressBlockedRunError"]


class BetaManagedAgentsMCPEgressBlockedRunError(BaseModel):
    """
    An MCP server host used by the deployment's agent is blocked by the environment's network policy.
    """

    message: str
    """Human-readable error description."""

    type: Literal["mcp_egress_blocked_error"]
