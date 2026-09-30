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
from .....types.beta.organization.rbac_groups.beta_rbac_group_member import BetaRBACGroupMember
from .....types.beta.organization.rbac_groups.member_remove_response import MemberRemoveResponse

__all__ = ["Members", "AsyncMembers"]


class Members(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MembersWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return MembersWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MembersWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return MembersWithStreamingResponse(self)

    def list(
        self,
        rbac_group_id: str,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaRBACGroupMember]:
        """
        List members of an RBAC Group.

        The RBAC Groups API is available to Claude Enterprise organizations only.

        Args:
          rbac_group_id: ID of the RBAC Group.

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `1000`.

          page: Optionally set to the `next_page` token from the previous response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rbac_group_id:
            raise ValueError(f"Expected a non-empty value for `rbac_group_id` but received {rbac_group_id!r}")
        return self._get_api_list(
            path_template(
                "/v1/organizations/rbac_groups/{rbac_group_id}/members?beta=true", rbac_group_id=rbac_group_id
            ),
            page=SyncPageCursor[BetaRBACGroupMember],
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
            model=BetaRBACGroupMember,
        )

    def add(
        self,
        rbac_group_id: str,
        *,
        user_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaRBACGroupMember:
        """Add a User to an RBAC Group.

        Membership of groups provisioned by an identity
        provider (source type `"scim"`) cannot be modified via the API while an
        organization in the tenant uses SCIM provisioning.

        The RBAC Groups API is available to Claude Enterprise organizations only.

        Args:
          rbac_group_id: ID of the RBAC Group.

          user_id: ID of the User.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rbac_group_id:
            raise ValueError(f"Expected a non-empty value for `rbac_group_id` but received {rbac_group_id!r}")
        return self._post(
            path_template(
                "/v1/organizations/rbac_groups/{rbac_group_id}/members?beta=true", rbac_group_id=rbac_group_id
            ),
            body={"user_id": user_id},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaRBACGroupMember,
        )

    def remove(
        self,
        user_id: str,
        *,
        rbac_group_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> MemberRemoveResponse:
        """Remove a User from an RBAC Group.

        Membership of groups provisioned by an
        identity provider (source type `"scim"`) cannot be modified via the API while an
        organization in the tenant uses SCIM provisioning.

        The RBAC Groups API is available to Claude Enterprise organizations only.

        Args:
          rbac_group_id: ID of the RBAC Group.

          user_id: ID of the User.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rbac_group_id:
            raise ValueError(f"Expected a non-empty value for `rbac_group_id` but received {rbac_group_id!r}")
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return self._delete(
            path_template(
                "/v1/organizations/rbac_groups/{rbac_group_id}/members/{user_id}?beta=true",
                rbac_group_id=rbac_group_id,
                user_id=user_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=MemberRemoveResponse,
        )


class AsyncMembers(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMembersWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMembersWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMembersWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncMembersWithStreamingResponse(self)

    def list(
        self,
        rbac_group_id: str,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaRBACGroupMember, AsyncPageCursor[BetaRBACGroupMember]]:
        """
        List members of an RBAC Group.

        The RBAC Groups API is available to Claude Enterprise organizations only.

        Args:
          rbac_group_id: ID of the RBAC Group.

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `1000`.

          page: Optionally set to the `next_page` token from the previous response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rbac_group_id:
            raise ValueError(f"Expected a non-empty value for `rbac_group_id` but received {rbac_group_id!r}")
        return self._get_api_list(
            path_template(
                "/v1/organizations/rbac_groups/{rbac_group_id}/members?beta=true", rbac_group_id=rbac_group_id
            ),
            page=AsyncPageCursor[BetaRBACGroupMember],
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
            model=BetaRBACGroupMember,
        )

    async def add(
        self,
        rbac_group_id: str,
        *,
        user_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaRBACGroupMember:
        """Add a User to an RBAC Group.

        Membership of groups provisioned by an identity
        provider (source type `"scim"`) cannot be modified via the API while an
        organization in the tenant uses SCIM provisioning.

        The RBAC Groups API is available to Claude Enterprise organizations only.

        Args:
          rbac_group_id: ID of the RBAC Group.

          user_id: ID of the User.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rbac_group_id:
            raise ValueError(f"Expected a non-empty value for `rbac_group_id` but received {rbac_group_id!r}")
        return await self._post(
            path_template(
                "/v1/organizations/rbac_groups/{rbac_group_id}/members?beta=true", rbac_group_id=rbac_group_id
            ),
            body={"user_id": user_id},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=BetaRBACGroupMember,
        )

    async def remove(
        self,
        user_id: str,
        *,
        rbac_group_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> MemberRemoveResponse:
        """Remove a User from an RBAC Group.

        Membership of groups provisioned by an
        identity provider (source type `"scim"`) cannot be modified via the API while an
        organization in the tenant uses SCIM provisioning.

        The RBAC Groups API is available to Claude Enterprise organizations only.

        Args:
          rbac_group_id: ID of the RBAC Group.

          user_id: ID of the User.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rbac_group_id:
            raise ValueError(f"Expected a non-empty value for `rbac_group_id` but received {rbac_group_id!r}")
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return await self._delete(
            path_template(
                "/v1/organizations/rbac_groups/{rbac_group_id}/members/{user_id}?beta=true",
                rbac_group_id=rbac_group_id,
                user_id=user_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=MemberRemoveResponse,
        )


class MembersWithRawResponse:
    def __init__(self, members: Members) -> None:
        self._members = members

        self.list = to_raw_response_wrapper(
            members.list,
        )
        self.add = to_raw_response_wrapper(
            members.add,
        )
        self.remove = to_raw_response_wrapper(
            members.remove,
        )


class AsyncMembersWithRawResponse:
    def __init__(self, members: AsyncMembers) -> None:
        self._members = members

        self.list = async_to_raw_response_wrapper(
            members.list,
        )
        self.add = async_to_raw_response_wrapper(
            members.add,
        )
        self.remove = async_to_raw_response_wrapper(
            members.remove,
        )


class MembersWithStreamingResponse:
    def __init__(self, members: Members) -> None:
        self._members = members

        self.list = to_streamed_response_wrapper(
            members.list,
        )
        self.add = to_streamed_response_wrapper(
            members.add,
        )
        self.remove = to_streamed_response_wrapper(
            members.remove,
        )


class AsyncMembersWithStreamingResponse:
    def __init__(self, members: AsyncMembers) -> None:
        self._members = members

        self.list = async_to_streamed_response_wrapper(
            members.list,
        )
        self.add = async_to_streamed_response_wrapper(
            members.add,
        )
        self.remove = async_to_streamed_response_wrapper(
            members.remove,
        )
