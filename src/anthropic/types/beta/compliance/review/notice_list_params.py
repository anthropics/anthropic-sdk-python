from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import TypedDict

from ....anthropic_beta_param import AnthropicBetaParam
from ..beta_compliance_review_order import BetaComplianceReviewOrder

__all__ = ["NoticeListParams"]


class NoticeListParams(TypedDict, total=False):
    case_id: str
    """Return only notices whose `case_ids` include this case (`rvc_...`).

    A case that the API key can't read returns an empty list.
    """

    created_at_gt: Union[str, datetime]
    """Return only notices whose `created_at` is after this time."""

    created_at_gte: Union[str, datetime]
    """Return notices whose `created_at` is at or after this time.

    Notices slightly older than this time are also returned, so that a poll misses
    no notice.
    """

    created_at_lt: Union[str, datetime]
    """Return only notices whose `created_at` is before this time."""

    created_at_lte: Union[str, datetime]
    """Return only notices whose `created_at` is at or before this time."""

    limit: int
    """Number of notices to return per page, between 1 and 100. Defaults to 20."""

    order: BetaComplianceReviewOrder
    """Sort direction, by `created_at` and then by `id`. Defaults to `desc`."""

    page: str
    """Opaque cursor from a previous response's `next_page`.

    Leave it out to get the first page. A cursor works only with the filters and
    sort order of the request that returned it.
    """

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""
