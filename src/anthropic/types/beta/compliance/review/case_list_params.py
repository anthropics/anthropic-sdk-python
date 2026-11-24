from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import TypedDict

from ....anthropic_beta_param import AnthropicBetaParam
from ..beta_compliance_review_order import BetaComplianceReviewOrder
from .beta_compliance_review_case_order_by import BetaComplianceReviewCaseOrderBy
from .beta_compliance_review_case_status_filter import BetaComplianceReviewCaseStatusFilter

__all__ = ["CaseListParams"]


class CaseListParams(TypedDict, total=False):
    created_at_gt: Union[str, datetime]
    """Return only cases whose `created_at` is after this time."""

    created_at_gte: Union[str, datetime]
    """Return only cases whose `created_at` is at or after this time."""

    created_at_lt: Union[str, datetime]
    """Return only cases whose `created_at` is before this time."""

    created_at_lte: Union[str, datetime]
    """Return only cases whose `created_at` is at or before this time."""

    limit: int
    """Number of cases to return per page, between 1 and 100. Defaults to 20."""

    order: BetaComplianceReviewOrder
    """Sort direction, by `order_by` and then by `id`. Defaults to `desc`."""

    order_by: BetaComplianceReviewCaseOrderBy
    """The field to sort by. Defaults to `created_at`."""

    page: str
    """Opaque cursor from a previous response's `next_page`.

    Leave it out to get the first page. A cursor works only with the filters and
    sort order of the request that returned it.
    """

    status: BetaComplianceReviewCaseStatusFilter
    """Return only cases with this status.

    Leave it out to get both open and closed cases.
    """

    updated_at_gt: Union[str, datetime]
    """Return only cases whose `updated_at` is after this time."""

    updated_at_gte: Union[str, datetime]
    """Return cases whose `updated_at` is at or after this time.

    Cases slightly older than this time are also returned, so that a sync misses no
    change.
    """

    updated_at_lt: Union[str, datetime]
    """Return only cases whose `updated_at` is before this time."""

    updated_at_lte: Union[str, datetime]
    """Return only cases whose `updated_at` is at or before this time."""

    user_profile_id: str
    """
    Return only cases where a message's `user_profile_id` is this ID, including
    cases that also have messages of other user profiles. A case stops matching once
    its messages' `user_profile_id` is null. An ID that matches no reachable case
    returns no cases. A request that sends the `anthropic-user-profile-id` header
    without this parameter returns a 400 error.
    """

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""
