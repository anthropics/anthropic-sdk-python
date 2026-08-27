# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Annotated, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo
from ..anthropic_beta_param import AnthropicBetaParam

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

    scope_id: str
    """Filter by scope ID.

    Only returns files associated with the specified scope (e.g., a session ID).
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
