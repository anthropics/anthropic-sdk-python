# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaJWKSDiscoveryParam"]


class BetaJWKSDiscoveryParam(TypedDict, total=False):
    """JWKS via the issuer's OIDC discovery document."""

    type: Required[Literal["discovery"]]

    ca_cert_pem: Optional[str]
    """Optional custom CA (PEM) for TLS verification of the JWKS fetch."""

    discovery_base: Optional[str]
    """Set when the discovery URL differs from `issuer_url`."""
