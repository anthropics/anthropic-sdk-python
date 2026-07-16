# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaTunnelToken"]


class BetaTunnelToken(BaseModel):
    """A tunnel's connector token."""

    id: str
    """Stable identifier for the current token value.

    Changes when the token is rotated.
    """

    tunnel_token: str
    """The connector token used to run the tunnel. Treat as a credential."""

    type: Literal["tunnel_token"]
