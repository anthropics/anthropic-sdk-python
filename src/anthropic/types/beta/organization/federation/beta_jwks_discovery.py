# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaJWKSDiscovery"]


class BetaJWKSDiscovery(BaseModel):
    """JWKS via the issuer's OIDC discovery document."""

    type: Literal["discovery"]

    ca_cert_pem: Optional[str] = None
    """Optional custom CA (PEM) for TLS verification of the JWKS fetch."""

    discovery_base: Optional[str] = None
    """Set when the discovery URL differs from `issuer_url`."""
