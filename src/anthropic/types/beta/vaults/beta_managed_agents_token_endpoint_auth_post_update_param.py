from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsTokenEndpointAuthPostUpdateParam"]


class BetaManagedAgentsTokenEndpointAuthPostUpdateParam(TypedDict, total=False):
    """Updated POST body authentication parameters for the token endpoint."""

    type: Required[Literal["client_secret_post"]]

    client_secret: Optional[str]
    """A new OAuth client secret to replace the stored one.

    The credential must already use `client_secret_basic` or `client_secret_post`.
    It keeps its current `token_endpoint_auth` type, even if the `type` sent with
    this secret is the other one.
    """
