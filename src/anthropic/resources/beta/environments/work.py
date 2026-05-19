# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Optional
from itertools import chain

import httpx

from .... import _legacy_response
from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import is_given, path_template, maybe_transform, strip_not_given, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ....pagination import SyncPageCursor, AsyncPageCursor
from ...._base_client import AsyncPaginator, make_request_options
from ....types.beta.environments import (
    work_list_params,
    work_poll_params,
    work_stop_params,
    work_update_params,
    work_heartbeat_params,
)
from ....types.anthropic_beta_param import AnthropicBetaParam
from ....types.beta.environments.beta_self_hosted_work import BetaSelfHostedWork
from ....types.beta.environments.beta_self_hosted_work_queue_stats import BetaSelfHostedWorkQueueStats
from ....types.beta.environments.beta_self_hosted_work_heartbeat_response import BetaSelfHostedWorkHeartbeatResponse

__all__ = ["Work", "AsyncWork"]


class Work(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> WorkWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return WorkWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WorkWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return WorkWithStreamingResponse(self)

    def retrieve(
        self,
        work_id: str,
        *,
        environment_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaSelfHostedWork:
        """
        Note: these endpoints are called automatically by the pre-built environment
        worker provided in the SDKs and CLI, for orchestrating sessions with self-hosted
        sandbox environments. They are included here as a reference; you do not need to
        invoke them directly.

        Retrieve detailed information about a specific work item.

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        if not work_id:
            raise ValueError(f"Expected a non-empty value for `work_id` but received {work_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return self._get(
            path_template(
                "/v1/environments/{environment_id}/work/{work_id}?beta=true",
                environment_id=environment_id,
                work_id=work_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaSelfHostedWork,
        )

    def update(
        self,
        work_id: str,
        *,
        environment_id: str,
        metadata: Dict[str, Optional[str]],
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaSelfHostedWork:
        """
        Note: these endpoints are called automatically by the pre-built environment
        worker provided in the SDKs and CLI, for orchestrating sessions with self-hosted
        sandbox environments. They are included here as a reference; you do not need to
        invoke them directly.

        Update work item metadata with merge semantics.

        Args:
          metadata: Metadata patch. Set a key to a string to upsert it, or to null to delete it.
              Omit the field to preserve existing metadata.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        if not work_id:
            raise ValueError(f"Expected a non-empty value for `work_id` but received {work_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return self._post(
            path_template(
                "/v1/environments/{environment_id}/work/{work_id}?beta=true",
                environment_id=environment_id,
                work_id=work_id,
            ),
            body=maybe_transform({"metadata": metadata}, work_update_params.WorkUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaSelfHostedWork,
        )

    def list(
        self,
        environment_id: str,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaSelfHostedWork]:
        """
        Note: these endpoints are called automatically by the pre-built environment
        worker provided in the SDKs and CLI, for orchestrating sessions with self-hosted
        sandbox environments. They are included here as a reference; you do not need to
        invoke them directly.

        List work items in an environment.

        Args:
          limit: Maximum number of work items to return

          page: Opaque cursor from previous response for pagination

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return self._get_api_list(
            path_template("/v1/environments/{environment_id}/work?beta=true", environment_id=environment_id),
            page=SyncPageCursor[BetaSelfHostedWork],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                    },
                    work_list_params.WorkListParams,
                ),
            ),
            model=BetaSelfHostedWork,
        )

    def ack(
        self,
        work_id: str,
        *,
        environment_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaSelfHostedWork:
        """
        Note: these endpoints are called automatically by the pre-built environment
        worker provided in the SDKs and CLI, for orchestrating sessions with self-hosted
        sandbox environments. They are included here as a reference; you do not need to
        invoke them directly.

        Acknowledge receipt of a work item, transitioning it from 'queued' to 'starting'
        and removing it from the queue.

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        if not work_id:
            raise ValueError(f"Expected a non-empty value for `work_id` but received {work_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return self._post(
            path_template(
                "/v1/environments/{environment_id}/work/{work_id}/ack?beta=true",
                environment_id=environment_id,
                work_id=work_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaSelfHostedWork,
        )

    def heartbeat(
        self,
        work_id: str,
        *,
        environment_id: str,
        desired_ttl_seconds: Optional[int] | Omit = omit,
        expected_last_heartbeat: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaSelfHostedWorkHeartbeatResponse:
        """
        Note: these endpoints are called automatically by the pre-built environment
        worker provided in the SDKs and CLI, for orchestrating sessions with self-hosted
        sandbox environments. They are included here as a reference; you do not need to
        invoke them directly.

        Record a heartbeat for a work item to maintain the lease.

        Args:
          desired_ttl_seconds: Desired TTL in seconds

          expected_last_heartbeat: Expected last_heartbeat for conditional update (optimistic concurrency). Use
              literal 'NO_HEARTBEAT' to claim an unclaimed lease (first heartbeat). For
              subsequent heartbeats, echo the server's previous last_heartbeat value exactly.
              Returns 412 Precondition Failed if the actual value doesn't match.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        if not work_id:
            raise ValueError(f"Expected a non-empty value for `work_id` but received {work_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return self._post(
            path_template(
                "/v1/environments/{environment_id}/work/{work_id}/heartbeat?beta=true",
                environment_id=environment_id,
                work_id=work_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "desired_ttl_seconds": desired_ttl_seconds,
                        "expected_last_heartbeat": expected_last_heartbeat,
                    },
                    work_heartbeat_params.WorkHeartbeatParams,
                ),
            ),
            cast_to=BetaSelfHostedWorkHeartbeatResponse,
        )

    def poll(
        self,
        environment_id: str,
        *,
        block_ms: Optional[int] | Omit = omit,
        reclaim_older_than_ms: Optional[int] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        anthropic_worker_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Optional[BetaSelfHostedWork]:
        """
        Note: these endpoints are called automatically by the pre-built environment
        worker provided in the SDKs and CLI, for orchestrating sessions with self-hosted
        sandbox environments. They are included here as a reference; you do not need to
        invoke them directly.

        Long poll for work items in the queue.

        Args:
          block_ms: How long to wait for work to arrive before returning. Must be 1-999 in
              milliseconds. Defaults to non-blocking (returns immediately if no work is
              available).

          reclaim_older_than_ms: Reclaim unacknowledged work items older than this many milliseconds. If omitted,
              uses the default (5000ms).

          betas: Optional header to specify the beta version(s) you want to use.

          anthropic_worker_id: Unique identifier for the specific worker polling, used to track aggregated
              environment-level work metrics in Console

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given,
                    "Anthropic-Worker-ID": anthropic_worker_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return self._get(
            path_template("/v1/environments/{environment_id}/work/poll?beta=true", environment_id=environment_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "block_ms": block_ms,
                        "reclaim_older_than_ms": reclaim_older_than_ms,
                    },
                    work_poll_params.WorkPollParams,
                ),
            ),
            cast_to=BetaSelfHostedWork,
        )

    def stats(
        self,
        environment_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaSelfHostedWorkQueueStats:
        """
        Get statistics about the work queue for an environment.

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return self._get(
            path_template("/v1/environments/{environment_id}/work/stats?beta=true", environment_id=environment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaSelfHostedWorkQueueStats,
        )

    def stop(
        self,
        work_id: str,
        *,
        environment_id: str,
        force: bool | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaSelfHostedWork:
        """
        Note: these endpoints are called automatically by the pre-built environment
        worker provided in the SDKs and CLI, for orchestrating sessions with self-hosted
        sandbox environments. They are included here as a reference; you do not need to
        invoke them directly.

        Stop a work item, initiating graceful or forced shutdown.

        Args:
          force: If true, immediately stop work without graceful shutdown

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        if not work_id:
            raise ValueError(f"Expected a non-empty value for `work_id` but received {work_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return self._post(
            path_template(
                "/v1/environments/{environment_id}/work/{work_id}/stop?beta=true",
                environment_id=environment_id,
                work_id=work_id,
            ),
            body=maybe_transform({"force": force}, work_stop_params.WorkStopParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaSelfHostedWork,
        )


class AsyncWork(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncWorkWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncWorkWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWorkWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncWorkWithStreamingResponse(self)

    async def retrieve(
        self,
        work_id: str,
        *,
        environment_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaSelfHostedWork:
        """
        Note: these endpoints are called automatically by the pre-built environment
        worker provided in the SDKs and CLI, for orchestrating sessions with self-hosted
        sandbox environments. They are included here as a reference; you do not need to
        invoke them directly.

        Retrieve detailed information about a specific work item.

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        if not work_id:
            raise ValueError(f"Expected a non-empty value for `work_id` but received {work_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return await self._get(
            path_template(
                "/v1/environments/{environment_id}/work/{work_id}?beta=true",
                environment_id=environment_id,
                work_id=work_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaSelfHostedWork,
        )

    async def update(
        self,
        work_id: str,
        *,
        environment_id: str,
        metadata: Dict[str, Optional[str]],
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaSelfHostedWork:
        """
        Note: these endpoints are called automatically by the pre-built environment
        worker provided in the SDKs and CLI, for orchestrating sessions with self-hosted
        sandbox environments. They are included here as a reference; you do not need to
        invoke them directly.

        Update work item metadata with merge semantics.

        Args:
          metadata: Metadata patch. Set a key to a string to upsert it, or to null to delete it.
              Omit the field to preserve existing metadata.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        if not work_id:
            raise ValueError(f"Expected a non-empty value for `work_id` but received {work_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/v1/environments/{environment_id}/work/{work_id}?beta=true",
                environment_id=environment_id,
                work_id=work_id,
            ),
            body=await async_maybe_transform({"metadata": metadata}, work_update_params.WorkUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaSelfHostedWork,
        )

    def list(
        self,
        environment_id: str,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaSelfHostedWork, AsyncPageCursor[BetaSelfHostedWork]]:
        """
        Note: these endpoints are called automatically by the pre-built environment
        worker provided in the SDKs and CLI, for orchestrating sessions with self-hosted
        sandbox environments. They are included here as a reference; you do not need to
        invoke them directly.

        List work items in an environment.

        Args:
          limit: Maximum number of work items to return

          page: Opaque cursor from previous response for pagination

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return self._get_api_list(
            path_template("/v1/environments/{environment_id}/work?beta=true", environment_id=environment_id),
            page=AsyncPageCursor[BetaSelfHostedWork],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                    },
                    work_list_params.WorkListParams,
                ),
            ),
            model=BetaSelfHostedWork,
        )

    async def ack(
        self,
        work_id: str,
        *,
        environment_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaSelfHostedWork:
        """
        Note: these endpoints are called automatically by the pre-built environment
        worker provided in the SDKs and CLI, for orchestrating sessions with self-hosted
        sandbox environments. They are included here as a reference; you do not need to
        invoke them directly.

        Acknowledge receipt of a work item, transitioning it from 'queued' to 'starting'
        and removing it from the queue.

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        if not work_id:
            raise ValueError(f"Expected a non-empty value for `work_id` but received {work_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/v1/environments/{environment_id}/work/{work_id}/ack?beta=true",
                environment_id=environment_id,
                work_id=work_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaSelfHostedWork,
        )

    async def heartbeat(
        self,
        work_id: str,
        *,
        environment_id: str,
        desired_ttl_seconds: Optional[int] | Omit = omit,
        expected_last_heartbeat: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaSelfHostedWorkHeartbeatResponse:
        """
        Note: these endpoints are called automatically by the pre-built environment
        worker provided in the SDKs and CLI, for orchestrating sessions with self-hosted
        sandbox environments. They are included here as a reference; you do not need to
        invoke them directly.

        Record a heartbeat for a work item to maintain the lease.

        Args:
          desired_ttl_seconds: Desired TTL in seconds

          expected_last_heartbeat: Expected last_heartbeat for conditional update (optimistic concurrency). Use
              literal 'NO_HEARTBEAT' to claim an unclaimed lease (first heartbeat). For
              subsequent heartbeats, echo the server's previous last_heartbeat value exactly.
              Returns 412 Precondition Failed if the actual value doesn't match.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        if not work_id:
            raise ValueError(f"Expected a non-empty value for `work_id` but received {work_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/v1/environments/{environment_id}/work/{work_id}/heartbeat?beta=true",
                environment_id=environment_id,
                work_id=work_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "desired_ttl_seconds": desired_ttl_seconds,
                        "expected_last_heartbeat": expected_last_heartbeat,
                    },
                    work_heartbeat_params.WorkHeartbeatParams,
                ),
            ),
            cast_to=BetaSelfHostedWorkHeartbeatResponse,
        )

    async def poll(
        self,
        environment_id: str,
        *,
        block_ms: Optional[int] | Omit = omit,
        reclaim_older_than_ms: Optional[int] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        anthropic_worker_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Optional[BetaSelfHostedWork]:
        """
        Note: these endpoints are called automatically by the pre-built environment
        worker provided in the SDKs and CLI, for orchestrating sessions with self-hosted
        sandbox environments. They are included here as a reference; you do not need to
        invoke them directly.

        Long poll for work items in the queue.

        Args:
          block_ms: How long to wait for work to arrive before returning. Must be 1-999 in
              milliseconds. Defaults to non-blocking (returns immediately if no work is
              available).

          reclaim_older_than_ms: Reclaim unacknowledged work items older than this many milliseconds. If omitted,
              uses the default (5000ms).

          betas: Optional header to specify the beta version(s) you want to use.

          anthropic_worker_id: Unique identifier for the specific worker polling, used to track aggregated
              environment-level work metrics in Console

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given,
                    "Anthropic-Worker-ID": anthropic_worker_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return await self._get(
            path_template("/v1/environments/{environment_id}/work/poll?beta=true", environment_id=environment_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "block_ms": block_ms,
                        "reclaim_older_than_ms": reclaim_older_than_ms,
                    },
                    work_poll_params.WorkPollParams,
                ),
            ),
            cast_to=BetaSelfHostedWork,
        )

    async def stats(
        self,
        environment_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaSelfHostedWorkQueueStats:
        """
        Get statistics about the work queue for an environment.

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return await self._get(
            path_template("/v1/environments/{environment_id}/work/stats?beta=true", environment_id=environment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaSelfHostedWorkQueueStats,
        )

    async def stop(
        self,
        work_id: str,
        *,
        environment_id: str,
        force: bool | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaSelfHostedWork:
        """
        Note: these endpoints are called automatically by the pre-built environment
        worker provided in the SDKs and CLI, for orchestrating sessions with self-hosted
        sandbox environments. They are included here as a reference; you do not need to
        invoke them directly.

        Stop a work item, initiating graceful or forced shutdown.

        Args:
          force: If true, immediately stop work without graceful shutdown

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not environment_id:
            raise ValueError(f"Expected a non-empty value for `environment_id` but received {environment_id!r}")
        if not work_id:
            raise ValueError(f"Expected a non-empty value for `work_id` but received {work_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/v1/environments/{environment_id}/work/{work_id}/stop?beta=true",
                environment_id=environment_id,
                work_id=work_id,
            ),
            body=await async_maybe_transform({"force": force}, work_stop_params.WorkStopParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaSelfHostedWork,
        )


class WorkWithRawResponse:
    def __init__(self, work: Work) -> None:
        self._work = work

        self.retrieve = _legacy_response.to_raw_response_wrapper(
            work.retrieve,
        )
        self.update = _legacy_response.to_raw_response_wrapper(
            work.update,
        )
        self.list = _legacy_response.to_raw_response_wrapper(
            work.list,
        )
        self.ack = _legacy_response.to_raw_response_wrapper(
            work.ack,
        )
        self.heartbeat = _legacy_response.to_raw_response_wrapper(
            work.heartbeat,
        )
        self.poll = _legacy_response.to_raw_response_wrapper(
            work.poll,
        )
        self.stats = _legacy_response.to_raw_response_wrapper(
            work.stats,
        )
        self.stop = _legacy_response.to_raw_response_wrapper(
            work.stop,
        )


class AsyncWorkWithRawResponse:
    def __init__(self, work: AsyncWork) -> None:
        self._work = work

        self.retrieve = _legacy_response.async_to_raw_response_wrapper(
            work.retrieve,
        )
        self.update = _legacy_response.async_to_raw_response_wrapper(
            work.update,
        )
        self.list = _legacy_response.async_to_raw_response_wrapper(
            work.list,
        )
        self.ack = _legacy_response.async_to_raw_response_wrapper(
            work.ack,
        )
        self.heartbeat = _legacy_response.async_to_raw_response_wrapper(
            work.heartbeat,
        )
        self.poll = _legacy_response.async_to_raw_response_wrapper(
            work.poll,
        )
        self.stats = _legacy_response.async_to_raw_response_wrapper(
            work.stats,
        )
        self.stop = _legacy_response.async_to_raw_response_wrapper(
            work.stop,
        )


class WorkWithStreamingResponse:
    def __init__(self, work: Work) -> None:
        self._work = work

        self.retrieve = to_streamed_response_wrapper(
            work.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            work.update,
        )
        self.list = to_streamed_response_wrapper(
            work.list,
        )
        self.ack = to_streamed_response_wrapper(
            work.ack,
        )
        self.heartbeat = to_streamed_response_wrapper(
            work.heartbeat,
        )
        self.poll = to_streamed_response_wrapper(
            work.poll,
        )
        self.stats = to_streamed_response_wrapper(
            work.stats,
        )
        self.stop = to_streamed_response_wrapper(
            work.stop,
        )


class AsyncWorkWithStreamingResponse:
    def __init__(self, work: AsyncWork) -> None:
        self._work = work

        self.retrieve = async_to_streamed_response_wrapper(
            work.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            work.update,
        )
        self.list = async_to_streamed_response_wrapper(
            work.list,
        )
        self.ack = async_to_streamed_response_wrapper(
            work.ack,
        )
        self.heartbeat = async_to_streamed_response_wrapper(
            work.heartbeat,
        )
        self.poll = async_to_streamed_response_wrapper(
            work.poll,
        )
        self.stats = async_to_streamed_response_wrapper(
            work.stats,
        )
        self.stop = async_to_streamed_response_wrapper(
            work.stop,
        )
