from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["ExternalKeyListParams"]


class ExternalKeyListParams(TypedDict, total=False):
    limit: int
    """Number of results per page."""

    page: Optional[str]
    """Opaque cursor from a previous response's `next_page`."""
