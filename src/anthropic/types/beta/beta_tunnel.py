# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaTunnel"]


class BetaTunnel(BaseModel):
    """An MCP tunnel."""

    id: str
    """Unique identifier for the tunnel, prefixed with `tnl_`."""

    archived_at: Optional[datetime] = None
    """A timestamp in RFC 3339 format"""

    created_at: datetime
    """A timestamp in RFC 3339 format"""

    display_name: Optional[str] = None
    """Human-readable name for the tunnel (1-255 characters). Null if unset."""

    domain: str
    """Anthropic-assigned hostname for the tunnel.

    MCP server URLs whose host is a subdomain of this value are routed through the
    tunnel. Globally unique and never reused, even after the tunnel is archived.
    """

    type: Literal["tunnel"]
