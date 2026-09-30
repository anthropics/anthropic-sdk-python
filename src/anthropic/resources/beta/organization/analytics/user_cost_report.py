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
from .....types.beta.organization.beta_analytics_cost_users_item import BetaAnalyticsCostUsersItem
from .....types.beta.organization.beta_analytics_claude_tag_category import BetaAnalyticsClaudeTagCategory
from .....types.beta.organization.beta_analytics_inference_geo_filter import BetaAnalyticsInferenceGeoFilter

__all__ = ["UserCostReport", "AsyncUserCostReport"]


class UserCostReport(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UserCostReportWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return UserCostReportWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UserCostReportWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return UserCostReportWithStreamingResponse(self)

    def list(
        self,
        *,
        starting_at: Union[str, datetime],
        bucket_width: Optional[Literal["1d", "1h", "1m"]] | Omit = omit,
        claude_tag_categories: Optional[List[BetaAnalyticsClaudeTagCategory]] | Omit = omit,
        claude_tag_user_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        context_windows: Optional[List[BetaAnalyticsContextWindow]] | Omit = omit,
        ending_at: Union[str, datetime, None] | Omit = omit,
        exclude_deleted_users: bool | Omit = omit,
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
        limit: int | Omit = omit,
        models: Optional[SequenceNotStr[str]] | Omit = omit,
        order: Literal["asc", "desc"] | Omit = omit,
        order_by: Literal["amount", "list_amount"] | Omit = omit,
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
    ) -> SyncPageCursor[BetaAnalyticsCostUsersItem]:
        """
        Get per-user cost in USD across a date range.

        Returns one row per user, ranked by spend. Use this to see which users account
        for the most cost. Only cost attributable to a seat user is included; for
        organization-wide totals including direct API-key and automation traffic, use
        the bucketed `/v1/organizations/analytics/cost_report` endpoint. Available to
        organizations on a Claude Enterprise plan. Requires an API key with the
        `read:analytics` scope.

        Args:
          starting_at: Start of range, inclusive. RFC 3339 tz-aware. Must be within the last 365 days
              and no earlier than 2026-01-01T00:00:00Z.

          bucket_width: Time-bucket granularity. When set, each row's `starting_at` and `ending_at` are
              populated and one actor may span several rows (one per time bucket with usage).
              The time bucket counts toward `limit`, so one page can return multiple rows for
              the same actor. `ending_at` is required when `bucket_width` is set, and with
              `bucket_width="1m"` the range may span at most 24 hours. When omitted, each row
              aggregates the full `[starting_at, ending_at)` range.

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

          exclude_deleted_users: If true, omit rows for users who are deleted (`deleted: true`). A page may
              contain fewer than `limit` rows; use `has_more` and `next_page` to paginate as
              usual.

          group_by: Break each actor's row out by the given dimensions. Accepts the same values as
              the bucketed `/cost_report` endpoint. The `product`, `model`, `context_window`,
              `inference_geo`, and `speed` dimensions — and the time bucket, when
              `bucket_width` is set — count toward `limit`. `cost_type` and `token_type` do
              not: `cost_type` returns one row per cost component (tokens, web search, code
              execution); `token_type` returns one row per token type, each with
              `cost_type: "tokens"`; combining both returns the per-token-type rows plus the
              web-search and code-execution rows. A page can therefore contain more rows than
              `limit` when `cost_type` or `token_type` is requested.

          inference_geos: Filter to specific inference regions. `not_available` matches rows where the
              region is unset. Use `group_by[]=inference_geo` to break out per-region values.

          limit: Number of rows per page (1-1000, default 20). One row per actor unless
              `group_by[]` or `bucket_width` splits an actor across rows;
              `cost_type`/`token_type` fan-out rows (cost endpoint only) are the exception —
              they do not count toward this limit, so `data` can exceed it.

          models: Models to include. Defaults to all models. Use `group_by[]=model` to break out
              per-model values.

          order: Sort direction. Defaults to `desc`.

          order_by: Metric to rank actors by. Defaults to `amount`.

          page: Opaque cursor from a previous response's `next_page` field.

          products: Product surfaces to include. Defaults to all products.

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
            "/v1/organizations/analytics/user_cost_report?beta=true",
            page=SyncPageCursor[BetaAnalyticsCostUsersItem],
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
                    "slack_channel_ids": slack_channel_ids,
                    "speeds": speeds,
                    "user_ids": user_ids,
                },
            ),
            model=BetaAnalyticsCostUsersItem,
        )


class AsyncUserCostReport(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUserCostReportWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncUserCostReportWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUserCostReportWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncUserCostReportWithStreamingResponse(self)

    def list(
        self,
        *,
        starting_at: Union[str, datetime],
        bucket_width: Optional[Literal["1d", "1h", "1m"]] | Omit = omit,
        claude_tag_categories: Optional[List[BetaAnalyticsClaudeTagCategory]] | Omit = omit,
        claude_tag_user_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        context_windows: Optional[List[BetaAnalyticsContextWindow]] | Omit = omit,
        ending_at: Union[str, datetime, None] | Omit = omit,
        exclude_deleted_users: bool | Omit = omit,
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
        limit: int | Omit = omit,
        models: Optional[SequenceNotStr[str]] | Omit = omit,
        order: Literal["asc", "desc"] | Omit = omit,
        order_by: Literal["amount", "list_amount"] | Omit = omit,
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
    ) -> AsyncPaginator[BetaAnalyticsCostUsersItem, AsyncPageCursor[BetaAnalyticsCostUsersItem]]:
        """
        Get per-user cost in USD across a date range.

        Returns one row per user, ranked by spend. Use this to see which users account
        for the most cost. Only cost attributable to a seat user is included; for
        organization-wide totals including direct API-key and automation traffic, use
        the bucketed `/v1/organizations/analytics/cost_report` endpoint. Available to
        organizations on a Claude Enterprise plan. Requires an API key with the
        `read:analytics` scope.

        Args:
          starting_at: Start of range, inclusive. RFC 3339 tz-aware. Must be within the last 365 days
              and no earlier than 2026-01-01T00:00:00Z.

          bucket_width: Time-bucket granularity. When set, each row's `starting_at` and `ending_at` are
              populated and one actor may span several rows (one per time bucket with usage).
              The time bucket counts toward `limit`, so one page can return multiple rows for
              the same actor. `ending_at` is required when `bucket_width` is set, and with
              `bucket_width="1m"` the range may span at most 24 hours. When omitted, each row
              aggregates the full `[starting_at, ending_at)` range.

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

          exclude_deleted_users: If true, omit rows for users who are deleted (`deleted: true`). A page may
              contain fewer than `limit` rows; use `has_more` and `next_page` to paginate as
              usual.

          group_by: Break each actor's row out by the given dimensions. Accepts the same values as
              the bucketed `/cost_report` endpoint. The `product`, `model`, `context_window`,
              `inference_geo`, and `speed` dimensions — and the time bucket, when
              `bucket_width` is set — count toward `limit`. `cost_type` and `token_type` do
              not: `cost_type` returns one row per cost component (tokens, web search, code
              execution); `token_type` returns one row per token type, each with
              `cost_type: "tokens"`; combining both returns the per-token-type rows plus the
              web-search and code-execution rows. A page can therefore contain more rows than
              `limit` when `cost_type` or `token_type` is requested.

          inference_geos: Filter to specific inference regions. `not_available` matches rows where the
              region is unset. Use `group_by[]=inference_geo` to break out per-region values.

          limit: Number of rows per page (1-1000, default 20). One row per actor unless
              `group_by[]` or `bucket_width` splits an actor across rows;
              `cost_type`/`token_type` fan-out rows (cost endpoint only) are the exception —
              they do not count toward this limit, so `data` can exceed it.

          models: Models to include. Defaults to all models. Use `group_by[]=model` to break out
              per-model values.

          order: Sort direction. Defaults to `desc`.

          order_by: Metric to rank actors by. Defaults to `amount`.

          page: Opaque cursor from a previous response's `next_page` field.

          products: Product surfaces to include. Defaults to all products.

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
            "/v1/organizations/analytics/user_cost_report?beta=true",
            page=AsyncPageCursor[BetaAnalyticsCostUsersItem],
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
                    "slack_channel_ids": slack_channel_ids,
                    "speeds": speeds,
                    "user_ids": user_ids,
                },
            ),
            model=BetaAnalyticsCostUsersItem,
        )


class UserCostReportWithRawResponse:
    def __init__(self, user_cost_report: UserCostReport) -> None:
        self._user_cost_report = user_cost_report

        self.list = to_raw_response_wrapper(
            user_cost_report.list,
        )


class AsyncUserCostReportWithRawResponse:
    def __init__(self, user_cost_report: AsyncUserCostReport) -> None:
        self._user_cost_report = user_cost_report

        self.list = async_to_raw_response_wrapper(
            user_cost_report.list,
        )


class UserCostReportWithStreamingResponse:
    def __init__(self, user_cost_report: UserCostReport) -> None:
        self._user_cost_report = user_cost_report

        self.list = to_streamed_response_wrapper(
            user_cost_report.list,
        )


class AsyncUserCostReportWithStreamingResponse:
    def __init__(self, user_cost_report: AsyncUserCostReport) -> None:
        self._user_cost_report = user_cost_report

        self.list = async_to_streamed_response_wrapper(
            user_cost_report.list,
        )
