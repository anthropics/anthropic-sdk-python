from __future__ import annotations

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Required, TypedDict

from ....._types import SequenceNotStr
from ..beta_analytics_speed import BetaAnalyticsSpeed
from ....anthropic_beta_param import AnthropicBetaParam
from ..beta_analytics_actor_type import BetaAnalyticsActorType
from ..beta_analytics_service_tier import BetaAnalyticsServiceTier
from .beta_analytics_usage_group_by import BetaAnalyticsUsageGroupBy
from .beta_analytics_usage_order_by import BetaAnalyticsUsageOrderBy
from ..beta_analytics_context_window import BetaAnalyticsContextWindow
from ..beta_analytics_time_bucket_width import BetaAnalyticsTimeBucketWidth
from ..beta_analytics_claude_tag_category import BetaAnalyticsClaudeTagCategory
from ..beta_analytics_inference_geo_filter import BetaAnalyticsInferenceGeoFilter
from ..beta_analytics_usage_cost_sort_order import BetaAnalyticsUsageCostSortOrder
from ..beta_analytics_usage_cost_product_filter import BetaAnalyticsUsageCostProductFilter

__all__ = ["UsageListParams"]


class UsageListParams(TypedDict, total=False):
    starting_at: Required[Union[str, datetime]]
    """Start of range, inclusive.

    RFC 3339 tz-aware. Must be within the last 365 days and no earlier than
    2026-01-01T00:00:00Z.
    """

    actor_ids: Optional[SequenceNotStr[str]]
    """
    Filter to usage attributed to specific identities, by tagged ID: a `user_...`,
    `svac_...` (service account), or `apikey_...` ID. An `apikey_` entry matches
    only usage attributed to the key itself, not usage on that key attributed to a
    user or service account (use `api_key_ids[]` for every request a key
    authenticated). Federated identities have no tagged ID; select them with
    `actor_types[]`. Use `group_by[]=actor` to break out per-identity values.
    """

    actor_types: Optional[List[BetaAnalyticsActorType]]
    """Filter to usage attributed to specific kinds of identity.

    Use `group_by[]=actor_type` to break out per-kind values.
    """

    agent_ids: Optional[SequenceNotStr[str]]
    """Filter to usage incurred by sessions of specific Claude Managed Agents agents.

    Use `group_by[]=agent_id` to break out per-agent values. Claude Developer
    Platform organizations only.
    """

    api_key_ids: Optional[SequenceNotStr[str]]
    """
    Filter to usage authenticated by specific API keys, by tagged API key ID
    (`apikey_...`), whichever identity the usage is attributed to. Include an empty
    entry (`api_key_ids[]=`) to also match usage that no API key authenticated. Use
    `group_by[]=api_key_id` to break out per-key values; usage without a key has a
    null `api_key_id`. Claude Developer Platform organizations only.
    """

    claude_tag_categories: Optional[List[BetaAnalyticsClaudeTagCategory]]
    """Filter to Claude Tag (Claude in Slack) usage in specific spend categories.

    Usage with no category never matches. `dm` usage is reported under the user's
    product rather than `claude_tag`, so combining this filter with
    `products[]=claude_tag` excludes it. Use `group_by[]=claude_tag_category` to
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

    deployment_ids: Optional[SequenceNotStr[str]]
    """
    Filter to usage incurred by Claude Managed Agents sessions that specific
    deployments started. Use `group_by[]=deployment_id` to break out per-deployment
    values. Claude Developer Platform organizations only.
    """

    ending_at: Union[str, datetime, None]
    """End of range, exclusive.

    Required when `time_bucket_width` is set. Without `time_bucket_width`, defaults
    to the earlier of now and `starting_at` + 31 days. The range may span at most 31
    days.
    """

    environment_ids: Optional[SequenceNotStr[str]]
    """
    Filter to usage incurred by Claude Managed Agents sessions that ran in specific
    environments. Use `group_by[]=environment_id` to break out per-environment
    values. Claude Developer Platform organizations only.
    """

    exclude_deleted_users: bool
    """If true, omit rows whose `actor` is a `user_actor` with `deleted: true`.

    Requires `group_by[]=actor`. Rows for other actor types, and rows whose `actor`
    is null, are always kept. A page may contain fewer than `limit` rows; use
    `has_more` and `next_page` to paginate as usual.
    """

    group_by: Optional[List[BetaAnalyticsUsageGroupBy]]
    """
    Dimensions to break usage out by (at most 5): one row per combination of their
    values with usage in the range (and per time bucket, when `time_bucket_width` is
    set), every combination returned across pages rather than a capped top set. When
    omitted, a single row aggregates the whole range.
    """

    inference_geos: Optional[List[BetaAnalyticsInferenceGeoFilter]]
    """Filter to specific inference regions.

    `not_available` matches rows where the region is unset. Use
    `group_by[]=inference_geo` to break out per-region values.
    """

    limit: int
    """Number of rows per page (1-1000, default 20).

    `cost_type`/`token_type` fan-out rows (cost endpoint only) do not count toward
    this limit, so `data` can exceed it.
    """

    models: Optional[SequenceNotStr[str]]
    """Models to include.

    Defaults to all models. Use `group_by[]=model` to break out per-model values.
    """

    order: BetaAnalyticsUsageCostSortOrder
    """
    Sort direction of the `order_by` metric, or of the time buckets when `order_by`
    is `time` and `time_bucket_width` is set. Defaults to `desc`.
    """

    order_by: BetaAnalyticsUsageOrderBy
    """Row order.

    A metric ranks rows by that metric in the `order` direction. `time` orders rows
    by time bucket in the `order` direction (newest first by default) and, within a
    bucket, by `total_tokens`, highest first. `time` takes effect only with
    `time_bucket_width`; without it, `time` is the same as `total_tokens`. Defaults
    to `total_tokens`.
    """

    page: Optional[str]
    """Opaque cursor from a previous response's `next_page` field."""

    products: Optional[List[BetaAnalyticsUsageCostProductFilter]]
    """Product surfaces to include. Defaults to all products."""

    rbac_group_ids: Optional[SequenceNotStr[str]]
    """Filter to usage attributed to specific RBAC groups.

    Accepts tagged RBAC group IDs (`rbac_group_...`) or bare group UUIDs. A row
    matches when the user belonged to any of the listed groups on the (UTC) day the
    usage occurred; usage with no group attribution never matches.
    """

    service_tiers: Optional[List[BetaAnalyticsServiceTier]]
    """Filter to specific service tiers.

    Use `group_by[]=service_tier` to break out per-tier values. Claude Developer
    Platform organizations only; matches nothing for a Claude Enterprise
    organization.
    """

    session_ids: Optional[SequenceNotStr[str]]
    """
    Filter to usage incurred by specific Claude Managed Agents sessions, by tagged
    session ID (`sesn_...`). Use `group_by[]=session_id` to break out per-session
    values. Claude Developer Platform organizations only.
    """

    slack_channel_ids: Optional[SequenceNotStr[str]]
    """Filter to usage originating from specific Slack channels.

    Use `group_by[]=slack_channel_id` to break out per-channel values.
    """

    speeds: Optional[List[BetaAnalyticsSpeed]]
    """Filter to fast or standard inference mode.

    Use `group_by[]=speed` to break out per-mode values.
    """

    time_bucket_width: Optional[BetaAnalyticsTimeBucketWidth]
    """Time-bucket granularity.

    When set, rows are returned per time bucket (one per bucket and dimension
    combination with usage) and each row's `starting_at` and `ending_at` are that
    bucket's bounds; the time bucket counts toward `limit`. `ending_at` is required
    when `time_bucket_width` is set, and with `time_bucket_width="1m"` the range may
    span at most 24 hours. When omitted, each row aggregates the requested range
    with `starting_at` and `ending_at` each rounded down to the hour.
    """

    user_profile_ids: Optional[SequenceNotStr[str]]
    """
    Filter to usage attributed to specific user profiles, by tagged user profile ID
    (`uprof_...`). Use `group_by[]=user_profile_id` to break out per-profile values.
    Claude Developer Platform organizations only.
    """

    workspace_ids: Optional[SequenceNotStr[str]]
    """Filter to usage in specific workspaces, by tagged workspace ID (`wrkspc_...`).

    Use `group_by[]=workspace_id` to break out per-workspace values. Claude
    Developer Platform organizations only; matches nothing for a Claude Enterprise
    organization.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `analytics-usage-cost-2026-08-24`
    in this header.
    """
