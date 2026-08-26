# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypedDict

__all__ = ["APIKeyUpdateParams"]


class APIKeyUpdateParams(TypedDict, total=False):
    name: Optional[str]
    """Name of the API key."""

    status: Optional[Literal["active", "archived", "inactive"]]
    """Status of the API key."""
