from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypedDict

__all__ = ["ServiceAccountUpdateParams"]


class ServiceAccountUpdateParams(TypedDict, total=False):
    description: Optional[str]
    """Replaces the description.

    Omit to leave unchanged; send `null` to clear (the field is stored as an empty
    string).
    """

    organization_role: Optional[Literal["admin", "developer"]]
    """Replaces the org-level role. Omit or send `null` to leave unchanged."""
