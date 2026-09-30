from __future__ import annotations

from typing import List, Optional

import httpx2

from ....._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ....._utils import path_template
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
from .....types.beta.organization import BetaSpendLimitPeriod
from .....types.beta.organization.beta_spend_limit_period import BetaSpendLimitPeriod
from .....types.beta.organization.spend_limits.beta_spend_limit_increase_request import BetaSpendLimitIncreaseRequest
from .....types.beta.organization.spend_limits.increase_request_approve_response import IncreaseRequestApproveResponse
from .....types.beta.organization.spend_limits.beta_spend_limit_increase_request_status import (
    BetaSpendLimitIncreaseRequestStatus,
)

__all__ = ["IncreaseRequests", "AsyncIncreaseRequests"]


class IncreaseRequests(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> IncreaseRequestsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return IncreaseRequestsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> IncreaseRequestsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return IncreaseRequestsWithStreamingResponse(self)

    def retrieve(
        self,
        spend_limit_increase_request_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaSpendLimitIncreaseRequest:
        """
        Retrieve a spend limit increase request.

        While `pending`, the response includes a live `spend_summary` for the requester
        at the request's period.

        Args:
          spend_limit_increase_request_id: ID of the spend limit increase request.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not spend_limit_increase_request_id:
            raise ValueError(
                f"Expected a non-empty value for `spend_limit_increase_request_id` but received {spend_limit_increase_request_id!r}"
            )
        return self._get(
            path_template(
                "/v1/organizations/spend_limit_increase_requests/{spend_limit_increase_request_id}?beta=true",
                spend_limit_increase_request_id=spend_limit_increase_request_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaSpendLimitIncreaseRequest,
        )

    def list(
        self,
        *,
        actor_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        status: Optional[List[BetaSpendLimitIncreaseRequestStatus]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaSpendLimitIncreaseRequest]:
        """
        List spend limit increase requests, most recent first.

        Pending requests include a live `spend_summary` for the requester. Requests
        whose requester is no longer a member are excluded.

        Args:
          actor_ids: Filter by requester, as `user_...` tagged IDs.

          page: Opaque cursor from a previous response's `next_page`.

          status: Filter by status. Omit to return all.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/spend_limit_increase_requests?beta=true",
            page=SyncPageCursor[BetaSpendLimitIncreaseRequest],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "actor_ids": actor_ids,
                    "limit": limit,
                    "page": page,
                    "status": status,
                },
            ),
            model=BetaSpendLimitIncreaseRequest,
        )

    def approve(
        self,
        spend_limit_increase_request_id: str,
        *,
        amount: str,
        period: Optional[BetaSpendLimitPeriod] | Omit = omit,
        suppress_notification: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> IncreaseRequestApproveResponse:
        """
        Approve a pending spend limit increase request.

        Writes a per-user spend limit at `amount` for the requester and transitions the
        request to `approved`. `period` defaults to the period the member was blocked
        on. Anthropic emails the requester unless `suppress_notification` is set.

        Args:
          spend_limit_increase_request_id: ID of the spend limit increase request.

          amount: New per-user spend limit as a non-negative integer decimal string (minor units).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not spend_limit_increase_request_id:
            raise ValueError(
                f"Expected a non-empty value for `spend_limit_increase_request_id` but received {spend_limit_increase_request_id!r}"
            )
        return self._post(
            path_template(
                "/v1/organizations/spend_limit_increase_requests/{spend_limit_increase_request_id}/approve?beta=true",
                spend_limit_increase_request_id=spend_limit_increase_request_id,
            ),
            body={
                "amount": amount,
                "period": period,
                "suppress_notification": suppress_notification,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=IncreaseRequestApproveResponse,
        )

    def deny(
        self,
        spend_limit_increase_request_id: str,
        *,
        suppress_notification: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaSpendLimitIncreaseRequest:
        """
        Deny a pending spend limit increase request.

        Idempotent on `denied`; denying an already-`approved` request returns 400.
        Anthropic emails the requester unless `suppress_notification` is set.

        Args:
          spend_limit_increase_request_id: ID of the spend limit increase request.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not spend_limit_increase_request_id:
            raise ValueError(
                f"Expected a non-empty value for `spend_limit_increase_request_id` but received {spend_limit_increase_request_id!r}"
            )
        return self._post(
            path_template(
                "/v1/organizations/spend_limit_increase_requests/{spend_limit_increase_request_id}/deny?beta=true",
                spend_limit_increase_request_id=spend_limit_increase_request_id,
            ),
            body={"suppress_notification": suppress_notification},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaSpendLimitIncreaseRequest,
        )


class AsyncIncreaseRequests(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncIncreaseRequestsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncIncreaseRequestsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncIncreaseRequestsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncIncreaseRequestsWithStreamingResponse(self)

    async def retrieve(
        self,
        spend_limit_increase_request_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaSpendLimitIncreaseRequest:
        """
        Retrieve a spend limit increase request.

        While `pending`, the response includes a live `spend_summary` for the requester
        at the request's period.

        Args:
          spend_limit_increase_request_id: ID of the spend limit increase request.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not spend_limit_increase_request_id:
            raise ValueError(
                f"Expected a non-empty value for `spend_limit_increase_request_id` but received {spend_limit_increase_request_id!r}"
            )
        return await self._get(
            path_template(
                "/v1/organizations/spend_limit_increase_requests/{spend_limit_increase_request_id}?beta=true",
                spend_limit_increase_request_id=spend_limit_increase_request_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaSpendLimitIncreaseRequest,
        )

    def list(
        self,
        *,
        actor_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        status: Optional[List[BetaSpendLimitIncreaseRequestStatus]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaSpendLimitIncreaseRequest, AsyncPageCursor[BetaSpendLimitIncreaseRequest]]:
        """
        List spend limit increase requests, most recent first.

        Pending requests include a live `spend_summary` for the requester. Requests
        whose requester is no longer a member are excluded.

        Args:
          actor_ids: Filter by requester, as `user_...` tagged IDs.

          page: Opaque cursor from a previous response's `next_page`.

          status: Filter by status. Omit to return all.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/spend_limit_increase_requests?beta=true",
            page=AsyncPageCursor[BetaSpendLimitIncreaseRequest],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "actor_ids": actor_ids,
                    "limit": limit,
                    "page": page,
                    "status": status,
                },
            ),
            model=BetaSpendLimitIncreaseRequest,
        )

    async def approve(
        self,
        spend_limit_increase_request_id: str,
        *,
        amount: str,
        period: Optional[BetaSpendLimitPeriod] | Omit = omit,
        suppress_notification: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> IncreaseRequestApproveResponse:
        """
        Approve a pending spend limit increase request.

        Writes a per-user spend limit at `amount` for the requester and transitions the
        request to `approved`. `period` defaults to the period the member was blocked
        on. Anthropic emails the requester unless `suppress_notification` is set.

        Args:
          spend_limit_increase_request_id: ID of the spend limit increase request.

          amount: New per-user spend limit as a non-negative integer decimal string (minor units).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not spend_limit_increase_request_id:
            raise ValueError(
                f"Expected a non-empty value for `spend_limit_increase_request_id` but received {spend_limit_increase_request_id!r}"
            )
        return await self._post(
            path_template(
                "/v1/organizations/spend_limit_increase_requests/{spend_limit_increase_request_id}/approve?beta=true",
                spend_limit_increase_request_id=spend_limit_increase_request_id,
            ),
            body={
                "amount": amount,
                "period": period,
                "suppress_notification": suppress_notification,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=IncreaseRequestApproveResponse,
        )

    async def deny(
        self,
        spend_limit_increase_request_id: str,
        *,
        suppress_notification: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaSpendLimitIncreaseRequest:
        """
        Deny a pending spend limit increase request.

        Idempotent on `denied`; denying an already-`approved` request returns 400.
        Anthropic emails the requester unless `suppress_notification` is set.

        Args:
          spend_limit_increase_request_id: ID of the spend limit increase request.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not spend_limit_increase_request_id:
            raise ValueError(
                f"Expected a non-empty value for `spend_limit_increase_request_id` but received {spend_limit_increase_request_id!r}"
            )
        return await self._post(
            path_template(
                "/v1/organizations/spend_limit_increase_requests/{spend_limit_increase_request_id}/deny?beta=true",
                spend_limit_increase_request_id=spend_limit_increase_request_id,
            ),
            body={"suppress_notification": suppress_notification},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaSpendLimitIncreaseRequest,
        )


class IncreaseRequestsWithRawResponse:
    def __init__(self, increase_requests: IncreaseRequests) -> None:
        self._increase_requests = increase_requests

        self.retrieve = to_raw_response_wrapper(
            increase_requests.retrieve,
        )
        self.list = to_raw_response_wrapper(
            increase_requests.list,
        )
        self.approve = to_raw_response_wrapper(
            increase_requests.approve,
        )
        self.deny = to_raw_response_wrapper(
            increase_requests.deny,
        )


class AsyncIncreaseRequestsWithRawResponse:
    def __init__(self, increase_requests: AsyncIncreaseRequests) -> None:
        self._increase_requests = increase_requests

        self.retrieve = async_to_raw_response_wrapper(
            increase_requests.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            increase_requests.list,
        )
        self.approve = async_to_raw_response_wrapper(
            increase_requests.approve,
        )
        self.deny = async_to_raw_response_wrapper(
            increase_requests.deny,
        )


class IncreaseRequestsWithStreamingResponse:
    def __init__(self, increase_requests: IncreaseRequests) -> None:
        self._increase_requests = increase_requests

        self.retrieve = to_streamed_response_wrapper(
            increase_requests.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            increase_requests.list,
        )
        self.approve = to_streamed_response_wrapper(
            increase_requests.approve,
        )
        self.deny = to_streamed_response_wrapper(
            increase_requests.deny,
        )


class AsyncIncreaseRequestsWithStreamingResponse:
    def __init__(self, increase_requests: AsyncIncreaseRequests) -> None:
        self._increase_requests = increase_requests

        self.retrieve = async_to_streamed_response_wrapper(
            increase_requests.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            increase_requests.list,
        )
        self.approve = async_to_streamed_response_wrapper(
            increase_requests.approve,
        )
        self.deny = async_to_streamed_response_wrapper(
            increase_requests.deny,
        )
