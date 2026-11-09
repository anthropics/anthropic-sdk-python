from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Required, TypeAlias, TypedDict

from .beta_managed_agents_token_endpoint_auth_none_param import BetaManagedAgentsTokenEndpointAuthNoneParam
from .beta_managed_agents_token_endpoint_auth_post_param import BetaManagedAgentsTokenEndpointAuthPostParam
from .beta_managed_agents_token_endpoint_auth_basic_param import BetaManagedAgentsTokenEndpointAuthBasicParam

__all__ = ["BetaManagedAgentsMCPOAuthRefreshParams", "TokenEndpointAuth"]

TokenEndpointAuth: TypeAlias = Union[
    BetaManagedAgentsTokenEndpointAuthNoneParam,
    BetaManagedAgentsTokenEndpointAuthBasicParam,
    BetaManagedAgentsTokenEndpointAuthPostParam,
]


class BetaManagedAgentsMCPOAuthRefreshParams(TypedDict, total=False):
    """OAuth refresh token parameters for creating a credential with refresh support."""

    client_id: Required[str]
    """The OAuth client ID to use when refreshing the access token.

    It can't be changed after the credential is created.
    """

    refresh_token: Required[str]
    """
    The OAuth refresh token that the API uses to get a new access token when the
    current one expires.
    """

    token_endpoint: Required[str]
    """Token endpoint URL used to refresh the access token."""

    token_endpoint_auth: Required[TokenEndpointAuth]

    resource: Optional[str]
    """OAuth resource indicator."""

    scope: Optional[str]
    """OAuth scope for the refresh request."""
