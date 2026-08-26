# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from ....._models import BaseModel

__all__ = ["BetaFederationIssuerPollStatus"]


class BetaFederationIssuerPollStatus(BaseModel):
    """Status of automatic JWKS polling for a federation issuer.

    Anthropic periodically fetches the issuer's signing keys in the
    background. These fields summarize the most recent fetches so the
    health of the JWKS endpoint can be monitored.
    """

    consecutive_failures: int
    """Consecutive fetch failures since the last success."""

    last_fetched_at: Optional[datetime] = None
    """When the last successful fetch completed."""

    next_poll_at: Optional[datetime] = None
    """When the next fetch is scheduled. Null if paused."""
