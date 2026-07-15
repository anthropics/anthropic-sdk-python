# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo
from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["MemoryStoreListParams"]


class MemoryStoreListParams(TypedDict, total=False):
    created_at_gte: Annotated[Union[str, datetime], PropertyInfo(alias="created_at[gte]", format="iso8601")]
    """Return only stores whose `created_at` is at or after this time (inclusive).

    Sent on the wire as `created_at[gte]`.
    """

    created_at_lte: Annotated[Union[str, datetime], PropertyInfo(alias="created_at[lte]", format="iso8601")]
    """Return only stores whose `created_at` is at or before this time (inclusive).

    Sent on the wire as `created_at[lte]`.
    """

    include_archived: bool
    """When `true`, archived stores are included in the results.

    Defaults to `false` (archived stores are excluded).
    """

    limit: int
    """Maximum number of stores to return per page.

    Must be between 1 and 100. Defaults to 20 when omitted.
    """

    page: str
    """Opaque pagination cursor (a `page_...` value).

    Pass the `next_page` value from a previous response to fetch the next page; omit
    for the first page.
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
