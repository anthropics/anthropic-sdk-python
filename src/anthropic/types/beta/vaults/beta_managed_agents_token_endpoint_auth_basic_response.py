from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsTokenEndpointAuthBasicResponse"]


class BetaManagedAgentsTokenEndpointAuthBasicResponse(BaseModel):
    """Token endpoint uses HTTP Basic authentication with client credentials."""

    type: Literal["client_secret_basic"]
