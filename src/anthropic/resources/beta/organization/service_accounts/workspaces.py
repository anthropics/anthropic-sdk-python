# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional

import httpx2

from ....._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ....._utils import is_given, path_template, maybe_transform, strip_not_given, async_maybe_transform
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
from .....types.beta.organization import BetaNoBillingWorkspaceRole
from .....types.anthropic_beta_param import AnthropicBetaParam
from .....types.beta.organization.service_accounts import workspace_add_params, workspace_list_params
from .....types.beta.organization.beta_no_billing_workspace_role import BetaNoBillingWorkspaceRole
from .....types.beta.organization.beta_service_account_workspace_member import BetaServiceAccountWorkspaceMember
from .....types.beta.organization.service_accounts.workspace_remove_response import WorkspaceRemoveResponse

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
        service_account_id: str,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaServiceAccountWorkspaceMember]:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        List the workspaces a service account is a member of.

        Each entry includes the service account's `workspace_role` in that workspace.
        Use `limit` and the `next_page` cursor to paginate. When the service account has
        no explicit default-workspace membership, the implicit (`implicit: true`)
        membership is returned as the first entry on the first page; with `limit=1` the
        first page may return up to 2 entries (the implicit entry plus one explicit
        membership) so a pagination cursor can be derived. Memberships are returned only
        while the service account is active. Without a `page` cursor, an archived
        service account returns an empty list. A `page` cursor that does not match an
        active membership returns a 400 invalid-request error. A cursor stops matching
        when the membership is removed, the workspace is deleted, or the service account
        is archived. Restart pagination from the first page to recover.

        Args:
          service_account_id: ID of the service account.

          limit: Number of results per page.

          page: Opaque cursor from a previous response's `next_page`.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not service_account_id:
            raise ValueError(f"Expected a non-empty value for `service_account_id` but received {service_account_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._get_api_list(
            path_template(
                "/v1/organizations/service_accounts/{service_account_id}/workspaces?beta=true",
                service_account_id=service_account_id,
            ),
            page=SyncPageCursor[BetaServiceAccountWorkspaceMember],
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
                    workspace_list_params.WorkspaceListParams,
                ),
            ),
            model=BetaServiceAccountWorkspaceMember,
        )

    def add(
        self,
        service_account_id: str,
        *,
        workspace_id: str,
        workspace_role: BetaNoBillingWorkspaceRole,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaServiceAccountWorkspaceMember:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Add a service account to a workspace with the given `workspace_role`.

        Mirror of `POST /workspaces/{workspace_id}/service_accounts`, addressed from the
        service-account side; both create the same membership. If the service account is
        already an explicit member of the workspace, its `workspace_role` is replaced
        with the value supplied here. Archived workspaces return 400. Archived service
        accounts cannot be added and are rejected.

        Args:
          service_account_id: ID of the service account.

          workspace_id: Tagged workspace ID to add the service account to.

          workspace_role: Role to assign to the service account in this workspace.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not service_account_id:
            raise ValueError(f"Expected a non-empty value for `service_account_id` but received {service_account_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._post(
            path_template(
                "/v1/organizations/service_accounts/{service_account_id}/workspaces?beta=true",
                service_account_id=service_account_id,
            ),
            body=maybe_transform(
                {
                    "workspace_id": workspace_id,
                    "workspace_role": workspace_role,
                },
                workspace_add_params.WorkspaceAddParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaServiceAccountWorkspaceMember,
        )

    def remove(
        self,
        workspace_id: str,
        *,
        service_account_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceRemoveResponse:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Remove a service account from a workspace.

        Mirror of
        `DELETE /workspaces/{workspace_id}/service_accounts/{service_account_id}`,
        addressed from the service-account side. Removal is idempotent (returns 200 even
        if the membership was already removed). A DELETE against the implicit
        default-workspace membership returns 200 but is a no-op and the membership
        persists; deleting an explicit default-workspace row reverts to the implicit
        `workspace_user` membership. Archived workspaces return 400.

        Args:
          service_account_id: ID of the service account.

          workspace_id: ID of the workspace.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not service_account_id:
            raise ValueError(f"Expected a non-empty value for `service_account_id` but received {service_account_id!r}")
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._delete(
            path_template(
                "/v1/organizations/service_accounts/{service_account_id}/workspaces/{workspace_id}?beta=true",
                service_account_id=service_account_id,
                workspace_id=workspace_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceRemoveResponse,
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
        service_account_id: str,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaServiceAccountWorkspaceMember, AsyncPageCursor[BetaServiceAccountWorkspaceMember]]:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        List the workspaces a service account is a member of.

        Each entry includes the service account's `workspace_role` in that workspace.
        Use `limit` and the `next_page` cursor to paginate. When the service account has
        no explicit default-workspace membership, the implicit (`implicit: true`)
        membership is returned as the first entry on the first page; with `limit=1` the
        first page may return up to 2 entries (the implicit entry plus one explicit
        membership) so a pagination cursor can be derived. Memberships are returned only
        while the service account is active. Without a `page` cursor, an archived
        service account returns an empty list. A `page` cursor that does not match an
        active membership returns a 400 invalid-request error. A cursor stops matching
        when the membership is removed, the workspace is deleted, or the service account
        is archived. Restart pagination from the first page to recover.

        Args:
          service_account_id: ID of the service account.

          limit: Number of results per page.

          page: Opaque cursor from a previous response's `next_page`.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not service_account_id:
            raise ValueError(f"Expected a non-empty value for `service_account_id` but received {service_account_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._get_api_list(
            path_template(
                "/v1/organizations/service_accounts/{service_account_id}/workspaces?beta=true",
                service_account_id=service_account_id,
            ),
            page=AsyncPageCursor[BetaServiceAccountWorkspaceMember],
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
                    workspace_list_params.WorkspaceListParams,
                ),
            ),
            model=BetaServiceAccountWorkspaceMember,
        )

    async def add(
        self,
        service_account_id: str,
        *,
        workspace_id: str,
        workspace_role: BetaNoBillingWorkspaceRole,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaServiceAccountWorkspaceMember:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Add a service account to a workspace with the given `workspace_role`.

        Mirror of `POST /workspaces/{workspace_id}/service_accounts`, addressed from the
        service-account side; both create the same membership. If the service account is
        already an explicit member of the workspace, its `workspace_role` is replaced
        with the value supplied here. Archived workspaces return 400. Archived service
        accounts cannot be added and are rejected.

        Args:
          service_account_id: ID of the service account.

          workspace_id: Tagged workspace ID to add the service account to.

          workspace_role: Role to assign to the service account in this workspace.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not service_account_id:
            raise ValueError(f"Expected a non-empty value for `service_account_id` but received {service_account_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._post(
            path_template(
                "/v1/organizations/service_accounts/{service_account_id}/workspaces?beta=true",
                service_account_id=service_account_id,
            ),
            body=await async_maybe_transform(
                {
                    "workspace_id": workspace_id,
                    "workspace_role": workspace_role,
                },
                workspace_add_params.WorkspaceAddParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaServiceAccountWorkspaceMember,
        )

    async def remove(
        self,
        workspace_id: str,
        *,
        service_account_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceRemoveResponse:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Remove a service account from a workspace.

        Mirror of
        `DELETE /workspaces/{workspace_id}/service_accounts/{service_account_id}`,
        addressed from the service-account side. Removal is idempotent (returns 200 even
        if the membership was already removed). A DELETE against the implicit
        default-workspace membership returns 200 but is a no-op and the membership
        persists; deleting an explicit default-workspace row reverts to the implicit
        `workspace_user` membership. Archived workspaces return 400.

        Args:
          service_account_id: ID of the service account.

          workspace_id: ID of the workspace.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not service_account_id:
            raise ValueError(f"Expected a non-empty value for `service_account_id` but received {service_account_id!r}")
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._delete(
            path_template(
                "/v1/organizations/service_accounts/{service_account_id}/workspaces/{workspace_id}?beta=true",
                service_account_id=service_account_id,
                workspace_id=workspace_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceRemoveResponse,
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
