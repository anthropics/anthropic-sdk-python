from __future__ import annotations

from typing import List, Union, Optional
from datetime import datetime
from itertools import chain

import httpx2

from ....._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ....._utils import is_given, strip_not_given
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .....pagination import SyncReportPageCursor, AsyncReportPageCursor
from ....._base_client import AsyncPaginator, make_request_options
from .....types.beta.organization import BetaAnalyticsTimeBucketWidth, BetaAnalyticsUsageCostSortOrder
from .....types.anthropic_beta_param import AnthropicBetaParam
from .....types.beta.organization.analytics import BetaAnalyticsUsageOrderBy
from .....types.beta.organization.beta_analytics_speed import BetaAnalyticsSpeed
from .....types.beta.organization.beta_analytics_actor_type import BetaAnalyticsActorType
from .....types.beta.organization.beta_analytics_service_tier import BetaAnalyticsServiceTier
from .....types.beta.organization.beta_analytics_context_window import BetaAnalyticsContextWindow
from .....types.beta.organization.beta_analytics_time_bucket_width import BetaAnalyticsTimeBucketWidth
from .....types.beta.organization.beta_analytics_claude_tag_category import BetaAnalyticsClaudeTagCategory
from .....types.beta.organization.analytics.beta_analytics_usage_item import BetaAnalyticsUsageItem
from .....types.beta.organization.beta_analytics_inference_geo_filter import BetaAnalyticsInferenceGeoFilter
from .....types.beta.organization.beta_analytics_usage_cost_sort_order import BetaAnalyticsUsageCostSortOrder
from .....types.beta.organization.analytics.beta_analytics_usage_group_by import BetaAnalyticsUsageGroupBy
from .....types.beta.organization.analytics.beta_analytics_usage_order_by import BetaAnalyticsUsageOrderBy
from .....types.beta.organization.beta_analytics_usage_cost_product_filter import BetaAnalyticsUsageCostProductFilter

__all__ = ["Usage", "AsyncUsage"]


