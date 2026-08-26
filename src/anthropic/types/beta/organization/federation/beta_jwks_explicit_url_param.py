# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaJWKSExplicitURLParam"]


class BetaJWKSExplicitURLParam(TypedDict, total=False):
    """JWKS fetched from a fixed endpoint."""

    type: Required[Literal["explicit_url"]]

    url: Required[str]
    """JWKS endpoint."""

    ca_cert_pem: Optional[str]
    """Optional custom CA (PEM) for TLS verification of the JWKS fetch."""
