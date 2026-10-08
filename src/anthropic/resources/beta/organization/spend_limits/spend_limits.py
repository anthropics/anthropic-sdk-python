from __future__ import annotations

from typing import List, Optional
from itertools import chain
from typing_extensions import Literal

import httpx2

from .effective import (
    Effective,
    AsyncEffective,
    EffectiveWithRawResponse,
    AsyncEffectiveWithRawResponse,
    EffectiveWithStreamingResponse,
    AsyncEffectiveWithStreamingResponse,
)
from ....._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ....._utils import is_given, path_template, strip_not_given
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
from .increase_requests import (
    IncreaseRequests,
    AsyncIncreaseRequests,
    IncreaseRequestsWithRawResponse,
    AsyncIncreaseRequestsWithRawResponse,
    IncreaseRequestsWithStreamingResponse,
    AsyncIncreaseRequestsWithStreamingResponse,
)
from .....types.beta.organization import BetaSpendLimitPeriod, spend_limit_set_params
from .....types.anthropic_beta_param import AnthropicBetaParam
from .....types.beta.organization.beta_spend_limit import BetaSpendLimit
from .....types.beta.organization.beta_spend_limit_period import BetaSpendLimitPeriod
from .....types.beta.organization.spend_limit_delete_response import SpendLimitDeleteResponse

__all__ = ["SpendLimits", "AsyncSpendLimits"]


