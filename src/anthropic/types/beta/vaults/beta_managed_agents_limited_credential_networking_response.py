from typing import List
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsLimitedCredentialNetworkingResponse"]


class BetaManagedAgentsLimitedCredentialNetworkingResponse(BaseModel):
    """The secret is substituted only on requests to the listed hosts."""

    allowed_hosts: List[str]
    """
    The destination hosts of the outbound requests that the credential's secret is
    substituted into.

    An entry matches the request host exactly. An entry such as `*.example.com`
    matches any subdomain of `example.com` but not `example.com` itself.
    """

    type: Literal["limited"]
