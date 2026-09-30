from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["RBACRoleListParams"]


class RBACRoleListParams(TypedDict, total=False):
    limit: int
    """Number of items to return per page.

    Defaults to `20`. Ranges from `1` to `1000`.
    """

    page: Optional[str]
    """Optionally set to the `next_page` token from the previous response."""
