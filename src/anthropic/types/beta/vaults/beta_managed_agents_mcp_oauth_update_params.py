from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Required, TypedDict

from .beta_managed_agents_mcp_oauth_refresh_update_params import BetaManagedAgentsMCPOAuthRefreshUpdateParams

__all__ = ["BetaManagedAgentsMCPOAuthUpdateParams"]


class BetaManagedAgentsMCPOAuthUpdateParams(TypedDict, total=False):
    """Parameters for updating an MCP OAuth credential.

    The `mcp_server_url` is immutable.
    """

    type: Required[Literal["mcp_oauth"]]

    access_token: Optional[str]
    """The new OAuth access token to replace the stored one."""

    expires_at: Union[str, datetime, None]
    """When the credential's access token expires, in RFC 3339.

    Leave it out to keep the stored expiry.

    If you send a new `access_token`, send its `expires_at` too, or the new token
    keeps the old expiry.

    Must be in the future.
    """

    refresh: Optional[BetaManagedAgentsMCPOAuthRefreshUpdateParams]
    """Updated refresh token configuration."""
