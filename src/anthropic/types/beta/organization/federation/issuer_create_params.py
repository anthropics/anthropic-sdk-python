# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Optional
from typing_extensions import Required, Annotated, TypeAlias, TypedDict

from ....._utils import PropertyInfo
from .beta_jwks_inline_param import BetaJWKSInlineParam
from ....anthropic_beta_param import AnthropicBetaParam
from .beta_jwks_discovery_param import BetaJWKSDiscoveryParam
from .beta_jwks_explicit_url_param import BetaJWKSExplicitURLParam

__all__ = ["IssuerCreateParams", "JWKS"]


class IssuerCreateParams(TypedDict, total=False):
    issuer_url: Required[str]
    """The `iss` claim value to match against."""

    name: Required[str]
    """Slug identifier (lowercase, digits, hyphens).

    Unique within the organization; a duplicate name returns 409.
    """

    check_jti: Optional[bool]
    """
    Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for
    tokens from this issuer. Defaults to true. Applies only to assertions carrying a
    `jti` claim; tokens without one are accepted without single-use enforcement.
    """

    jwks: JWKS
    """How signing keys are obtained. Defaults to OIDC discovery."""

    max_jwt_lifetime_seconds: Optional[int]
    """
    Maximum allowed iat→exp spread for assertions from this issuer (1-176400
    seconds, i.e. up to 49h). Defaults to 3600 (1h). Assertions must carry both
    `iat` and `exp`; a missing `iat` is rejected.
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""


JWKS: TypeAlias = Union[BetaJWKSDiscoveryParam, BetaJWKSExplicitURLParam, BetaJWKSInlineParam]
