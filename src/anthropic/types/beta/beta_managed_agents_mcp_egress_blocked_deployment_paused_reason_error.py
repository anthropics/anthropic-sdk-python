# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsMCPEgressBlockedDeploymentPausedReasonError"]


class BetaManagedAgentsMCPEgressBlockedDeploymentPausedReasonError(BaseModel):
    """
    An MCP server host used by the deployment's agent is blocked by the environment's network policy.
    """

    type: Literal["mcp_egress_blocked_error"]
