# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Dict, List, Optional, cast
from itertools import chain

import httpx

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from ...._client import AsyncAnthropic
    from ....lib.environments._worker import EnvironmentWorker, EnvironmentWorkerTools

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

    def poller(
        self,
        *,
        environment_id: str,
        environment_key: str,
        worker_id: str | None = None,
        block_ms: int | None | NotGiven = not_given,
        reclaim_older_than_ms: int | None = None,
        drain: bool = False,
        auto_stop: bool = True,
        extra_headers: Headers | None = None,
    ) -> AsyncIterator[BetaSelfHostedWork]:
        """Async-iterate work items claimed from a self-hosted environment.

        Each yielded item has been ack'd. The environment key authenticates the
        poll, ack, and stop calls via a scoped sub-client (built once per
        call). Async only — available on :class:`~anthropic.AsyncAnthropic`
        (the sync client does not expose ``poller``).

        With the defaults this loops forever and calls ``stop`` after the
        consuming ``async for`` body returns or raises (long-running runner
        shape). Pass ``drain=True, auto_stop=False`` to drain whatever is queued
        and return without owning the stop call (webhook-dispatch shape — each
        item is handed off to another process that calls ``stop`` when done).

        Args:
          environment_id: The self-hosted environment to claim work from.
          environment_key: The environment key — used as the Bearer credential
            on the scoped sub-client that issues poll / ack / stop requests.
          worker_id: Optional identifier sent on each poll. Defaults to a
            unique, hostname-prefixed id.
          block_ms: How long the server should hold an empty poll open before
            returning (long-poll). Server caps this at 999. Defaults to
            ``POLL_BLOCK_MS`` (999) when not given. Pass ``None`` to omit for a
            non-blocking poll — the server rejects ``0``.
          reclaim_older_than_ms: Reclaim un-ack'd work older than this many ms.
            Forwarded to the underlying poll request.
          drain: When True, return after the first empty poll instead of
            sleeping and re-polling.
          auto_stop: When True (default), call ``stop`` after the consumer's
            loop body completes. Set False when handing items off to another
            process that owns the stop call.
          extra_headers: Optional headers passed through per request on the
            poll / ack / stop calls. They are threaded into each call's
            ``extra_headers=`` and never assigned onto the client, so client
            state is not mutated. Auth and ``x-stainless-helper`` are supplied
            by the scoped sub-client built here (and the parent client's
            ``default_headers`` propagate via its ``client.copy()``); a header
            given here overrides the scoped client's same-named default for
            that request, so use it for caller passthrough (e.g. trace ids),
            not to set auth.
        """
        # POLL_BLOCK_MS is resolved here, not used as a literal signature
        # default: importing _poller at module load would form an import cycle
        # (_poller imports this module) and pull the host-only environment lib
        # into ``import anthropic``. The sentinel keeps a single source of truth
        # for the default so it can't drift from the constant.
        from ....lib._scoped_client import _copy_client_with_bearer_auth
        from ....lib.environments._poller import POLL_BLOCK_MS, aiter_work

        if not is_given(block_ms):
            block_ms = POLL_BLOCK_MS

        scoped = _copy_client_with_bearer_auth(
            cast("AsyncAnthropic", self._client),
            auth_token=environment_key,
            helper="environments-work-poller",
        )
        return aiter_work(
            scoped.beta.environments.work,
            environment_id=environment_id,
            worker_id=worker_id,
            block_ms=block_ms,
            reclaim_older_than_ms=reclaim_older_than_ms,
            drain=drain,
            auto_stop=auto_stop,
            extra_headers=extra_headers,
        )

    def worker(
        self,
        *,
        environment_id: str | None = None,
        environment_key: str | None = None,
        tools: EnvironmentWorkerTools | None = None,
        workdir: str | os.PathLike[str] | None = None,
        unrestricted_paths: bool = False,
        max_file_bytes: int | None | NotGiven = not_given,
        max_idle: float | None | NotGiven = not_given,
        worker_id: str | None = None,
        extra_headers: Headers | None = None,
    ) -> EnvironmentWorker:
        """Build an :class:`~anthropic.lib.environments.EnvironmentWorker` bound to this async client.

        The full worker: it polls the environment for work, and for each claimed
        session sets up the workdir + downloads the session agent's skills, runs
        the given ``tools`` against the session's tool-call events while
        heartbeating the work-item lease, force-stops the work on exit, and
        loops. Composed from this resource's :meth:`poller` and the per-session
        session tool runner.

        ``EnvironmentWorker`` is async only — its ``run`` / ``handle_item``
        coroutines need an event loop. With this :class:`~anthropic.AsyncAnthropic`
        client the returned worker is ready to ``await worker.run()`` (long-running
        poll loop) or ``await worker.handle_item()`` (single already-claimed work
        item). It can also be constructed directly:
        ``EnvironmentWorker(client, ...)``.

        Args:
          environment_id: The self-hosted environment to poll for work. Required
            by ``EnvironmentWorker.run``; not used by
            ``EnvironmentWorker.handle_item``.
          environment_key: The environment key — the worker's single credential,
            used as Bearer auth on the control-plane and session-level calls.
          tools: Tools to expose to each claimed session. Either a fixed list or
            a factory invoked once per session with that session's
            ``AgentToolContext``. Defaults to ``beta_agent_toolset_20260401(env)``.
          workdir: Base directory for the per-session ``AgentToolContext``.
            Defaults to ``os.getcwd()`` captured when the worker is constructed
            (TS parity: ``process.cwd()`` at construction).
          unrestricted_paths: Forwarded to the per-session ``AgentToolContext``.
          max_file_bytes: Forwarded to the per-session ``AgentToolContext`` — the
            size cap (bytes) for the ``read``/``edit`` tools. ``not_given``
            (default) uses the built-in 256 KiB cap; a positive int sets a custom
            cap; ``None`` disables the cap.
          max_idle: Seconds to keep running after the session goes idle with
            ``stop_reason`` ``end_turn``. Defaults to ``DEFAULT_MAX_IDLE`` (60s)
            when not given. ``None`` disables it.
          worker_id: Optional identifier sent on each poll. Defaults to a unique,
            hostname-prefixed id.
          extra_headers: Optional headers passed through per request on every
            call the worker makes (poll / ack / stop / heartbeat and the
            session tool runner's event stream / list / send). They are
            threaded into each call's ``extra_headers=`` and never assigned
            onto the client, so client state is not mutated. Auth and
            ``x-stainless-helper`` are supplied by the worker's scoped
            sub-clients (and the parent client's ``default_headers`` propagate
            via their ``client.copy()``); a header given here overrides a
            scoped client's same-named default for that request, so use it for
            caller passthrough (e.g. trace ids), not to set auth.
        """
        # DEFAULT_MAX_IDLE resolved here rather than as a literal signature
        # default so the value can't drift from the constant; the lazy import
        # also keeps the host-only environment lib out of ``import anthropic``.
        from ....lib.environments._worker import EnvironmentWorker
        from ....lib.tools._beta_session_runner import DEFAULT_MAX_IDLE

        if not is_given(max_idle):
            max_idle = DEFAULT_MAX_IDLE

        return EnvironmentWorker(
            cast("AsyncAnthropic", self._client),
            environment_id=environment_id,
            environment_key=environment_key,
            tools=tools,
            workdir=workdir,
            unrestricted_paths=unrestricted_paths,
            max_file_bytes=max_file_bytes,
            max_idle=max_idle,
            worker_id=worker_id,
            extra_headers=extra_headers,
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
