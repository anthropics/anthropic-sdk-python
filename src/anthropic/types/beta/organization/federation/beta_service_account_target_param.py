# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaServiceAccountTargetParam"]


class BetaServiceAccountTargetParam(TypedDict, total=False):
    """Bind to a fixed service account by ID."""

    service_account_id: Required[str]
    """Tagged ID of the service account to mint tokens for."""

    type: Required[Literal["service_account"]]

    service_account_name: Optional[str]
    """Service account's display name at read time. Ignored on writes."""
