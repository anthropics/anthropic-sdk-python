from __future__ import annotations

from typing import Union, Optional
from datetime import date

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
from .....types.beta.organization.beta_analytics_single_day_activity_summary import (
    BetaAnalyticsSingleDayActivitySummary,
)

__all__ = ["Summaries", "AsyncSummaries"]


class Summaries(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SummariesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return SummariesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SummariesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return SummariesWithStreamingResponse(self)

    def list(
        self,
        *,
        starting_date: Union[str, date],
        ending_date: Union[str, date, None] | Omit = omit,
        filter: Optional[SequenceNotStr[str]] | Omit = omit,
        limit: Optional[int] | Omit = omit,
        page: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaAnalyticsSingleDayActivitySummary]:
        """
        Get organization-wide activity summaries for a date range.

        Returns one entry per day from `starting_date` (inclusive) to `ending_date`
        (exclusive) in `data`, the same `data` / `next_page` envelope as the other
        analytics list endpoints; the series is currently returned in full, so
        `next_page` is always null. Data is typically available with a 1-day lag and may
        be revised by a few percent over the following days: when `ending_date` is
        omitted it defaults to the most recent available day + 1, so the last entry
        covers the most recent available day. The series can be scoped to an RBAC group
        via `filter[]=rbac_group_id:{id}`. Available to organizations on a Claude
        Enterprise plan. Requires an API key with the `read:analytics` scope.

        Args:
          starting_date: UTC date in YYYY-MM-DD format. Start of the date range (inclusive). Data is
              typically available with a 1-day lag (varies by query; the error for a
              too-recent date names the latest available day) and may be revised by a few
              percent over the following days. No earlier than 2026-01-01.

          ending_date: UTC date in YYYY-MM-DD format. End of the date range (exclusive). Data is
              typically available with a 1-day lag, so this can be at most today — which is
              also the default when omitted, making the last entry cover the most recent
              available day. Data may be revised by a few percent over the following days. The
              range may span at most 366 days.

          filter: Filters as `dimension:value`. Only `rbac_group_id` is supported (e.g.
              `filter[]=rbac_group_id:{id}`); repeat the param to OR across groups. Scopes the
              whole day series to members of the matching group(s), re-aggregated from
              member-level activity — org-wide seat/invite fields and the adoption rates
              derived from them are null on scoped rows. `rbac_group_id` accepts the tagged id
              (`rbac_group_...`, as emitted in responses and by the spend-limits API) or a
              bare group UUID, and matches users who held the group at any point during each
              UTC day (time-of-usage attribution). At most 100 entries.

          limit: Number of results per page (1-1000, default 100). The day series (at most 366
              entries) is currently returned in full in a single page, so `limit` does not yet
              shorten it.

          page: Opaque cursor from a previous response's `next_page` field. `next_page` is
              currently always null, so there is never a cursor to send.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/analytics/summaries?beta=true",
            page=SyncPageCursor[BetaAnalyticsSingleDayActivitySummary],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "starting_date": starting_date,
                    "ending_date": ending_date,
                    "filter": filter,
                    "limit": limit,
                    "page": page,
                },
            ),
            model=BetaAnalyticsSingleDayActivitySummary,
        )


class AsyncSummaries(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSummariesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSummariesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSummariesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncSummariesWithStreamingResponse(self)

    def list(
        self,
        *,
        starting_date: Union[str, date],
        ending_date: Union[str, date, None] | Omit = omit,
        filter: Optional[SequenceNotStr[str]] | Omit = omit,
        limit: Optional[int] | Omit = omit,
        page: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaAnalyticsSingleDayActivitySummary, AsyncPageCursor[BetaAnalyticsSingleDayActivitySummary]]:
        """
        Get organization-wide activity summaries for a date range.

        Returns one entry per day from `starting_date` (inclusive) to `ending_date`
        (exclusive) in `data`, the same `data` / `next_page` envelope as the other
        analytics list endpoints; the series is currently returned in full, so
        `next_page` is always null. Data is typically available with a 1-day lag and may
        be revised by a few percent over the following days: when `ending_date` is
        omitted it defaults to the most recent available day + 1, so the last entry
        covers the most recent available day. The series can be scoped to an RBAC group
        via `filter[]=rbac_group_id:{id}`. Available to organizations on a Claude
        Enterprise plan. Requires an API key with the `read:analytics` scope.

        Args:
          starting_date: UTC date in YYYY-MM-DD format. Start of the date range (inclusive). Data is
              typically available with a 1-day lag (varies by query; the error for a
              too-recent date names the latest available day) and may be revised by a few
              percent over the following days. No earlier than 2026-01-01.

          ending_date: UTC date in YYYY-MM-DD format. End of the date range (exclusive). Data is
              typically available with a 1-day lag, so this can be at most today — which is
              also the default when omitted, making the last entry cover the most recent
              available day. Data may be revised by a few percent over the following days. The
              range may span at most 366 days.

          filter: Filters as `dimension:value`. Only `rbac_group_id` is supported (e.g.
              `filter[]=rbac_group_id:{id}`); repeat the param to OR across groups. Scopes the
              whole day series to members of the matching group(s), re-aggregated from
              member-level activity — org-wide seat/invite fields and the adoption rates
              derived from them are null on scoped rows. `rbac_group_id` accepts the tagged id
              (`rbac_group_...`, as emitted in responses and by the spend-limits API) or a
              bare group UUID, and matches users who held the group at any point during each
              UTC day (time-of-usage attribution). At most 100 entries.

          limit: Number of results per page (1-1000, default 100). The day series (at most 366
              entries) is currently returned in full in a single page, so `limit` does not yet
              shorten it.

          page: Opaque cursor from a previous response's `next_page` field. `next_page` is
              currently always null, so there is never a cursor to send.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/analytics/summaries?beta=true",
            page=AsyncPageCursor[BetaAnalyticsSingleDayActivitySummary],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "starting_date": starting_date,
                    "ending_date": ending_date,
                    "filter": filter,
                    "limit": limit,
                    "page": page,
                },
            ),
            model=BetaAnalyticsSingleDayActivitySummary,
        )


class SummariesWithRawResponse:
    def __init__(self, summaries: Summaries) -> None:
        self._summaries = summaries

        self.list = to_raw_response_wrapper(
            summaries.list,
        )


class AsyncSummariesWithRawResponse:
    def __init__(self, summaries: AsyncSummaries) -> None:
        self._summaries = summaries

        self.list = async_to_raw_response_wrapper(
            summaries.list,
        )


class SummariesWithStreamingResponse:
    def __init__(self, summaries: Summaries) -> None:
        self._summaries = summaries

        self.list = to_streamed_response_wrapper(
            summaries.list,
        )


class AsyncSummariesWithStreamingResponse:
    def __init__(self, summaries: AsyncSummaries) -> None:
        self._summaries = summaries

        self.list = async_to_streamed_response_wrapper(
            summaries.list,
        )
