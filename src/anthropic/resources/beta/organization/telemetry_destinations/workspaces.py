from __future__ import annotations

from typing import List
from itertools import chain

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
from .....types.anthropic_beta_param import AnthropicBetaParam
from .....types.beta.organization.telemetry_destinations.beta_telemetry_destination_workspace import (
    BetaTelemetryDestinationWorkspace,
)
from .....types.beta.organization.telemetry_destinations.beta_deleted_telemetry_destination_workspace import (
    BetaDeletedTelemetryDestinationWorkspace,
)

__all__ = ["Workspaces", "AsyncWorkspaces"]


class Workspaces(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> WorkspacesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return WorkspacesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WorkspacesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return WorkspacesWithStreamingResponse(self)

    def list(
        self,
        destination_id: str,
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
    ) -> SyncPageCursor[BetaTelemetryDestinationWorkspace]:
        """
        List the workspaces on a destination's workspace list, newest entry first.

        A destination whose `workspaces.type` is `all` doesn't have a list, so its page
        is empty. The list includes archived workspaces.

        See the
        [OpenTelemetry export guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry#choose-workspaces-for-a-destination)
        to learn more about choosing the workspaces of a destination.

        Args:
          destination_id: ID of the destination (`tdst_...`).

          limit: Number of entries to return per page, between 1 and 1,000. Defaults to 20.

          page: Opaque cursor from a previous response's `next_page`. Leave it out to get the
              first page.

          betas: This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not destination_id:
            raise ValueError(f"Expected a non-empty value for `destination_id` but received {destination_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["telemetry-destinations-2026-08-11"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "telemetry-destinations-2026-08-11", **(extra_headers or {})}
        return self._get_api_list(
            path_template(
                "/v1/organizations/telemetry_destinations/{destination_id}/workspaces?beta=true",
                destination_id=destination_id,
            ),
            page=SyncPageCursor[BetaTelemetryDestinationWorkspace],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "page": page,
                },
                span_name="anthropic.organization.telemetry_destinations.workspaces.list",
                span_route="/v1/organizations/telemetry_destinations/{destination_id}/workspaces",
                span_attributes={"anthropic.organization.telemetry_destination.id": destination_id},
            ),
            model=BetaTelemetryDestinationWorkspace,
        )

    def add(
        self,
        workspace_id: str,
        *,
        destination_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaTelemetryDestinationWorkspace:
        """
        Add one workspace to a destination's workspace list.

        Under `include` the workspace's spans start going to the destination. Under
        `exclude` they stop. A list holds at most 1,000 workspaces.

        Adding a workspace that is already on the list changes nothing and returns the
        existing entry. An archived workspace that isn't on the list yet can't be added.
        A destination whose `workspaces.type` is `all` doesn't have a list, so the API
        returns 400. To change which workspaces such a destination covers, update its
        `workspaces`.

        See the
        [OpenTelemetry export guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry#choose-workspaces-for-a-destination)
        to learn more about choosing the workspaces of a destination.

        Args:
          destination_id: ID of the destination (`tdst_...`).

          workspace_id: ID of the workspace to add (`wrkspc_...`).

          betas: This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not destination_id:
            raise ValueError(f"Expected a non-empty value for `destination_id` but received {destination_id!r}")
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["telemetry-destinations-2026-08-11"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "telemetry-destinations-2026-08-11", **(extra_headers or {})}
        return self._post(
            path_template(
                "/v1/organizations/telemetry_destinations/{destination_id}/workspaces/{workspace_id}?beta=true",
                destination_id=destination_id,
                workspace_id=workspace_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.organization.telemetry_destinations.workspaces.add",
                span_route="/v1/organizations/telemetry_destinations/{destination_id}/workspaces/{workspace_id}",
                span_attributes={
                    "anthropic.organization.telemetry_destination.id": destination_id,
                    "anthropic.organization.telemetry_destination.workspace.id": workspace_id,
                },
            ),
            cast_to=BetaTelemetryDestinationWorkspace,
        )

    def remove(
        self,
        workspace_id: str,
        *,
        destination_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDeletedTelemetryDestinationWorkspace:
        """
        Remove one workspace from a destination's workspace list.

        Under `include` the workspace's spans stop going to the destination. Under
        `exclude` they start. An archived workspace can be removed too.

        The API returns 404 when the workspace isn't on the list. A destination whose
        `workspaces.type` is `all` doesn't have a list, so the API returns 400.

        See the
        [OpenTelemetry export guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry#choose-workspaces-for-a-destination)
        to learn more about choosing the workspaces of a destination.

        Args:
          destination_id: ID of the destination (`tdst_...`).

          workspace_id: ID of the workspace to remove (`wrkspc_...`).

          betas: This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not destination_id:
            raise ValueError(f"Expected a non-empty value for `destination_id` but received {destination_id!r}")
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["telemetry-destinations-2026-08-11"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "telemetry-destinations-2026-08-11", **(extra_headers or {})}
        return self._delete(
            path_template(
                "/v1/organizations/telemetry_destinations/{destination_id}/workspaces/{workspace_id}?beta=true",
                destination_id=destination_id,
                workspace_id=workspace_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.organization.telemetry_destinations.workspaces.remove",
                span_route="/v1/organizations/telemetry_destinations/{destination_id}/workspaces/{workspace_id}",
                span_attributes={
                    "anthropic.organization.telemetry_destination.id": destination_id,
                    "anthropic.organization.telemetry_destination.workspace.id": workspace_id,
                },
            ),
            cast_to=BetaDeletedTelemetryDestinationWorkspace,
        )


class AsyncWorkspaces(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncWorkspacesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncWorkspacesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWorkspacesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncWorkspacesWithStreamingResponse(self)

    def list(
        self,
        destination_id: str,
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
    ) -> AsyncPaginator[BetaTelemetryDestinationWorkspace, AsyncPageCursor[BetaTelemetryDestinationWorkspace]]:
        """
        List the workspaces on a destination's workspace list, newest entry first.

        A destination whose `workspaces.type` is `all` doesn't have a list, so its page
        is empty. The list includes archived workspaces.

        See the
        [OpenTelemetry export guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry#choose-workspaces-for-a-destination)
        to learn more about choosing the workspaces of a destination.

        Args:
          destination_id: ID of the destination (`tdst_...`).

          limit: Number of entries to return per page, between 1 and 1,000. Defaults to 20.

          page: Opaque cursor from a previous response's `next_page`. Leave it out to get the
              first page.

          betas: This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not destination_id:
            raise ValueError(f"Expected a non-empty value for `destination_id` but received {destination_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["telemetry-destinations-2026-08-11"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "telemetry-destinations-2026-08-11", **(extra_headers or {})}
        return self._get_api_list(
            path_template(
                "/v1/organizations/telemetry_destinations/{destination_id}/workspaces?beta=true",
                destination_id=destination_id,
            ),
            page=AsyncPageCursor[BetaTelemetryDestinationWorkspace],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "page": page,
                },
                span_name="anthropic.organization.telemetry_destinations.workspaces.list",
                span_route="/v1/organizations/telemetry_destinations/{destination_id}/workspaces",
                span_attributes={"anthropic.organization.telemetry_destination.id": destination_id},
            ),
            model=BetaTelemetryDestinationWorkspace,
        )

    async def add(
        self,
        workspace_id: str,
        *,
        destination_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaTelemetryDestinationWorkspace:
        """
        Add one workspace to a destination's workspace list.

        Under `include` the workspace's spans start going to the destination. Under
        `exclude` they stop. A list holds at most 1,000 workspaces.

        Adding a workspace that is already on the list changes nothing and returns the
        existing entry. An archived workspace that isn't on the list yet can't be added.
        A destination whose `workspaces.type` is `all` doesn't have a list, so the API
        returns 400. To change which workspaces such a destination covers, update its
        `workspaces`.

        See the
        [OpenTelemetry export guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry#choose-workspaces-for-a-destination)
        to learn more about choosing the workspaces of a destination.

        Args:
          destination_id: ID of the destination (`tdst_...`).

          workspace_id: ID of the workspace to add (`wrkspc_...`).

          betas: This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not destination_id:
            raise ValueError(f"Expected a non-empty value for `destination_id` but received {destination_id!r}")
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["telemetry-destinations-2026-08-11"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "telemetry-destinations-2026-08-11", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/v1/organizations/telemetry_destinations/{destination_id}/workspaces/{workspace_id}?beta=true",
                destination_id=destination_id,
                workspace_id=workspace_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.organization.telemetry_destinations.workspaces.add",
                span_route="/v1/organizations/telemetry_destinations/{destination_id}/workspaces/{workspace_id}",
                span_attributes={
                    "anthropic.organization.telemetry_destination.id": destination_id,
                    "anthropic.organization.telemetry_destination.workspace.id": workspace_id,
                },
            ),
            cast_to=BetaTelemetryDestinationWorkspace,
        )

    async def remove(
        self,
        workspace_id: str,
        *,
        destination_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDeletedTelemetryDestinationWorkspace:
        """
        Remove one workspace from a destination's workspace list.

        Under `include` the workspace's spans stop going to the destination. Under
        `exclude` they start. An archived workspace can be removed too.

        The API returns 404 when the workspace isn't on the list. A destination whose
        `workspaces.type` is `all` doesn't have a list, so the API returns 400.

        See the
        [OpenTelemetry export guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry#choose-workspaces-for-a-destination)
        to learn more about choosing the workspaces of a destination.

        Args:
          destination_id: ID of the destination (`tdst_...`).

          workspace_id: ID of the workspace to remove (`wrkspc_...`).

          betas: This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not destination_id:
            raise ValueError(f"Expected a non-empty value for `destination_id` but received {destination_id!r}")
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["telemetry-destinations-2026-08-11"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "telemetry-destinations-2026-08-11", **(extra_headers or {})}
        return await self._delete(
            path_template(
                "/v1/organizations/telemetry_destinations/{destination_id}/workspaces/{workspace_id}?beta=true",
                destination_id=destination_id,
                workspace_id=workspace_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.organization.telemetry_destinations.workspaces.remove",
                span_route="/v1/organizations/telemetry_destinations/{destination_id}/workspaces/{workspace_id}",
                span_attributes={
                    "anthropic.organization.telemetry_destination.id": destination_id,
                    "anthropic.organization.telemetry_destination.workspace.id": workspace_id,
                },
            ),
            cast_to=BetaDeletedTelemetryDestinationWorkspace,
        )


class WorkspacesWithRawResponse:
    def __init__(self, workspaces: Workspaces) -> None:
        self._workspaces = workspaces

        self.list = to_raw_response_wrapper(
            workspaces.list,
        )
        self.add = to_raw_response_wrapper(
            workspaces.add,
        )
        self.remove = to_raw_response_wrapper(
            workspaces.remove,
        )


class AsyncWorkspacesWithRawResponse:
    def __init__(self, workspaces: AsyncWorkspaces) -> None:
        self._workspaces = workspaces

        self.list = async_to_raw_response_wrapper(
            workspaces.list,
        )
        self.add = async_to_raw_response_wrapper(
            workspaces.add,
        )
        self.remove = async_to_raw_response_wrapper(
            workspaces.remove,
        )


class WorkspacesWithStreamingResponse:
    def __init__(self, workspaces: Workspaces) -> None:
        self._workspaces = workspaces

        self.list = to_streamed_response_wrapper(
            workspaces.list,
        )
        self.add = to_streamed_response_wrapper(
            workspaces.add,
        )
        self.remove = to_streamed_response_wrapper(
            workspaces.remove,
        )


class AsyncWorkspacesWithStreamingResponse:
    def __init__(self, workspaces: AsyncWorkspaces) -> None:
        self._workspaces = workspaces

        self.list = async_to_streamed_response_wrapper(
            workspaces.list,
        )
        self.add = async_to_streamed_response_wrapper(
            workspaces.add,
        )
        self.remove = async_to_streamed_response_wrapper(
            workspaces.remove,
        )
