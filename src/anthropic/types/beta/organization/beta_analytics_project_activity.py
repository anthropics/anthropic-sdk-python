from typing import Optional
from datetime import datetime

from ...._models import BaseModel
from .beta_analytics_user import BetaAnalyticsUser

__all__ = ["BetaAnalyticsProjectActivity"]


class BetaAnalyticsProjectActivity(BaseModel):
    """Per-project activity data for a given day."""

    distinct_user_count: int
    """
    Number of distinct users who used the project on the requested day, or, in
    date-range mode, over the requested window — recomputed as an exact distinct
    count over the window's per-member daily rows, never a sum of per-day values.
    """

    message_count: int
    """Number of messages sent in the project on the requested day"""

    project_id: str
    """Tagged project identifier (e.g. `claude_proj_...`)"""

    project_name: str
    """Name of the project"""

    created_at: Optional[datetime] = None
    """Project creation timestamp in RFC 3339 format.

    Null if the project was deleted before attribution was recorded.
    """

    created_by: Optional[BetaAnalyticsUser] = None
    """User who created the project.

    Null if the project was deleted before attribution was recorded, or if the
    creator's account no longer exists.
    """

    distinct_conversation_count: Optional[int] = None
    """Number of distinct conversations in the project.

    Null on aggregated rows where a distinct count cannot be computed.
    """

    product: Optional[str] = None
    """
    Product that produced this row's activity: one of `chat`, `claude_code`,
    `cowork`, or `office_agent` (the canonical Cost & Usage product naming; an
    `office_agent` row's per-surface breakdown is in its `office_metrics`). On
    `/plugins` only `cowork` and `claude_code` occur (the only surfaces with plugin
    attribution); on `/artifacts` only `chat`, `claude_code`, and `cowork` occur
    (the surfaces that create artifacts); `/apps/chat/projects` does not support the
    product dimension (a `product` entry in `group_by[]` or `filter[]` there is
    rejected). Present only when the request grouped by `product`.
    """

    rbac_group_id: Optional[str] = None
    """
    Tagged RBAC group identifier (`rbac_group_...`), matching the spend-limits API
    spelling. Present only when the request grouped by `rbac_group_id`.
    """

    rbac_group_name: Optional[str] = None
    """
    Resolved RBAC group display name, alongside `rbac_group_id` when name resolution
    is available. Null if the group has been deleted or its name could not be
    resolved; `rbac_group_id` remains the stable key.
    """

    user_id: Optional[str] = None
    """Tagged user identifier (e.g.

    `user_...`). Present only when the request grouped by `user_id`.
    """
