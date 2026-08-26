# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaJWKSExplicitURL"]


class BetaJWKSExplicitURL(BaseModel):
    """JWKS fetched from a fixed endpoint."""

    type: Literal["explicit_url"]

    url: str
    """JWKS endpoint."""

    ca_cert_pem: Optional[str] = None
    """Optional custom CA (PEM) for TLS verification of the JWKS fetch."""
