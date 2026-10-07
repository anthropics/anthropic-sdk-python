from __future__ import annotations

from typing import List, Optional
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
from .....types.beta.organization.beta_spend_summary import BetaSpendSummary

__all__ = ["Effective", "AsyncEffective"]


class Effective(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EffectiveWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return EffectiveWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EffectiveWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return EffectiveWithStreamingResponse(self)

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        period: Optional[List[Literal["daily", "monthly", "weekly"]]] | Omit = omit,
        user_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaSpendSummary]:
        """
        List each member's effective spend limit and period-to-date spend.

        Returns one row per (member, period) the member resolves a spend limit for, with
        the `source` scope the spend limit was inherited from. Paginates by member, so a
        member's periods never split across pages. Listing Claude Console limits is in
        an early access preview. To request access, contact your Anthropic account team.

        Args:
          limit: Maximum number of members per page. A member's period rows never split across
              pages, so a page may carry more rows than this. Defaults to `20`.

          page: Opaque cursor from a previous response's `next_page` field.

          period: Restrict the report to these limit periods. Omit to return one row per period
              each member resolves a spend limit for.

          user_ids: Restrict the report to these members, by tagged user ID (`user_...`). At most
              100 entries.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/spend_limits/effective?beta=true",
            page=SyncPageCursor[BetaSpendSummary],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "page": page,
                    "period": period,
                    "user_ids": user_ids,
                },
            ),
            model=BetaSpendSummary,
        )


class AsyncEffective(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEffectiveWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEffectiveWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEffectiveWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncEffectiveWithStreamingResponse(self)

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        period: Optional[List[Literal["daily", "monthly", "weekly"]]] | Omit = omit,
        user_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaSpendSummary, AsyncPageCursor[BetaSpendSummary]]:
        """
        List each member's effective spend limit and period-to-date spend.

        Returns one row per (member, period) the member resolves a spend limit for, with
        the `source` scope the spend limit was inherited from. Paginates by member, so a
        member's periods never split across pages. Listing Claude Console limits is in
        an early access preview. To request access, contact your Anthropic account team.

        Args:
          limit: Maximum number of members per page. A member's period rows never split across
              pages, so a page may carry more rows than this. Defaults to `20`.

          page: Opaque cursor from a previous response's `next_page` field.

          period: Restrict the report to these limit periods. Omit to return one row per period
              each member resolves a spend limit for.

          user_ids: Restrict the report to these members, by tagged user ID (`user_...`). At most
              100 entries.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/spend_limits/effective?beta=true",
            page=AsyncPageCursor[BetaSpendSummary],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "page": page,
                    "period": period,
                    "user_ids": user_ids,
                },
            ),
            model=BetaSpendSummary,
        )


class EffectiveWithRawResponse:
    def __init__(self, effective: Effective) -> None:
        self._effective = effective

        self.list = to_raw_response_wrapper(
            effective.list,
        )


class AsyncEffectiveWithRawResponse:
    def __init__(self, effective: AsyncEffective) -> None:
        self._effective = effective

        self.list = async_to_raw_response_wrapper(
            effective.list,
        )


class EffectiveWithStreamingResponse:
    def __init__(self, effective: Effective) -> None:
        self._effective = effective

        self.list = to_streamed_response_wrapper(
            effective.list,
        )


class AsyncEffectiveWithStreamingResponse:
    def __init__(self, effective: AsyncEffective) -> None:
        self._effective = effective

        self.list = async_to_streamed_response_wrapper(
            effective.list,
        )
