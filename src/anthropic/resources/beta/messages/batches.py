# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable

import httpx

from .... import _legacy_response
from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    is_given,
    maybe_transform,
    strip_not_given,
    async_maybe_transform,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_streamed_response_wrapper,
    to_custom_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ....pagination import SyncPage, AsyncPage
from ...._base_client import AsyncPaginator, make_request_options
from ....types.beta.messages import batch_list_params, batch_create_params
from ....types.anthropic_beta_param import AnthropicBetaParam
from ....types.beta.messages.beta_message_batch import BetaMessageBatch

__all__ = ["Batches", "AsyncBatches"]


class Batches(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BatchesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return BatchesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BatchesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return BatchesWithStreamingResponse(self)

    def create(
        self,
        *,
        requests: Iterable[batch_create_params.Request],
        betas: List[AnthropicBetaParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BetaMessageBatch:
        """
        Send a batch of requests to create Messages.

        The Messages Batch API can be used to process multiple Messages API requests at
        once. Once a Message Batch is created, it begins processing immediately.

        Args:
          requests: List of requests for prompt completion. Each is an individual request to create
              a Message.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"anthropic-beta": "message-batches-2024-09-24", **(extra_headers or {})}
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else NOT_GIVEN}),
            **(extra_headers or {}),
        }
        return self._post(
            "/v1/messages/batches?beta=true",
            body=maybe_transform({"requests": requests}, batch_create_params.BatchCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaMessageBatch,
        )

    def retrieve(
        self,
        message_batch_id: str,
        *,
        betas: List[AnthropicBetaParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BetaMessageBatch:
        """This endpoint is idempotent and can be used to poll for Message Batch
        completion.

        To access the results of a Message Batch, use the `responses_url`
        field in the response.

        Args:
          message_batch_id: ID of the Message Batch.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not message_batch_id:
            raise ValueError(f"Expected a non-empty value for `message_batch_id` but received {message_batch_id!r}")
        extra_headers = {"anthropic-beta": "message-batches-2024-09-24", **(extra_headers or {})}
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else NOT_GIVEN}),
            **(extra_headers or {}),
        }
        return self._get(
            f"/v1/messages/batches/{message_batch_id}?beta=true",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaMessageBatch,
        )

    def list(
        self,
        *,
        after_id: str | NotGiven = NOT_GIVEN,
        before_id: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        betas: List[AnthropicBetaParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncPage[BetaMessageBatch]:
        """
        List all Message Batches within a Workspace.

        Args:
          after_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately after this object.

          before_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately before this object.

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `100`.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"anthropic-beta": "message-batches-2024-09-24", **(extra_headers or {})}
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else NOT_GIVEN}),
            **(extra_headers or {}),
        }
        return self._get_api_list(
            "/v1/messages/batches?beta=true",
            page=SyncPage[BetaMessageBatch],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "limit": limit,
                    },
                    batch_list_params.BatchListParams,
                ),
            ),
            model=BetaMessageBatch,
        )

    def cancel(
        self,
        message_batch_id: str,
        *,
        betas: List[AnthropicBetaParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BetaMessageBatch:
        """Batches may be canceled any time before processing ends.

        The system may complete
        any in-progress, non-interruptible operations before finalizing cancellation.

        Args:
          message_batch_id: ID of the Message Batch.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not message_batch_id:
            raise ValueError(f"Expected a non-empty value for `message_batch_id` but received {message_batch_id!r}")
        extra_headers = {"anthropic-beta": "message-batches-2024-09-24", **(extra_headers or {})}
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else NOT_GIVEN}),
            **(extra_headers or {}),
        }
        return self._post(
            f"/v1/messages/batches/{message_batch_id}/cancel?beta=true",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaMessageBatch,
        )

    def results(
        self,
        message_batch_id: str,
        *,
        betas: List[AnthropicBetaParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        Streams the results of a Message Batch as a `.jsonl` file.

        Each line in the file is a JSON object containing the result of a single request
        in the Message Batch. Results are not guaranteed to be in the same order as
        requests. Use the `custom_id` field to match results to requests.

        Args:
          message_batch_id: ID of the Message Batch.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not message_batch_id:
            raise ValueError(f"Expected a non-empty value for `message_batch_id` but received {message_batch_id!r}")
        extra_headers = {"anthropic-beta": "message-batches-2024-09-24", **(extra_headers or {})}
        extra_headers = {"Accept": "application/binary", **(extra_headers or {})}
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else NOT_GIVEN}),
            **(extra_headers or {}),
        }
        return self._get(
            f"/v1/messages/batches/{message_batch_id}/results?beta=true",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncBatches(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBatchesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncBatchesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBatchesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncBatchesWithStreamingResponse(self)

    async def create(
        self,
        *,
        requests: Iterable[batch_create_params.Request],
        betas: List[AnthropicBetaParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BetaMessageBatch:
        """
        Send a batch of requests to create Messages.

        The Messages Batch API can be used to process multiple Messages API requests at
        once. Once a Message Batch is created, it begins processing immediately.

        Args:
          requests: List of requests for prompt completion. Each is an individual request to create
              a Message.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"anthropic-beta": "message-batches-2024-09-24", **(extra_headers or {})}
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else NOT_GIVEN}),
            **(extra_headers or {}),
        }
        return await self._post(
            "/v1/messages/batches?beta=true",
            body=await async_maybe_transform({"requests": requests}, batch_create_params.BatchCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaMessageBatch,
        )

    async def retrieve(
        self,
        message_batch_id: str,
        *,
        betas: List[AnthropicBetaParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BetaMessageBatch:
        """This endpoint is idempotent and can be used to poll for Message Batch
        completion.

        To access the results of a Message Batch, use the `responses_url`
        field in the response.

        Args:
          message_batch_id: ID of the Message Batch.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not message_batch_id:
            raise ValueError(f"Expected a non-empty value for `message_batch_id` but received {message_batch_id!r}")
        extra_headers = {"anthropic-beta": "message-batches-2024-09-24", **(extra_headers or {})}
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else NOT_GIVEN}),
            **(extra_headers or {}),
        }
        return await self._get(
            f"/v1/messages/batches/{message_batch_id}?beta=true",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaMessageBatch,
        )

    def list(
        self,
        *,
        after_id: str | NotGiven = NOT_GIVEN,
        before_id: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        betas: List[AnthropicBetaParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[BetaMessageBatch, AsyncPage[BetaMessageBatch]]:
        """
        List all Message Batches within a Workspace.

        Args:
          after_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately after this object.

          before_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately before this object.

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `100`.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"anthropic-beta": "message-batches-2024-09-24", **(extra_headers or {})}
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else NOT_GIVEN}),
            **(extra_headers or {}),
        }
        return self._get_api_list(
            "/v1/messages/batches?beta=true",
            page=AsyncPage[BetaMessageBatch],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "limit": limit,
                    },
                    batch_list_params.BatchListParams,
                ),
            ),
            model=BetaMessageBatch,
        )

    async def cancel(
        self,
        message_batch_id: str,
        *,
        betas: List[AnthropicBetaParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BetaMessageBatch:
        """Batches may be canceled any time before processing ends.

        The system may complete
        any in-progress, non-interruptible operations before finalizing cancellation.

        Args:
          message_batch_id: ID of the Message Batch.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not message_batch_id:
            raise ValueError(f"Expected a non-empty value for `message_batch_id` but received {message_batch_id!r}")
        extra_headers = {"anthropic-beta": "message-batches-2024-09-24", **(extra_headers or {})}
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else NOT_GIVEN}),
            **(extra_headers or {}),
        }
        return await self._post(
            f"/v1/messages/batches/{message_batch_id}/cancel?beta=true",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaMessageBatch,
        )

    async def results(
        self,
        message_batch_id: str,
        *,
        betas: List[AnthropicBetaParam] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        Streams the results of a Message Batch as a `.jsonl` file.

        Each line in the file is a JSON object containing the result of a single request
        in the Message Batch. Results are not guaranteed to be in the same order as
        requests. Use the `custom_id` field to match results to requests.

        Args:
          message_batch_id: ID of the Message Batch.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not message_batch_id:
            raise ValueError(f"Expected a non-empty value for `message_batch_id` but received {message_batch_id!r}")
        extra_headers = {"anthropic-beta": "message-batches-2024-09-24", **(extra_headers or {})}
        extra_headers = {"Accept": "application/binary", **(extra_headers or {})}
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else NOT_GIVEN}),
            **(extra_headers or {}),
        }
        return await self._get(
            f"/v1/messages/batches/{message_batch_id}/results?beta=true",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class BatchesWithRawResponse:
    def __init__(self, batches: Batches) -> None:
        self._batches = batches

        self.create = _legacy_response.to_raw_response_wrapper(
            batches.create,
        )
        self.retrieve = _legacy_response.to_raw_response_wrapper(
            batches.retrieve,
        )
        self.list = _legacy_response.to_raw_response_wrapper(
            batches.list,
        )
        self.cancel = _legacy_response.to_raw_response_wrapper(
            batches.cancel,
        )
        self.results = to_custom_raw_response_wrapper(
            batches.results,
            BinaryAPIResponse,
        )


class AsyncBatchesWithRawResponse:
    def __init__(self, batches: AsyncBatches) -> None:
        self._batches = batches

        self.create = _legacy_response.async_to_raw_response_wrapper(
            batches.create,
        )
        self.retrieve = _legacy_response.async_to_raw_response_wrapper(
            batches.retrieve,
        )
        self.list = _legacy_response.async_to_raw_response_wrapper(
            batches.list,
        )
        self.cancel = _legacy_response.async_to_raw_response_wrapper(
            batches.cancel,
        )
        self.results = async_to_custom_raw_response_wrapper(
            batches.results,
            AsyncBinaryAPIResponse,
        )


class BatchesWithStreamingResponse:
    def __init__(self, batches: Batches) -> None:
        self._batches = batches

        self.create = to_streamed_response_wrapper(
            batches.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            batches.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            batches.list,
        )
        self.cancel = to_streamed_response_wrapper(
            batches.cancel,
        )
        self.results = to_custom_streamed_response_wrapper(
            batches.results,
            StreamedBinaryAPIResponse,
        )


class AsyncBatchesWithStreamingResponse:
    def __init__(self, batches: AsyncBatches) -> None:
        self._batches = batches

        self.create = async_to_streamed_response_wrapper(
            batches.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            batches.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            batches.list,
        )
        self.cancel = async_to_streamed_response_wrapper(
            batches.cancel,
        )
        self.results = async_to_custom_streamed_response_wrapper(
            batches.results,
            AsyncStreamedBinaryAPIResponse,
        )