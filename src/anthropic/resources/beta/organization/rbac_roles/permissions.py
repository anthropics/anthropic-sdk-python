from __future__ import annotations

from typing import Optional

import httpx2

from ....._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ....._utils import path_template
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
from .....types.beta.organization.rbac_roles.beta_rbac_role_permission import BetaRBACRolePermission

__all__ = ["Permissions", "AsyncPermissions"]


class Permissions(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PermissionsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return PermissionsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PermissionsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return PermissionsWithStreamingResponse(self)

    def list(
        self,
        rbac_role_id: str,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaRBACRolePermission]:
        """
        List the permissions an RBAC Role grants.

        The RBAC Roles API is available to Claude Enterprise organizations only.

        Args:
          rbac_role_id: ID of the RBAC Role.

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `1000`.

          page: Optionally set to the `next_page` token from the previous response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rbac_role_id:
            raise ValueError(f"Expected a non-empty value for `rbac_role_id` but received {rbac_role_id!r}")
        return self._get_api_list(
            path_template(
                "/v1/organizations/rbac_roles/{rbac_role_id}/permissions?beta=true", rbac_role_id=rbac_role_id
            ),
            page=SyncPageCursor[BetaRBACRolePermission],
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
            model=BetaRBACRolePermission,
        )


class AsyncPermissions(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPermissionsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPermissionsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPermissionsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncPermissionsWithStreamingResponse(self)

    def list(
        self,
        rbac_role_id: str,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaRBACRolePermission, AsyncPageCursor[BetaRBACRolePermission]]:
        """
        List the permissions an RBAC Role grants.

        The RBAC Roles API is available to Claude Enterprise organizations only.

        Args:
          rbac_role_id: ID of the RBAC Role.

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `1000`.

          page: Optionally set to the `next_page` token from the previous response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rbac_role_id:
            raise ValueError(f"Expected a non-empty value for `rbac_role_id` but received {rbac_role_id!r}")
        return self._get_api_list(
            path_template(
                "/v1/organizations/rbac_roles/{rbac_role_id}/permissions?beta=true", rbac_role_id=rbac_role_id
            ),
            page=AsyncPageCursor[BetaRBACRolePermission],
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
            model=BetaRBACRolePermission,
        )


class PermissionsWithRawResponse:
    def __init__(self, permissions: Permissions) -> None:
        self._permissions = permissions

        self.list = to_raw_response_wrapper(
            permissions.list,
        )


class AsyncPermissionsWithRawResponse:
    def __init__(self, permissions: AsyncPermissions) -> None:
        self._permissions = permissions

        self.list = async_to_raw_response_wrapper(
            permissions.list,
        )


class PermissionsWithStreamingResponse:
    def __init__(self, permissions: Permissions) -> None:
        self._permissions = permissions

        self.list = to_streamed_response_wrapper(
            permissions.list,
        )


class AsyncPermissionsWithStreamingResponse:
    def __init__(self, permissions: AsyncPermissions) -> None:
        self._permissions = permissions

        self.list = async_to_streamed_response_wrapper(
            permissions.list,
        )
