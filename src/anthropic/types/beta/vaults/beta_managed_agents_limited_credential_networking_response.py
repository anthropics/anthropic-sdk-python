# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsLimitedCredentialNetworkingResponse"]


class BetaManagedAgentsLimitedCredentialNetworkingResponse(BaseModel):
    """The secret is substituted only on requests to the listed hosts."""

    allowed_hosts: List[str]
    """Hostnames on which the secret will be substituted.

    An entry matches the request host exactly; a `*.`-prefixed entry matches any
    subdomain of the named domain but not the domain itself.
    """

    type: Literal["limited"]
