from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tunnel_transport import BetaTunnelTransport

__all__ = ["BetaTunnel"]


class BetaTunnel(BaseModel):
    """An MCP tunnel."""

    id: str
    """Unique identifier for the tunnel, prefixed with `tnl_`."""

    archived_at: Optional[datetime] = None
    """RFC 3339 datetime string indicating when the tunnel was archived.

    Null if it is not archived.
    """

    created_at: datetime
    """RFC 3339 datetime string indicating when the tunnel was created."""

    display_name: Optional[str] = None
    """Human-readable name for the tunnel (1-255 characters). Null if unset."""

    domain: str
    """Anthropic-assigned hostname for the tunnel.

    MCP server URLs whose host is a subdomain of this value are routed through the
    tunnel. Globally unique and never reused, even after the tunnel is archived.
    """

    transport: BetaTunnelTransport
    """How traffic reaches the tunnel.

    Chosen by Anthropic per organization when the tunnel is created; read-only and
    present on every tunnel, so automation can tell which connector to deploy. A
    union discriminated on `type`: `{"type": "cloudflare"}` or `{"type": "relay"}`.
    In the create response a `relay` tunnel's transport also carries `token`, its
    relay token, shown that once; no read carries a token.
    """

    type: Literal["tunnel"]
