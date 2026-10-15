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
    """RFC 3339 datetime string indicating when the certificate was archived.

    Null if it is still in the trusted set.
    """

    created_at: datetime
    """RFC 3339 datetime string indicating when the certificate was registered."""

    expires_at: Optional[datetime] = None
    """
    RFC 3339 datetime string indicating when the certificate expires, or `null` if
    it does not expire.
    """

    fingerprint: str
    """Lowercase hex SHA-256 fingerprint of the certificate's DER encoding."""

    tunnel_id: str
    """ID of the tunnel the certificate is registered against."""

    type: Literal["tunnel_certificate"]
