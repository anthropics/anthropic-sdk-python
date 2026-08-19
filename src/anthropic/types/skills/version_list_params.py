# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["VersionListParams"]


class VersionListParams(TypedDict, total=False):
    limit: Optional[int]
    """Number of results to return per page.

    Ranges from `1` to `1000`. Defaults to `20`.
    """

    page: Optional[str]
    """Optionally set to the `next_page` token from the previous response."""
