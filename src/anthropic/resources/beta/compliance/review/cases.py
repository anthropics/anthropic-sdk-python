from __future__ import annotations

from typing import List, Union, Iterable
from datetime import datetime

import httpx2

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
from .....types.beta.compliance import BetaComplianceReviewOrder
from .....types.anthropic_beta_param import AnthropicBetaParam
from .....types.beta.compliance.review import (
    BetaComplianceReviewCaseOrderBy,
    BetaComplianceReviewDetermination,
    BetaComplianceReviewCaseStatusFilter,
)
from .....types.beta.compliance.beta_compliance_review_order import BetaComplianceReviewOrder
from .....types.beta.compliance.review.beta_compliance_review_case import BetaComplianceReviewCase
from .....types.beta.compliance.review.beta_compliance_review_case_order_by import BetaComplianceReviewCaseOrderBy
from .....types.beta.compliance.review.beta_compliance_review_determination import BetaComplianceReviewDetermination
from .....types.beta.compliance.review.beta_compliance_review_verdict_param import BetaComplianceReviewVerdictParam
from .....types.beta.compliance.review.beta_compliance_review_case_status_filter import (
    BetaComplianceReviewCaseStatusFilter,
)
from .....types.beta.compliance.review.beta_compliance_review_violated_policy_category import (
    BetaComplianceReviewViolatedPolicyCategory,
)

__all__ = ["Cases", "AsyncCases"]


