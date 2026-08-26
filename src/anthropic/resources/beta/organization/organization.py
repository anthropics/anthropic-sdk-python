# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx2

from .users import (
    Users,
    AsyncUsers,
    UsersWithRawResponse,
    AsyncUsersWithRawResponse,
    UsersWithStreamingResponse,
    AsyncUsersWithStreamingResponse,
)
from .invites import (
    Invites,
    AsyncInvites,
    InvitesWithRawResponse,
    AsyncInvitesWithRawResponse,
    InvitesWithStreamingResponse,
    AsyncInvitesWithStreamingResponse,
)
from .api_keys import (
    APIKeys,
    AsyncAPIKeys,
    APIKeysWithRawResponse,
    AsyncAPIKeysWithRawResponse,
    APIKeysWithStreamingResponse,
    AsyncAPIKeysWithStreamingResponse,
)
from ...._types import Body, Query, Headers, NotGiven, not_given
from ...._compat import cached_property
from .rate_limits import (
    RateLimits,
    AsyncRateLimits,
    RateLimitsWithRawResponse,
    AsyncRateLimitsWithRawResponse,
    RateLimitsWithStreamingResponse,
    AsyncRateLimitsWithStreamingResponse,
)
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .external_keys import (
    ExternalKeys,
    AsyncExternalKeys,
    ExternalKeysWithRawResponse,
    AsyncExternalKeysWithRawResponse,
    ExternalKeysWithStreamingResponse,
    AsyncExternalKeysWithStreamingResponse,
)
from ...._base_client import make_request_options
from .federation.federation import (
    Federation,
    AsyncFederation,
    FederationWithRawResponse,
    AsyncFederationWithRawResponse,
    FederationWithStreamingResponse,
    AsyncFederationWithStreamingResponse,
)
from .workspaces.workspaces import (
    Workspaces,
    AsyncWorkspaces,
    WorkspacesWithRawResponse,
    AsyncWorkspacesWithRawResponse,
    WorkspacesWithStreamingResponse,
    AsyncWorkspacesWithStreamingResponse,
)
from ....types.beta.beta_organization import BetaOrganization
from .service_accounts.service_accounts import (
    ServiceAccounts,
    AsyncServiceAccounts,
    ServiceAccountsWithRawResponse,
    AsyncServiceAccountsWithRawResponse,
    ServiceAccountsWithStreamingResponse,
    AsyncServiceAccountsWithStreamingResponse,
)

__all__ = ["Organization", "AsyncOrganization"]


class Organization(SyncAPIResource):
    @cached_property
    def api_keys(self) -> APIKeys:
        return APIKeys(self._client)

    @cached_property
    def external_keys(self) -> ExternalKeys:
        return ExternalKeys(self._client)

    @cached_property
    def federation(self) -> Federation:
        return Federation(self._client)

    @cached_property
    def invites(self) -> Invites:
        return Invites(self._client)

    @cached_property
    def service_accounts(self) -> ServiceAccounts:
        return ServiceAccounts(self._client)

    @cached_property
    def users(self) -> Users:
        return Users(self._client)

    @cached_property
    def workspaces(self) -> Workspaces:
        return Workspaces(self._client)

    @cached_property
    def rate_limits(self) -> RateLimits:
        return RateLimits(self._client)

    @cached_property
    def with_raw_response(self) -> OrganizationWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return OrganizationWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OrganizationWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return OrganizationWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaOrganization:
        """
        Retrieve information about the organization associated with the authenticated
        API key.
        """
        return self._get(
            "/v1/organizations/me?beta=true",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaOrganization,
        )


