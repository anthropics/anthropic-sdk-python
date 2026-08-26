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
from .....types.beta.organization.workspaces import (
    service_account_add_params,
    service_account_list_params,
    service_account_update_params,
)
from .....types.beta.organization.beta_no_billing_workspace_role import BetaNoBillingWorkspaceRole
from .....types.beta.organization.beta_service_account_workspace_member import BetaServiceAccountWorkspaceMember
from .....types.beta.organization.workspaces.service_account_remove_response import ServiceAccountRemoveResponse

__all__ = ["ServiceAccounts", "AsyncServiceAccounts"]


class ServiceAccounts(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ServiceAccountsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return ServiceAccountsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ServiceAccountsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return ServiceAccountsWithStreamingResponse(self)

    def retrieve(
        self,
        service_account_id: str,
        *,
        workspace_id: str,
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

        Retrieve a service account's membership in a workspace.

        Returns the membership record, including the service account's `workspace_role`
        in this workspace. Archived workspaces return 400. For the default workspace,
        returns the implicit (`implicit: true`) membership when no explicit membership
        exists; an explicitly added membership is returned with its assigned role. An
        archived service account returns 404.

        Args:
          workspace_id: ID of the workspace.

          service_account_id: ID of the service account.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        if not service_account_id:
            raise ValueError(f"Expected a non-empty value for `service_account_id` but received {service_account_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._get(
            path_template(
                "/v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}?beta=true",
                workspace_id=workspace_id,
                service_account_id=service_account_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaServiceAccountWorkspaceMember,
        )

    def update(
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

        Change a service account's role in a workspace.

        The new `workspace_role` replaces the current one. Only explicit memberships can
        be updated; to set a role on the implicit default-workspace membership, add the
        service account explicitly with
        `POST /workspaces/{workspace_id}/service_accounts`. Archived workspaces
        return 400. Archived service accounts cannot be updated and are rejected.

        Args:
          workspace_id: ID of the workspace.

          service_account_id: ID of the service account.

          workspace_role: New role for the service account in this workspace.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        if not service_account_id:
            raise ValueError(f"Expected a non-empty value for `service_account_id` but received {service_account_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._post(
            path_template(
                "/v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}?beta=true",
                workspace_id=workspace_id,
                service_account_id=service_account_id,
            ),
            body=maybe_transform(
                {"workspace_role": workspace_role}, service_account_update_params.ServiceAccountUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaServiceAccountWorkspaceMember,
        )

    def list(
        self,
        workspace_id: str,
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

        List the service accounts that are members of a workspace.

        Each entry includes the service account's `workspace_role`. Use `limit` and the
        `next_page` cursor to paginate. Archived workspaces return 400; use
        `GET /service_accounts/{id}/workspaces` to audit memberships of an archived
        workspace. The implicit default-workspace membership is not included in this
        list. Memberships of archived service accounts are omitted from the results.

        Args:
          workspace_id: ID of the workspace.

          limit: Number of results per page.

          page: Opaque cursor from a previous response's `next_page`.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._get_api_list(
            path_template(
                "/v1/organizations/workspaces/{workspace_id}/service_accounts?beta=true", workspace_id=workspace_id
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
                    service_account_list_params.ServiceAccountListParams,
                ),
            ),
            model=BetaServiceAccountWorkspaceMember,
        )

    def add(
        self,
        workspace_id: str,
        *,
        service_account_id: str,
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

        The role determines what the service account can do in the workspace and which
        workspace-scoped permissions it can be granted when authenticating through
        federation. Every service account is already an implicit `workspace_user` member
        of the default workspace; adding it explicitly assigns a chosen role. If the
        service account is already an explicit member of the workspace, its
        `workspace_role` is replaced with the value supplied here. Archived workspaces
        return 400. Archived service accounts cannot be added and are rejected.

        Args:
          workspace_id: ID of the workspace.

          service_account_id: Tagged service account ID to add.

          workspace_role: Role to assign to the service account in this workspace.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._post(
            path_template(
                "/v1/organizations/workspaces/{workspace_id}/service_accounts?beta=true", workspace_id=workspace_id
            ),
            body=maybe_transform(
                {
                    "service_account_id": service_account_id,
                    "workspace_role": workspace_role,
                },
                service_account_add_params.ServiceAccountAddParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaServiceAccountWorkspaceMember,
        )

    def remove(
        self,
        service_account_id: str,
        *,
        workspace_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> ServiceAccountRemoveResponse:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Remove a service account from a workspace.

        Removal is idempotent (returns 200 even if the membership was already removed).
        A DELETE against the implicit default-workspace membership returns 200 but is a
        no-op and the membership persists; deleting an explicit default-workspace row
        reverts to the implicit `workspace_user` membership. Archived workspaces
        return 400.

        Args:
          workspace_id: ID of the workspace.

          service_account_id: ID of the service account.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        if not service_account_id:
            raise ValueError(f"Expected a non-empty value for `service_account_id` but received {service_account_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._delete(
            path_template(
                "/v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}?beta=true",
                workspace_id=workspace_id,
                service_account_id=service_account_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ServiceAccountRemoveResponse,
        )


class AsyncServiceAccounts(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncServiceAccountsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncServiceAccountsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncServiceAccountsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncServiceAccountsWithStreamingResponse(self)

    async def retrieve(
        self,
        service_account_id: str,
        *,
        workspace_id: str,
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

        Retrieve a service account's membership in a workspace.

        Returns the membership record, including the service account's `workspace_role`
        in this workspace. Archived workspaces return 400. For the default workspace,
        returns the implicit (`implicit: true`) membership when no explicit membership
        exists; an explicitly added membership is returned with its assigned role. An
        archived service account returns 404.

        Args:
          workspace_id: ID of the workspace.

          service_account_id: ID of the service account.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        if not service_account_id:
            raise ValueError(f"Expected a non-empty value for `service_account_id` but received {service_account_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._get(
            path_template(
                "/v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}?beta=true",
                workspace_id=workspace_id,
                service_account_id=service_account_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaServiceAccountWorkspaceMember,
        )

    async def update(
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

        Change a service account's role in a workspace.

        The new `workspace_role` replaces the current one. Only explicit memberships can
        be updated; to set a role on the implicit default-workspace membership, add the
        service account explicitly with
        `POST /workspaces/{workspace_id}/service_accounts`. Archived workspaces
        return 400. Archived service accounts cannot be updated and are rejected.

        Args:
          workspace_id: ID of the workspace.

          service_account_id: ID of the service account.

          workspace_role: New role for the service account in this workspace.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        if not service_account_id:
            raise ValueError(f"Expected a non-empty value for `service_account_id` but received {service_account_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._post(
            path_template(
                "/v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}?beta=true",
                workspace_id=workspace_id,
                service_account_id=service_account_id,
            ),
            body=await async_maybe_transform(
                {"workspace_role": workspace_role}, service_account_update_params.ServiceAccountUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaServiceAccountWorkspaceMember,
        )

    def list(
        self,
        workspace_id: str,
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

        List the service accounts that are members of a workspace.

        Each entry includes the service account's `workspace_role`. Use `limit` and the
        `next_page` cursor to paginate. Archived workspaces return 400; use
        `GET /service_accounts/{id}/workspaces` to audit memberships of an archived
        workspace. The implicit default-workspace membership is not included in this
        list. Memberships of archived service accounts are omitted from the results.

        Args:
          workspace_id: ID of the workspace.

          limit: Number of results per page.

          page: Opaque cursor from a previous response's `next_page`.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return self._get_api_list(
            path_template(
                "/v1/organizations/workspaces/{workspace_id}/service_accounts?beta=true", workspace_id=workspace_id
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
                    service_account_list_params.ServiceAccountListParams,
                ),
            ),
            model=BetaServiceAccountWorkspaceMember,
        )

    async def add(
        self,
        workspace_id: str,
        *,
        service_account_id: str,
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

        The role determines what the service account can do in the workspace and which
        workspace-scoped permissions it can be granted when authenticating through
        federation. Every service account is already an implicit `workspace_user` member
        of the default workspace; adding it explicitly assigns a chosen role. If the
        service account is already an explicit member of the workspace, its
        `workspace_role` is replaced with the value supplied here. Archived workspaces
        return 400. Archived service accounts cannot be added and are rejected.

        Args:
          workspace_id: ID of the workspace.

          service_account_id: Tagged service account ID to add.

          workspace_role: Role to assign to the service account in this workspace.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._post(
            path_template(
                "/v1/organizations/workspaces/{workspace_id}/service_accounts?beta=true", workspace_id=workspace_id
            ),
            body=await async_maybe_transform(
                {
                    "service_account_id": service_account_id,
                    "workspace_role": workspace_role,
                },
                service_account_add_params.ServiceAccountAddParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaServiceAccountWorkspaceMember,
        )

    async def remove(
        self,
        service_account_id: str,
        *,
        workspace_id: str,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> ServiceAccountRemoveResponse:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Remove a service account from a workspace.

        Removal is idempotent (returns 200 even if the membership was already removed).
        A DELETE against the implicit default-workspace membership returns 200 but is a
        no-op and the membership persists; deleting an explicit default-workspace row
        reverts to the implicit `workspace_user` membership. Archived workspaces
        return 400.

        Args:
          workspace_id: ID of the workspace.

          service_account_id: ID of the service account.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        if not service_account_id:
            raise ValueError(f"Expected a non-empty value for `service_account_id` but received {service_account_id!r}")
        extra_headers = {
            **strip_not_given({"anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given}),
            **(extra_headers or {}),
        }
        return await self._delete(
            path_template(
                "/v1/organizations/workspaces/{workspace_id}/service_accounts/{service_account_id}?beta=true",
                workspace_id=workspace_id,
                service_account_id=service_account_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ServiceAccountRemoveResponse,
        )


class ServiceAccountsWithRawResponse:
    def __init__(self, service_accounts: ServiceAccounts) -> None:
        self._service_accounts = service_accounts

        self.retrieve = to_raw_response_wrapper(
            service_accounts.retrieve,
        )
        self.update = to_raw_response_wrapper(
            service_accounts.update,
        )
        self.list = to_raw_response_wrapper(
            service_accounts.list,
        )
        self.add = to_raw_response_wrapper(
            service_accounts.add,
        )
        self.remove = to_raw_response_wrapper(
            service_accounts.remove,
        )


class AsyncServiceAccountsWithRawResponse:
    def __init__(self, service_accounts: AsyncServiceAccounts) -> None:
        self._service_accounts = service_accounts

        self.retrieve = async_to_raw_response_wrapper(
            service_accounts.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            service_accounts.update,
        )
        self.list = async_to_raw_response_wrapper(
            service_accounts.list,
        )
        self.add = async_to_raw_response_wrapper(
            service_accounts.add,
        )
        self.remove = async_to_raw_response_wrapper(
            service_accounts.remove,
        )


class ServiceAccountsWithStreamingResponse:
    def __init__(self, service_accounts: ServiceAccounts) -> None:
        self._service_accounts = service_accounts

        self.retrieve = to_streamed_response_wrapper(
            service_accounts.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            service_accounts.update,
        )
        self.list = to_streamed_response_wrapper(
            service_accounts.list,
        )
        self.add = to_streamed_response_wrapper(
            service_accounts.add,
        )
        self.remove = to_streamed_response_wrapper(
            service_accounts.remove,
        )


class AsyncServiceAccountsWithStreamingResponse:
    def __init__(self, service_accounts: AsyncServiceAccounts) -> None:
        self._service_accounts = service_accounts

        self.retrieve = async_to_streamed_response_wrapper(
            service_accounts.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            service_accounts.update,
        )
        self.list = async_to_streamed_response_wrapper(
            service_accounts.list,
        )
        self.add = async_to_streamed_response_wrapper(
            service_accounts.add,
        )
        self.remove = async_to_streamed_response_wrapper(
            service_accounts.remove,
        )