class Cases(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CasesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return CasesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CasesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return CasesWithStreamingResponse(self)

    def retrieve(
        self,
        case_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaComplianceReviewCase:
        """
        Read one review case.

        A case that the API key can't reach, or that Anthropic hasn't sent, returns the
        same 404 as a case that doesn't exist.

        An Admin API key with the `read:compliance_review_cases` scope can call this
        endpoint.

        Args:
          case_id: The ID of the case (`rvc_...`).

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not case_id:
            raise ValueError(f"Expected a non-empty value for `case_id` but received {case_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._get(
            path_template("/v1/compliance/review/cases/{case_id}", case_id=case_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.compliance.review.cases.retrieve",
                span_route="/v1/compliance/review/cases/{case_id}",
                span_attributes={"anthropic.compliance.review.case.id": case_id},
            ),
            cast_to=BetaComplianceReviewCase,
        )

    def list(
        self,
        *,
        created_at_gt: Union[str, datetime] | Omit = omit,
        created_at_gte: Union[str, datetime] | Omit = omit,
        created_at_lt: Union[str, datetime] | Omit = omit,
        created_at_lte: Union[str, datetime] | Omit = omit,
        limit: int | Omit = omit,
        order: BetaComplianceReviewOrder | Omit = omit,
        order_by: BetaComplianceReviewCaseOrderBy | Omit = omit,
        page: str | Omit = omit,
        status: BetaComplianceReviewCaseStatusFilter | Omit = omit,
        updated_at_gt: Union[str, datetime] | Omit = omit,
        updated_at_gte: Union[str, datetime] | Omit = omit,
        updated_at_lt: Union[str, datetime] | Omit = omit,
        updated_at_lte: Union[str, datetime] | Omit = omit,
        user_profile_id: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaComplianceReviewCase]:
        """
        List the review cases of every organization that the API key can reach, newest
        first by default. Both open and closed cases are returned unless `status` is
        set.

        To sync, store the largest `updated_at` you have read, and send it as the
        at-or-after filter on `updated_at`, sorted by `updated_at` ascending. That finds
        new cases, newly closed cases, and cases with a new notice. Read every page,
        match results by `id`, and store the new largest value after the last page.

        A request with the `anthropic-user-profile-id` header and no `user_profile_id`
        parameter returns a 400 error.

        An Admin API key with the `read:compliance_review_cases` scope can call this
        endpoint.

        Args:
          created_at_gt: Return only cases whose `created_at` is after this time.

          created_at_gte: Return only cases whose `created_at` is at or after this time.

          created_at_lt: Return only cases whose `created_at` is before this time.

          created_at_lte: Return only cases whose `created_at` is at or before this time.

          limit: Number of cases to return per page, between 1 and 100. Defaults to 20.

          order: Sort direction, by `order_by` and then by `id`. Defaults to `desc`.

          order_by: The field to sort by. Defaults to `created_at`.

          page: Opaque cursor from a previous response's `next_page`. Leave it out to get the
              first page. A cursor works only with the filters and sort order of the request
              that returned it.

          status: Return only cases with this status. Leave it out to get both open and closed
              cases.

          updated_at_gt: Return only cases whose `updated_at` is after this time.

          updated_at_gte: Return cases whose `updated_at` is at or after this time. Cases slightly older
              than this time are also returned, so that a sync misses no change.

          updated_at_lt: Return only cases whose `updated_at` is before this time.

          updated_at_lte: Return only cases whose `updated_at` is at or before this time.

          user_profile_id: Return only cases where a message's `user_profile_id` is this ID, including
              cases that also have messages of other user profiles. A case stops matching once
              its messages' `user_profile_id` is null. An ID that matches no reachable case
              returns no cases. A request that sends the `anthropic-user-profile-id` header
              without this parameter returns a 400 error.

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
        return self._get_api_list(
            "/v1/compliance/review/cases",
            page=SyncPageCursor[BetaComplianceReviewCase],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "created_at[gt]": created_at_gt,
                    "created_at[gte]": created_at_gte,
                    "created_at[lt]": created_at_lt,
                    "created_at[lte]": created_at_lte,
                    "limit": limit,
                    "order": order,
                    "order_by": order_by,
                    "page": page,
                    "status": status,
                    "updated_at[gt]": updated_at_gt,
                    "updated_at[gte]": updated_at_gte,
                    "updated_at[lt]": updated_at_lt,
                    "updated_at[lte]": updated_at_lte,
                    "user_profile_id": user_profile_id,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.compliance.review.cases.list",
                span_route="/v1/compliance/review/cases",
            ),
            model=BetaComplianceReviewCase,
        )

    def respond(
        self,
        case_id: str,
        *,
        determination: BetaComplianceReviewDetermination,
        policy_categories: List[BetaComplianceReviewViolatedPolicyCategory] | Omit = omit,
        verdicts: Iterable[BetaComplianceReviewVerdictParam] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaComplianceReviewCase:
        """Send your conclusion on a review case.

        A response closes the case, and a closed
        case can't be reopened.

        Only the first response counts. A request is safe to send again: if the closed
        case has a response with the same field values, in any list order, the API
        returns 200 and changes nothing. If the closed case has a different response, or
        none, the API returns a 400 with `case_closed` in `error.details.error_code`.

        If your end customer reviews this case instead of you, the API returns a 403
        with `case_reviewed_by_end_customer` in `error.details.error_code`.

        An Admin API key with the `write:compliance_review_cases` scope can call this
        endpoint.

        Args:
          case_id: The ID of the case (`rvc_...`).

          determination: Your conclusion on the case as a whole. Anthropic doesn't check it against
              `verdicts`.

          policy_categories: The policy categories that you found were violated. Send one to four with
              `violation`, and none with `no_violation`. They need not match the case's own.
              Each value is one of `cyber`, `bio`, `chem`, `radnuc` (radiological or nuclear
              weapons), `cgw` (conventional weapons), `mgw` (military-grade weapons systems),
              `io` (influence operations), `fraud`, `violent_extremism`, `surveillance`,
              `human_exploitation`, `self_harm`, `adult_content`, `reasoning_extraction`,
              `frontier_llm` (use of the model to accelerate frontier AI research and
              development in restricted ways), `compromised_key` or `other`, and can appear
              once.

          verdicts: Your conclusions on individual messages of the case. They need not cover every
              message, and each `item_id` can appear once.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not case_id:
            raise ValueError(f"Expected a non-empty value for `case_id` but received {case_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._post(
            path_template("/v1/compliance/review/cases/{case_id}/respond", case_id=case_id),
            body={
                "determination": determination,
                "policy_categories": policy_categories,
                "verdicts": verdicts,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.compliance.review.cases.respond",
                span_route="/v1/compliance/review/cases/{case_id}/respond",
                span_attributes={"anthropic.compliance.review.case.id": case_id},
            ),
            cast_to=BetaComplianceReviewCase,
        )


class AsyncCases(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCasesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncCasesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCasesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncCasesWithStreamingResponse(self)

    async def retrieve(
        self,
        case_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaComplianceReviewCase:
        """
        Read one review case.

        A case that the API key can't reach, or that Anthropic hasn't sent, returns the
        same 404 as a case that doesn't exist.

        An Admin API key with the `read:compliance_review_cases` scope can call this
        endpoint.

        Args:
          case_id: The ID of the case (`rvc_...`).

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not case_id:
            raise ValueError(f"Expected a non-empty value for `case_id` but received {case_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._get(
            path_template("/v1/compliance/review/cases/{case_id}", case_id=case_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.compliance.review.cases.retrieve",
                span_route="/v1/compliance/review/cases/{case_id}",
                span_attributes={"anthropic.compliance.review.case.id": case_id},
            ),
            cast_to=BetaComplianceReviewCase,
        )

    def list(
        self,
        *,
        created_at_gt: Union[str, datetime] | Omit = omit,
        created_at_gte: Union[str, datetime] | Omit = omit,
        created_at_lt: Union[str, datetime] | Omit = omit,
        created_at_lte: Union[str, datetime] | Omit = omit,
        limit: int | Omit = omit,
        order: BetaComplianceReviewOrder | Omit = omit,
        order_by: BetaComplianceReviewCaseOrderBy | Omit = omit,
        page: str | Omit = omit,
        status: BetaComplianceReviewCaseStatusFilter | Omit = omit,
        updated_at_gt: Union[str, datetime] | Omit = omit,
        updated_at_gte: Union[str, datetime] | Omit = omit,
        updated_at_lt: Union[str, datetime] | Omit = omit,
        updated_at_lte: Union[str, datetime] | Omit = omit,
        user_profile_id: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaComplianceReviewCase, AsyncPageCursor[BetaComplianceReviewCase]]:
        """
        List the review cases of every organization that the API key can reach, newest
        first by default. Both open and closed cases are returned unless `status` is
        set.

        To sync, store the largest `updated_at` you have read, and send it as the
        at-or-after filter on `updated_at`, sorted by `updated_at` ascending. That finds
        new cases, newly closed cases, and cases with a new notice. Read every page,
        match results by `id`, and store the new largest value after the last page.

        A request with the `anthropic-user-profile-id` header and no `user_profile_id`
        parameter returns a 400 error.

        An Admin API key with the `read:compliance_review_cases` scope can call this
        endpoint.

        Args:
          created_at_gt: Return only cases whose `created_at` is after this time.

          created_at_gte: Return only cases whose `created_at` is at or after this time.

          created_at_lt: Return only cases whose `created_at` is before this time.

          created_at_lte: Return only cases whose `created_at` is at or before this time.

          limit: Number of cases to return per page, between 1 and 100. Defaults to 20.

          order: Sort direction, by `order_by` and then by `id`. Defaults to `desc`.

          order_by: The field to sort by. Defaults to `created_at`.

          page: Opaque cursor from a previous response's `next_page`. Leave it out to get the
              first page. A cursor works only with the filters and sort order of the request
              that returned it.

          status: Return only cases with this status. Leave it out to get both open and closed
              cases.

          updated_at_gt: Return only cases whose `updated_at` is after this time.

          updated_at_gte: Return cases whose `updated_at` is at or after this time. Cases slightly older
              than this time are also returned, so that a sync misses no change.

          updated_at_lt: Return only cases whose `updated_at` is before this time.

          updated_at_lte: Return only cases whose `updated_at` is at or before this time.

          user_profile_id: Return only cases where a message's `user_profile_id` is this ID, including
              cases that also have messages of other user profiles. A case stops matching once
              its messages' `user_profile_id` is null. An ID that matches no reachable case
              returns no cases. A request that sends the `anthropic-user-profile-id` header
              without this parameter returns a 400 error.

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
        return self._get_api_list(
            "/v1/compliance/review/cases",
            page=AsyncPageCursor[BetaComplianceReviewCase],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "created_at[gt]": created_at_gt,
                    "created_at[gte]": created_at_gte,
                    "created_at[lt]": created_at_lt,
                    "created_at[lte]": created_at_lte,
                    "limit": limit,
                    "order": order,
                    "order_by": order_by,
                    "page": page,
                    "status": status,
                    "updated_at[gt]": updated_at_gt,
                    "updated_at[gte]": updated_at_gte,
                    "updated_at[lt]": updated_at_lt,
                    "updated_at[lte]": updated_at_lte,
                    "user_profile_id": user_profile_id,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.compliance.review.cases.list",
                span_route="/v1/compliance/review/cases",
            ),
            model=BetaComplianceReviewCase,
        )

    async def respond(
        self,
        case_id: str,
        *,
        determination: BetaComplianceReviewDetermination,
        policy_categories: List[BetaComplianceReviewViolatedPolicyCategory] | Omit = omit,
        verdicts: Iterable[BetaComplianceReviewVerdictParam] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaComplianceReviewCase:
        """Send your conclusion on a review case.

        A response closes the case, and a closed
        case can't be reopened.

        Only the first response counts. A request is safe to send again: if the closed
        case has a response with the same field values, in any list order, the API
        returns 200 and changes nothing. If the closed case has a different response, or
        none, the API returns a 400 with `case_closed` in `error.details.error_code`.

        If your end customer reviews this case instead of you, the API returns a 403
        with `case_reviewed_by_end_customer` in `error.details.error_code`.

        An Admin API key with the `write:compliance_review_cases` scope can call this
        endpoint.

        Args:
          case_id: The ID of the case (`rvc_...`).

          determination: Your conclusion on the case as a whole. Anthropic doesn't check it against
              `verdicts`.

          policy_categories: The policy categories that you found were violated. Send one to four with
              `violation`, and none with `no_violation`. They need not match the case's own.
              Each value is one of `cyber`, `bio`, `chem`, `radnuc` (radiological or nuclear
              weapons), `cgw` (conventional weapons), `mgw` (military-grade weapons systems),
              `io` (influence operations), `fraud`, `violent_extremism`, `surveillance`,
              `human_exploitation`, `self_harm`, `adult_content`, `reasoning_extraction`,
              `frontier_llm` (use of the model to accelerate frontier AI research and
              development in restricted ways), `compromised_key` or `other`, and can appear
              once.

          verdicts: Your conclusions on individual messages of the case. They need not cover every
              message, and each `item_id` can appear once.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not case_id:
            raise ValueError(f"Expected a non-empty value for `case_id` but received {case_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._post(
            path_template("/v1/compliance/review/cases/{case_id}/respond", case_id=case_id),
            body={
                "determination": determination,
                "policy_categories": policy_categories,
                "verdicts": verdicts,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.compliance.review.cases.respond",
                span_route="/v1/compliance/review/cases/{case_id}/respond",
                span_attributes={"anthropic.compliance.review.case.id": case_id},
            ),
            cast_to=BetaComplianceReviewCase,
        )


class CasesWithRawResponse:
    def __init__(self, cases: Cases) -> None:
        self._cases = cases

        self.retrieve = to_raw_response_wrapper(
            cases.retrieve,
        )
        self.list = to_raw_response_wrapper(
            cases.list,
        )
        self.respond = to_raw_response_wrapper(
            cases.respond,
        )


class AsyncCasesWithRawResponse:
    def __init__(self, cases: AsyncCases) -> None:
        self._cases = cases

        self.retrieve = async_to_raw_response_wrapper(
            cases.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            cases.list,
        )
        self.respond = async_to_raw_response_wrapper(
            cases.respond,
        )


class CasesWithStreamingResponse:
    def __init__(self, cases: Cases) -> None:
        self._cases = cases

        self.retrieve = to_streamed_response_wrapper(
            cases.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            cases.list,
        )
        self.respond = to_streamed_response_wrapper(
            cases.respond,
        )


class AsyncCasesWithStreamingResponse:
    def __init__(self, cases: AsyncCases) -> None:
        self._cases = cases

        self.retrieve = async_to_streamed_response_wrapper(
            cases.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            cases.list,
        )
        self.respond = async_to_streamed_response_wrapper(
            cases.respond,
        )