class AsyncOrganization(AsyncAPIResource):
    @cached_property
    def api_keys(self) -> AsyncAPIKeys:
        return AsyncAPIKeys(self._client)

    @cached_property
    def external_keys(self) -> AsyncExternalKeys:
        return AsyncExternalKeys(self._client)

    @cached_property
    def federation(self) -> AsyncFederation:
        return AsyncFederation(self._client)

    @cached_property
    def invites(self) -> AsyncInvites:
        return AsyncInvites(self._client)

    @cached_property
    def service_accounts(self) -> AsyncServiceAccounts:
        return AsyncServiceAccounts(self._client)

    @cached_property
    def users(self) -> AsyncUsers:
        return AsyncUsers(self._client)

    @cached_property
    def workspaces(self) -> AsyncWorkspaces:
        return AsyncWorkspaces(self._client)

    @cached_property
    def rate_limits(self) -> AsyncRateLimits:
        return AsyncRateLimits(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncOrganizationWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncOrganizationWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOrganizationWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncOrganizationWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaOrganization:
        """
        Retrieve information about the organization associated with the authenticated
        API key.
        """
        return await self._get(
            "/v1/organizations/me?beta=true",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaOrganization,
        )


class OrganizationWithRawResponse:
    def __init__(self, organization: Organization) -> None:
        self._organization = organization

        self.retrieve = to_raw_response_wrapper(
            organization.retrieve,
        )

    @cached_property
    def api_keys(self) -> APIKeysWithRawResponse:
        return APIKeysWithRawResponse(self._organization.api_keys)

    @cached_property
    def external_keys(self) -> ExternalKeysWithRawResponse:
        return ExternalKeysWithRawResponse(self._organization.external_keys)

    @cached_property
    def federation(self) -> FederationWithRawResponse:
        return FederationWithRawResponse(self._organization.federation)

    @cached_property
    def invites(self) -> InvitesWithRawResponse:
        return InvitesWithRawResponse(self._organization.invites)

    @cached_property
    def service_accounts(self) -> ServiceAccountsWithRawResponse:
        return ServiceAccountsWithRawResponse(self._organization.service_accounts)

    @cached_property
    def users(self) -> UsersWithRawResponse:
        return UsersWithRawResponse(self._organization.users)

    @cached_property
    def workspaces(self) -> WorkspacesWithRawResponse:
        return WorkspacesWithRawResponse(self._organization.workspaces)

    @cached_property
    def rate_limits(self) -> RateLimitsWithRawResponse:
        return RateLimitsWithRawResponse(self._organization.rate_limits)


class AsyncOrganizationWithRawResponse:
    def __init__(self, organization: AsyncOrganization) -> None:
        self._organization = organization

        self.retrieve = async_to_raw_response_wrapper(
            organization.retrieve,
        )

    @cached_property
    def api_keys(self) -> AsyncAPIKeysWithRawResponse:
        return AsyncAPIKeysWithRawResponse(self._organization.api_keys)

    @cached_property
    def external_keys(self) -> AsyncExternalKeysWithRawResponse:
        return AsyncExternalKeysWithRawResponse(self._organization.external_keys)

    @cached_property
    def federation(self) -> AsyncFederationWithRawResponse:
        return AsyncFederationWithRawResponse(self._organization.federation)

    @cached_property
    def invites(self) -> AsyncInvitesWithRawResponse:
        return AsyncInvitesWithRawResponse(self._organization.invites)

    @cached_property
    def service_accounts(self) -> AsyncServiceAccountsWithRawResponse:
        return AsyncServiceAccountsWithRawResponse(self._organization.service_accounts)

    @cached_property
    def users(self) -> AsyncUsersWithRawResponse:
        return AsyncUsersWithRawResponse(self._organization.users)

    @cached_property
    def workspaces(self) -> AsyncWorkspacesWithRawResponse:
        return AsyncWorkspacesWithRawResponse(self._organization.workspaces)

    @cached_property
    def rate_limits(self) -> AsyncRateLimitsWithRawResponse:
        return AsyncRateLimitsWithRawResponse(self._organization.rate_limits)


class OrganizationWithStreamingResponse:
    def __init__(self, organization: Organization) -> None:
        self._organization = organization

        self.retrieve = to_streamed_response_wrapper(
            organization.retrieve,
        )

    @cached_property
    def api_keys(self) -> APIKeysWithStreamingResponse:
        return APIKeysWithStreamingResponse(self._organization.api_keys)

    @cached_property
    def external_keys(self) -> ExternalKeysWithStreamingResponse:
        return ExternalKeysWithStreamingResponse(self._organization.external_keys)

    @cached_property
    def federation(self) -> FederationWithStreamingResponse:
        return FederationWithStreamingResponse(self._organization.federation)

    @cached_property
    def invites(self) -> InvitesWithStreamingResponse:
        return InvitesWithStreamingResponse(self._organization.invites)

    @cached_property
    def service_accounts(self) -> ServiceAccountsWithStreamingResponse:
        return ServiceAccountsWithStreamingResponse(self._organization.service_accounts)

    @cached_property
    def users(self) -> UsersWithStreamingResponse:
        return UsersWithStreamingResponse(self._organization.users)

    @cached_property
    def workspaces(self) -> WorkspacesWithStreamingResponse:
        return WorkspacesWithStreamingResponse(self._organization.workspaces)

    @cached_property
    def rate_limits(self) -> RateLimitsWithStreamingResponse:
        return RateLimitsWithStreamingResponse(self._organization.rate_limits)


class AsyncOrganizationWithStreamingResponse:
    def __init__(self, organization: AsyncOrganization) -> None:
        self._organization = organization

        self.retrieve = async_to_streamed_response_wrapper(
            organization.retrieve,
        )

    @cached_property
    def api_keys(self) -> AsyncAPIKeysWithStreamingResponse:
        return AsyncAPIKeysWithStreamingResponse(self._organization.api_keys)

    @cached_property
    def external_keys(self) -> AsyncExternalKeysWithStreamingResponse:
        return AsyncExternalKeysWithStreamingResponse(self._organization.external_keys)

    @cached_property
    def federation(self) -> AsyncFederationWithStreamingResponse:
        return AsyncFederationWithStreamingResponse(self._organization.federation)

    @cached_property
    def invites(self) -> AsyncInvitesWithStreamingResponse:
        return AsyncInvitesWithStreamingResponse(self._organization.invites)

    @cached_property
    def service_accounts(self) -> AsyncServiceAccountsWithStreamingResponse:
        return AsyncServiceAccountsWithStreamingResponse(self._organization.service_accounts)

    @cached_property
    def users(self) -> AsyncUsersWithStreamingResponse:
        return AsyncUsersWithStreamingResponse(self._organization.users)

    @cached_property
    def workspaces(self) -> AsyncWorkspacesWithStreamingResponse:
        return AsyncWorkspacesWithStreamingResponse(self._organization.workspaces)

    @cached_property
    def rate_limits(self) -> AsyncRateLimitsWithStreamingResponse:
        return AsyncRateLimitsWithStreamingResponse(self._organization.rate_limits)
