from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsTokenEndpointAuthPostParam"]


class BetaManagedAgentsTokenEndpointAuthPostParam(TypedDict, total=False):
    """Token endpoint uses POST body authentication with client credentials."""

    client_secret: Required[str]
    """The OAuth client secret, sent to `token_endpoint` in the POST body."""

    type: Required[Literal["client_secret_post"]]
