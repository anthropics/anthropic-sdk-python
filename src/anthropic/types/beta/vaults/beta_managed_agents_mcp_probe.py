# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ...._models import BaseModel
from .beta_managed_agents_refresh_http_response import BetaManagedAgentsRefreshHTTPResponse

__all__ = ["BetaManagedAgentsMCPProbe"]


class BetaManagedAgentsMCPProbe(BaseModel):
    """The failing step of an MCP validation probe."""

    http_response: Optional[BetaManagedAgentsRefreshHTTPResponse] = None
    """An HTTP response captured during a credential validation probe."""

    method: str
    """The MCP method that failed (for example `initialize` or `tools/list`)."""
