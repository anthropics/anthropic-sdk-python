from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .beta_relay_tunnel_transport import BetaRelayTunnelTransport
from .beta_cloudflare_tunnel_transport import BetaCloudflareTunnelTransport

__all__ = ["BetaTunnelTransport"]

BetaTunnelTransport: TypeAlias = Annotated[
    Union[BetaCloudflareTunnelTransport, BetaRelayTunnelTransport], UnionDiscriminator("type")
]
