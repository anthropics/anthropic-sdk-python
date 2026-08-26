# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Optional

import httpx2

from .members import (
    Members,
    AsyncMembers,
    MembersWithRawResponse,
    AsyncMembersWithRawResponse,
    MembersWithStreamingResponse,
    AsyncMembersWithStreamingResponse,
)
from ....._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ....._utils import is_given, path_template, maybe_transform, strip_not_given, async_maybe_transform
from ....._compat import cached_property
from .rate_limits import (
    RateLimits,
    AsyncRateLimits,
    RateLimitsWithRawResponse,
    AsyncRateLimitsWithRawResponse,
    RateLimitsWithStreamingResponse,
    AsyncRateLimitsWithStreamingResponse,
)
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .....pagination import SyncPage, AsyncPage
from ....._base_client import AsyncPaginator, make_request_options
from .service_accounts import (
    ServiceAccounts,
    AsyncServiceAccounts,
    ServiceAccountsWithRawResponse,
    AsyncServiceAccountsWithRawResponse,
    ServiceAccountsWithStreamingResponse,
    AsyncServiceAccountsWithStreamingResponse,
)
from .....types.beta.organization import (
    workspace_list_params,
    workspace_create_params,
    workspace_update_params,
)
from .....types.anthropic_beta_param import AnthropicBetaParam
from .....types.beta.organization.beta_workspace import BetaWorkspace
from .....types.beta.organization.beta_data_residency_create_config_param import BetaDataResidencyCreateConfigParam
from .....types.beta.organization.beta_data_residency_update_config_param import BetaDataResidencyUpdateConfigParam

__all__ = ["Workspaces", "AsyncWorkspaces"]


