# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaTunnelCertificate"]


class BetaTunnelCertificate(BaseModel):
    """A CA certificate attached to a tunnel."""

    id: str
    """Unique identifier for the certificate, prefixed with `tcrt_`."""

    archived_at: Optional[datetime] = None
    """A timestamp in RFC 3339 format"""

    created_at: datetime
    """A timestamp in RFC 3339 format"""

    expires_at: Optional[datetime] = None
    """A timestamp in RFC 3339 format"""

    fingerprint: str
    """Lowercase hex SHA-256 fingerprint of the certificate's DER encoding."""

    tunnel_id: str
    """ID of the tunnel the certificate is registered against."""

    type: Literal["tunnel_certificate"]
