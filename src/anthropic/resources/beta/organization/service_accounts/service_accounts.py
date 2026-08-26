# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal

import httpx2

from ....._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ....._utils import is_given, path_template, maybe_transform, strip_not_given, async_maybe_transform
from .workspaces import (
    Workspaces,
    AsyncWorkspaces,
    WorkspacesWithRawResponse,
    AsyncWorkspacesWithRawResponse,
    WorkspacesWithStreamingResponse,
    AsyncWorkspacesWithStreamingResponse,
)
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
from .....types.beta.organization import (
    service_account_list_params,
    service_account_create_params,
    service_account_update_params,
)
from .....types.anthropic_beta_param import AnthropicBetaParam
from .....types.beta.organization.beta_service_account import BetaServiceAccount

__all__ = ["ServiceAccounts", "AsyncServiceAccounts"]


class ServiceAccounts(SyncAPIResource):
    @cached_property
    def workspaces(self) -> Workspaces:
        return Workspaces(self._client)

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

    def create(
        self,
        *,
        name: str,
        description: Optional[str] | Omit = omit,
        organization_role: Literal["admin", "developer"] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaServiceAccount:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Create a service account.

        A service account is a named workload identity that federation rules target.
        `organization_role` is `developer` (default) or `admin`; a rule may only be
        created or retargeted to grant `org:admin` scope when the target's
        `organization_role` is `admin`. Creating an `admin`-role service account
        requires an interactive credential (a user OAuth token or a Console session) — a
        workload may only create `developer`-role service accounts.

        Args:
          name: Slug identifier (lowercase, digits, hyphens). Unique within the organization; a
              duplicate name returns 409.

          description: Optional free-text description.

          organization_role: Org-level role. Defaults to `developer`.

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
            "/v1/organizations/service_accounts?beta=true",
            body=maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "organization_role": organization_role,
                },
                service_account_create_params.ServiceAccountCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaServiceAccount,
        )

    def retrieve(
        self,
        service_account_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaServiceAccount:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Retrieve a service account by its ID (`svac_...`).

        Args:
          service_account_id: ID of the service account.

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
        return self._get(
            path_template(
                "/v1/organizations/service_accounts/{service_account_id}?beta=true",
                service_account_id=service_account_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaServiceAccount,
        )

    def update(
        self,
        service_account_id: str,
        *,
        description: Optional[str] | Omit = omit,
        organization_role: Optional[Literal["admin", "developer"]] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaServiceAccount:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Update a service account.

        Only `description` and `organization_role` are mutable; `name` cannot be
        changed. Archived service accounts cannot be updated; this returns 400. Setting
        `organization_role` to `admin` (even when unchanged) requires an interactive
        credential (a user OAuth token or a Console session).

        Args:
          service_account_id: ID of the service account to update.

          description: Replaces the description. Omit to leave unchanged; send `null` to clear (the
              field is stored as an empty string).

          organization_role: Replaces the org-level role. Omit or send `null` to leave unchanged.

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
                "/v1/organizations/service_accounts/{service_account_id}?beta=true",
                service_account_id=service_account_id,
            ),
            body=maybe_transform(
                {
                    "description": description,
                    "organization_role": organization_role,
                },
                service_account_update_params.ServiceAccountUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaServiceAccount,
        )

    def list(
        self,
        *,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaServiceAccount]:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        List service accounts in the caller's organization.

        Results are ordered by creation time, newest first. Use `limit` and the
        `next_page` cursor to paginate; set `include_archived=true` to include archived
        service accounts.

        Args:
          include_archived: Include archived resources. Defaults to false.

          limit: Number of results per page.

          page: Opaque cursor from a previous response's `next_page`.

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
        return self._get_api_list(
            "/v1/organizations/service_accounts?beta=true",
            page=SyncPageCursor[BetaServiceAccount],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "include_archived": include_archived,
                        "limit": limit,
                        "page": page,
                    },
                    service_account_list_params.ServiceAccountListParams,
                ),
            ),
            model=BetaServiceAccount,
        )

    def archive(
        self,
        service_account_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaServiceAccount:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Archive a service account.

        Idempotent; re-archiving returns the service account with its original
        `archived_at`. Rejected with 400 if any live (non-archived) federation rule
        still targets this service account, same as issuer archival; archive those rules
        first or change their target to another service account.

        Args:
          service_account_id: ID of the service account to archive.

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
                "/v1/organizations/service_accounts/{service_account_id}/archive?beta=true",
                service_account_id=service_account_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaServiceAccount,
        )


