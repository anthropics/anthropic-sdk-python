from __future__ import annotations

from typing import Optional

import httpx2

from ....._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ....._utils import path_template
from ....._compat import cached_property
from .permissions import (
    Permissions,
    AsyncPermissions,
    PermissionsWithRawResponse,
    AsyncPermissionsWithRawResponse,
    PermissionsWithStreamingResponse,
    AsyncPermissionsWithStreamingResponse,
)
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .....pagination import SyncPageCursor, AsyncPageCursor
from ....._base_client import AsyncPaginator, make_request_options
from .....types.beta.organization.beta_rbac_role import BetaRBACRole

__all__ = ["RBACRoles", "AsyncRBACRoles"]


class RBACRoles(SyncAPIResource):
    @cached_property
    def permissions(self) -> Permissions:
        return Permissions(self._client)

    @cached_property
    def with_raw_response(self) -> RBACRolesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return RBACRolesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RBACRolesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return RBACRolesWithStreamingResponse(self)

    def retrieve(
        self,
        rbac_role_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaRBACRole:
        """
        Retrieve an RBAC Role by ID.

        The RBAC Roles API is available to Claude Enterprise organizations only.

        Args:
          rbac_role_id: ID of the RBAC Role.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rbac_role_id:
            raise ValueError(f"Expected a non-empty value for `rbac_role_id` but received {rbac_role_id!r}")
        return self._get(
            path_template("/v1/organizations/rbac_roles/{rbac_role_id}?beta=true", rbac_role_id=rbac_role_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaRBACRole,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaRBACRole]:
        """
        List RBAC Roles in the organization.

        The RBAC Roles API is available to Claude Enterprise organizations only.

        Args:
          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `1000`.

          page: Optionally set to the `next_page` token from the previous response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/rbac_roles?beta=true",
            page=SyncPageCursor[BetaRBACRole],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "page": page,
                },
            ),
            model=BetaRBACRole,
        )


class AsyncRBACRoles(AsyncAPIResource):
    @cached_property
    def permissions(self) -> AsyncPermissions:
        return AsyncPermissions(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncRBACRolesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncRBACRolesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRBACRolesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncRBACRolesWithStreamingResponse(self)

    async def retrieve(
        self,
        rbac_role_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaRBACRole:
        """
        Retrieve an RBAC Role by ID.

        The RBAC Roles API is available to Claude Enterprise organizations only.

        Args:
          rbac_role_id: ID of the RBAC Role.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rbac_role_id:
            raise ValueError(f"Expected a non-empty value for `rbac_role_id` but received {rbac_role_id!r}")
        return await self._get(
            path_template("/v1/organizations/rbac_roles/{rbac_role_id}?beta=true", rbac_role_id=rbac_role_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaRBACRole,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaRBACRole, AsyncPageCursor[BetaRBACRole]]:
        """
        List RBAC Roles in the organization.

        The RBAC Roles API is available to Claude Enterprise organizations only.

        Args:
          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `1000`.

          page: Optionally set to the `next_page` token from the previous response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/rbac_roles?beta=true",
            page=AsyncPageCursor[BetaRBACRole],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "page": page,
                },
            ),
            model=BetaRBACRole,
        )


class RBACRolesWithRawResponse:
    def __init__(self, rbac_roles: RBACRoles) -> None:
        self._rbac_roles = rbac_roles

        self.retrieve = to_raw_response_wrapper(
            rbac_roles.retrieve,
        )
        self.list = to_raw_response_wrapper(
            rbac_roles.list,
        )

    @cached_property
    def permissions(self) -> PermissionsWithRawResponse:
        return PermissionsWithRawResponse(self._rbac_roles.permissions)


class AsyncRBACRolesWithRawResponse:
    def __init__(self, rbac_roles: AsyncRBACRoles) -> None:
        self._rbac_roles = rbac_roles

        self.retrieve = async_to_raw_response_wrapper(
            rbac_roles.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            rbac_roles.list,
        )

    @cached_property
    def permissions(self) -> AsyncPermissionsWithRawResponse:
        return AsyncPermissionsWithRawResponse(self._rbac_roles.permissions)


class RBACRolesWithStreamingResponse:
    def __init__(self, rbac_roles: RBACRoles) -> None:
        self._rbac_roles = rbac_roles

        self.retrieve = to_streamed_response_wrapper(
            rbac_roles.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            rbac_roles.list,
        )

    @cached_property
    def permissions(self) -> PermissionsWithStreamingResponse:
        return PermissionsWithStreamingResponse(self._rbac_roles.permissions)


class AsyncRBACRolesWithStreamingResponse:
    def __init__(self, rbac_roles: AsyncRBACRoles) -> None:
        self._rbac_roles = rbac_roles

        self.retrieve = async_to_streamed_response_wrapper(
            rbac_roles.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            rbac_roles.list,
        )

    @cached_property
    def permissions(self) -> AsyncPermissionsWithStreamingResponse:
        return AsyncPermissionsWithStreamingResponse(self._rbac_roles.permissions)
