from typing import Optional

from ...._models import BaseModel
from .beta_managed_agents_refresh_http_response import BetaManagedAgentsRefreshHTTPResponse

__all__ = ["BetaManagedAgentsMCPProbe"]


class BetaManagedAgentsMCPProbe(BaseModel):
    """The failing step of an MCP validation probe."""

    http_response: Optional[BetaManagedAgentsRefreshHTTPResponse] = None
    """
    The HTTP error response from the MCP server, or `null` if the MCP server didn't
    return one for the failing step, for example after a timeout or a DNS or TLS
    failure.
    """

    method: str
    """The MCP method that failed (for example `initialize` or `tools/list`)."""