class AsyncServiceAccounts(AsyncAPIResource):
    @cached_property
    def workspaces(self) -> AsyncWorkspaces:
        return AsyncWorkspaces(self._client)

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

    async def create(
        self,
        *,
        name: str,
        description: Optional[str] | Omit = omit,
        organization_role: Literal["admin", "developer"] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaServiceAccount:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Create a service account.

        A service account is a named workload identity that federation rules target.
        `organization_role` is `developer` (default) or `admin`; a rule may only be
        created or retargeted to grant `org:admin` scope when the target's
        `organization_role` is `admin`. Creating an `admin`-role service account
        requires an interactive credential (a user OAuth token or a Console session) — a
        workload may only create `developer`-role service accounts.

        Args:
          name: Slug identifier (lowercase, digits, hyphens). Unique within the organization; a
              duplicate name returns 409.

          description: Optional free-text description.

          organization_role: Org-level role. Defaults to `developer`.

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
            "/v1/organizations/service_accounts?beta=true",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "organization_role": organization_role,
                },
                service_account_create_params.ServiceAccountCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaServiceAccount,
        )

    async def retrieve(
        self,
        service_account_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaServiceAccount:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Retrieve a service account by its ID (`svac_...`).

        Args:
          service_account_id: ID of the service account.

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
        return await self._get(
            path_template(
                "/v1/organizations/service_accounts/{service_account_id}?beta=true",
                service_account_id=service_account_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaServiceAccount,
        )

    async def update(
        self,
        service_account_id: str,
        *,
        description: Optional[str] | Omit = omit,
        organization_role: Optional[Literal["admin", "developer"]] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaServiceAccount:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Update a service account.

        Only `description` and `organization_role` are mutable; `name` cannot be
        changed. Archived service accounts cannot be updated; this returns 400. Setting
        `organization_role` to `admin` (even when unchanged) requires an interactive
        credential (a user OAuth token or a Console session).

        Args:
          service_account_id: ID of the service account to update.

          description: Replaces the description. Omit to leave unchanged; send `null` to clear (the
              field is stored as an empty string).

          organization_role: Replaces the org-level role. Omit or send `null` to leave unchanged.

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
                "/v1/organizations/service_accounts/{service_account_id}?beta=true",
                service_account_id=service_account_id,
            ),
            body=await async_maybe_transform(
                {
                    "description": description,
                    "organization_role": organization_role,
                },
                service_account_update_params.ServiceAccountUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaServiceAccount,
        )

    def list(
        self,
        *,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaServiceAccount, AsyncPageCursor[BetaServiceAccount]]:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        List service accounts in the caller's organization.

        Results are ordered by creation time, newest first. Use `limit` and the
        `next_page` cursor to paginate; set `include_archived=true` to include archived
        service accounts.

        Args:
          include_archived: Include archived resources. Defaults to false.

          limit: Number of results per page.

          page: Opaque cursor from a previous response's `next_page`.

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
        return self._get_api_list(
            "/v1/organizations/service_accounts?beta=true",
            page=AsyncPageCursor[BetaServiceAccount],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "include_archived": include_archived,
                        "limit": limit,
                        "page": page,
                    },
                    service_account_list_params.ServiceAccountListParams,
                ),
            ),
            model=BetaServiceAccount,
        )

    async def archive(
        self,
        service_account_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaServiceAccount:
        """
        **Requires an OAuth access token with the `org:admin` scope**, from
        `ant auth login --scope org:admin` or a workload identity federation rule; Admin
        API keys are not accepted. See
        [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api).

        Archive a service account.

        Idempotent; re-archiving returns the service account with its original
        `archived_at`. Rejected with 400 if any live (non-archived) federation rule
        still targets this service account, same as issuer archival; archive those rules
        first or change their target to another service account.

        Args:
          service_account_id: ID of the service account to archive.

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
                "/v1/organizations/service_accounts/{service_account_id}/archive?beta=true",
                service_account_id=service_account_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaServiceAccount,
        )


class ServiceAccountsWithRawResponse:
    def __init__(self, service_accounts: ServiceAccounts) -> None:
        self._service_accounts = service_accounts

        self.create = to_raw_response_wrapper(
            service_accounts.create,
        )
        self.retrieve = to_raw_response_wrapper(
            service_accounts.retrieve,
        )
        self.update = to_raw_response_wrapper(
            service_accounts.update,
        )
        self.list = to_raw_response_wrapper(
            service_accounts.list,
        )
        self.archive = to_raw_response_wrapper(
            service_accounts.archive,
        )

    @cached_property
    def workspaces(self) -> WorkspacesWithRawResponse:
        return WorkspacesWithRawResponse(self._service_accounts.workspaces)


class AsyncServiceAccountsWithRawResponse:
    def __init__(self, service_accounts: AsyncServiceAccounts) -> None:
        self._service_accounts = service_accounts

        self.create = async_to_raw_response_wrapper(
            service_accounts.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            service_accounts.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            service_accounts.update,
        )
        self.list = async_to_raw_response_wrapper(
            service_accounts.list,
        )
        self.archive = async_to_raw_response_wrapper(
            service_accounts.archive,
        )

    @cached_property
    def workspaces(self) -> AsyncWorkspacesWithRawResponse:
        return AsyncWorkspacesWithRawResponse(self._service_accounts.workspaces)


class ServiceAccountsWithStreamingResponse:
    def __init__(self, service_accounts: ServiceAccounts) -> None:
        self._service_accounts = service_accounts

        self.create = to_streamed_response_wrapper(
            service_accounts.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            service_accounts.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            service_accounts.update,
        )
        self.list = to_streamed_response_wrapper(
            service_accounts.list,
        )
        self.archive = to_streamed_response_wrapper(
            service_accounts.archive,
        )

    @cached_property
    def workspaces(self) -> WorkspacesWithStreamingResponse:
        return WorkspacesWithStreamingResponse(self._service_accounts.workspaces)


class AsyncServiceAccountsWithStreamingResponse:
    def __init__(self, service_accounts: AsyncServiceAccounts) -> None:
        self._service_accounts = service_accounts

        self.create = async_to_streamed_response_wrapper(
            service_accounts.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            service_accounts.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            service_accounts.update,
        )
        self.list = async_to_streamed_response_wrapper(
            service_accounts.list,
        )
        self.archive = async_to_streamed_response_wrapper(
            service_accounts.archive,
        )

    @cached_property
    def workspaces(self) -> AsyncWorkspacesWithStreamingResponse:
        return AsyncWorkspacesWithStreamingResponse(self._service_accounts.workspaces)
