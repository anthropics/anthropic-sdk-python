# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx2

from ....._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ....._utils import path_template, maybe_transform, async_maybe_transform
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .....pagination import SyncPage, AsyncPage
from ....._base_client import AsyncPaginator, make_request_options
from .....types.beta.organization import BetaWorkspaceRole, BetaNoBillingWorkspaceRole
from .....types.beta.organization.workspaces import member_add_params, member_list_params, member_update_params
from .....types.beta.organization.beta_workspace_role import BetaWorkspaceRole
from .....types.beta.organization.beta_workspace_member import BetaWorkspaceMember
from .....types.beta.organization.beta_no_billing_workspace_role import BetaNoBillingWorkspaceRole
from .....types.beta.organization.workspaces.member_remove_response import MemberRemoveResponse

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

    def retrieve(
        self,
        user_id: str,
        *,
        workspace_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaWorkspaceMember:
        """
        Get Workspace Member

        Args:
          workspace_id: ID of the Workspace.

          user_id: ID of the User.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return self._get(
            path_template(
                "/v1/organizations/workspaces/{workspace_id}/members/{user_id}?beta=true",
                workspace_id=workspace_id,
                user_id=user_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaWorkspaceMember,
        )

    def update(
        self,
        user_id: str,
        *,
        workspace_id: str,
        workspace_role: BetaWorkspaceRole,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaWorkspaceMember:
        """
        Update Workspace Member

        Args:
          workspace_id: ID of the Workspace.

          user_id: ID of the User.

          workspace_role: New workspace role for the User.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return self._post(
            path_template(
                "/v1/organizations/workspaces/{workspace_id}/members/{user_id}?beta=true",
                workspace_id=workspace_id,
                user_id=user_id,
            ),
            body=maybe_transform({"workspace_role": workspace_role}, member_update_params.MemberUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaWorkspaceMember,
        )

    def list(
        self,
        workspace_id: str,
        *,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPage[BetaWorkspaceMember]:
        """
        List Workspace Members

        Args:
          workspace_id: ID of the Workspace.

          after_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately after this object.

          before_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately before this object.

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `1000`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return self._get_api_list(
            path_template("/v1/organizations/workspaces/{workspace_id}/members?beta=true", workspace_id=workspace_id),
            page=SyncPage[BetaWorkspaceMember],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "limit": limit,
                    },
                    member_list_params.MemberListParams,
                ),
            ),
            model=BetaWorkspaceMember,
        )

    def add(
        self,
        workspace_id: str,
        *,
        user_id: str,
        workspace_role: BetaNoBillingWorkspaceRole,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaWorkspaceMember:
        """
        Create Workspace Member

        Args:
          workspace_id: ID of the Workspace.

          user_id: ID of the User.

          workspace_role: Role of the new Workspace Member. Cannot be `workspace_billing`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return self._post(
            path_template("/v1/organizations/workspaces/{workspace_id}/members?beta=true", workspace_id=workspace_id),
            body=maybe_transform(
                {
                    "user_id": user_id,
                    "workspace_role": workspace_role,
                },
                member_add_params.MemberAddParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaWorkspaceMember,
        )

    def remove(
        self,
        user_id: str,
        *,
        workspace_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> MemberRemoveResponse:
        """
        Delete Workspace Member

        Args:
          workspace_id: ID of the Workspace.

          user_id: ID of the User.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return self._delete(
            path_template(
                "/v1/organizations/workspaces/{workspace_id}/members/{user_id}?beta=true",
                workspace_id=workspace_id,
                user_id=user_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
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

    async def retrieve(
        self,
        user_id: str,
        *,
        workspace_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaWorkspaceMember:
        """
        Get Workspace Member

        Args:
          workspace_id: ID of the Workspace.

          user_id: ID of the User.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return await self._get(
            path_template(
                "/v1/organizations/workspaces/{workspace_id}/members/{user_id}?beta=true",
                workspace_id=workspace_id,
                user_id=user_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaWorkspaceMember,
        )

    async def update(
        self,
        user_id: str,
        *,
        workspace_id: str,
        workspace_role: BetaWorkspaceRole,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaWorkspaceMember:
        """
        Update Workspace Member

        Args:
          workspace_id: ID of the Workspace.

          user_id: ID of the User.

          workspace_role: New workspace role for the User.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return await self._post(
            path_template(
                "/v1/organizations/workspaces/{workspace_id}/members/{user_id}?beta=true",
                workspace_id=workspace_id,
                user_id=user_id,
            ),
            body=await async_maybe_transform(
                {"workspace_role": workspace_role}, member_update_params.MemberUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaWorkspaceMember,
        )

    def list(
        self,
        workspace_id: str,
        *,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaWorkspaceMember, AsyncPage[BetaWorkspaceMember]]:
        """
        List Workspace Members

        Args:
          workspace_id: ID of the Workspace.

          after_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately after this object.

          before_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately before this object.

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `1000`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return self._get_api_list(
            path_template("/v1/organizations/workspaces/{workspace_id}/members?beta=true", workspace_id=workspace_id),
            page=AsyncPage[BetaWorkspaceMember],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "limit": limit,
                    },
                    member_list_params.MemberListParams,
                ),
            ),
            model=BetaWorkspaceMember,
        )

    async def add(
        self,
        workspace_id: str,
        *,
        user_id: str,
        workspace_role: BetaNoBillingWorkspaceRole,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaWorkspaceMember:
        """
        Create Workspace Member

        Args:
          workspace_id: ID of the Workspace.

          user_id: ID of the User.

          workspace_role: Role of the new Workspace Member. Cannot be `workspace_billing`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return await self._post(
            path_template("/v1/organizations/workspaces/{workspace_id}/members?beta=true", workspace_id=workspace_id),
            body=await async_maybe_transform(
                {
                    "user_id": user_id,
                    "workspace_role": workspace_role,
                },
                member_add_params.MemberAddParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaWorkspaceMember,
        )

    async def remove(
        self,
        user_id: str,
        *,
        workspace_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> MemberRemoveResponse:
        """
        Delete Workspace Member

        Args:
          workspace_id: ID of the Workspace.

          user_id: ID of the User.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return await self._delete(
            path_template(
                "/v1/organizations/workspaces/{workspace_id}/members/{user_id}?beta=true",
                workspace_id=workspace_id,
                user_id=user_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MemberRemoveResponse,
        )


class MembersWithRawResponse:
    def __init__(self, members: Members) -> None:
        self._members = members

        self.retrieve = to_raw_response_wrapper(
            members.retrieve,
        )
        self.update = to_raw_response_wrapper(
            members.update,
        )
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

        self.retrieve = async_to_raw_response_wrapper(
            members.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            members.update,
        )
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

        self.retrieve = to_streamed_response_wrapper(
            members.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            members.update,
        )
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

        self.retrieve = async_to_streamed_response_wrapper(
            members.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            members.update,
        )
        self.list = async_to_streamed_response_wrapper(
            members.list,
        )
        self.add = async_to_streamed_response_wrapper(
            members.add,
        )
        self.remove = async_to_streamed_response_wrapper(
            members.remove,
        )
