from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tunnel_token import BetaTunnelToken

__all__ = ["BetaRelayTunnelTransport"]


class BetaRelayTunnelTransport(BaseModel):
    """The tunnel is connected through Anthropic's relay.

    In the create response `token` is the tunnel's relay token, shown that once (only a hash is kept, so reveal_token refuses a relay tunnel and rotate_token issues a new one); reads never carry it.
    """

    type: Literal["relay"]

    token: Optional[BetaTunnelToken] = None
    """The tunnel's relay token.

    Present only in the create response, which issues it; absent on every read.
    Store it: Anthropic keeps only a hash, reveal_token refuses a relay tunnel, and
    rotate_token is the only way to obtain a new one.
    """
