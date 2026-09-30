from __future__ import annotations

from typing import List, Union, Optional
from datetime import date
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
from .....types.beta.organization.beta_analytics_plugin_activity import BetaAnalyticsPluginActivity

__all__ = ["Plugins", "AsyncPlugins"]


class Plugins(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PluginsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return PluginsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PluginsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return PluginsWithStreamingResponse(self)

    def list(
        self,
        *,
        date: Union[str, date, None] | Omit = omit,
        ending_date: Union[str, date, None] | Omit = omit,
        filter: Optional[SequenceNotStr[str]] | Omit = omit,
        group_by: Optional[List[Literal["product", "rbac_group_id", "user_id"]]] | Omit = omit,
        limit: Optional[int] | Omit = omit,
        order: Optional[Literal["asc", "desc"]] | Omit = omit,
        order_by: Optional[str] | Omit = omit,
        page: Optional[str] | Omit = omit,
        starting_date: Union[str, date, None] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaAnalyticsPluginActivity]:
        """
        Get per-plugin install + invocation usage for a given day, with pagination.

        Returns plugin usage metrics for the organization across Cowork and Claude Code,
        sorted by plugin name. The `plugin_name` value `third-party` is an aggregate
        bucket, not a plugin: it collects plugin activity, from either surface, for
        which the reporting client did not provide a plugin name — so an organization's
        own plugins can contribute both to their own named rows and to this bucket. Use
        `group_by[]` to break usage out per member, per RBAC group, or per product
        surface (Cowork / Claude Code), and `filter[]` to scope results; the parameter
        descriptions list the supported dimensions. Requires an API key with the
        `read:analytics` scope. `starting_date` / `ending_date` select range-rollup mode
        like `/skills`.

        Args:
          date: UTC date in YYYY-MM-DD format. The day to get plugin usage for. Data is
              typically available with a 1-day lag (varies by query; the error for a
              too-recent date names the latest available day) and may be revised by a few
              percent over the following days. No earlier than 2026-01-01.

          ending_date: UTC date in YYYY-MM-DD format. End of the date range (exclusive); only valid
              with `starting_date`. Data is typically available with a 1-day lag (varies by
              query; the error for a too-recent date names the latest available day), so this
              can be at most today — which is also the default when omitted, resolved once
              when the first page is served and reused for the rest of the pagination
              sequence. At most 366 days after `starting_date`.

          filter: Filters as `dimension:value`, e.g. `filter[]=rbac_group_id:{id}`. Repeat the
              param for OR within a dimension and across dimensions for AND. Supported
              dimensions on this endpoint: `plugin_name`, `product`, `rbac_group_id`,
              `user_id`. Value forms: `plugin_name` matches case-insensitively; `product` is
              `claude_code` or `cowork` (the only surfaces with plugin attribution);
              `rbac_group_id` takes the tagged id (`rbac_group_...`, as emitted in responses
              and by the spend-limits API) or a bare group UUID, and matches users who held
              the group at any point during each covered UTC day (time-of-usage attribution);
              `user_id` takes a tagged user id (`user_...`), as emitted in responses. An
              unsupported dimension returns 400. At most 100 entries.

          group_by: Dimensions to break results out by (e.g. `group_by[]=user_id`). Supported on
              this endpoint: `product`, `rbac_group_id`, `user_id`. On this endpoint `product`
              takes the values `claude_code` or `cowork` only (the surfaces with plugin
              attribution). Grouped rows carry the requested dimension values as additional
              fields and paginate like ungrouped responses via `next_page`; an unsupported
              dimension returns 400. `rbac_group_id` attributes a user to every group they
              held at any point during each covered UTC day, so grouped rows are not an
              exclusive partition and can sum above org-level totals. At most 100 entries.

          limit: Number of results per page (1-1000, default 100).

          order: Sort direction: `asc` or `desc`. Defaults to `asc` for the endpoint's sort
              column and to `desc` when `order_by` names a metric (a top-N ranking). Applies
              to `order_by`, or to the endpoint's default sort field when `order_by` is
              omitted.

          order_by: Sort field. Restricted to the endpoint's sort column plus its rankable metrics
              (metrics default to descending; a few metrics rank in date-range mode only, per
              the endpoint's documented orderable set).

          page: Opaque cursor from a previous response's `next_page` field.

          starting_date: UTC date in YYYY-MM-DD format. Start of a date range (inclusive). Enables rollup
              mode: one row per entity aggregated over the whole range — addable counters are
              summed across days, and a distinct count is never summed where summing could
              double-count (a field's range value is recomputed exactly over the window,
              approximate via HLL with typical error under 2%, null, or — for the
              creation-event counts, whose per-day values cannot overlap — a per-day sum that
              is itself exact; each field's own description says which). Use either `date` or
              `starting_date`, not both. Data is typically available with a 1-day lag (varies
              by query; the error for a too-recent date names the latest available day) and
              may be revised by a few percent over the following days. No earlier than
              2026-01-01.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/analytics/plugins?beta=true",
            page=SyncPageCursor[BetaAnalyticsPluginActivity],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "date": date,
                    "ending_date": ending_date,
                    "filter": filter,
                    "group_by": group_by,
                    "limit": limit,
                    "order": order,
                    "order_by": order_by,
                    "page": page,
                    "starting_date": starting_date,
                },
            ),
            model=BetaAnalyticsPluginActivity,
        )


class AsyncPlugins(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPluginsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPluginsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPluginsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncPluginsWithStreamingResponse(self)

    def list(
        self,
        *,
        date: Union[str, date, None] | Omit = omit,
        ending_date: Union[str, date, None] | Omit = omit,
        filter: Optional[SequenceNotStr[str]] | Omit = omit,
        group_by: Optional[List[Literal["product", "rbac_group_id", "user_id"]]] | Omit = omit,
        limit: Optional[int] | Omit = omit,
        order: Optional[Literal["asc", "desc"]] | Omit = omit,
        order_by: Optional[str] | Omit = omit,
        page: Optional[str] | Omit = omit,
        starting_date: Union[str, date, None] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaAnalyticsPluginActivity, AsyncPageCursor[BetaAnalyticsPluginActivity]]:
        """
        Get per-plugin install + invocation usage for a given day, with pagination.

        Returns plugin usage metrics for the organization across Cowork and Claude Code,
        sorted by plugin name. The `plugin_name` value `third-party` is an aggregate
        bucket, not a plugin: it collects plugin activity, from either surface, for
        which the reporting client did not provide a plugin name — so an organization's
        own plugins can contribute both to their own named rows and to this bucket. Use
        `group_by[]` to break usage out per member, per RBAC group, or per product
        surface (Cowork / Claude Code), and `filter[]` to scope results; the parameter
        descriptions list the supported dimensions. Requires an API key with the
        `read:analytics` scope. `starting_date` / `ending_date` select range-rollup mode
        like `/skills`.

        Args:
          date: UTC date in YYYY-MM-DD format. The day to get plugin usage for. Data is
              typically available with a 1-day lag (varies by query; the error for a
              too-recent date names the latest available day) and may be revised by a few
              percent over the following days. No earlier than 2026-01-01.

          ending_date: UTC date in YYYY-MM-DD format. End of the date range (exclusive); only valid
              with `starting_date`. Data is typically available with a 1-day lag (varies by
              query; the error for a too-recent date names the latest available day), so this
              can be at most today — which is also the default when omitted, resolved once
              when the first page is served and reused for the rest of the pagination
              sequence. At most 366 days after `starting_date`.

          filter: Filters as `dimension:value`, e.g. `filter[]=rbac_group_id:{id}`. Repeat the
              param for OR within a dimension and across dimensions for AND. Supported
              dimensions on this endpoint: `plugin_name`, `product`, `rbac_group_id`,
              `user_id`. Value forms: `plugin_name` matches case-insensitively; `product` is
              `claude_code` or `cowork` (the only surfaces with plugin attribution);
              `rbac_group_id` takes the tagged id (`rbac_group_...`, as emitted in responses
              and by the spend-limits API) or a bare group UUID, and matches users who held
              the group at any point during each covered UTC day (time-of-usage attribution);
              `user_id` takes a tagged user id (`user_...`), as emitted in responses. An
              unsupported dimension returns 400. At most 100 entries.

          group_by: Dimensions to break results out by (e.g. `group_by[]=user_id`). Supported on
              this endpoint: `product`, `rbac_group_id`, `user_id`. On this endpoint `product`
              takes the values `claude_code` or `cowork` only (the surfaces with plugin
              attribution). Grouped rows carry the requested dimension values as additional
              fields and paginate like ungrouped responses via `next_page`; an unsupported
              dimension returns 400. `rbac_group_id` attributes a user to every group they
              held at any point during each covered UTC day, so grouped rows are not an
              exclusive partition and can sum above org-level totals. At most 100 entries.

          limit: Number of results per page (1-1000, default 100).

          order: Sort direction: `asc` or `desc`. Defaults to `asc` for the endpoint's sort
              column and to `desc` when `order_by` names a metric (a top-N ranking). Applies
              to `order_by`, or to the endpoint's default sort field when `order_by` is
              omitted.

          order_by: Sort field. Restricted to the endpoint's sort column plus its rankable metrics
              (metrics default to descending; a few metrics rank in date-range mode only, per
              the endpoint's documented orderable set).

          page: Opaque cursor from a previous response's `next_page` field.

          starting_date: UTC date in YYYY-MM-DD format. Start of a date range (inclusive). Enables rollup
              mode: one row per entity aggregated over the whole range — addable counters are
              summed across days, and a distinct count is never summed where summing could
              double-count (a field's range value is recomputed exactly over the window,
              approximate via HLL with typical error under 2%, null, or — for the
              creation-event counts, whose per-day values cannot overlap — a per-day sum that
              is itself exact; each field's own description says which). Use either `date` or
              `starting_date`, not both. Data is typically available with a 1-day lag (varies
              by query; the error for a too-recent date names the latest available day) and
              may be revised by a few percent over the following days. No earlier than
              2026-01-01.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/analytics/plugins?beta=true",
            page=AsyncPageCursor[BetaAnalyticsPluginActivity],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "date": date,
                    "ending_date": ending_date,
                    "filter": filter,
                    "group_by": group_by,
                    "limit": limit,
                    "order": order,
                    "order_by": order_by,
                    "page": page,
                    "starting_date": starting_date,
                },
            ),
            model=BetaAnalyticsPluginActivity,
        )


class PluginsWithRawResponse:
    def __init__(self, plugins: Plugins) -> None:
        self._plugins = plugins

        self.list = to_raw_response_wrapper(
            plugins.list,
        )


class AsyncPluginsWithRawResponse:
    def __init__(self, plugins: AsyncPlugins) -> None:
        self._plugins = plugins

        self.list = async_to_raw_response_wrapper(
            plugins.list,
        )


class PluginsWithStreamingResponse:
    def __init__(self, plugins: Plugins) -> None:
        self._plugins = plugins

        self.list = to_streamed_response_wrapper(
            plugins.list,
        )


class AsyncPluginsWithStreamingResponse:
    def __init__(self, plugins: AsyncPlugins) -> None:
        self._plugins = plugins

        self.list = async_to_streamed_response_wrapper(
            plugins.list,
        )
