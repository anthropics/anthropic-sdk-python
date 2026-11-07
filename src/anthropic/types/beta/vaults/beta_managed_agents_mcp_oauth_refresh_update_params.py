from __future__ import annotations

from typing import Union, Optional
from typing_extensions import TypeAlias, TypedDict

from .beta_managed_agents_token_endpoint_auth_post_update_param import BetaManagedAgentsTokenEndpointAuthPostUpdateParam
from .beta_managed_agents_token_endpoint_auth_basic_update_param import (
    BetaManagedAgentsTokenEndpointAuthBasicUpdateParam,
)

__all__ = ["BetaManagedAgentsMCPOAuthRefreshUpdateParams", "TokenEndpointAuth"]

TokenEndpointAuth: TypeAlias = Union[
    BetaManagedAgentsTokenEndpointAuthBasicUpdateParam, BetaManagedAgentsTokenEndpointAuthPostUpdateParam
]


class BetaManagedAgentsMCPOAuthRefreshUpdateParams(TypedDict, total=False):
    """Parameters for updating OAuth refresh token configuration."""

    refresh_token: Optional[str]
    """The new OAuth refresh token to replace the stored one."""

    scope: Optional[str]
    """The new OAuth scope for refresh requests.

    Send an empty string to clear the stored scope.
    """

    token_endpoint_auth: TokenEndpointAuth
