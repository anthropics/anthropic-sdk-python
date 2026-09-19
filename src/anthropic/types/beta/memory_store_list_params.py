from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import TypedDict

from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["MemoryStoreListParams"]


class MemoryStoreListParams(TypedDict, total=False):
    created_at_gte: Union[str, datetime]
    """Return only stores whose `created_at` is at or after this time (inclusive).

    Sent on the wire as `created_at[gte]`.
    """

    created_at_lte: Union[str, datetime]
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

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
