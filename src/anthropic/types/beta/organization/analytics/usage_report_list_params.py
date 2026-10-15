from __future__ import annotations

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Required, TypedDict

from ....._types import SequenceNotStr
from ..beta_analytics_context_window import BetaAnalyticsContextWindow
from ..beta_analytics_product_filter import BetaAnalyticsProductFilter
from ..beta_analytics_claude_tag_category import BetaAnalyticsClaudeTagCategory
from ..beta_analytics_inference_geo_filter import BetaAnalyticsInferenceGeoFilter

__all__ = ["UsageReportListParams"]


class UsageReportListParams(TypedDict, total=False):
    starting_at: Required[Union[str, datetime]]
    """Start of range, inclusive.

    RFC 3339 tz-aware. Must be within the last 365 days and no earlier than
    2026-01-01T00:00:00Z.
    """

    bucket_width: Literal["1d", "1h", "1m"]
    """Time bucket granularity."""

    claude_tag_categories: Optional[List[BetaAnalyticsClaudeTagCategory]]
    """Filter to Claude Tag (Claude in Slack) usage in specific spend categories.

    Usage with no category never matches. `dm` usage is reported under the user's
    product rather than `claude-tag`, so combining this filter with
    `products[]=claude-tag` excludes it. Use `group_by[]=claude_tag_category` to
    break out per-category values.
    """

    claude_tag_user_ids: Optional[SequenceNotStr[str]]
    """
    Filter to Claude Tag (Claude in Slack) usage attributed to specific Slack users,
    by Slack user ID (for example `U0123ABCDEF`), not claude.ai user ID. Usage that
    is not Claude Tag, and Claude Tag usage not attributed to a single user, never
    matches. Use `group_by[]=claude_tag_user_id` to break out per-user values.
    """

    context_windows: Optional[List[BetaAnalyticsContextWindow]]
    """Filter to specific context-window pricing tiers.

    Use `group_by[]=context_window` to break out per-tier values.
    """

    ending_at: Union[str, datetime, None]
    """End of range, exclusive.

    When omitted, defaults to the earlier of now and `starting_at` + 31 days. The
    range may span at most 31 days.
    """

    group_by: Optional[
        List[
            Literal[
                "claude_tag_category",
                "claude_tag_user_id",
                "context_window",
                "inference_geo",
                "model",
                "product",
                "rbac_group_id",
                "slack_channel_id",
                "speed",
            ]
        ]
    ]
    """Dimensions to break each time bucket out by.

    Defaults to no grouping (one total per bucket). Each bucket reports at most its
    top 100 groups; a group beyond that cap has no row in that bucket (there is no
    remainder row), so grouped buckets are not exhaustive when a dimension has more
    than 100 distinct values.
    """

    inference_geos: Optional[List[BetaAnalyticsInferenceGeoFilter]]
    """Filter to specific inference regions.

    `not_available` matches rows where the region is unset. Use
    `group_by[]=inference_geo` to break out per-region values.
    """

    limit: Optional[int]
    """Maximum number of time buckets per page.

    Defaults and caps vary by `bucket_width` (`1d`: default 7, max 31; `1h`: default
    24, max 168; `1m`: default 60, max 256).
    """

    models: Optional[SequenceNotStr[str]]
    """Models to include.

    Defaults to all models. Use `group_by[]=model` to break out per-model values.
    """

    page: Optional[str]
    """Opaque cursor from a previous response's `next_page` field."""

    products: Optional[List[BetaAnalyticsProductFilter]]
    """Product surfaces to include.

    Defaults to all products. Use `group_by[]=product` to break out per-product
    values.
    """

    rbac_group_ids: Optional[SequenceNotStr[str]]
    """Filter to usage attributed to specific RBAC groups.

    Accepts tagged RBAC group IDs (`rbac_group_...`) or bare group UUIDs. A row
    matches when the user belonged to any of the listed groups on the (UTC) day the
    usage occurred; usage with no group attribution never matches.
    """

    slack_channel_ids: Optional[SequenceNotStr[str]]
    """Filter to usage originating from specific Slack channels.

    Use `group_by[]=slack_channel_id` to break out per-channel values.
    """

    speeds: Optional[List[Literal["fast", "standard"]]]
    """Filter to fast or standard inference mode.

    Use `group_by[]=speed` to break out per-mode values.
    """

    user_ids: Optional[SequenceNotStr[str]]
    """Filter to specific users by tagged user ID."""
