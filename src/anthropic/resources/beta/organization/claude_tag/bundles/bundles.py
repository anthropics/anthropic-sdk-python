from __future__ import annotations

from typing import List
from itertools import chain

import httpx2

from .targets import (
    Targets,
    AsyncTargets,
    TargetsWithRawResponse,
    AsyncTargetsWithRawResponse,
    TargetsWithStreamingResponse,
    AsyncTargetsWithStreamingResponse,
)
from ......_types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ......_utils import is_given, path_template, strip_not_given
from ......_compat import cached_property
from ......_resource import SyncAPIResource, AsyncAPIResource
from ......_response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ......pagination import SyncPageCursor, AsyncPageCursor
from ......_base_client import AsyncPaginator, make_request_options
from ......types.anthropic_beta_param import AnthropicBetaParam
from ......types.beta.organization.claude_tag.beta_claude_tag_bundle import BetaClaudeTagBundle

__all__ = ["Bundles", "AsyncBundles"]


class Bundles(SyncAPIResource):
    @cached_property
    def targets(self) -> Targets:
        return Targets(self._client)

    @cached_property
    def with_raw_response(self) -> BundlesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return BundlesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BundlesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return BundlesWithStreamingResponse(self)

    def retrieve(
        self,
        bundle_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeTagBundle:
        """Get one Bundle.

        What the Bundle grants (connectors, repositories and
        credentials) is never returned.

        Args:
          bundle_id: The Bundle's identifier, starting with `capp_`.

          betas: This endpoint is in beta: requests must send
              `experimental-claude-tag-2026-10-21` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bundle_id:
            raise ValueError(f"Expected a non-empty value for `bundle_id` but received {bundle_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["experimental-claude-tag-2026-10-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "experimental-claude-tag-2026-10-21", **(extra_headers or {})}
        return self._get(
            path_template("/v1/organizations/claude_tag/bundles/{bundle_id}", bundle_id=bundle_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.bundles.retrieve",
                span_route="/v1/organizations/claude_tag/bundles/{bundle_id}",
                span_attributes={"anthropic.organization.claude_tag.bundle.id": bundle_id},
            ),
            cast_to=BetaClaudeTagBundle,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaClaudeTagBundle]:
        """List the organization's Bundles, newest first by `created_at`.

        A Bundle that
        Claude Tag manages for itself is not listed.

        Args:
          limit: Number of items to return per page, between 1 and 100. Defaults to 20.

          page: Opaque cursor from a previous response's `next_page`.

          betas: This endpoint is in beta: requests must send
              `experimental-claude-tag-2026-10-21` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["experimental-claude-tag-2026-10-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "experimental-claude-tag-2026-10-21", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/organizations/claude_tag/bundles",
            page=SyncPageCursor[BetaClaudeTagBundle],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "page": page,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.bundles.list",
                span_route="/v1/organizations/claude_tag/bundles",
            ),
            model=BetaClaudeTagBundle,
        )


class AsyncBundles(AsyncAPIResource):
    @cached_property
    def targets(self) -> AsyncTargets:
        return AsyncTargets(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncBundlesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncBundlesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBundlesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncBundlesWithStreamingResponse(self)

    async def retrieve(
        self,
        bundle_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaClaudeTagBundle:
        """Get one Bundle.

        What the Bundle grants (connectors, repositories and
        credentials) is never returned.

        Args:
          bundle_id: The Bundle's identifier, starting with `capp_`.

          betas: This endpoint is in beta: requests must send
              `experimental-claude-tag-2026-10-21` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bundle_id:
            raise ValueError(f"Expected a non-empty value for `bundle_id` but received {bundle_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["experimental-claude-tag-2026-10-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "experimental-claude-tag-2026-10-21", **(extra_headers or {})}
        return await self._get(
            path_template("/v1/organizations/claude_tag/bundles/{bundle_id}", bundle_id=bundle_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.bundles.retrieve",
                span_route="/v1/organizations/claude_tag/bundles/{bundle_id}",
                span_attributes={"anthropic.organization.claude_tag.bundle.id": bundle_id},
            ),
            cast_to=BetaClaudeTagBundle,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaClaudeTagBundle, AsyncPageCursor[BetaClaudeTagBundle]]:
        """List the organization's Bundles, newest first by `created_at`.

        A Bundle that
        Claude Tag manages for itself is not listed.

        Args:
          limit: Number of items to return per page, between 1 and 100. Defaults to 20.

          page: Opaque cursor from a previous response's `next_page`.

          betas: This endpoint is in beta: requests must send
              `experimental-claude-tag-2026-10-21` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["experimental-claude-tag-2026-10-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "experimental-claude-tag-2026-10-21", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/organizations/claude_tag/bundles",
            page=AsyncPageCursor[BetaClaudeTagBundle],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "page": page,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.claude_tag.bundles.list",
                span_route="/v1/organizations/claude_tag/bundles",
            ),
            model=BetaClaudeTagBundle,
        )


class BundlesWithRawResponse:
    def __init__(self, bundles: Bundles) -> None:
        self._bundles = bundles

        self.retrieve = to_raw_response_wrapper(
            bundles.retrieve,
        )
        self.list = to_raw_response_wrapper(
            bundles.list,
        )

    @cached_property
    def targets(self) -> TargetsWithRawResponse:
        return TargetsWithRawResponse(self._bundles.targets)


class AsyncBundlesWithRawResponse:
    def __init__(self, bundles: AsyncBundles) -> None:
        self._bundles = bundles

        self.retrieve = async_to_raw_response_wrapper(
            bundles.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            bundles.list,
        )

    @cached_property
    def targets(self) -> AsyncTargetsWithRawResponse:
        return AsyncTargetsWithRawResponse(self._bundles.targets)


class BundlesWithStreamingResponse:
    def __init__(self, bundles: Bundles) -> None:
        self._bundles = bundles

        self.retrieve = to_streamed_response_wrapper(
            bundles.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            bundles.list,
        )

    @cached_property
    def targets(self) -> TargetsWithStreamingResponse:
        return TargetsWithStreamingResponse(self._bundles.targets)


class AsyncBundlesWithStreamingResponse:
    def __init__(self, bundles: AsyncBundles) -> None:
        self._bundles = bundles

        self.retrieve = async_to_streamed_response_wrapper(
            bundles.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            bundles.list,
        )

    @cached_property
    def targets(self) -> AsyncTargetsWithStreamingResponse:
        return AsyncTargetsWithStreamingResponse(self._bundles.targets)
