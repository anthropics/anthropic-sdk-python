# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Optional
from typing_extensions import Annotated, TypeAlias, TypedDict

from ....._utils import PropertyInfo
from .beta_jwks_inline_param import BetaJWKSInlineParam
from ....anthropic_beta_param import AnthropicBetaParam
from .beta_jwks_discovery_param import BetaJWKSDiscoveryParam
from .beta_jwks_explicit_url_param import BetaJWKSExplicitURLParam

__all__ = ["IssuerUpdateParams", "JWKS"]


class IssuerUpdateParams(TypedDict, total=False):
    check_jti: Optional[bool]
    """
    Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for
    tokens from this issuer. Applies only to assertions carrying a `jti` claim;
    tokens without one are accepted without single-use enforcement.
    """

    issuer_url: Optional[str]
    """Replaces the `iss` claim value to match against.

    For discovery-mode issuers without a `discovery_base`, this is also the URL
    Anthropic fetches the OIDC discovery document and signing keys from, so changing
    it repoints the JWKS source. Changing the issuer URL to a well-known shared
    platform is rejected while any live rule under this issuer would not constrain
    tenant identity.
    """

    jwks: Optional[JWKS]
    """Replaces the entire JWKS configuration."""

    jwks_polling_disabled: Optional[bool]
    """Only `false` is accepted, to re-enable polling after the system pauses it.

    Polling is paused automatically; sending `true` is rejected.
    """

    max_jwt_lifetime_seconds: Optional[int]
    """
    Maximum allowed iat→exp spread for assertions from this issuer (1-176400
    seconds, i.e. up to 49h). Assertions must carry both `iat` and `exp`; a missing
    `iat` is rejected.
    """

    name: Optional[str]
    """Replaces the slug identifier (lowercase, digits, hyphens).

    Unique within the organization; a duplicate name returns 409.
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""


JWKS: TypeAlias = Union[BetaJWKSDiscoveryParam, BetaJWKSExplicitURLParam, BetaJWKSInlineParam]
