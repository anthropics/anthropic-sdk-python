# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["SkillListParams"]


class SkillListParams(TypedDict, total=False):
    limit: int
    """Number of results to return per page.

    Ranges from `1` to `1000`. Defaults to `20`.
    """

    page: Optional[str]
    """Pagination token for fetching a specific page of results.

    Pass the value from a previous response's `next_page` field to get the next page
    of results.
    """

    source: Optional[str]
    """Filter skills by source.

    If provided, only skills from the specified source will be returned:

    - `"custom"`: only return user-created skills
    - `"anthropic"`: only return Anthropic-created skills
    """
