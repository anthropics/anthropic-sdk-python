# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from datetime import datetime
from itertools import chain

import httpx

from ... import _legacy_response
from ..._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import is_given, path_template, maybe_transform, strip_not_given, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...pagination import SyncPageCursor, AsyncPageCursor
from ...types.beta import (
    BetaManagedAgentsScheduleParams,
    BetaManagedAgentsDeploymentStatus,
    deployment_list_params,
    deployment_create_params,
    deployment_update_params,
)
from ..._base_client import AsyncPaginator, make_request_options
from ...types.anthropic_beta_param import AnthropicBetaParam
from ...types.beta.beta_managed_agents_deployment import BetaManagedAgentsDeployment
from ...types.beta.beta_managed_agents_deployment_run import BetaManagedAgentsDeploymentRun
from ...types.beta.beta_managed_agents_schedule_params import BetaManagedAgentsScheduleParams
from ...types.beta.beta_managed_agents_deployment_status import BetaManagedAgentsDeploymentStatus
from ...types.beta.beta_managed_agents_deployment_initial_event_params import (
    BetaManagedAgentsDeploymentInitialEventParams,
)

__all__ = ["Deployments", "AsyncDeployments"]


class Deployments(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DeploymentsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return DeploymentsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DeploymentsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return DeploymentsWithStreamingResponse(self)

    def create(
        self,
        *,
        agent: deployment_create_params.Agent,
        environment_id: str,
        initial_events: Iterable[BetaManagedAgentsDeploymentInitialEventParams],
        name: str,
        description: Optional[str] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        resources: Iterable[deployment_create_params.Resource] | Omit = omit,
        schedule: Optional[BetaManagedAgentsScheduleParams] | Omit = omit,
        vault_ids: SequenceNotStr[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsDeployment:
        """Create Deployment

        Args:
          agent: Agent to deploy.

        Accepts the `agent` ID string, which pins the latest version,
              or an `agent` object with both id and version specified. The agent must exist
              and not be archived.

          environment_id: ID of the `environment` defining the container configuration for sessions
              created from this deployment.

          initial_events: Events to send to each session immediately after creation. At least 1,
              maximum 50.

          name: Human-readable name for the deployment.

          description: Description of what the deployment does.

          metadata: Arbitrary key-value metadata. Maximum 16 pairs, keys up to 64 chars, values up
              to 512 chars.

          resources: Resources (e.g. repositories, files) to mount into each session's container.
              Maximum 500.

          schedule: 5-field POSIX cron schedule. Literal wall-clock matching in the configured
              timezone.

          vault_ids: Vault IDs for stored credentials the agent can use during sessions created from
              this deployment. Maximum 50.

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
        return self._post(
            "/v1/deployments?beta=true",
            body=maybe_transform(
                {
                    "agent": agent,
                    "environment_id": environment_id,
                    "initial_events": initial_events,
                    "name": name,
                    "description": description,
                    "metadata": metadata,
                    "resources": resources,
                    "schedule": schedule,
                    "vault_ids": vault_ids,
                },
                deployment_create_params.DeploymentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaManagedAgentsDeployment,
        )

    def retrieve(
        self,
        deployment_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsDeployment:
        """
        Get Deployment

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
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
            path_template("/v1/deployments/{deployment_id}?beta=true", deployment_id=deployment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaManagedAgentsDeployment,
        )

    def update(
        self,
        deployment_id: str,
        *,
        agent: deployment_update_params.Agent | Omit = omit,
        description: Optional[str] | Omit = omit,
        environment_id: str | Omit = omit,
        initial_events: Iterable[BetaManagedAgentsDeploymentInitialEventParams] | Omit = omit,
        metadata: Optional[Dict[str, Optional[str]]] | Omit = omit,
        name: str | Omit = omit,
        resources: Optional[Iterable[deployment_update_params.Resource]] | Omit = omit,
        schedule: Optional[BetaManagedAgentsScheduleParams] | Omit = omit,
        vault_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsDeployment:
        """Update Deployment

        Args:
          agent: Agent to deploy.

        Accepts the `agent` ID string, which re-pins to the latest
              version, or an `agent` object with both id and version specified. Omit to
              preserve. Cannot be cleared.

          description: Description. Omit to preserve; send empty string or null to clear.

          environment_id: ID of the `environment` where sessions run. Omit to preserve. Cannot be cleared.

          initial_events: Initial events. Full replacement. Omit to preserve. Cannot be cleared. At least
              1, maximum 50.

          metadata: Metadata patch. Set a key to a string to upsert it, or to null to delete it.
              Omit the field to preserve. The stored bag is limited to 16 keys (up to 64 chars
              each) with values up to 512 chars.

          name: Human-readable name. Must be non-empty. Omit to preserve. Cannot be cleared.

          resources: Session resources. Full replacement. Omit to preserve; send empty array or null
              to clear. Maximum 500.

          schedule: 5-field POSIX cron schedule. Literal wall-clock matching in the configured
              timezone.

          vault_ids: Vault IDs. Full replacement. Omit to preserve; send empty array or null to
              clear. Maximum 50.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
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
            path_template("/v1/deployments/{deployment_id}?beta=true", deployment_id=deployment_id),
            body=maybe_transform(
                {
                    "agent": agent,
                    "description": description,
                    "environment_id": environment_id,
                    "initial_events": initial_events,
                    "metadata": metadata,
                    "name": name,
                    "resources": resources,
                    "schedule": schedule,
                    "vault_ids": vault_ids,
                },
                deployment_update_params.DeploymentUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaManagedAgentsDeployment,
        )

    def list(
        self,
        *,
        agent_id: str | Omit = omit,
        created_at_gte: Union[str, datetime] | Omit = omit,
        created_at_lte: Union[str, datetime] | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        status: BetaManagedAgentsDeploymentStatus | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaManagedAgentsDeployment]:
        """
        List Deployments

        Args:
          agent_id: Filter by agent ID.

          created_at_gte: Return deployments created at or after this time (inclusive).

          created_at_lte: Return deployments created at or before this time (inclusive).

          include_archived: When true, includes archived deployments. Default: false (exclude archived).

          limit: Maximum results per page. Default 20, maximum 100.

          page: Opaque pagination cursor.

          status: Filter by status: active or paused. Omit for both. To include archived
              deployments, use include_archived instead; the two cannot be combined.

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
            "/v1/deployments?beta=true",
            page=SyncPageCursor[BetaManagedAgentsDeployment],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "agent_id": agent_id,
                        "created_at_gte": created_at_gte,
                        "created_at_lte": created_at_lte,
                        "include_archived": include_archived,
                        "limit": limit,
                        "page": page,
                        "status": status,
                    },
                    deployment_list_params.DeploymentListParams,
                ),
            ),
            model=BetaManagedAgentsDeployment,
        )

    def archive(
        self,
        deployment_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsDeployment:
        """
        Archive Deployment

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
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
            path_template("/v1/deployments/{deployment_id}/archive?beta=true", deployment_id=deployment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaManagedAgentsDeployment,
        )

    def pause(
        self,
        deployment_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsDeployment:
        """
        Pause Deployment

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
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
            path_template("/v1/deployments/{deployment_id}/pause?beta=true", deployment_id=deployment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaManagedAgentsDeployment,
        )

    def run(
        self,
        deployment_id: str,
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
        Run Deployment Now

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
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
            path_template("/v1/deployments/{deployment_id}/run?beta=true", deployment_id=deployment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaManagedAgentsDeploymentRun,
        )

    def unpause(
        self,
        deployment_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsDeployment:
        """
        Unpause Deployment

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
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
            path_template("/v1/deployments/{deployment_id}/unpause?beta=true", deployment_id=deployment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaManagedAgentsDeployment,
        )


class AsyncDeployments(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDeploymentsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDeploymentsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDeploymentsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncDeploymentsWithStreamingResponse(self)

    async def create(
        self,
        *,
        agent: deployment_create_params.Agent,
        environment_id: str,
        initial_events: Iterable[BetaManagedAgentsDeploymentInitialEventParams],
        name: str,
        description: Optional[str] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        resources: Iterable[deployment_create_params.Resource] | Omit = omit,
        schedule: Optional[BetaManagedAgentsScheduleParams] | Omit = omit,
        vault_ids: SequenceNotStr[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsDeployment:
        """Create Deployment

        Args:
          agent: Agent to deploy.

        Accepts the `agent` ID string, which pins the latest version,
              or an `agent` object with both id and version specified. The agent must exist
              and not be archived.

          environment_id: ID of the `environment` defining the container configuration for sessions
              created from this deployment.

          initial_events: Events to send to each session immediately after creation. At least 1,
              maximum 50.

          name: Human-readable name for the deployment.

          description: Description of what the deployment does.

          metadata: Arbitrary key-value metadata. Maximum 16 pairs, keys up to 64 chars, values up
              to 512 chars.

          resources: Resources (e.g. repositories, files) to mount into each session's container.
              Maximum 500.

          schedule: 5-field POSIX cron schedule. Literal wall-clock matching in the configured
              timezone.

          vault_ids: Vault IDs for stored credentials the agent can use during sessions created from
              this deployment. Maximum 50.

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
        return await self._post(
            "/v1/deployments?beta=true",
            body=await async_maybe_transform(
                {
                    "agent": agent,
                    "environment_id": environment_id,
                    "initial_events": initial_events,
                    "name": name,
                    "description": description,
                    "metadata": metadata,
                    "resources": resources,
                    "schedule": schedule,
                    "vault_ids": vault_ids,
                },
                deployment_create_params.DeploymentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaManagedAgentsDeployment,
        )

    async def retrieve(
        self,
        deployment_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsDeployment:
        """
        Get Deployment

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
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
            path_template("/v1/deployments/{deployment_id}?beta=true", deployment_id=deployment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaManagedAgentsDeployment,
        )

    async def update(
        self,
        deployment_id: str,
        *,
        agent: deployment_update_params.Agent | Omit = omit,
        description: Optional[str] | Omit = omit,
        environment_id: str | Omit = omit,
        initial_events: Iterable[BetaManagedAgentsDeploymentInitialEventParams] | Omit = omit,
        metadata: Optional[Dict[str, Optional[str]]] | Omit = omit,
        name: str | Omit = omit,
        resources: Optional[Iterable[deployment_update_params.Resource]] | Omit = omit,
        schedule: Optional[BetaManagedAgentsScheduleParams] | Omit = omit,
        vault_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsDeployment:
        """Update Deployment

        Args:
          agent: Agent to deploy.

        Accepts the `agent` ID string, which re-pins to the latest
              version, or an `agent` object with both id and version specified. Omit to
              preserve. Cannot be cleared.

          description: Description. Omit to preserve; send empty string or null to clear.

          environment_id: ID of the `environment` where sessions run. Omit to preserve. Cannot be cleared.

          initial_events: Initial events. Full replacement. Omit to preserve. Cannot be cleared. At least
              1, maximum 50.

          metadata: Metadata patch. Set a key to a string to upsert it, or to null to delete it.
              Omit the field to preserve. The stored bag is limited to 16 keys (up to 64 chars
              each) with values up to 512 chars.

          name: Human-readable name. Must be non-empty. Omit to preserve. Cannot be cleared.

          resources: Session resources. Full replacement. Omit to preserve; send empty array or null
              to clear. Maximum 500.

          schedule: 5-field POSIX cron schedule. Literal wall-clock matching in the configured
              timezone.

          vault_ids: Vault IDs. Full replacement. Omit to preserve; send empty array or null to
              clear. Maximum 50.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
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
            path_template("/v1/deployments/{deployment_id}?beta=true", deployment_id=deployment_id),
            body=await async_maybe_transform(
                {
                    "agent": agent,
                    "description": description,
                    "environment_id": environment_id,
                    "initial_events": initial_events,
                    "metadata": metadata,
                    "name": name,
                    "resources": resources,
                    "schedule": schedule,
                    "vault_ids": vault_ids,
                },
                deployment_update_params.DeploymentUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaManagedAgentsDeployment,
        )

    def list(
        self,
        *,
        agent_id: str | Omit = omit,
        created_at_gte: Union[str, datetime] | Omit = omit,
        created_at_lte: Union[str, datetime] | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        status: BetaManagedAgentsDeploymentStatus | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaManagedAgentsDeployment, AsyncPageCursor[BetaManagedAgentsDeployment]]:
        """
        List Deployments

        Args:
          agent_id: Filter by agent ID.

          created_at_gte: Return deployments created at or after this time (inclusive).

          created_at_lte: Return deployments created at or before this time (inclusive).

          include_archived: When true, includes archived deployments. Default: false (exclude archived).

          limit: Maximum results per page. Default 20, maximum 100.

          page: Opaque pagination cursor.

          status: Filter by status: active or paused. Omit for both. To include archived
              deployments, use include_archived instead; the two cannot be combined.

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
            "/v1/deployments?beta=true",
            page=AsyncPageCursor[BetaManagedAgentsDeployment],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "agent_id": agent_id,
                        "created_at_gte": created_at_gte,
                        "created_at_lte": created_at_lte,
                        "include_archived": include_archived,
                        "limit": limit,
                        "page": page,
                        "status": status,
                    },
                    deployment_list_params.DeploymentListParams,
                ),
            ),
            model=BetaManagedAgentsDeployment,
        )

    async def archive(
        self,
        deployment_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsDeployment:
        """
        Archive Deployment

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
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
            path_template("/v1/deployments/{deployment_id}/archive?beta=true", deployment_id=deployment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaManagedAgentsDeployment,
        )

    async def pause(
        self,
        deployment_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsDeployment:
        """
        Pause Deployment

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
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
            path_template("/v1/deployments/{deployment_id}/pause?beta=true", deployment_id=deployment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaManagedAgentsDeployment,
        )

    async def run(
        self,
        deployment_id: str,
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
        Run Deployment Now

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
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
            path_template("/v1/deployments/{deployment_id}/run?beta=true", deployment_id=deployment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaManagedAgentsDeploymentRun,
        )

    async def unpause(
        self,
        deployment_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsDeployment:
        """
        Unpause Deployment

        Args:
          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
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
            path_template("/v1/deployments/{deployment_id}/unpause?beta=true", deployment_id=deployment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaManagedAgentsDeployment,
        )


class DeploymentsWithRawResponse:
    def __init__(self, deployments: Deployments) -> None:
        self._deployments = deployments

        self.create = _legacy_response.to_raw_response_wrapper(
            deployments.create,
        )
        self.retrieve = _legacy_response.to_raw_response_wrapper(
            deployments.retrieve,
        )
        self.update = _legacy_response.to_raw_response_wrapper(
            deployments.update,
        )
        self.list = _legacy_response.to_raw_response_wrapper(
            deployments.list,
        )
        self.archive = _legacy_response.to_raw_response_wrapper(
            deployments.archive,
        )
        self.pause = _legacy_response.to_raw_response_wrapper(
            deployments.pause,
        )
        self.run = _legacy_response.to_raw_response_wrapper(
            deployments.run,
        )
        self.unpause = _legacy_response.to_raw_response_wrapper(
            deployments.unpause,
        )


class AsyncDeploymentsWithRawResponse:
    def __init__(self, deployments: AsyncDeployments) -> None:
        self._deployments = deployments

        self.create = _legacy_response.async_to_raw_response_wrapper(
            deployments.create,
        )
        self.retrieve = _legacy_response.async_to_raw_response_wrapper(
            deployments.retrieve,
        )
        self.update = _legacy_response.async_to_raw_response_wrapper(
            deployments.update,
        )
        self.list = _legacy_response.async_to_raw_response_wrapper(
            deployments.list,
        )
        self.archive = _legacy_response.async_to_raw_response_wrapper(
            deployments.archive,
        )
        self.pause = _legacy_response.async_to_raw_response_wrapper(
            deployments.pause,
        )
        self.run = _legacy_response.async_to_raw_response_wrapper(
            deployments.run,
        )
        self.unpause = _legacy_response.async_to_raw_response_wrapper(
            deployments.unpause,
        )


class DeploymentsWithStreamingResponse:
    def __init__(self, deployments: Deployments) -> None:
        self._deployments = deployments

        self.create = to_streamed_response_wrapper(
            deployments.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            deployments.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            deployments.update,
        )
        self.list = to_streamed_response_wrapper(
            deployments.list,
        )
        self.archive = to_streamed_response_wrapper(
            deployments.archive,
        )
        self.pause = to_streamed_response_wrapper(
            deployments.pause,
        )
        self.run = to_streamed_response_wrapper(
            deployments.run,
        )
        self.unpause = to_streamed_response_wrapper(
            deployments.unpause,
        )


class AsyncDeploymentsWithStreamingResponse:
    def __init__(self, deployments: AsyncDeployments) -> None:
        self._deployments = deployments

        self.create = async_to_streamed_response_wrapper(
            deployments.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            deployments.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            deployments.update,
        )
        self.list = async_to_streamed_response_wrapper(
            deployments.list,
        )
        self.archive = async_to_streamed_response_wrapper(
            deployments.archive,
        )
        self.pause = async_to_streamed_response_wrapper(
            deployments.pause,
        )
        self.run = async_to_streamed_response_wrapper(
            deployments.run,
        )
        self.unpause = async_to_streamed_response_wrapper(
            deployments.unpause,
        )
