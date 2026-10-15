from __future__ import annotations

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Required, TypedDict

from ....._types import SequenceNotStr
from ..beta_analytics_context_window import BetaAnalyticsContextWindow
from ..beta_analytics_product_filter import BetaAnalyticsProductFilter
from ..beta_analytics_claude_tag_category import BetaAnalyticsClaudeTagCategory
from ..beta_analytics_inference_geo_filter import BetaAnalyticsInferenceGeoFilter

__all__ = ["UserCostReportListParams"]


class UserCostReportListParams(TypedDict, total=False):
    starting_at: Required[Union[str, datetime]]
    """Start of range, inclusive.

    RFC 3339 tz-aware. Must be within the last 365 days and no earlier than
    2026-01-01T00:00:00Z.
    """

    bucket_width: Optional[Literal["1d", "1h", "1m"]]
    """Time-bucket granularity.

    When set, each row's `starting_at` and `ending_at` are populated and one actor
    may span several rows (one per time bucket with usage). The time bucket counts
    toward `limit`, so one page can return multiple rows for the same actor.
    `ending_at` is required when `bucket_width` is set, and with `bucket_width="1m"`
    the range may span at most 24 hours. When omitted, each row aggregates the full
    `[starting_at, ending_at)` range.
    """

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

    exclude_deleted_users: bool
    """If true, omit rows for users who are deleted (`deleted: true`).

    A page may contain fewer than `limit` rows; use `has_more` and `next_page` to
    paginate as usual.
    """

    group_by: Optional[
        List[
            Literal[
                "claude_tag_category",
                "claude_tag_user_id",
                "context_window",
                "cost_type",
                "inference_geo",
                "model",
                "product",
                "rbac_group_id",
                "slack_channel_id",
                "speed",
                "token_type",
            ]
        ]
    ]
    """Break each actor's row out by the given dimensions.

    Accepts the same values as the bucketed `/cost_report` endpoint. The `product`,
    `model`, `context_window`, `inference_geo`, and `speed` dimensions — and the
    time bucket, when `bucket_width` is set — count toward `limit`. `cost_type` and
    `token_type` do not: `cost_type` returns one row per cost component (tokens, web
    search, code execution); `token_type` returns one row per token type, each with
    `cost_type: "tokens"`; combining both returns the per-token-type rows plus the
    web-search and code-execution rows. A page can therefore contain more rows than
    `limit` when `cost_type` or `token_type` is requested.
    """

    inference_geos: Optional[List[BetaAnalyticsInferenceGeoFilter]]
    """Filter to specific inference regions.

    `not_available` matches rows where the region is unset. Use
    `group_by[]=inference_geo` to break out per-region values.
    """

    limit: int
    """Number of rows per page (1-1000, default 20).

    One row per actor unless `group_by[]` or `bucket_width` splits an actor across
    rows; `cost_type`/`token_type` fan-out rows (cost endpoint only) are the
    exception — they do not count toward this limit, so `data` can exceed it.
    """

    models: Optional[SequenceNotStr[str]]
    """Models to include.

    Defaults to all models. Use `group_by[]=model` to break out per-model values.
    """

    order: Literal["asc", "desc"]
    """Sort direction. Defaults to `desc`."""

    order_by: Literal["amount", "list_amount"]
    """Metric to rank actors by. Defaults to `amount`."""

    page: Optional[str]
    """Opaque cursor from a previous response's `next_page` field."""

    products: Optional[List[BetaAnalyticsProductFilter]]
    """Product surfaces to include. Defaults to all products."""

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
