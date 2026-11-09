from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["RuleListParams"]


class RuleListParams(TypedDict, total=False):
    include_archived: bool
    """Include archived resources. Defaults to false."""

    issuer_id: Optional[str]
    """Filter to rules referencing this federation issuer."""

    limit: int
    """Number of results per page."""

    page: Optional[str]
    """Opaque cursor from a previous response's `next_page`."""
