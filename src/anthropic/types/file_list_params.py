# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .._types import SequenceNotStr

__all__ = ["FileListParams"]


class FileListParams(TypedDict, total=False):
    ids: Optional[SequenceNotStr[str]]
    """Restrict the result set to Files whose `id` is in this list.

    At most 100 entries (after de-duplication). Mutually exclusive with `page` and
    `limit`. When supplied, the response is always a single page (`next_page` is
    null). IDs that do not resolve to a visible File — including deleted Files — are
    silently omitted.
    """

    limit: int
    """Number of items to return per page.

    Defaults to `20`. Ranges from `1` to `1000`.
    """

    page: Optional[str]
    """Opaque page cursor returned in a prior list response's `next_page`.

    Prefixed `page_`.
    """