class SpendLimits(SyncAPIResource):
    @cached_property
    def effective(self) -> Effective:
        return Effective(self._client)

    @cached_property
    def increase_requests(self) -> IncreaseRequests:
        return IncreaseRequests(self._client)

    @cached_property
    def with_raw_response(self) -> SpendLimitsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return SpendLimitsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SpendLimitsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return SpendLimitsWithStreamingResponse(self)

    def retrieve(
        self,
        spend_limit_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaSpendLimit:
        """
        Retrieve a spend limit by ID.

        Args:
          spend_limit_id: ID of the Spend Limit.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not spend_limit_id:
            raise ValueError(f"Expected a non-empty value for `spend_limit_id` but received {spend_limit_id!r}")
        return self._get(
            path_template("/v1/organizations/spend_limits/{spend_limit_id}?beta=true", spend_limit_id=spend_limit_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaSpendLimit,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        scope_type: Optional[
            List[Literal["organization", "organization_service", "rbac_group", "seat_tier", "user", "workspace"]]
        ]
        | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaSpendLimit]:
        """
        List the organization's spend limits.

        A Claude Console organization's limits come in an order that is stable across
        pages. A Claude Enterprise organization's are grouped by scope type, in the
        order `organization`, `seat_tier`, `rbac_group`, `organization_service`, `user`;
        within a type they come in a fixed order that is not creation order. Listing
        Claude Console limits is in an early access preview. To request access, contact
        your Anthropic account team.

        Args:
          limit: Maximum number of limits per page. Defaults to `20`.

          page: Opaque cursor from a previous response's `next_page` field.

          scope_type: Return only limits with these scope types. A Claude Console organization has
              `organization` and `workspace` limits; a Claude Enterprise organization has
              `organization`, `seat_tier`, `rbac_group`, `organization_service` and `user`
              limits. Omit for all.

          betas: This endpoint is in beta: requests must send `spend-limit-reads-2026-09-26` in
              this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["spend-limit-reads-2026-09-26"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "spend-limit-reads-2026-09-26", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/organizations/spend_limits?beta=true",
            page=SyncPageCursor[BetaSpendLimit],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "page": page,
                    "scope_type": scope_type,
                },
            ),
            model=BetaSpendLimit,
        )

    def delete(
        self,
        spend_limit_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SpendLimitDeleteResponse:
        """
        Delete a spend limit.

        For a Claude Enterprise organization, this deletes a per-user override, and the
        member falls back to any inherited spend limit at that period. Its seat-tier,
        group, and organization-level rows cannot be deleted via this endpoint. A Claude
        Console organization deletes its organization and workspace limits. Deleting
        them through the API is in an early access preview.

        Args:
          spend_limit_id: ID of the Spend Limit.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not spend_limit_id:
            raise ValueError(f"Expected a non-empty value for `spend_limit_id` but received {spend_limit_id!r}")
        return self._delete(
            path_template("/v1/organizations/spend_limits/{spend_limit_id}?beta=true", spend_limit_id=spend_limit_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=SpendLimitDeleteResponse,
        )

    def set(
        self,
        *,
        amount: Optional[str],
        scope: spend_limit_set_params.Scope,
        period: BetaSpendLimitPeriod | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaSpendLimit:
        """
        Set a spend limit.

        Upsert keyed on (scope, period): setting a limit that already exists overwrites
        it in place. A Claude Enterprise organization sets `user` limits. Its seat-tier,
        group, and organization-level defaults are configured in claude.ai. A Claude
        Console organization sets `organization` and `workspace` limits, which are
        monthly and always carry an amount. Setting those limits is in an early access
        preview. To request access, contact your Anthropic account team.

        Args:
          amount: Limit amount as a non-negative integer decimal string in the minor unit of the
              organization's billing currency (cents for USD): "50000" is $500.00. `null` sets
              an explicit no-limit override for this scope and `period` only — each period
              resolves independently, so caps for other periods still apply.

          scope: What the limit applies to. Claude Enterprise organizations set `user` limits.
              Claude Console organizations set `organization` and `workspace` limits. Any
              other combination returns 400. Setting `organization` and `workspace` limits
              through the API is in an early access preview. To request access, contact your
              Anthropic account team.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._post(
            "/v1/organizations/spend_limits?beta=true",
            body={
                "amount": amount,
                "scope": scope,
                "period": period,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaSpendLimit,
        )


class AsyncSpendLimits(AsyncAPIResource):
    @cached_property
    def effective(self) -> AsyncEffective:
        return AsyncEffective(self._client)

    @cached_property
    def increase_requests(self) -> AsyncIncreaseRequests:
        return AsyncIncreaseRequests(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSpendLimitsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSpendLimitsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSpendLimitsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncSpendLimitsWithStreamingResponse(self)

    async def retrieve(
        self,
        spend_limit_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaSpendLimit:
        """
        Retrieve a spend limit by ID.

        Args:
          spend_limit_id: ID of the Spend Limit.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not spend_limit_id:
            raise ValueError(f"Expected a non-empty value for `spend_limit_id` but received {spend_limit_id!r}")
        return await self._get(
            path_template("/v1/organizations/spend_limits/{spend_limit_id}?beta=true", spend_limit_id=spend_limit_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaSpendLimit,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        scope_type: Optional[
            List[Literal["organization", "organization_service", "rbac_group", "seat_tier", "user", "workspace"]]
        ]
        | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaSpendLimit, AsyncPageCursor[BetaSpendLimit]]:
        """
        List the organization's spend limits.

        A Claude Console organization's limits come in an order that is stable across
        pages. A Claude Enterprise organization's are grouped by scope type, in the
        order `organization`, `seat_tier`, `rbac_group`, `organization_service`, `user`;
        within a type they come in a fixed order that is not creation order. Listing
        Claude Console limits is in an early access preview. To request access, contact
        your Anthropic account team.

        Args:
          limit: Maximum number of limits per page. Defaults to `20`.

          page: Opaque cursor from a previous response's `next_page` field.

          scope_type: Return only limits with these scope types. A Claude Console organization has
              `organization` and `workspace` limits; a Claude Enterprise organization has
              `organization`, `seat_tier`, `rbac_group`, `organization_service` and `user`
              limits. Omit for all.

          betas: This endpoint is in beta: requests must send `spend-limit-reads-2026-09-26` in
              this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["spend-limit-reads-2026-09-26"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "spend-limit-reads-2026-09-26", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/organizations/spend_limits?beta=true",
            page=AsyncPageCursor[BetaSpendLimit],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "page": page,
                    "scope_type": scope_type,
                },
            ),
            model=BetaSpendLimit,
        )

    async def delete(
        self,
        spend_limit_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SpendLimitDeleteResponse:
        """
        Delete a spend limit.

        For a Claude Enterprise organization, this deletes a per-user override, and the
        member falls back to any inherited spend limit at that period. Its seat-tier,
        group, and organization-level rows cannot be deleted via this endpoint. A Claude
        Console organization deletes its organization and workspace limits. Deleting
        them through the API is in an early access preview.

        Args:
          spend_limit_id: ID of the Spend Limit.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not spend_limit_id:
            raise ValueError(f"Expected a non-empty value for `spend_limit_id` but received {spend_limit_id!r}")
        return await self._delete(
            path_template("/v1/organizations/spend_limits/{spend_limit_id}?beta=true", spend_limit_id=spend_limit_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=SpendLimitDeleteResponse,
        )

    async def set(
        self,
        *,
        amount: Optional[str],
        scope: spend_limit_set_params.Scope,
        period: BetaSpendLimitPeriod | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaSpendLimit:
        """
        Set a spend limit.

        Upsert keyed on (scope, period): setting a limit that already exists overwrites
        it in place. A Claude Enterprise organization sets `user` limits. Its seat-tier,
        group, and organization-level defaults are configured in claude.ai. A Claude
        Console organization sets `organization` and `workspace` limits, which are
        monthly and always carry an amount. Setting those limits is in an early access
        preview. To request access, contact your Anthropic account team.

        Args:
          amount: Limit amount as a non-negative integer decimal string in the minor unit of the
              organization's billing currency (cents for USD): "50000" is $500.00. `null` sets
              an explicit no-limit override for this scope and `period` only — each period
              resolves independently, so caps for other periods still apply.

          scope: What the limit applies to. Claude Enterprise organizations set `user` limits.
              Claude Console organizations set `organization` and `workspace` limits. Any
              other combination returns 400. Setting `organization` and `workspace` limits
              through the API is in an early access preview. To request access, contact your
              Anthropic account team.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._post(
            "/v1/organizations/spend_limits?beta=true",
            body={
                "amount": amount,
                "scope": scope,
                "period": period,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaSpendLimit,
        )


class SpendLimitsWithRawResponse:
    def __init__(self, spend_limits: SpendLimits) -> None:
        self._spend_limits = spend_limits

        self.retrieve = to_raw_response_wrapper(
            spend_limits.retrieve,
        )
        self.list = to_raw_response_wrapper(
            spend_limits.list,
        )
        self.delete = to_raw_response_wrapper(
            spend_limits.delete,
        )
        self.set = to_raw_response_wrapper(
            spend_limits.set,
        )

    @cached_property
    def effective(self) -> EffectiveWithRawResponse:
        return EffectiveWithRawResponse(self._spend_limits.effective)

    @cached_property
    def increase_requests(self) -> IncreaseRequestsWithRawResponse:
        return IncreaseRequestsWithRawResponse(self._spend_limits.increase_requests)


class AsyncSpendLimitsWithRawResponse:
    def __init__(self, spend_limits: AsyncSpendLimits) -> None:
        self._spend_limits = spend_limits

        self.retrieve = async_to_raw_response_wrapper(
            spend_limits.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            spend_limits.list,
        )
        self.delete = async_to_raw_response_wrapper(
            spend_limits.delete,
        )
        self.set = async_to_raw_response_wrapper(
            spend_limits.set,
        )

    @cached_property
    def effective(self) -> AsyncEffectiveWithRawResponse:
        return AsyncEffectiveWithRawResponse(self._spend_limits.effective)

    @cached_property
    def increase_requests(self) -> AsyncIncreaseRequestsWithRawResponse:
        return AsyncIncreaseRequestsWithRawResponse(self._spend_limits.increase_requests)


class SpendLimitsWithStreamingResponse:
    def __init__(self, spend_limits: SpendLimits) -> None:
        self._spend_limits = spend_limits

        self.retrieve = to_streamed_response_wrapper(
            spend_limits.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            spend_limits.list,
        )
        self.delete = to_streamed_response_wrapper(
            spend_limits.delete,
        )
        self.set = to_streamed_response_wrapper(
            spend_limits.set,
        )

    @cached_property
    def effective(self) -> EffectiveWithStreamingResponse:
        return EffectiveWithStreamingResponse(self._spend_limits.effective)

    @cached_property
    def increase_requests(self) -> IncreaseRequestsWithStreamingResponse:
        return IncreaseRequestsWithStreamingResponse(self._spend_limits.increase_requests)


class AsyncSpendLimitsWithStreamingResponse:
    def __init__(self, spend_limits: AsyncSpendLimits) -> None:
        self._spend_limits = spend_limits

        self.retrieve = async_to_streamed_response_wrapper(
            spend_limits.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            spend_limits.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            spend_limits.delete,
        )
        self.set = async_to_streamed_response_wrapper(
            spend_limits.set,
        )

    @cached_property
    def effective(self) -> AsyncEffectiveWithStreamingResponse:
        return AsyncEffectiveWithStreamingResponse(self._spend_limits.effective)

    @cached_property
    def increase_requests(self) -> AsyncIncreaseRequestsWithStreamingResponse:
        return AsyncIncreaseRequestsWithStreamingResponse(self._spend_limits.increase_requests)
