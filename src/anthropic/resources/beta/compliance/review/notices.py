from __future__ import annotations

from typing import List, Union
from datetime import datetime

import httpx2

from ....._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ....._utils import is_given, strip_not_given
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
from .....types.beta.compliance.beta_compliance_review_order import BetaComplianceReviewOrder
from .....types.beta.compliance.review.beta_compliance_review_notice import BetaComplianceReviewNotice

__all__ = ["Notices", "AsyncNotices"]


class Notices(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> NoticesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return NoticesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> NoticesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return NoticesWithStreamingResponse(self)

    def list(
        self,
        *,
        case_id: str | Omit = omit,
        created_at_gt: Union[str, datetime] | Omit = omit,
        created_at_gte: Union[str, datetime] | Omit = omit,
        created_at_lt: Union[str, datetime] | Omit = omit,
        created_at_lte: Union[str, datetime] | Omit = omit,
        limit: int | Omit = omit,
        order: BetaComplianceReviewOrder | Omit = omit,
        page: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaComplianceReviewNotice]:
        """
        List Anthropic's notices to the organizations that the API key can reach, newest
        first by default. A notice is returned only if the API key can read every case
        in its `case_ids`.

        To poll, store the largest `created_at` you have read, and send it as the
        at-or-after filter on `created_at`. Read every page, match results by `id`, and
        store the new largest value after the last page.

        An Admin API key with the `read:compliance_review_cases` scope can call this
        endpoint.

        Args:
          case_id: Return only notices whose `case_ids` include this case (`rvc_...`). A case that
              the API key can't read returns an empty list.

          created_at_gt: Return only notices whose `created_at` is after this time.

          created_at_gte: Return notices whose `created_at` is at or after this time. Notices slightly
              older than this time are also returned, so that a poll misses no notice.

          created_at_lt: Return only notices whose `created_at` is before this time.

          created_at_lte: Return only notices whose `created_at` is at or before this time.

          limit: Number of notices to return per page, between 1 and 100. Defaults to 20.

          order: Sort direction, by `created_at` and then by `id`. Defaults to `desc`.

          page: Opaque cursor from a previous response's `next_page`. Leave it out to get the
              first page. A cursor works only with the filters and sort order of the request
              that returned it.

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
            "/v1/compliance/review/notices",
            page=SyncPageCursor[BetaComplianceReviewNotice],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "case_id": case_id,
                    "created_at[gt]": created_at_gt,
                    "created_at[gte]": created_at_gte,
                    "created_at[lt]": created_at_lt,
                    "created_at[lte]": created_at_lte,
                    "limit": limit,
                    "order": order,
                    "page": page,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.compliance.review.notices.list",
                span_route="/v1/compliance/review/notices",
            ),
            model=BetaComplianceReviewNotice,
        )


class AsyncNotices(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncNoticesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncNoticesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncNoticesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncNoticesWithStreamingResponse(self)

    def list(
        self,
        *,
        case_id: str | Omit = omit,
        created_at_gt: Union[str, datetime] | Omit = omit,
        created_at_gte: Union[str, datetime] | Omit = omit,
        created_at_lt: Union[str, datetime] | Omit = omit,
        created_at_lte: Union[str, datetime] | Omit = omit,
        limit: int | Omit = omit,
        order: BetaComplianceReviewOrder | Omit = omit,
        page: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaComplianceReviewNotice, AsyncPageCursor[BetaComplianceReviewNotice]]:
        """
        List Anthropic's notices to the organizations that the API key can reach, newest
        first by default. A notice is returned only if the API key can read every case
        in its `case_ids`.

        To poll, store the largest `created_at` you have read, and send it as the
        at-or-after filter on `created_at`. Read every page, match results by `id`, and
        store the new largest value after the last page.

        An Admin API key with the `read:compliance_review_cases` scope can call this
        endpoint.

        Args:
          case_id: Return only notices whose `case_ids` include this case (`rvc_...`). A case that
              the API key can't read returns an empty list.

          created_at_gt: Return only notices whose `created_at` is after this time.

          created_at_gte: Return notices whose `created_at` is at or after this time. Notices slightly
              older than this time are also returned, so that a poll misses no notice.

          created_at_lt: Return only notices whose `created_at` is before this time.

          created_at_lte: Return only notices whose `created_at` is at or before this time.

          limit: Number of notices to return per page, between 1 and 100. Defaults to 20.

          order: Sort direction, by `created_at` and then by `id`. Defaults to `desc`.

          page: Opaque cursor from a previous response's `next_page`. Leave it out to get the
              first page. A cursor works only with the filters and sort order of the request
              that returned it.

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
            "/v1/compliance/review/notices",
            page=AsyncPageCursor[BetaComplianceReviewNotice],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "case_id": case_id,
                    "created_at[gt]": created_at_gt,
                    "created_at[gte]": created_at_gte,
                    "created_at[lt]": created_at_lt,
                    "created_at[lte]": created_at_lte,
                    "limit": limit,
                    "order": order,
                    "page": page,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.compliance.review.notices.list",
                span_route="/v1/compliance/review/notices",
            ),
            model=BetaComplianceReviewNotice,
        )


class NoticesWithRawResponse:
    def __init__(self, notices: Notices) -> None:
        self._notices = notices

        self.list = to_raw_response_wrapper(
            notices.list,
        )


class AsyncNoticesWithRawResponse:
    def __init__(self, notices: AsyncNotices) -> None:
        self._notices = notices

        self.list = async_to_raw_response_wrapper(
            notices.list,
        )


class NoticesWithStreamingResponse:
    def __init__(self, notices: Notices) -> None:
        self._notices = notices

        self.list = to_streamed_response_wrapper(
            notices.list,
        )


class AsyncNoticesWithStreamingResponse:
    def __init__(self, notices: AsyncNotices) -> None:
        self._notices = notices

        self.list = async_to_streamed_response_wrapper(
            notices.list,
        )
