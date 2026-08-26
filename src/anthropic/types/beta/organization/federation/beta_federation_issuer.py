# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ....._utils import PropertyInfo
from ....._models import BaseModel
from .beta_jwks_inline import BetaJWKSInline
from .beta_jwks_discovery import BetaJWKSDiscovery
from .beta_jwks_explicit_url import BetaJWKSExplicitURL
from .beta_federation_issuer_poll_status import BetaFederationIssuerPollStatus

__all__ = ["BetaFederationIssuer", "JWKS"]

JWKS: TypeAlias = Annotated[
    Union[BetaJWKSDiscovery, BetaJWKSExplicitURL, BetaJWKSInline], PropertyInfo(discriminator="type")
]


class BetaFederationIssuer(BaseModel):
    """Registered external OIDC identity provider.

    Records an external IdP the organization trusts for the RFC 7523
    jwt-bearer grant. The `issuer_url` must match the JWT `iss` claim exactly.
    """

    id: str
    """Tagged ID of the federation issuer."""

    archived_at: Optional[datetime] = None
    """If set, all rules referencing this issuer reject token exchange."""

    archived_by_actor_id: Optional[str] = None
    """Tagged ID (`user_`/`svac_`) of the actor that archived this issuer."""

    check_jti: bool
    """
    Whether the jwt-bearer exchange enforces JTI single-use (replay protection) for
    tokens from this issuer. Applies only to assertions carrying a `jti` claim;
    tokens without one are accepted without single-use enforcement.
    """

    created_at: datetime
    """When this issuer was created."""

    created_by_actor_id: Optional[str] = None
    """Tagged ID (`user_`/`svac_`) of the actor that created this issuer."""

    issuer_url: str
    """The `iss` claim value. Incoming JWTs must match exactly."""

    jwks: JWKS
    """How signing keys are obtained for signature verification."""

    jwks_polling_disabled_at: Optional[datetime] = None
    """
    If set, Anthropic's JWKS poller has paused polling for this issuer after
    repeated fetch failures. Re-enable by sending `jwks_polling_disabled: false` via
    the issuer update endpoint (POST) once the upstream JWKS endpoint is fixed. An
    OAuth caller cannot send this when the issuer backs a rule with any scope other
    than `workspace:developer` or `workspace:inference`; use a Console session.
    """

    max_jwt_lifetime_seconds: int
    """
    Maximum allowed iat→exp spread for assertions from this issuer (1-176400
    seconds, i.e. up to 49h). Assertions must carry both `iat` and `exp`; a missing
    `iat` is rejected.
    """

    name: str
    """Admin-chosen slug identifier."""

    poll_status: Optional[BetaFederationIssuerPollStatus] = None
    """Status of automatic JWKS polling for a federation issuer.

    Anthropic periodically fetches the issuer's signing keys in the background.
    These fields summarize the most recent fetches so the health of the JWKS
    endpoint can be monitored.
    """

    type: Literal["federation_issuer"]

    updated_at: datetime
    """When this issuer was last updated."""

    updated_by_actor_id: Optional[str] = None
    """Tagged ID (`user_`/`svac_`) of the actor that last updated this issuer."""
