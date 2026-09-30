from __future__ import annotations

from typing import Optional

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
from .....types.beta.organization.beta_rbac_group import BetaRBACGroup
from .....types.beta.organization.rbac_group_delete_response import RBACGroupDeleteResponse

__all__ = ["RBACGroups", "AsyncRBACGroups"]


class RBACGroups(SyncAPIResource):
    @cached_property
    def members(self) -> Members:
        return Members(self._client)

    @cached_property
    def with_raw_response(self) -> RBACGroupsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return RBACGroupsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RBACGroupsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return RBACGroupsWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaRBACGroup:
        """Create an RBAC Group in the Claude Enterprise tenant.

        Groups created via the API
        have source type `"direct"`.

        The RBAC Groups API is available to Claude Enterprise organizations only.

        Args:
          name: Name of the RBAC Group. Not uniqueness-enforced.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/organizations/rbac_groups?beta=true",
            body={"name": name},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaRBACGroup,
        )

    def retrieve(
        self,
        rbac_group_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaRBACGroup:
        """
        Retrieve an RBAC Group by ID.

        The RBAC Groups API is available to Claude Enterprise organizations only.

        Args:
          rbac_group_id: ID of the RBAC Group.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rbac_group_id:
            raise ValueError(f"Expected a non-empty value for `rbac_group_id` but received {rbac_group_id!r}")
        return self._get(
            path_template("/v1/organizations/rbac_groups/{rbac_group_id}?beta=true", rbac_group_id=rbac_group_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaRBACGroup,
        )

    def update(
        self,
        rbac_group_id: str,
        *,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaRBACGroup:
        """Update an RBAC Group's name.

        Groups provisioned by an identity provider (source
        type `"scim"`) cannot be modified via the API while an organization in the
        tenant uses SCIM provisioning.

        The RBAC Groups API is available to Claude Enterprise organizations only.

        Args:
          rbac_group_id: ID of the RBAC Group.

          name: Name of the RBAC Group. Not uniqueness-enforced.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rbac_group_id:
            raise ValueError(f"Expected a non-empty value for `rbac_group_id` but received {rbac_group_id!r}")
        return self._post(
            path_template("/v1/organizations/rbac_groups/{rbac_group_id}?beta=true", rbac_group_id=rbac_group_id),
            body={"name": name},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaRBACGroup,
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
    ) -> SyncPageCursor[BetaRBACGroup]:
        """
        List RBAC Groups in the Claude Enterprise tenant.

        The RBAC Groups API is available to Claude Enterprise organizations only.

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
            "/v1/organizations/rbac_groups?beta=true",
            page=SyncPageCursor[BetaRBACGroup],
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
            model=BetaRBACGroup,
        )

    def delete(
        self,
        rbac_group_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> RBACGroupDeleteResponse:
        """Delete an RBAC Group.

        Groups provisioned by an identity provider (source type
        `"scim"`) cannot be deleted via the API while an organization in the tenant uses
        SCIM provisioning.

        The RBAC Groups API is available to Claude Enterprise organizations only.

        Args:
          rbac_group_id: ID of the RBAC Group.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rbac_group_id:
            raise ValueError(f"Expected a non-empty value for `rbac_group_id` but received {rbac_group_id!r}")
        return self._delete(
            path_template("/v1/organizations/rbac_groups/{rbac_group_id}?beta=true", rbac_group_id=rbac_group_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=RBACGroupDeleteResponse,
        )


class AsyncRBACGroups(AsyncAPIResource):
    @cached_property
    def members(self) -> AsyncMembers:
        return AsyncMembers(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncRBACGroupsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncRBACGroupsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRBACGroupsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncRBACGroupsWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaRBACGroup:
        """Create an RBAC Group in the Claude Enterprise tenant.

        Groups created via the API
        have source type `"direct"`.

        The RBAC Groups API is available to Claude Enterprise organizations only.

        Args:
          name: Name of the RBAC Group. Not uniqueness-enforced.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/organizations/rbac_groups?beta=true",
            body={"name": name},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaRBACGroup,
        )

    async def retrieve(
        self,
        rbac_group_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaRBACGroup:
        """
        Retrieve an RBAC Group by ID.

        The RBAC Groups API is available to Claude Enterprise organizations only.

        Args:
          rbac_group_id: ID of the RBAC Group.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rbac_group_id:
            raise ValueError(f"Expected a non-empty value for `rbac_group_id` but received {rbac_group_id!r}")
        return await self._get(
            path_template("/v1/organizations/rbac_groups/{rbac_group_id}?beta=true", rbac_group_id=rbac_group_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaRBACGroup,
        )

    async def update(
        self,
        rbac_group_id: str,
        *,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaRBACGroup:
        """Update an RBAC Group's name.

        Groups provisioned by an identity provider (source
        type `"scim"`) cannot be modified via the API while an organization in the
        tenant uses SCIM provisioning.

        The RBAC Groups API is available to Claude Enterprise organizations only.

        Args:
          rbac_group_id: ID of the RBAC Group.

          name: Name of the RBAC Group. Not uniqueness-enforced.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rbac_group_id:
            raise ValueError(f"Expected a non-empty value for `rbac_group_id` but received {rbac_group_id!r}")
        return await self._post(
            path_template("/v1/organizations/rbac_groups/{rbac_group_id}?beta=true", rbac_group_id=rbac_group_id),
            body={"name": name},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaRBACGroup,
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
    ) -> AsyncPaginator[BetaRBACGroup, AsyncPageCursor[BetaRBACGroup]]:
        """
        List RBAC Groups in the Claude Enterprise tenant.

        The RBAC Groups API is available to Claude Enterprise organizations only.

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
            "/v1/organizations/rbac_groups?beta=true",
            page=AsyncPageCursor[BetaRBACGroup],
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
            model=BetaRBACGroup,
        )

    async def delete(
        self,
        rbac_group_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> RBACGroupDeleteResponse:
        """Delete an RBAC Group.

        Groups provisioned by an identity provider (source type
        `"scim"`) cannot be deleted via the API while an organization in the tenant uses
        SCIM provisioning.

        The RBAC Groups API is available to Claude Enterprise organizations only.

        Args:
          rbac_group_id: ID of the RBAC Group.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rbac_group_id:
            raise ValueError(f"Expected a non-empty value for `rbac_group_id` but received {rbac_group_id!r}")
        return await self._delete(
            path_template("/v1/organizations/rbac_groups/{rbac_group_id}?beta=true", rbac_group_id=rbac_group_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=RBACGroupDeleteResponse,
        )


class RBACGroupsWithRawResponse:
    def __init__(self, rbac_groups: RBACGroups) -> None:
        self._rbac_groups = rbac_groups

        self.create = to_raw_response_wrapper(
            rbac_groups.create,
        )
        self.retrieve = to_raw_response_wrapper(
            rbac_groups.retrieve,
        )
        self.update = to_raw_response_wrapper(
            rbac_groups.update,
        )
        self.list = to_raw_response_wrapper(
            rbac_groups.list,
        )
        self.delete = to_raw_response_wrapper(
            rbac_groups.delete,
        )

    @cached_property
    def members(self) -> MembersWithRawResponse:
        return MembersWithRawResponse(self._rbac_groups.members)


class AsyncRBACGroupsWithRawResponse:
    def __init__(self, rbac_groups: AsyncRBACGroups) -> None:
        self._rbac_groups = rbac_groups

        self.create = async_to_raw_response_wrapper(
            rbac_groups.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            rbac_groups.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            rbac_groups.update,
        )
        self.list = async_to_raw_response_wrapper(
            rbac_groups.list,
        )
        self.delete = async_to_raw_response_wrapper(
            rbac_groups.delete,
        )

    @cached_property
    def members(self) -> AsyncMembersWithRawResponse:
        return AsyncMembersWithRawResponse(self._rbac_groups.members)


class RBACGroupsWithStreamingResponse:
    def __init__(self, rbac_groups: RBACGroups) -> None:
        self._rbac_groups = rbac_groups

        self.create = to_streamed_response_wrapper(
            rbac_groups.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            rbac_groups.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            rbac_groups.update,
        )
        self.list = to_streamed_response_wrapper(
            rbac_groups.list,
        )
        self.delete = to_streamed_response_wrapper(
            rbac_groups.delete,
        )

    @cached_property
    def members(self) -> MembersWithStreamingResponse:
        return MembersWithStreamingResponse(self._rbac_groups.members)


class AsyncRBACGroupsWithStreamingResponse:
    def __init__(self, rbac_groups: AsyncRBACGroups) -> None:
        self._rbac_groups = rbac_groups

        self.create = async_to_streamed_response_wrapper(
            rbac_groups.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            rbac_groups.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            rbac_groups.update,
        )
        self.list = async_to_streamed_response_wrapper(
            rbac_groups.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            rbac_groups.delete,
        )

    @cached_property
    def members(self) -> AsyncMembersWithStreamingResponse:
        return AsyncMembersWithStreamingResponse(self._rbac_groups.members)
