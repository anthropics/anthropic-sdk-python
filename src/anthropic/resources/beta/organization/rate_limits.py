# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal

import httpx2

from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....pagination import SyncPageCursor, AsyncPageCursor
from ...._base_client import AsyncPaginator, make_request_options
from ....types.beta.organization import rate_limit_list_params
from ....types.beta.organization.beta_organization_rate_limit import BetaOrganizationRateLimit

__all__ = ["RateLimits", "AsyncRateLimits"]


class RateLimits(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RateLimitsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return RateLimitsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RateLimitsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return RateLimitsWithStreamingResponse(self)

    def list(
        self,
        *,
        group_type: Optional[Literal["batch", "files", "model_group", "skills", "token_count", "web_search"]]
        | Omit = omit,
        limit: Optional[int] | Omit = omit,
        model: Optional[str] | Omit = omit,
        page: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaOrganizationRateLimit]:
        """
        List Messages API rate limits for your organization.

        Each entry corresponds to one rate-limit group (either a model family or an
        API-surface category such as the Files API or Message Batches) and contains the
        set of limiter values that apply to it.

        When `limit` is omitted, every matching entry is returned in a single page; when
        `limit` truncates the result, follow `next_page` to fetch the remaining entries.

        Args:
          group_type: Filter by group type.

          limit: Maximum number of items to return per page. Ranges from `1` to `1000`.

              When omitted, every remaining entry is returned in a single page and `next_page`
              is `null`.

          model: Filter to the single entry containing this model. Accepts full model names and
              aliases. Returns 404 if the model is not found or has no rate limits for this
              organization.

          page: Opaque cursor from a previous response's `next_page`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/rate_limits?beta=true",
            page=SyncPageCursor[BetaOrganizationRateLimit],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "group_type": group_type,
                        "limit": limit,
                        "model": model,
                        "page": page,
                    },
                    rate_limit_list_params.RateLimitListParams,
                ),
            ),
            model=BetaOrganizationRateLimit,
        )


class AsyncRateLimits(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRateLimitsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncRateLimitsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRateLimitsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncRateLimitsWithStreamingResponse(self)

    def list(
        self,
        *,
        group_type: Optional[Literal["batch", "files", "model_group", "skills", "token_count", "web_search"]]
        | Omit = omit,
        limit: Optional[int] | Omit = omit,
        model: Optional[str] | Omit = omit,
        page: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaOrganizationRateLimit, AsyncPageCursor[BetaOrganizationRateLimit]]:
        """
        List Messages API rate limits for your organization.

        Each entry corresponds to one rate-limit group (either a model family or an
        API-surface category such as the Files API or Message Batches) and contains the
        set of limiter values that apply to it.

        When `limit` is omitted, every matching entry is returned in a single page; when
        `limit` truncates the result, follow `next_page` to fetch the remaining entries.

        Args:
          group_type: Filter by group type.

          limit: Maximum number of items to return per page. Ranges from `1` to `1000`.

              When omitted, every remaining entry is returned in a single page and `next_page`
              is `null`.

          model: Filter to the single entry containing this model. Accepts full model names and
              aliases. Returns 404 if the model is not found or has no rate limits for this
              organization.

          page: Opaque cursor from a previous response's `next_page`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/rate_limits?beta=true",
            page=AsyncPageCursor[BetaOrganizationRateLimit],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "group_type": group_type,
                        "limit": limit,
                        "model": model,
                        "page": page,
                    },
                    rate_limit_list_params.RateLimitListParams,
                ),
            ),
            model=BetaOrganizationRateLimit,
        )


class RateLimitsWithRawResponse:
    def __init__(self, rate_limits: RateLimits) -> None:
        self._rate_limits = rate_limits

        self.list = to_raw_response_wrapper(
            rate_limits.list,
        )


class AsyncRateLimitsWithRawResponse:
    def __init__(self, rate_limits: AsyncRateLimits) -> None:
        self._rate_limits = rate_limits

        self.list = async_to_raw_response_wrapper(
            rate_limits.list,
        )


class RateLimitsWithStreamingResponse:
    def __init__(self, rate_limits: RateLimits) -> None:
        self._rate_limits = rate_limits

        self.list = to_streamed_response_wrapper(
            rate_limits.list,
        )


class AsyncRateLimitsWithStreamingResponse:
    def __init__(self, rate_limits: AsyncRateLimits) -> None:
        self._rate_limits = rate_limits

        self.list = async_to_streamed_response_wrapper(
            rate_limits.list,
        )
