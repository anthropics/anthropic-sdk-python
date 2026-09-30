from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ServiceAccountCreateParams"]


class ServiceAccountCreateParams(TypedDict, total=False):
    name: Required[str]
    """Slug identifier (lowercase, digits, hyphens).

    Unique within the organization; a duplicate name returns 409.
    """

    description: Optional[str]
    """Optional free-text description."""

    organization_role: Literal["admin", "developer"]
    """Org-level role. Defaults to `developer`."""
