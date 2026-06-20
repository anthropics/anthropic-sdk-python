# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsUnrestrictedCredentialNetworkingResponse"]


class BetaManagedAgentsUnrestrictedCredentialNetworkingResponse(BaseModel):
    """
    The secret is substituted on any host the session's Environment network policy permits egress to.
    """

    type: Literal["unrestricted"]
