# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaServiceAccountTarget"]


class BetaServiceAccountTarget(BaseModel):
    """Bind to a fixed service account by ID."""

    service_account_id: str
    """Tagged ID of the service account to mint tokens for."""

    type: Literal["service_account"]

    service_account_name: Optional[str] = None
    """Service account's display name at read time. Ignored on writes."""
