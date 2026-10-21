from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsTokenEndpointAuthBasicParam"]


class BetaManagedAgentsTokenEndpointAuthBasicParam(TypedDict, total=False):
    """Token endpoint uses HTTP Basic authentication with client credentials."""

    client_secret: Required[str]
    """
    The OAuth client secret, sent to `token_endpoint` with HTTP Basic
    authentication.
    """

    type: Required[Literal["client_secret_basic"]]