class Workspaces(SyncAPIResource):
    @cached_property
    def rate_limits(self) -> RateLimits:
        return RateLimits(self._client)

    @cached_property
    def members(self) -> Members:
        return Members(self._client)

    @cached_property
    def service_accounts(self) -> ServiceAccounts:
        return ServiceAccounts(self._client)

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

    def create(
        self,
        *,
        name: str,
        data_residency: Optional[BetaDataResidencyCreateConfigParam] | Omit = omit,
        display_color: Optional[str] | Omit = omit,
        external_key_id: Optional[str] | Omit = omit,
        tags: Optional[Dict[str, str]] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaWorkspace:
        """
        Create Workspace

        Args:
          name: Name of the Workspace.

          data_residency: Data residency configuration for the workspace. If omitted, defaults to
              `workspace_geo: "us"`, `allowed_inference_geos: "unrestricted"`, and
              `default_inference_geo: "global"`.

          display_color: Hex color code representing the Workspace in the Anthropic Console.

          external_key_id: ID of the customer-managed encryption key (CMEK) configuration to use for this
              Workspace. Setting this field requires CMEK to be enabled for your organization.
              When set, data stored for this Workspace is encrypted with the referenced key.
              Create key configurations with the External Keys API. This field is write-once:
              once a key is attached to a Workspace it cannot be detached or replaced. To
              rotate key material, rotate the underlying key on your cloud KMS; the
              `external_key_id` stays the same.

          tags: User-defined tags as string key-value pairs. Keys may not begin with
              `anthropic`.

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
        return self._post(
            "/v1/organizations/workspaces?beta=true",
            body=maybe_transform(
                {
                    "name": name,
                    "data_residency": data_residency,
                    "display_color": display_color,
                    "external_key_id": external_key_id,
                    "tags": tags,
                },
                workspace_create_params.WorkspaceCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaWorkspace,
        )

    def retrieve(
        self,
        workspace_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaWorkspace:
        """
        Get Workspace

        Args:
          workspace_id: ID of the Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return self._get(
            path_template("/v1/organizations/workspaces/{workspace_id}?beta=true", workspace_id=workspace_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaWorkspace,
        )

    def update(
        self,
        workspace_id: str,
        *,
        data_residency: Optional[BetaDataResidencyUpdateConfigParam] | Omit = omit,
        display_color: str | Omit = omit,
        external_key_id: str | Omit = omit,
        name: str | Omit = omit,
        tags: Optional[Dict[str, Optional[str]]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaWorkspace:
        """
        Update Workspace

        Args:
          data_residency: Data residency configuration for the workspace.

          display_color: Hex color code representing the Workspace in the Anthropic Console.

          external_key_id: ID of the customer-managed encryption key (CMEK) configuration to use for this
              Workspace. Setting this field requires CMEK to be enabled for your organization.
              When set, data stored for this Workspace is encrypted with the referenced key.
              Create key configurations with the External Keys API. This field is write-once:
              once a key is attached to a Workspace it cannot be detached or replaced. To
              rotate key material, rotate the underlying key on your cloud KMS; the
              `external_key_id` stays the same.

          name: Name of the Workspace.

          tags: User-defined tags as string key-value pairs. Keys may not begin with
              `anthropic`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return self._post(
            path_template("/v1/organizations/workspaces/{workspace_id}?beta=true", workspace_id=workspace_id),
            body=maybe_transform(
                {
                    "data_residency": data_residency,
                    "display_color": display_color,
                    "external_key_id": external_key_id,
                    "name": name,
                    "tags": tags,
                },
                workspace_update_params.WorkspaceUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaWorkspace,
        )

    def list(
        self,
        *,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPage[BetaWorkspace]:
        """
        List Workspaces

        Args:
          after_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately after this object.

          before_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately before this object.

          include_archived: Whether to include Workspaces that have been archived in the response

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `1000`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/workspaces?beta=true",
            page=SyncPage[BetaWorkspace],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "include_archived": include_archived,
                        "limit": limit,
                    },
                    workspace_list_params.WorkspaceListParams,
                ),
            ),
            model=BetaWorkspace,
        )

    def archive(
        self,
        workspace_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaWorkspace:
        """
        Archive Workspace

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return self._post(
            path_template("/v1/organizations/workspaces/{workspace_id}/archive?beta=true", workspace_id=workspace_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaWorkspace,
        )


class AsyncWorkspaces(AsyncAPIResource):
    @cached_property
    def rate_limits(self) -> AsyncRateLimits:
        return AsyncRateLimits(self._client)

    @cached_property
    def members(self) -> AsyncMembers:
        return AsyncMembers(self._client)

    @cached_property
    def service_accounts(self) -> AsyncServiceAccounts:
        return AsyncServiceAccounts(self._client)

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

    async def create(
        self,
        *,
        name: str,
        data_residency: Optional[BetaDataResidencyCreateConfigParam] | Omit = omit,
        display_color: Optional[str] | Omit = omit,
        external_key_id: Optional[str] | Omit = omit,
        tags: Optional[Dict[str, str]] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaWorkspace:
        """
        Create Workspace

        Args:
          name: Name of the Workspace.

          data_residency: Data residency configuration for the workspace. If omitted, defaults to
              `workspace_geo: "us"`, `allowed_inference_geos: "unrestricted"`, and
              `default_inference_geo: "global"`.

          display_color: Hex color code representing the Workspace in the Anthropic Console.

          external_key_id: ID of the customer-managed encryption key (CMEK) configuration to use for this
              Workspace. Setting this field requires CMEK to be enabled for your organization.
              When set, data stored for this Workspace is encrypted with the referenced key.
              Create key configurations with the External Keys API. This field is write-once:
              once a key is attached to a Workspace it cannot be detached or replaced. To
              rotate key material, rotate the underlying key on your cloud KMS; the
              `external_key_id` stays the same.

          tags: User-defined tags as string key-value pairs. Keys may not begin with
              `anthropic`.

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
        return await self._post(
            "/v1/organizations/workspaces?beta=true",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "data_residency": data_residency,
                    "display_color": display_color,
                    "external_key_id": external_key_id,
                    "tags": tags,
                },
                workspace_create_params.WorkspaceCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaWorkspace,
        )

    async def retrieve(
        self,
        workspace_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaWorkspace:
        """
        Get Workspace

        Args:
          workspace_id: ID of the Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return await self._get(
            path_template("/v1/organizations/workspaces/{workspace_id}?beta=true", workspace_id=workspace_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaWorkspace,
        )

    async def update(
        self,
        workspace_id: str,
        *,
        data_residency: Optional[BetaDataResidencyUpdateConfigParam] | Omit = omit,
        display_color: str | Omit = omit,
        external_key_id: str | Omit = omit,
        name: str | Omit = omit,
        tags: Optional[Dict[str, Optional[str]]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaWorkspace:
        """
        Update Workspace

        Args:
          data_residency: Data residency configuration for the workspace.

          display_color: Hex color code representing the Workspace in the Anthropic Console.

          external_key_id: ID of the customer-managed encryption key (CMEK) configuration to use for this
              Workspace. Setting this field requires CMEK to be enabled for your organization.
              When set, data stored for this Workspace is encrypted with the referenced key.
              Create key configurations with the External Keys API. This field is write-once:
              once a key is attached to a Workspace it cannot be detached or replaced. To
              rotate key material, rotate the underlying key on your cloud KMS; the
              `external_key_id` stays the same.

          name: Name of the Workspace.

          tags: User-defined tags as string key-value pairs. Keys may not begin with
              `anthropic`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return await self._post(
            path_template("/v1/organizations/workspaces/{workspace_id}?beta=true", workspace_id=workspace_id),
            body=await async_maybe_transform(
                {
                    "data_residency": data_residency,
                    "display_color": display_color,
                    "external_key_id": external_key_id,
                    "name": name,
                    "tags": tags,
                },
                workspace_update_params.WorkspaceUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaWorkspace,
        )

    def list(
        self,
        *,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaWorkspace, AsyncPage[BetaWorkspace]]:
        """
        List Workspaces

        Args:
          after_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately after this object.

          before_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately before this object.

          include_archived: Whether to include Workspaces that have been archived in the response

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `1000`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/workspaces?beta=true",
            page=AsyncPage[BetaWorkspace],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "include_archived": include_archived,
                        "limit": limit,
                    },
                    workspace_list_params.WorkspaceListParams,
                ),
            ),
            model=BetaWorkspace,
        )

    async def archive(
        self,
        workspace_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaWorkspace:
        """
        Archive Workspace

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return await self._post(
            path_template("/v1/organizations/workspaces/{workspace_id}/archive?beta=true", workspace_id=workspace_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaWorkspace,
        )


class WorkspacesWithRawResponse:
    def __init__(self, workspaces: Workspaces) -> None:
        self._workspaces = workspaces

        self.create = to_raw_response_wrapper(
            workspaces.create,
        )
        self.retrieve = to_raw_response_wrapper(
            workspaces.retrieve,
        )
        self.update = to_raw_response_wrapper(
            workspaces.update,
        )
        self.list = to_raw_response_wrapper(
            workspaces.list,
        )
        self.archive = to_raw_response_wrapper(
            workspaces.archive,
        )

    @cached_property
    def rate_limits(self) -> RateLimitsWithRawResponse:
        return RateLimitsWithRawResponse(self._workspaces.rate_limits)

    @cached_property
    def members(self) -> MembersWithRawResponse:
        return MembersWithRawResponse(self._workspaces.members)

    @cached_property
    def service_accounts(self) -> ServiceAccountsWithRawResponse:
        return ServiceAccountsWithRawResponse(self._workspaces.service_accounts)


class AsyncWorkspacesWithRawResponse:
    def __init__(self, workspaces: AsyncWorkspaces) -> None:
        self._workspaces = workspaces

        self.create = async_to_raw_response_wrapper(
            workspaces.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            workspaces.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            workspaces.update,
        )
        self.list = async_to_raw_response_wrapper(
            workspaces.list,
        )
        self.archive = async_to_raw_response_wrapper(
            workspaces.archive,
        )

    @cached_property
    def rate_limits(self) -> AsyncRateLimitsWithRawResponse:
        return AsyncRateLimitsWithRawResponse(self._workspaces.rate_limits)

    @cached_property
    def members(self) -> AsyncMembersWithRawResponse:
        return AsyncMembersWithRawResponse(self._workspaces.members)

    @cached_property
    def service_accounts(self) -> AsyncServiceAccountsWithRawResponse:
        return AsyncServiceAccountsWithRawResponse(self._workspaces.service_accounts)


class WorkspacesWithStreamingResponse:
    def __init__(self, workspaces: Workspaces) -> None:
        self._workspaces = workspaces

        self.create = to_streamed_response_wrapper(
            workspaces.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            workspaces.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            workspaces.update,
        )
        self.list = to_streamed_response_wrapper(
            workspaces.list,
        )
        self.archive = to_streamed_response_wrapper(
            workspaces.archive,
        )

    @cached_property
    def rate_limits(self) -> RateLimitsWithStreamingResponse:
        return RateLimitsWithStreamingResponse(self._workspaces.rate_limits)

    @cached_property
    def members(self) -> MembersWithStreamingResponse:
        return MembersWithStreamingResponse(self._workspaces.members)

    @cached_property
    def service_accounts(self) -> ServiceAccountsWithStreamingResponse:
        return ServiceAccountsWithStreamingResponse(self._workspaces.service_accounts)


class AsyncWorkspacesWithStreamingResponse:
    def __init__(self, workspaces: AsyncWorkspaces) -> None:
        self._workspaces = workspaces

        self.create = async_to_streamed_response_wrapper(
            workspaces.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            workspaces.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            workspaces.update,
        )
        self.list = async_to_streamed_response_wrapper(
            workspaces.list,
        )
        self.archive = async_to_streamed_response_wrapper(
            workspaces.archive,
        )

    @cached_property
    def rate_limits(self) -> AsyncRateLimitsWithStreamingResponse:
        return AsyncRateLimitsWithStreamingResponse(self._workspaces.rate_limits)

    @cached_property
    def members(self) -> AsyncMembersWithStreamingResponse:
        return AsyncMembersWithStreamingResponse(self._workspaces.members)

    @cached_property
    def service_accounts(self) -> AsyncServiceAccountsWithStreamingResponse:
        return AsyncServiceAccountsWithStreamingResponse(self._workspaces.service_accounts)
