from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .jwks_inline import JWKSInline
from .jwks_discovery import JWKSDiscovery
from .jwks_explicit_url import JWKSExplicitURL
from .federation_issuer_poll_status import FederationIssuerPollStatus

__all__ = ["FederationIssuer", "JWKS"]

JWKS: TypeAlias = Annotated[Union[JWKSDiscovery, JWKSExplicitURL, JWKSInline], UnionDiscriminator("type")]


class FederationIssuer(BaseModel):
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

    poll_status: Optional[FederationIssuerPollStatus] = None
    """Live state of Anthropic's JWKS polling for this issuer.

    Populated on both single-issuer retrieval and list responses, including archived
    issuers. Typically null for inline-key issuers (no polling), or when poll status
    is temporarily unavailable or polling has not started yet.
    """

    type: Literal["federation_issuer"]

    updated_at: datetime
    """When this issuer was last updated."""

    updated_by_actor_id: Optional[str] = None
    """Tagged ID (`user_`/`svac_`) of the actor that last updated this issuer."""
