# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from datetime import datetime
from itertools import chain

import httpx

from ... import _legacy_response
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import is_given, path_template, maybe_transform, strip_not_given, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...pagination import SyncPageCursor, AsyncPageCursor
from ...types.beta import dream_list_params, dream_create_params
from ..._base_client import AsyncPaginator, make_request_options
from ...types.beta.beta_dream import BetaDream
from ...types.anthropic_beta_param import AnthropicBetaParam
from ...types.beta.beta_dream_status import BetaDreamStatus
from ...types.beta.beta_dream_input_param import BetaDreamInputParam

__all__ = ["Dreams", "AsyncDreams"]


class Dreams(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DreamsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return DreamsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DreamsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return DreamsWithStreamingResponse(self)

    def create(
        self,
        *,
        inputs: Iterable[BetaDreamInputParam],
        model: dream_create_params.Model,
        instructions: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaDream:
        """
        Create a Dream

        Args:
          model: Model identifier and configuration applied to every pipeline stage.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return self._post(
            "/v1/dreams?beta=true",
            body=maybe_transform(
                {
                    "inputs": inputs,
                    "model": model,
                    "instructions": instructions,
                },
                dream_create_params.DreamCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaDream,
        )

    def retrieve(
        self,
        dream_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaDream:
        """
        Get a Dream

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dream_id:
            raise ValueError(f"Expected a non-empty value for `dream_id` but received {dream_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return self._get(
            path_template("/v1/dreams/{dream_id}?beta=true", dream_id=dream_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaDream,
        )

    def list(
        self,
        *,
        created_at_gt: Union[str, datetime] | Omit = omit,
        created_at_lt: Union[str, datetime] | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        statuses: List[BetaDreamStatus] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaDream]:
        """
        List Dreams

        Args:
          created_at_gt: Return dreams with `created_at` strictly after this timestamp (exclusive lower
              bound, RFC 3339). Unset applies no lower bound.

          created_at_lt: Return dreams with `created_at` strictly before this timestamp (exclusive upper
              bound, RFC 3339). Unset applies no upper bound.

          include_archived: Query parameter for include_archived

          limit: Query parameter for limit

          page: Query parameter for page

          statuses: Filter by lifecycle status. Repeat the parameter to match any of multiple
              statuses. Empty applies no status filter.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/dreams?beta=true",
            page=SyncPageCursor[BetaDream],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "created_at_gt": created_at_gt,
                        "created_at_lt": created_at_lt,
                        "include_archived": include_archived,
                        "limit": limit,
                        "page": page,
                        "statuses": statuses,
                    },
                    dream_list_params.DreamListParams,
                ),
            ),
            model=BetaDream,
        )

    def archive(
        self,
        dream_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaDream:
        """
        Archive a Dream

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dream_id:
            raise ValueError(f"Expected a non-empty value for `dream_id` but received {dream_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return self._post(
            path_template("/v1/dreams/{dream_id}/archive?beta=true", dream_id=dream_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaDream,
        )

    def cancel(
        self,
        dream_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaDream:
        """
        Cancel a Dream

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dream_id:
            raise ValueError(f"Expected a non-empty value for `dream_id` but received {dream_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return self._post(
            path_template("/v1/dreams/{dream_id}/cancel?beta=true", dream_id=dream_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaDream,
        )


class AsyncDreams(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDreamsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDreamsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDreamsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncDreamsWithStreamingResponse(self)

    async def create(
        self,
        *,
        inputs: Iterable[BetaDreamInputParam],
        model: dream_create_params.Model,
        instructions: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaDream:
        """
        Create a Dream

        Args:
          model: Model identifier and configuration applied to every pipeline stage.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return await self._post(
            "/v1/dreams?beta=true",
            body=await async_maybe_transform(
                {
                    "inputs": inputs,
                    "model": model,
                    "instructions": instructions,
                },
                dream_create_params.DreamCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaDream,
        )

    async def retrieve(
        self,
        dream_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaDream:
        """
        Get a Dream

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dream_id:
            raise ValueError(f"Expected a non-empty value for `dream_id` but received {dream_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return await self._get(
            path_template("/v1/dreams/{dream_id}?beta=true", dream_id=dream_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaDream,
        )

    def list(
        self,
        *,
        created_at_gt: Union[str, datetime] | Omit = omit,
        created_at_lt: Union[str, datetime] | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        statuses: List[BetaDreamStatus] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaDream, AsyncPageCursor[BetaDream]]:
        """
        List Dreams

        Args:
          created_at_gt: Return dreams with `created_at` strictly after this timestamp (exclusive lower
              bound, RFC 3339). Unset applies no lower bound.

          created_at_lt: Return dreams with `created_at` strictly before this timestamp (exclusive upper
              bound, RFC 3339). Unset applies no upper bound.

          include_archived: Query parameter for include_archived

          limit: Query parameter for limit

          page: Query parameter for page

          statuses: Filter by lifecycle status. Repeat the parameter to match any of multiple
              statuses. Empty applies no status filter.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/dreams?beta=true",
            page=AsyncPageCursor[BetaDream],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "created_at_gt": created_at_gt,
                        "created_at_lt": created_at_lt,
                        "include_archived": include_archived,
                        "limit": limit,
                        "page": page,
                        "statuses": statuses,
                    },
                    dream_list_params.DreamListParams,
                ),
            ),
            model=BetaDream,
        )

    async def archive(
        self,
        dream_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaDream:
        """
        Archive a Dream

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dream_id:
            raise ValueError(f"Expected a non-empty value for `dream_id` but received {dream_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return await self._post(
            path_template("/v1/dreams/{dream_id}/archive?beta=true", dream_id=dream_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaDream,
        )

    async def cancel(
        self,
        dream_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaDream:
        """
        Cancel a Dream

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dream_id:
            raise ValueError(f"Expected a non-empty value for `dream_id` but received {dream_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["dreaming-2026-04-21"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "dreaming-2026-04-21", **(extra_headers or {})}
        return await self._post(
            path_template("/v1/dreams/{dream_id}/cancel?beta=true", dream_id=dream_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaDream,
        )


class DreamsWithRawResponse:
    def __init__(self, dreams: Dreams) -> None:
        self._dreams = dreams

        self.create = _legacy_response.to_raw_response_wrapper(
            dreams.create,
        )
        self.retrieve = _legacy_response.to_raw_response_wrapper(
            dreams.retrieve,
        )
        self.list = _legacy_response.to_raw_response_wrapper(
            dreams.list,
        )
        self.archive = _legacy_response.to_raw_response_wrapper(
            dreams.archive,
        )
        self.cancel = _legacy_response.to_raw_response_wrapper(
            dreams.cancel,
        )


class AsyncDreamsWithRawResponse:
    def __init__(self, dreams: AsyncDreams) -> None:
        self._dreams = dreams

        self.create = _legacy_response.async_to_raw_response_wrapper(
            dreams.create,
        )
        self.retrieve = _legacy_response.async_to_raw_response_wrapper(
            dreams.retrieve,
        )
        self.list = _legacy_response.async_to_raw_response_wrapper(
            dreams.list,
        )
        self.archive = _legacy_response.async_to_raw_response_wrapper(
            dreams.archive,
        )
        self.cancel = _legacy_response.async_to_raw_response_wrapper(
            dreams.cancel,
        )


class DreamsWithStreamingResponse:
    def __init__(self, dreams: Dreams) -> None:
        self._dreams = dreams

        self.create = to_streamed_response_wrapper(
            dreams.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            dreams.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            dreams.list,
        )
        self.archive = to_streamed_response_wrapper(
            dreams.archive,
        )
        self.cancel = to_streamed_response_wrapper(
            dreams.cancel,
        )


class AsyncDreamsWithStreamingResponse:
    def __init__(self, dreams: AsyncDreams) -> None:
        self._dreams = dreams

        self.create = async_to_streamed_response_wrapper(
            dreams.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            dreams.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            dreams.list,
        )
        self.archive = async_to_streamed_response_wrapper(
            dreams.archive,
        )
        self.cancel = async_to_streamed_response_wrapper(
            dreams.cancel,
        )
