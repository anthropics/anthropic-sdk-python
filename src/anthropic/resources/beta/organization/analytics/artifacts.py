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
from .....types.beta.organization.beta_analytics_artifact_activity import BetaAnalyticsArtifactActivity

__all__ = ["Artifacts", "AsyncArtifacts"]


class Artifacts(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ArtifactsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return ArtifactsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ArtifactsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return ArtifactsWithStreamingResponse(self)

    def list(
        self,
        *,
        date: Union[str, date],
        filter: Optional[SequenceNotStr[str]] | Omit = omit,
        group_by: Optional[List[Literal["product", "rbac_group_id", "user_id"]]] | Omit = omit,
        limit: Optional[int] | Omit = omit,
        page: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaAnalyticsArtifactActivity]:
        """
        Get artifact-creation activity for a given day, broken out by MIME type.

        Returns the full (`artifact_type`, `is_shared`) cube for the organization;
        `next_page` is null except for grouped queries, which paginate. The cube can be
        broken out per product, per member, or per RBAC group via `group_by[]`, and
        scoped via `filter[]`. Requires an API key with the `read:analytics` scope.

        Args:
          date: UTC date in YYYY-MM-DD format. The day to get artifact activity for. Data is
              typically available with a 1-day lag (varies by query; the error for a
              too-recent date names the latest available day) and may be revised by a few
              percent over the following days. No earlier than 2026-01-01.

          filter: Filters as `dimension:value`, e.g. `filter[]=rbac_group_id:{id}`. Repeat the
              param for OR within a dimension and across dimensions for AND. Supported
              dimensions on this endpoint: `artifact_type`, `is_shared`, `product`,
              `rbac_group_id`, `user_id`. Value forms: `artifact_type` is a canonical artifact
              MIME type (e.g. `text/markdown`) or `other`; `is_shared` is `true` or `false`;
              `product` is `chat`, `claude_code`, or `cowork` (the surfaces that create
              artifacts); `rbac_group_id` takes the tagged id (`rbac_group_...`, as emitted in
              responses and by the spend-limits API) or a bare group UUID, and matches users
              who held the group at any point during each covered UTC day (time-of-usage
              attribution); `user_id` takes a tagged user id (`user_...`), as emitted in
              responses. An unsupported dimension returns 400. At most 100 entries.

          group_by: Dimensions to break results out by: `product`, `user_id` and/or `rbac_group_id`.
              The ungrouped artifact-type cube is finite and returned in full; grouped queries
              multiply the cube and paginate via `next_page`. `product` takes the values
              `chat`, `claude_code`, or `cowork` (the surfaces that create artifacts).
              `rbac_group_id` attributes a user to every group they held at any point during
              the requested UTC day, so grouped rows are not an exclusive partition. At most
              100 entries.

          limit: Maximum rows to return (1-1000, default 100). The ungrouped artifact-type cube
              is finite and returned in full; `limit` is the page size only when `group_by[]`
              multiplies the cube.

          page: Opaque cursor from a previous response's `next_page` field. Only valid with
              `group_by[]` — the ungrouped cube is never paginated.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/analytics/artifacts?beta=true",
            page=SyncPageCursor[BetaAnalyticsArtifactActivity],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "date": date,
                    "filter": filter,
                    "group_by": group_by,
                    "limit": limit,
                    "page": page,
                },
            ),
            model=BetaAnalyticsArtifactActivity,
        )


class AsyncArtifacts(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncArtifactsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncArtifactsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncArtifactsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncArtifactsWithStreamingResponse(self)

    def list(
        self,
        *,
        date: Union[str, date],
        filter: Optional[SequenceNotStr[str]] | Omit = omit,
        group_by: Optional[List[Literal["product", "rbac_group_id", "user_id"]]] | Omit = omit,
        limit: Optional[int] | Omit = omit,
        page: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaAnalyticsArtifactActivity, AsyncPageCursor[BetaAnalyticsArtifactActivity]]:
        """
        Get artifact-creation activity for a given day, broken out by MIME type.

        Returns the full (`artifact_type`, `is_shared`) cube for the organization;
        `next_page` is null except for grouped queries, which paginate. The cube can be
        broken out per product, per member, or per RBAC group via `group_by[]`, and
        scoped via `filter[]`. Requires an API key with the `read:analytics` scope.

        Args:
          date: UTC date in YYYY-MM-DD format. The day to get artifact activity for. Data is
              typically available with a 1-day lag (varies by query; the error for a
              too-recent date names the latest available day) and may be revised by a few
              percent over the following days. No earlier than 2026-01-01.

          filter: Filters as `dimension:value`, e.g. `filter[]=rbac_group_id:{id}`. Repeat the
              param for OR within a dimension and across dimensions for AND. Supported
              dimensions on this endpoint: `artifact_type`, `is_shared`, `product`,
              `rbac_group_id`, `user_id`. Value forms: `artifact_type` is a canonical artifact
              MIME type (e.g. `text/markdown`) or `other`; `is_shared` is `true` or `false`;
              `product` is `chat`, `claude_code`, or `cowork` (the surfaces that create
              artifacts); `rbac_group_id` takes the tagged id (`rbac_group_...`, as emitted in
              responses and by the spend-limits API) or a bare group UUID, and matches users
              who held the group at any point during each covered UTC day (time-of-usage
              attribution); `user_id` takes a tagged user id (`user_...`), as emitted in
              responses. An unsupported dimension returns 400. At most 100 entries.

          group_by: Dimensions to break results out by: `product`, `user_id` and/or `rbac_group_id`.
              The ungrouped artifact-type cube is finite and returned in full; grouped queries
              multiply the cube and paginate via `next_page`. `product` takes the values
              `chat`, `claude_code`, or `cowork` (the surfaces that create artifacts).
              `rbac_group_id` attributes a user to every group they held at any point during
              the requested UTC day, so grouped rows are not an exclusive partition. At most
              100 entries.

          limit: Maximum rows to return (1-1000, default 100). The ungrouped artifact-type cube
              is finite and returned in full; `limit` is the page size only when `group_by[]`
              multiplies the cube.

          page: Opaque cursor from a previous response's `next_page` field. Only valid with
              `group_by[]` — the ungrouped cube is never paginated.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/analytics/artifacts?beta=true",
            page=AsyncPageCursor[BetaAnalyticsArtifactActivity],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "date": date,
                    "filter": filter,
                    "group_by": group_by,
                    "limit": limit,
                    "page": page,
                },
            ),
            model=BetaAnalyticsArtifactActivity,
        )


class ArtifactsWithRawResponse:
    def __init__(self, artifacts: Artifacts) -> None:
        self._artifacts = artifacts

        self.list = to_raw_response_wrapper(
            artifacts.list,
        )


class AsyncArtifactsWithRawResponse:
    def __init__(self, artifacts: AsyncArtifacts) -> None:
        self._artifacts = artifacts

        self.list = async_to_raw_response_wrapper(
            artifacts.list,
        )


class ArtifactsWithStreamingResponse:
    def __init__(self, artifacts: Artifacts) -> None:
        self._artifacts = artifacts

        self.list = to_streamed_response_wrapper(
            artifacts.list,
        )


class AsyncArtifactsWithStreamingResponse:
    def __init__(self, artifacts: AsyncArtifacts) -> None:
        self._artifacts = artifacts

        self.list = async_to_streamed_response_wrapper(
            artifacts.list,
        )
