from __future__ import annotations

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal

import httpx2

from ....._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .....pagination import SyncPageCursor, AsyncPageCursor
from ....._base_client import AsyncPaginator, make_request_options
from .....types.beta.organization.beta_analytics_context_window import BetaAnalyticsContextWindow
from .....types.beta.organization.beta_analytics_product_filter import BetaAnalyticsProductFilter
from .....types.beta.organization.beta_analytics_claude_tag_category import BetaAnalyticsClaudeTagCategory
from .....types.beta.organization.beta_analytics_inference_geo_filter import BetaAnalyticsInferenceGeoFilter
from .....types.beta.organization.beta_analytics_cost_report_time_bucket import BetaAnalyticsCostReportTimeBucket

__all__ = ["CostReport", "AsyncCostReport"]


class CostReport(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CostReportWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return CostReportWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CostReportWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return CostReportWithStreamingResponse(self)

    def list(
        self,
        *,
        starting_at: Union[str, datetime],
        bucket_width: Literal["1d", "1h", "1m"] | Omit = omit,
        claude_tag_categories: Optional[List[BetaAnalyticsClaudeTagCategory]] | Omit = omit,
        claude_tag_user_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        context_windows: Optional[List[BetaAnalyticsContextWindow]] | Omit = omit,
        ending_at: Union[str, datetime, None] | Omit = omit,
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
        | Omit = omit,
        inference_geos: Optional[List[BetaAnalyticsInferenceGeoFilter]] | Omit = omit,
        limit: Optional[int] | Omit = omit,
        models: Optional[SequenceNotStr[str]] | Omit = omit,
        page: Optional[str] | Omit = omit,
        products: Optional[List[BetaAnalyticsProductFilter]] | Omit = omit,
        rbac_group_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        slack_channel_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        speeds: Optional[List[Literal["fast", "standard"]]] | Omit = omit,
        user_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaAnalyticsCostReportTimeBucket]:
        """
        Get cost in USD over time across a date range.

        Returns cost bucketed by minute, hour, or day, optionally broken down by
        product, model, context window, inference region, speed, cost type, or token
        type. Available to organizations on a Claude Enterprise plan. Requires an API
        key with the `read:analytics` scope.

        Args:
          starting_at: Start of range, inclusive. RFC 3339 tz-aware. Must be within the last 365 days
              and no earlier than 2026-01-01T00:00:00Z.

          bucket_width: Time bucket granularity.

          claude_tag_categories: Filter to Claude Tag (Claude in Slack) usage in specific spend categories. Usage
              with no category never matches. `dm` usage is reported under the user's product
              rather than `claude-tag`, so combining this filter with `products[]=claude-tag`
              excludes it. Use `group_by[]=claude_tag_category` to break out per-category
              values.

          claude_tag_user_ids: Filter to Claude Tag (Claude in Slack) usage attributed to specific Slack users,
              by Slack user ID (for example `U0123ABCDEF`), not claude.ai user ID. Usage that
              is not Claude Tag, and Claude Tag usage not attributed to a single user, never
              matches. Use `group_by[]=claude_tag_user_id` to break out per-user values.

          context_windows: Filter to specific context-window pricing tiers. Use `group_by[]=context_window`
              to break out per-tier values.

          ending_at: End of range, exclusive. When omitted, defaults to the earlier of now and
              `starting_at` + 31 days. The range may span at most 31 days.

          group_by: Dimensions to break each time bucket out by. Defaults to no grouping (one total
              per bucket). Each bucket reports at most its top 100 groups; a group beyond that
              cap has no row in that bucket (there is no remainder row), so grouped buckets
              are not exhaustive when a dimension has more than 100 distinct values.

          inference_geos: Filter to specific inference regions. `not_available` matches rows where the
              region is unset. Use `group_by[]=inference_geo` to break out per-region values.

          limit: Maximum number of time buckets per page. Defaults and caps vary by
              `bucket_width` (`1d`: default 7, max 31; `1h`: default 24, max 168; `1m`:
              default 60, max 256).

          models: Models to include. Defaults to all models. Use `group_by[]=model` to break out
              per-model values.

          page: Opaque cursor from a previous response's `next_page` field.

          products: Product surfaces to include. Defaults to all products. Use `group_by[]=product`
              to break out per-product values.

          rbac_group_ids: Filter to usage attributed to specific RBAC groups. Accepts tagged RBAC group
              IDs (`rbac_group_...`) or bare group UUIDs. A row matches when the user belonged
              to any of the listed groups on the (UTC) day the usage occurred; usage with no
              group attribution never matches.

          slack_channel_ids: Filter to usage originating from specific Slack channels. Use
              `group_by[]=slack_channel_id` to break out per-channel values.

          speeds: Filter to fast or standard inference mode. Use `group_by[]=speed` to break out
              per-mode values.

          user_ids: Filter to specific users by tagged user ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/analytics/cost_report?beta=true",
            page=SyncPageCursor[BetaAnalyticsCostReportTimeBucket],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "starting_at": starting_at,
                    "bucket_width": bucket_width,
                    "claude_tag_categories": claude_tag_categories,
                    "claude_tag_user_ids": claude_tag_user_ids,
                    "context_windows": context_windows,
                    "ending_at": ending_at,
                    "group_by": group_by,
                    "inference_geos": inference_geos,
                    "limit": limit,
                    "models": models,
                    "page": page,
                    "products": products,
                    "rbac_group_ids": rbac_group_ids,
                    "slack_channel_ids": slack_channel_ids,
                    "speeds": speeds,
                    "user_ids": user_ids,
                },
            ),
            model=BetaAnalyticsCostReportTimeBucket,
        )


class AsyncCostReport(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCostReportWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCostReportWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCostReportWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncCostReportWithStreamingResponse(self)

    def list(
        self,
        *,
        starting_at: Union[str, datetime],
        bucket_width: Literal["1d", "1h", "1m"] | Omit = omit,
        claude_tag_categories: Optional[List[BetaAnalyticsClaudeTagCategory]] | Omit = omit,
        claude_tag_user_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        context_windows: Optional[List[BetaAnalyticsContextWindow]] | Omit = omit,
        ending_at: Union[str, datetime, None] | Omit = omit,
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
        | Omit = omit,
        inference_geos: Optional[List[BetaAnalyticsInferenceGeoFilter]] | Omit = omit,
        limit: Optional[int] | Omit = omit,
        models: Optional[SequenceNotStr[str]] | Omit = omit,
        page: Optional[str] | Omit = omit,
        products: Optional[List[BetaAnalyticsProductFilter]] | Omit = omit,
        rbac_group_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        slack_channel_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        speeds: Optional[List[Literal["fast", "standard"]]] | Omit = omit,
        user_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaAnalyticsCostReportTimeBucket, AsyncPageCursor[BetaAnalyticsCostReportTimeBucket]]:
        """
        Get cost in USD over time across a date range.

        Returns cost bucketed by minute, hour, or day, optionally broken down by
        product, model, context window, inference region, speed, cost type, or token
        type. Available to organizations on a Claude Enterprise plan. Requires an API
        key with the `read:analytics` scope.

        Args:
          starting_at: Start of range, inclusive. RFC 3339 tz-aware. Must be within the last 365 days
              and no earlier than 2026-01-01T00:00:00Z.

          bucket_width: Time bucket granularity.

          claude_tag_categories: Filter to Claude Tag (Claude in Slack) usage in specific spend categories. Usage
              with no category never matches. `dm` usage is reported under the user's product
              rather than `claude-tag`, so combining this filter with `products[]=claude-tag`
              excludes it. Use `group_by[]=claude_tag_category` to break out per-category
              values.

          claude_tag_user_ids: Filter to Claude Tag (Claude in Slack) usage attributed to specific Slack users,
              by Slack user ID (for example `U0123ABCDEF`), not claude.ai user ID. Usage that
              is not Claude Tag, and Claude Tag usage not attributed to a single user, never
              matches. Use `group_by[]=claude_tag_user_id` to break out per-user values.

          context_windows: Filter to specific context-window pricing tiers. Use `group_by[]=context_window`
              to break out per-tier values.

          ending_at: End of range, exclusive. When omitted, defaults to the earlier of now and
              `starting_at` + 31 days. The range may span at most 31 days.

          group_by: Dimensions to break each time bucket out by. Defaults to no grouping (one total
              per bucket). Each bucket reports at most its top 100 groups; a group beyond that
              cap has no row in that bucket (there is no remainder row), so grouped buckets
              are not exhaustive when a dimension has more than 100 distinct values.

          inference_geos: Filter to specific inference regions. `not_available` matches rows where the
              region is unset. Use `group_by[]=inference_geo` to break out per-region values.

          limit: Maximum number of time buckets per page. Defaults and caps vary by
              `bucket_width` (`1d`: default 7, max 31; `1h`: default 24, max 168; `1m`:
              default 60, max 256).

          models: Models to include. Defaults to all models. Use `group_by[]=model` to break out
              per-model values.

          page: Opaque cursor from a previous response's `next_page` field.

          products: Product surfaces to include. Defaults to all products. Use `group_by[]=product`
              to break out per-product values.

          rbac_group_ids: Filter to usage attributed to specific RBAC groups. Accepts tagged RBAC group
              IDs (`rbac_group_...`) or bare group UUIDs. A row matches when the user belonged
              to any of the listed groups on the (UTC) day the usage occurred; usage with no
              group attribution never matches.

          slack_channel_ids: Filter to usage originating from specific Slack channels. Use
              `group_by[]=slack_channel_id` to break out per-channel values.

          speeds: Filter to fast or standard inference mode. Use `group_by[]=speed` to break out
              per-mode values.

          user_ids: Filter to specific users by tagged user ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/analytics/cost_report?beta=true",
            page=AsyncPageCursor[BetaAnalyticsCostReportTimeBucket],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "starting_at": starting_at,
                    "bucket_width": bucket_width,
                    "claude_tag_categories": claude_tag_categories,
                    "claude_tag_user_ids": claude_tag_user_ids,
                    "context_windows": context_windows,
                    "ending_at": ending_at,
                    "group_by": group_by,
                    "inference_geos": inference_geos,
                    "limit": limit,
                    "models": models,
                    "page": page,
                    "products": products,
                    "rbac_group_ids": rbac_group_ids,
                    "slack_channel_ids": slack_channel_ids,
                    "speeds": speeds,
                    "user_ids": user_ids,
                },
            ),
            model=BetaAnalyticsCostReportTimeBucket,
        )


class CostReportWithRawResponse:
    def __init__(self, cost_report: CostReport) -> None:
        self._cost_report = cost_report

        self.list = to_raw_response_wrapper(
            cost_report.list,
        )


class AsyncCostReportWithRawResponse:
    def __init__(self, cost_report: AsyncCostReport) -> None:
        self._cost_report = cost_report

        self.list = async_to_raw_response_wrapper(
            cost_report.list,
        )


class CostReportWithStreamingResponse:
    def __init__(self, cost_report: CostReport) -> None:
        self._cost_report = cost_report

        self.list = to_streamed_response_wrapper(
            cost_report.list,
        )


class AsyncCostReportWithStreamingResponse:
    def __init__(self, cost_report: AsyncCostReport) -> None:
        self._cost_report = cost_report

        self.list = async_to_streamed_response_wrapper(
            cost_report.list,
        )
