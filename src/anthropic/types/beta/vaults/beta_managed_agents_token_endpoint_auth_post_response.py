from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsTokenEndpointAuthPostResponse"]


class BetaManagedAgentsTokenEndpointAuthPostResponse(BaseModel):
    """Token endpoint uses POST body authentication with client credentials."""

    type: Literal["client_secret_post"]
