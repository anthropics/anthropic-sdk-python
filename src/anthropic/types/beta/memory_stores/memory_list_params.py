# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from ...._utils import PropertyInfo
from ...anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_memory_view import BetaManagedAgentsMemoryView

__all__ = ["MemoryListParams"]


class MemoryListParams(TypedDict, total=False):
    depth: int
    """`0` (or omitted) returns all descendants below `path_prefix` (recursive).

    `1` returns immediate children only; deeper entries roll up as `memory_prefix`
    items. `depth=1` behaves like `ls`; omitting `depth` behaves like `find`.
    """

    limit: int
    """Maximum number of items to return per page.

    Must be between 1 and 100. Defaults to 20 when omitted. Capped at 20 when
    `view=full`. Both `memory` and `memory_prefix` items count toward the limit.
    """

    order: Literal["asc", "desc"]
    """Query parameter for order"""

    order_by: str
    """Query parameter for order_by"""

    page: str
    """Opaque pagination cursor (a `page_...` value).

    Pass the `next_page` value from a previous response to fetch the next page; omit
    for the first page.
    """

    path_prefix: str
    """Optional path prefix filter.

    Must end with `/` (segment-aligned), e.g., `/notes/`. This value appears in
    request URLs. Do not include secrets or personally identifiable information.
    """

    view: BetaManagedAgentsMemoryView
    """Which projection of each `memory` to return.

    Defaults to `basic` (content omitted). `full` populates `content` on each item
    and caps `limit` at 20; use this as the bulk-read path for export and sync.
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
