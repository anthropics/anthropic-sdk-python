from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaCloudflareTunnelTransport"]


class BetaCloudflareTunnelTransport(BaseModel):
    """The tunnel is connected through the Cloudflare connector.

    Its connector token is fetched with reveal_token. `type` is transitional: it reads `relay` for every tunnel once the Cloudflare transport is retired.
    """

    type: Literal["cloudflare"]
