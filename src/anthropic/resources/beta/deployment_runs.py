# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from datetime import datetime
from itertools import chain

import httpx

from ... import _legacy_response
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import is_given, path_template, maybe_transform, strip_not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...pagination import SyncPageCursor, AsyncPageCursor
from ...types.beta import BetaManagedAgentsTriggerType, deployment_run_list_params
from ..._base_client import AsyncPaginator, make_request_options
from ...types.anthropic_beta_param import AnthropicBetaParam
from ...types.beta.beta_managed_agents_trigger_type import BetaManagedAgentsTriggerType
from ...types.beta.beta_managed_agents_deployment_run import BetaManagedAgentsDeploymentRun

__all__ = ["DeploymentRuns", "AsyncDeploymentRuns"]


class DeploymentRuns(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DeploymentRunsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return DeploymentRunsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DeploymentRunsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return DeploymentRunsWithStreamingResponse(self)

    def retrieve(
        self,
        deployment_run_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsDeploymentRun:
        """
        Get Deployment Run

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_run_id:
            raise ValueError(f"Expected a non-empty value for `deployment_run_id` but received {deployment_run_id!r}")
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
            path_template("/v1/deployment_runs/{deployment_run_id}?beta=true", deployment_run_id=deployment_run_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaManagedAgentsDeploymentRun,
        )

    def list(
        self,
        *,
        created_at_gt: Union[str, datetime] | Omit = omit,
        created_at_gte: Union[str, datetime] | Omit = omit,
        created_at_lt: Union[str, datetime] | Omit = omit,
        created_at_lte: Union[str, datetime] | Omit = omit,
        deployment_id: str | Omit = omit,
        has_error: bool | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        trigger_type: BetaManagedAgentsTriggerType | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaManagedAgentsDeploymentRun]:
        """
        List Deployment Runs

        Args:
          created_at_gt: Return runs created strictly after this time (exclusive).

          created_at_gte: Return runs created at or after this time (inclusive).

          created_at_lt: Return runs created strictly before this time (exclusive).

          created_at_lte: Return runs created at or before this time (inclusive).

          deployment_id: Filter to a specific deployment. Omit to list across all deployments in the
              workspace. Filtering by a non-existent deployment_id returns 200 with empty
              data.

          has_error: Filter: true for runs with non-null error, false for runs with non-null
              session_id. Omit for all.

          limit: Maximum results per page. Default 20, maximum 1000.

          page: Opaque pagination cursor. Pass next_page from the previous response. Invalid or
              expired cursors return 400.

          trigger_type: Filter runs by what triggered them. Omit to return all runs.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
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
            "/v1/deployment_runs?beta=true",
            page=SyncPageCursor[BetaManagedAgentsDeploymentRun],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "created_at_gt": created_at_gt,
                        "created_at_gte": created_at_gte,
                        "created_at_lt": created_at_lt,
                        "created_at_lte": created_at_lte,
                        "deployment_id": deployment_id,
                        "has_error": has_error,
                        "limit": limit,
                        "page": page,
                        "trigger_type": trigger_type,
                    },
                    deployment_run_list_params.DeploymentRunListParams,
                ),
            ),
            model=BetaManagedAgentsDeploymentRun,
        )


class AsyncDeploymentRuns(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDeploymentRunsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDeploymentRunsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDeploymentRunsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncDeploymentRunsWithStreamingResponse(self)

    async def retrieve(
        self,
        deployment_run_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsDeploymentRun:
        """
        Get Deployment Run

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_run_id:
            raise ValueError(f"Expected a non-empty value for `deployment_run_id` but received {deployment_run_id!r}")
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
            path_template("/v1/deployment_runs/{deployment_run_id}?beta=true", deployment_run_id=deployment_run_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaManagedAgentsDeploymentRun,
        )

    def list(
        self,
        *,
        created_at_gt: Union[str, datetime] | Omit = omit,
        created_at_gte: Union[str, datetime] | Omit = omit,
        created_at_lt: Union[str, datetime] | Omit = omit,
        created_at_lte: Union[str, datetime] | Omit = omit,
        deployment_id: str | Omit = omit,
        has_error: bool | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        trigger_type: BetaManagedAgentsTriggerType | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaManagedAgentsDeploymentRun, AsyncPageCursor[BetaManagedAgentsDeploymentRun]]:
        """
        List Deployment Runs

        Args:
          created_at_gt: Return runs created strictly after this time (exclusive).

          created_at_gte: Return runs created at or after this time (inclusive).

          created_at_lt: Return runs created strictly before this time (exclusive).

          created_at_lte: Return runs created at or before this time (inclusive).

          deployment_id: Filter to a specific deployment. Omit to list across all deployments in the
              workspace. Filtering by a non-existent deployment_id returns 200 with empty
              data.

          has_error: Filter: true for runs with non-null error, false for runs with non-null
              session_id. Omit for all.

          limit: Maximum results per page. Default 20, maximum 1000.

          page: Opaque pagination cursor. Pass next_page from the previous response. Invalid or
              expired cursors return 400.

          trigger_type: Filter runs by what triggered them. Omit to return all runs.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
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
            "/v1/deployment_runs?beta=true",
            page=AsyncPageCursor[BetaManagedAgentsDeploymentRun],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "created_at_gt": created_at_gt,
                        "created_at_gte": created_at_gte,
                        "created_at_lt": created_at_lt,
                        "created_at_lte": created_at_lte,
                        "deployment_id": deployment_id,
                        "has_error": has_error,
                        "limit": limit,
                        "page": page,
                        "trigger_type": trigger_type,
                    },
                    deployment_run_list_params.DeploymentRunListParams,
                ),
            ),
            model=BetaManagedAgentsDeploymentRun,
        )


class DeploymentRunsWithRawResponse:
    def __init__(self, deployment_runs: DeploymentRuns) -> None:
        self._deployment_runs = deployment_runs

        self.retrieve = _legacy_response.to_raw_response_wrapper(
            deployment_runs.retrieve,
        )
        self.list = _legacy_response.to_raw_response_wrapper(
            deployment_runs.list,
        )


class AsyncDeploymentRunsWithRawResponse:
    def __init__(self, deployment_runs: AsyncDeploymentRuns) -> None:
        self._deployment_runs = deployment_runs

        self.retrieve = _legacy_response.async_to_raw_response_wrapper(
            deployment_runs.retrieve,
        )
        self.list = _legacy_response.async_to_raw_response_wrapper(
            deployment_runs.list,
        )


class DeploymentRunsWithStreamingResponse:
    def __init__(self, deployment_runs: DeploymentRuns) -> None:
        self._deployment_runs = deployment_runs

        self.retrieve = to_streamed_response_wrapper(
            deployment_runs.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            deployment_runs.list,
        )


class AsyncDeploymentRunsWithStreamingResponse:
    def __init__(self, deployment_runs: AsyncDeploymentRuns) -> None:
        self._deployment_runs = deployment_runs

        self.retrieve = async_to_streamed_response_wrapper(
            deployment_runs.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            deployment_runs.list,
        )