class Usage(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UsageWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return UsageWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UsageWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return UsageWithStreamingResponse(self)

    def list(
        self,
        *,
        starting_at: Union[str, datetime],
        actor_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        actor_types: Optional[List[BetaAnalyticsActorType]] | Omit = omit,
        agent_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        api_key_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        claude_tag_categories: Optional[List[BetaAnalyticsClaudeTagCategory]] | Omit = omit,
        claude_tag_user_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        context_windows: Optional[List[BetaAnalyticsContextWindow]] | Omit = omit,
        deployment_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        ending_at: Union[str, datetime, None] | Omit = omit,
        environment_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        exclude_deleted_users: bool | Omit = omit,
        group_by: Optional[List[BetaAnalyticsUsageGroupBy]] | Omit = omit,
        inference_geos: Optional[List[BetaAnalyticsInferenceGeoFilter]] | Omit = omit,
        limit: int | Omit = omit,
        models: Optional[SequenceNotStr[str]] | Omit = omit,
        order: BetaAnalyticsUsageCostSortOrder | Omit = omit,
        order_by: BetaAnalyticsUsageOrderBy | Omit = omit,
        page: Optional[str] | Omit = omit,
        products: Optional[List[BetaAnalyticsUsageCostProductFilter]] | Omit = omit,
        rbac_group_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        service_tiers: Optional[List[BetaAnalyticsServiceTier]] | Omit = omit,
        session_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        slack_channel_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        speeds: Optional[List[BetaAnalyticsSpeed]] | Omit = omit,
        time_bucket_width: Optional[BetaAnalyticsTimeBucketWidth] | Omit = omit,
        user_profile_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        workspace_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncReportPageCursor[BetaAnalyticsUsageItem]:
        """
        Get token usage across a date range, broken out by dimension.

        Returns one row per combination of the requested `group_by[]` dimensions (and
        time bucket, when `time_bucket_width` is set) that has usage in the range,
        ranked by the `order_by` metric or ordered by time bucket; every combination is
        returned across pages. With no `group_by[]` and no `time_bucket_width`, a single
        row aggregates the whole range. Includes all usage, whether or not it is
        attributable to a seat user. Requires an API key with the `read:analytics`
        scope, or an Admin API key.

        Args:
          starting_at: Start of range, inclusive. RFC 3339 tz-aware. Must be within the last 365 days
              and no earlier than 2026-01-01T00:00:00Z.

          actor_ids: Filter to usage attributed to specific identities, by tagged ID: a `user_...`,
              `svac_...` (service account), or `apikey_...` ID. An `apikey_` entry matches
              only usage attributed to the key itself, not usage on that key attributed to a
              user or service account (use `api_key_ids[]` for every request a key
              authenticated). Federated identities have no tagged ID; select them with
              `actor_types[]`. Use `group_by[]=actor` to break out per-identity values.

          actor_types: Filter to usage attributed to specific kinds of identity. Use
              `group_by[]=actor_type` to break out per-kind values.

          agent_ids: Filter to usage incurred by sessions of specific Claude Managed Agents agents.
              Use `group_by[]=agent_id` to break out per-agent values. Claude Developer
              Platform organizations only.

          api_key_ids: Filter to usage authenticated by specific API keys, by tagged API key ID
              (`apikey_...`), whichever identity the usage is attributed to. Include an empty
              entry (`api_key_ids[]=`) to also match usage that no API key authenticated. Use
              `group_by[]=api_key_id` to break out per-key values; usage without a key has a
              null `api_key_id`. Claude Developer Platform organizations only.

          claude_tag_categories: Filter to Claude Tag (Claude in Slack) usage in specific spend categories. Usage
              with no category never matches. `dm` usage is reported under the user's product
              rather than `claude_tag`, so combining this filter with `products[]=claude_tag`
              excludes it. Use `group_by[]=claude_tag_category` to break out per-category
              values.

          claude_tag_user_ids: Filter to Claude Tag (Claude in Slack) usage attributed to specific Slack users,
              by Slack user ID (for example `U0123ABCDEF`), not claude.ai user ID. Usage that
              is not Claude Tag, and Claude Tag usage not attributed to a single user, never
              matches. Use `group_by[]=claude_tag_user_id` to break out per-user values.

          context_windows: Filter to specific context-window pricing tiers. Use `group_by[]=context_window`
              to break out per-tier values.

          deployment_ids: Filter to usage incurred by Claude Managed Agents sessions that specific
              deployments started. Use `group_by[]=deployment_id` to break out per-deployment
              values. Claude Developer Platform organizations only.

          ending_at: End of range, exclusive. Required when `time_bucket_width` is set. Without
              `time_bucket_width`, defaults to the earlier of now and `starting_at` + 31 days.
              The range may span at most 31 days.

          environment_ids: Filter to usage incurred by Claude Managed Agents sessions that ran in specific
              environments. Use `group_by[]=environment_id` to break out per-environment
              values. Claude Developer Platform organizations only.

          exclude_deleted_users: If true, omit rows whose `actor` is a `user_actor` with `deleted: true`.
              Requires `group_by[]=actor`. Rows for other actor types, and rows whose `actor`
              is null, are always kept. A page may contain fewer than `limit` rows; use
              `has_more` and `next_page` to paginate as usual.

          group_by: Dimensions to break usage out by (at most 5): one row per combination of their
              values with usage in the range (and per time bucket, when `time_bucket_width` is
              set), every combination returned across pages rather than a capped top set. When
              omitted, a single row aggregates the whole range.

          inference_geos: Filter to specific inference regions. `not_available` matches rows where the
              region is unset. Use `group_by[]=inference_geo` to break out per-region values.

          limit: Number of rows per page (1-1000, default 20). `cost_type`/`token_type` fan-out
              rows (cost endpoint only) do not count toward this limit, so `data` can exceed
              it.

          models: Models to include. Defaults to all models. Use `group_by[]=model` to break out
              per-model values.

          order: Sort direction of the `order_by` metric, or of the time buckets when `order_by`
              is `time` and `time_bucket_width` is set. Defaults to `desc`.

          order_by: Row order. A metric ranks rows by that metric in the `order` direction. `time`
              orders rows by time bucket in the `order` direction (newest first by default)
              and, within a bucket, by `total_tokens`, highest first. `time` takes effect only
              with `time_bucket_width`; without it, `time` is the same as `total_tokens`.
              Defaults to `total_tokens`.

          page: Opaque cursor from a previous response's `next_page` field.

          products: Product surfaces to include. Defaults to all products.

          rbac_group_ids: Filter to usage attributed to specific RBAC groups. Accepts tagged RBAC group
              IDs (`rbac_group_...`) or bare group UUIDs. A row matches when the user belonged
              to any of the listed groups on the (UTC) day the usage occurred; usage with no
              group attribution never matches.

          service_tiers: Filter to specific service tiers. Use `group_by[]=service_tier` to break out
              per-tier values. Claude Developer Platform organizations only; matches nothing
              for a Claude Enterprise organization.

          session_ids: Filter to usage incurred by specific Claude Managed Agents sessions, by tagged
              session ID (`sesn_...`). Use `group_by[]=session_id` to break out per-session
              values. Claude Developer Platform organizations only.

          slack_channel_ids: Filter to usage originating from specific Slack channels. Use
              `group_by[]=slack_channel_id` to break out per-channel values.

          speeds: Filter to fast or standard inference mode. Use `group_by[]=speed` to break out
              per-mode values.

          time_bucket_width: Time-bucket granularity. When set, rows are returned per time bucket (one per
              bucket and dimension combination with usage) and each row's `starting_at` and
              `ending_at` are that bucket's bounds; the time bucket counts toward `limit`.
              `ending_at` is required when `time_bucket_width` is set, and with
              `time_bucket_width="1m"` the range may span at most 24 hours. When omitted, each
              row aggregates the requested range with `starting_at` and `ending_at` each
              rounded down to the hour.

          user_profile_ids: Filter to usage attributed to specific user profiles, by tagged user profile ID
              (`uprof_...`). Use `group_by[]=user_profile_id` to break out per-profile values.
              Claude Developer Platform organizations only.

          workspace_ids: Filter to usage in specific workspaces, by tagged workspace ID (`wrkspc_...`).
              Use `group_by[]=workspace_id` to break out per-workspace values. Claude
              Developer Platform organizations only; matches nothing for a Claude Enterprise
              organization.

          betas: This endpoint is in beta: requests must send `analytics-usage-cost-2026-08-24`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["analytics-usage-cost-2026-08-24"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "analytics-usage-cost-2026-08-24", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/organizations/analytics/usage",
            page=SyncReportPageCursor[BetaAnalyticsUsageItem],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "starting_at": starting_at,
                    "actor_ids": actor_ids,
                    "actor_types": actor_types,
                    "agent_ids": agent_ids,
                    "api_key_ids": api_key_ids,
                    "claude_tag_categories": claude_tag_categories,
                    "claude_tag_user_ids": claude_tag_user_ids,
                    "context_windows": context_windows,
                    "deployment_ids": deployment_ids,
                    "ending_at": ending_at,
                    "environment_ids": environment_ids,
                    "exclude_deleted_users": exclude_deleted_users,
                    "group_by": group_by,
                    "inference_geos": inference_geos,
                    "limit": limit,
                    "models": models,
                    "order": order,
                    "order_by": order_by,
                    "page": page,
                    "products": products,
                    "rbac_group_ids": rbac_group_ids,
                    "service_tiers": service_tiers,
                    "session_ids": session_ids,
                    "slack_channel_ids": slack_channel_ids,
                    "speeds": speeds,
                    "time_bucket_width": time_bucket_width,
                    "user_profile_ids": user_profile_ids,
                    "workspace_ids": workspace_ids,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.analytics.usage.list",
                span_route="/v1/organizations/analytics/usage",
            ),
            model=BetaAnalyticsUsageItem,
        )


class AsyncUsage(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUsageWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncUsageWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUsageWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncUsageWithStreamingResponse(self)

    def list(
        self,
        *,
        starting_at: Union[str, datetime],
        actor_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        actor_types: Optional[List[BetaAnalyticsActorType]] | Omit = omit,
        agent_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        api_key_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        claude_tag_categories: Optional[List[BetaAnalyticsClaudeTagCategory]] | Omit = omit,
        claude_tag_user_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        context_windows: Optional[List[BetaAnalyticsContextWindow]] | Omit = omit,
        deployment_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        ending_at: Union[str, datetime, None] | Omit = omit,
        environment_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        exclude_deleted_users: bool | Omit = omit,
        group_by: Optional[List[BetaAnalyticsUsageGroupBy]] | Omit = omit,
        inference_geos: Optional[List[BetaAnalyticsInferenceGeoFilter]] | Omit = omit,
        limit: int | Omit = omit,
        models: Optional[SequenceNotStr[str]] | Omit = omit,
        order: BetaAnalyticsUsageCostSortOrder | Omit = omit,
        order_by: BetaAnalyticsUsageOrderBy | Omit = omit,
        page: Optional[str] | Omit = omit,
        products: Optional[List[BetaAnalyticsUsageCostProductFilter]] | Omit = omit,
        rbac_group_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        service_tiers: Optional[List[BetaAnalyticsServiceTier]] | Omit = omit,
        session_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        slack_channel_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        speeds: Optional[List[BetaAnalyticsSpeed]] | Omit = omit,
        time_bucket_width: Optional[BetaAnalyticsTimeBucketWidth] | Omit = omit,
        user_profile_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        workspace_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaAnalyticsUsageItem, AsyncReportPageCursor[BetaAnalyticsUsageItem]]:
        """
        Get token usage across a date range, broken out by dimension.

        Returns one row per combination of the requested `group_by[]` dimensions (and
        time bucket, when `time_bucket_width` is set) that has usage in the range,
        ranked by the `order_by` metric or ordered by time bucket; every combination is
        returned across pages. With no `group_by[]` and no `time_bucket_width`, a single
        row aggregates the whole range. Includes all usage, whether or not it is
        attributable to a seat user. Requires an API key with the `read:analytics`
        scope, or an Admin API key.

        Args:
          starting_at: Start of range, inclusive. RFC 3339 tz-aware. Must be within the last 365 days
              and no earlier than 2026-01-01T00:00:00Z.

          actor_ids: Filter to usage attributed to specific identities, by tagged ID: a `user_...`,
              `svac_...` (service account), or `apikey_...` ID. An `apikey_` entry matches
              only usage attributed to the key itself, not usage on that key attributed to a
              user or service account (use `api_key_ids[]` for every request a key
              authenticated). Federated identities have no tagged ID; select them with
              `actor_types[]`. Use `group_by[]=actor` to break out per-identity values.

          actor_types: Filter to usage attributed to specific kinds of identity. Use
              `group_by[]=actor_type` to break out per-kind values.

          agent_ids: Filter to usage incurred by sessions of specific Claude Managed Agents agents.
              Use `group_by[]=agent_id` to break out per-agent values. Claude Developer
              Platform organizations only.

          api_key_ids: Filter to usage authenticated by specific API keys, by tagged API key ID
              (`apikey_...`), whichever identity the usage is attributed to. Include an empty
              entry (`api_key_ids[]=`) to also match usage that no API key authenticated. Use
              `group_by[]=api_key_id` to break out per-key values; usage without a key has a
              null `api_key_id`. Claude Developer Platform organizations only.

          claude_tag_categories: Filter to Claude Tag (Claude in Slack) usage in specific spend categories. Usage
              with no category never matches. `dm` usage is reported under the user's product
              rather than `claude_tag`, so combining this filter with `products[]=claude_tag`
              excludes it. Use `group_by[]=claude_tag_category` to break out per-category
              values.

          claude_tag_user_ids: Filter to Claude Tag (Claude in Slack) usage attributed to specific Slack users,
              by Slack user ID (for example `U0123ABCDEF`), not claude.ai user ID. Usage that
              is not Claude Tag, and Claude Tag usage not attributed to a single user, never
              matches. Use `group_by[]=claude_tag_user_id` to break out per-user values.

          context_windows: Filter to specific context-window pricing tiers. Use `group_by[]=context_window`
              to break out per-tier values.

          deployment_ids: Filter to usage incurred by Claude Managed Agents sessions that specific
              deployments started. Use `group_by[]=deployment_id` to break out per-deployment
              values. Claude Developer Platform organizations only.

          ending_at: End of range, exclusive. Required when `time_bucket_width` is set. Without
              `time_bucket_width`, defaults to the earlier of now and `starting_at` + 31 days.
              The range may span at most 31 days.

          environment_ids: Filter to usage incurred by Claude Managed Agents sessions that ran in specific
              environments. Use `group_by[]=environment_id` to break out per-environment
              values. Claude Developer Platform organizations only.

          exclude_deleted_users: If true, omit rows whose `actor` is a `user_actor` with `deleted: true`.
              Requires `group_by[]=actor`. Rows for other actor types, and rows whose `actor`
              is null, are always kept. A page may contain fewer than `limit` rows; use
              `has_more` and `next_page` to paginate as usual.

          group_by: Dimensions to break usage out by (at most 5): one row per combination of their
              values with usage in the range (and per time bucket, when `time_bucket_width` is
              set), every combination returned across pages rather than a capped top set. When
              omitted, a single row aggregates the whole range.

          inference_geos: Filter to specific inference regions. `not_available` matches rows where the
              region is unset. Use `group_by[]=inference_geo` to break out per-region values.

          limit: Number of rows per page (1-1000, default 20). `cost_type`/`token_type` fan-out
              rows (cost endpoint only) do not count toward this limit, so `data` can exceed
              it.

          models: Models to include. Defaults to all models. Use `group_by[]=model` to break out
              per-model values.

          order: Sort direction of the `order_by` metric, or of the time buckets when `order_by`
              is `time` and `time_bucket_width` is set. Defaults to `desc`.

          order_by: Row order. A metric ranks rows by that metric in the `order` direction. `time`
              orders rows by time bucket in the `order` direction (newest first by default)
              and, within a bucket, by `total_tokens`, highest first. `time` takes effect only
              with `time_bucket_width`; without it, `time` is the same as `total_tokens`.
              Defaults to `total_tokens`.

          page: Opaque cursor from a previous response's `next_page` field.

          products: Product surfaces to include. Defaults to all products.

          rbac_group_ids: Filter to usage attributed to specific RBAC groups. Accepts tagged RBAC group
              IDs (`rbac_group_...`) or bare group UUIDs. A row matches when the user belonged
              to any of the listed groups on the (UTC) day the usage occurred; usage with no
              group attribution never matches.

          service_tiers: Filter to specific service tiers. Use `group_by[]=service_tier` to break out
              per-tier values. Claude Developer Platform organizations only; matches nothing
              for a Claude Enterprise organization.

          session_ids: Filter to usage incurred by specific Claude Managed Agents sessions, by tagged
              session ID (`sesn_...`). Use `group_by[]=session_id` to break out per-session
              values. Claude Developer Platform organizations only.

          slack_channel_ids: Filter to usage originating from specific Slack channels. Use
              `group_by[]=slack_channel_id` to break out per-channel values.

          speeds: Filter to fast or standard inference mode. Use `group_by[]=speed` to break out
              per-mode values.

          time_bucket_width: Time-bucket granularity. When set, rows are returned per time bucket (one per
              bucket and dimension combination with usage) and each row's `starting_at` and
              `ending_at` are that bucket's bounds; the time bucket counts toward `limit`.
              `ending_at` is required when `time_bucket_width` is set, and with
              `time_bucket_width="1m"` the range may span at most 24 hours. When omitted, each
              row aggregates the requested range with `starting_at` and `ending_at` each
              rounded down to the hour.

          user_profile_ids: Filter to usage attributed to specific user profiles, by tagged user profile ID
              (`uprof_...`). Use `group_by[]=user_profile_id` to break out per-profile values.
              Claude Developer Platform organizations only.

          workspace_ids: Filter to usage in specific workspaces, by tagged workspace ID (`wrkspc_...`).
              Use `group_by[]=workspace_id` to break out per-workspace values. Claude
              Developer Platform organizations only; matches nothing for a Claude Enterprise
              organization.

          betas: This endpoint is in beta: requests must send `analytics-usage-cost-2026-08-24`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["analytics-usage-cost-2026-08-24"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "analytics-usage-cost-2026-08-24", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/organizations/analytics/usage",
            page=AsyncReportPageCursor[BetaAnalyticsUsageItem],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "starting_at": starting_at,
                    "actor_ids": actor_ids,
                    "actor_types": actor_types,
                    "agent_ids": agent_ids,
                    "api_key_ids": api_key_ids,
                    "claude_tag_categories": claude_tag_categories,
                    "claude_tag_user_ids": claude_tag_user_ids,
                    "context_windows": context_windows,
                    "deployment_ids": deployment_ids,
                    "ending_at": ending_at,
                    "environment_ids": environment_ids,
                    "exclude_deleted_users": exclude_deleted_users,
                    "group_by": group_by,
                    "inference_geos": inference_geos,
                    "limit": limit,
                    "models": models,
                    "order": order,
                    "order_by": order_by,
                    "page": page,
                    "products": products,
                    "rbac_group_ids": rbac_group_ids,
                    "service_tiers": service_tiers,
                    "session_ids": session_ids,
                    "slack_channel_ids": slack_channel_ids,
                    "speeds": speeds,
                    "time_bucket_width": time_bucket_width,
                    "user_profile_ids": user_profile_ids,
                    "workspace_ids": workspace_ids,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.analytics.usage.list",
                span_route="/v1/organizations/analytics/usage",
            ),
            model=BetaAnalyticsUsageItem,
        )


class UsageWithRawResponse:
    def __init__(self, usage: Usage) -> None:
        self._usage = usage

        self.list = to_raw_response_wrapper(
            usage.list,
        )


class AsyncUsageWithRawResponse:
    def __init__(self, usage: AsyncUsage) -> None:
        self._usage = usage

        self.list = async_to_raw_response_wrapper(
            usage.list,
        )


class UsageWithStreamingResponse:
    def __init__(self, usage: Usage) -> None:
        self._usage = usage

        self.list = to_streamed_response_wrapper(
            usage.list,
        )


class AsyncUsageWithStreamingResponse:
    def __init__(self, usage: AsyncUsage) -> None:
        self._usage = usage

        self.list = async_to_streamed_response_wrapper(
            usage.list,
        )
