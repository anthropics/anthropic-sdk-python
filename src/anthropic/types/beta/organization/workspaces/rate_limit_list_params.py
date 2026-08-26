# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypedDict

__all__ = ["RateLimitListParams"]


class RateLimitListParams(TypedDict, total=False):
    group_type: Optional[Literal["batch", "files", "model_group", "skills", "token_count", "web_search"]]
    """Filter by group type."""

    limit: Optional[int]
    """Maximum number of items to return per page. Ranges from `1` to `1000`.

    Accepted for request-shape compatibility and currently ignored: every entry is
    returned in a single page.
    """

    page: Optional[str]
    """Opaque cursor from a previous response's `next_page`."""
