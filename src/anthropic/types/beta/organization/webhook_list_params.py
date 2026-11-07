from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["WebhookListParams"]


class WebhookListParams(TypedDict, total=False):
    after_id: Optional[str]
    """ID of the object to use as a cursor for pagination.

    When provided, returns the page of results immediately after this object.
    """

    before_id: Optional[str]
    """ID of a webhook endpoint to use as a cursor.

    Returns the first `limit` endpoints that come before it in list order, not the
    `limit` endpoints just before it.
    """

    limit: int
    """Number of items to return per page, up to `100`. The default, `0`, means `20`."""

    order: Optional[Literal["asc", "desc"]]
    """Sort order by `created_at`. Defaults to `desc`, newest first."""

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `webhooks-2026-10-07` in this
    header.
    """
