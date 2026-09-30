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
from .....types.beta.organization.beta_analytics_user_activity import BetaAnalyticsUserActivity

__all__ = ["Users", "AsyncUsers"]


class Users(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UsersWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return UsersWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UsersWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return UsersWithStreamingResponse(self)

    def list(
        self,
        *,
        date: Union[str, date, None] | Omit = omit,
        ending_date: Union[str, date, None] | Omit = omit,
        filter: Optional[SequenceNotStr[str]] | Omit = omit,
        group_by: Optional[List[Literal["rbac_group_id"]]] | Omit = omit,
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
    ) -> SyncPageCursor[BetaAnalyticsUserActivity]:
        """
        Get per-user activity for a given day, with cursor-based pagination.

        Returns activity metrics for each user in the organization, sorted by email
        address. Use `group_by[]` for per-RBAC-group aggregates, or `filter[]` to scope
        results to specific members, groups, or a chat project. Available to
        organizations on a Claude Enterprise plan. Requires an API key with the
        `read:analytics` scope.

        Args:
          date: UTC date in YYYY-MM-DD format. The day to get user activity for. Data is
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
              dimensions on this endpoint: `project_id`, `rbac_group_id`, `user_id`. Value
              forms: `project_id` takes a tagged project id (`claude_proj_...`) and scopes
              each member's row to their claude.ai chat activity within that project (it
              cannot be combined with `group_by[]` or an `rbac_group_id` filter);
              `rbac_group_id` takes the tagged id (`rbac_group_...`, as emitted in responses
              and by the spend-limits API) or a bare group UUID, and matches users who held
              the group at any point during each covered UTC day (time-of-usage attribution);
              `user_id` takes a tagged user id (`user_...`), as emitted in responses. An
              unsupported dimension returns 400. At most 100 entries.

          group_by: Dimensions to break results out by (e.g. `group_by[]=rbac_group_id`). Supported
              on this endpoint: `rbac_group_id`. Rows are already per-member, so the one
              supported grouping aggregates them per RBAC group instead. Grouped rows carry
              the requested dimension values as additional fields and paginate like ungrouped
              responses via `next_page`; an unsupported dimension returns 400. `rbac_group_id`
              attributes a user to every group they held at any point during each covered UTC
              day, so grouped rows are not an exclusive partition and can sum above org-level
              totals. At most 100 entries.

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
            "/v1/organizations/analytics/users?beta=true",
            page=SyncPageCursor[BetaAnalyticsUserActivity],
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
            model=BetaAnalyticsUserActivity,
        )


class AsyncUsers(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUsersWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncUsersWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUsersWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncUsersWithStreamingResponse(self)

    def list(
        self,
        *,
        date: Union[str, date, None] | Omit = omit,
        ending_date: Union[str, date, None] | Omit = omit,
        filter: Optional[SequenceNotStr[str]] | Omit = omit,
        group_by: Optional[List[Literal["rbac_group_id"]]] | Omit = omit,
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
    ) -> AsyncPaginator[BetaAnalyticsUserActivity, AsyncPageCursor[BetaAnalyticsUserActivity]]:
        """
        Get per-user activity for a given day, with cursor-based pagination.

        Returns activity metrics for each user in the organization, sorted by email
        address. Use `group_by[]` for per-RBAC-group aggregates, or `filter[]` to scope
        results to specific members, groups, or a chat project. Available to
        organizations on a Claude Enterprise plan. Requires an API key with the
        `read:analytics` scope.

        Args:
          date: UTC date in YYYY-MM-DD format. The day to get user activity for. Data is
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
              dimensions on this endpoint: `project_id`, `rbac_group_id`, `user_id`. Value
              forms: `project_id` takes a tagged project id (`claude_proj_...`) and scopes
              each member's row to their claude.ai chat activity within that project (it
              cannot be combined with `group_by[]` or an `rbac_group_id` filter);
              `rbac_group_id` takes the tagged id (`rbac_group_...`, as emitted in responses
              and by the spend-limits API) or a bare group UUID, and matches users who held
              the group at any point during each covered UTC day (time-of-usage attribution);
              `user_id` takes a tagged user id (`user_...`), as emitted in responses. An
              unsupported dimension returns 400. At most 100 entries.

          group_by: Dimensions to break results out by (e.g. `group_by[]=rbac_group_id`). Supported
              on this endpoint: `rbac_group_id`. Rows are already per-member, so the one
              supported grouping aggregates them per RBAC group instead. Grouped rows carry
              the requested dimension values as additional fields and paginate like ungrouped
              responses via `next_page`; an unsupported dimension returns 400. `rbac_group_id`
              attributes a user to every group they held at any point during each covered UTC
              day, so grouped rows are not an exclusive partition and can sum above org-level
              totals. At most 100 entries.

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
            "/v1/organizations/analytics/users?beta=true",
            page=AsyncPageCursor[BetaAnalyticsUserActivity],
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
            model=BetaAnalyticsUserActivity,
        )


class UsersWithRawResponse:
    def __init__(self, users: Users) -> None:
        self._users = users

        self.list = to_raw_response_wrapper(
            users.list,
        )


class AsyncUsersWithRawResponse:
    def __init__(self, users: AsyncUsers) -> None:
        self._users = users

        self.list = async_to_raw_response_wrapper(
            users.list,
        )


class UsersWithStreamingResponse:
    def __init__(self, users: Users) -> None:
        self._users = users

        self.list = to_streamed_response_wrapper(
            users.list,
        )


class AsyncUsersWithStreamingResponse:
    def __init__(self, users: AsyncUsers) -> None:
        self._users = users

        self.list = async_to_streamed_response_wrapper(
            users.list,
        )
