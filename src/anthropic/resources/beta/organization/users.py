from __future__ import annotations

from typing import List
from itertools import chain
from typing_extensions import Literal

import httpx2

from ...._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ...._utils import is_given, path_template, strip_not_given
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....pagination import SyncPage, AsyncPage
from ...._base_client import AsyncPaginator, make_request_options
from ....types.anthropic_beta_param import AnthropicBetaParam
from ....types.beta.organization.user_remove_response import UserRemoveResponse
from ....types.beta.organization.beta_organization_user import BetaOrganizationUser

__all__ = ["Users", "AsyncUsers"]


class Users(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UsersWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return UsersWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UsersWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return UsersWithStreamingResponse(self)

    def retrieve(
        self,
        user_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaOrganizationUser:
        """
        Retrieve a member of the organization by user ID.

        Args:
          user_id: ID of the User.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return self._get(
            path_template("/v1/organizations/users/{user_id}", user_id=user_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.users.retrieve",
                span_route="/v1/organizations/users/{user_id}",
                span_attributes={"anthropic.organization.user.id": user_id},
            ),
            cast_to=BetaOrganizationUser,
        )

    def update(
        self,
        user_id: str,
        *,
        role: Literal["billing", "claude_code_user", "developer", "managed", "user"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaOrganizationUser:
        """
        Update a member's organization role.

        Args:
          user_id: ID of the User.

          role: New role for the User.

              The accepted values depend on the organization type. Console and API
              organizations accept `user`, `developer`, `billing`, and `claude_code_user`;
              `admin` cannot be assigned through the API. Claude Enterprise organizations
              accept `user` and `managed`; changing a User's role to `managed` requires the
              `write:rbac_groups` scope in addition to `write:members`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          SandboxEgressRestrictedError:
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return self._post(
            path_template("/v1/organizations/users/{user_id}", user_id=user_id),
            body={"role": role},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.users.update",
                span_route="/v1/organizations/users/{user_id}",
                span_attributes={"anthropic.organization.user.id": user_id},
            ),
            cast_to=BetaOrganizationUser,
        )

    def list(
        self,
        *,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        email: str | Omit = omit,
        limit: int | Omit = omit,
        roles: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPage[BetaOrganizationUser]:
        """
        List the organization's members.

        Args:
          after_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately after this object.

          before_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately before this object.

          email: Filter by user email.

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `1000`.

          roles: Filter to items whose `role` equals one of the supplied values. Repeatable;
              values are OR'ed together.

              Accepted values depend on the organization type: Console and API organizations
              accept `user`, `developer`, `billing`, `admin`, and `claude_code_user`; Claude
              Enterprise organizations accept `user`, `owner`, `primary_owner`,
              `membership_admin`, and `managed`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/users",
            page=SyncPage[BetaOrganizationUser],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "after_id": after_id,
                    "before_id": before_id,
                    "email": email,
                    "limit": limit,
                    "roles": roles,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.users.list",
                span_route="/v1/organizations/users",
            ),
            model=BetaOrganizationUser,
        )

    def remove(
        self,
        user_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> UserRemoveResponse:
        """
        Remove a member from the organization.

        Args:
          user_id: ID of the User.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          CannotRemoveLastMemberError:

          SandboxEgressRestrictedError:

          ConcurrentMembershipChangeError:
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return self._delete(
            path_template("/v1/organizations/users/{user_id}", user_id=user_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.users.remove",
                span_route="/v1/organizations/users/{user_id}",
                span_attributes={"anthropic.organization.user.id": user_id},
            ),
            cast_to=UserRemoveResponse,
        )

    def sign_out(
        self,
        user_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaOrganizationUser:
        """
        Sign a member out of Claude everywhere, without removing them from the
        organization. This ends their sign-in sessions and removes their trusted devices
        wherever they use Claude, including other organizations and individual plans. It
        also ends the OAuth tokens issued to them for this organization, so apps such as
        Claude Code must sign in again.

        A token can take up to an hour to stop working, though it almost always stops at
        once. The member keeps their role and can sign in again right away. To keep them
        out, remove them from the organization or, if your organization uses single
        sign-on, block them in your identity provider. Signing out does not end API
        keys, OAuth tokens that were not issued for this organization, or the member's
        Claude Code cloud sessions and routines.

        You cannot sign out the organization's primary owner or the person your API key
        or token acts for, and a request to sign out another owner, a member with owner
        permissions, or a membership admin may be refused. A refused request returns a
        `400` or `403` error that says why. If the request returns `503`, send it again
        to finish; anything already ended stays ended.

        Every request must include the beta header
        `anthropic-beta: admin-user-sign-out-2026-10-08`. A request without it returns
        `400`. Sign-out is in beta for Claude Enterprise organizations. In an
        organization where it is not enabled, a request returns `400` with `error_code`
        `organization_not_enrolled_in_beta`. In a Claude Enterprise organization, an API
        key needs the `write:members` scope; a key without it gets `403`.

        Args:
          user_id: ID of the User.

          betas: This endpoint is in beta: requests must send `admin-user-sign-out-2026-10-08` in
              this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaCannotSignOutPrimaryOwnerError:

          BetaCannotSignOutSelfError:

          BetaOrganizationNotEnrolledInBetaError:

          BetaCannotSignOutManagedMemberError:

          BetaCannotSignOutMembershipAdminError:

          BetaCannotSignOutOwnerError:

          BetaCannotSignOutPrivilegedMemberError:

          SandboxEgressRestrictedError:
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["admin-user-sign-out-2026-10-08"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "admin-user-sign-out-2026-10-08", **(extra_headers or {})}
        return self._post(
            path_template("/v1/organizations/users/{user_id}/sign_out", user_id=user_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.users.sign_out",
                span_route="/v1/organizations/users/{user_id}/sign_out",
                span_attributes={"anthropic.organization.user.id": user_id},
            ),
            cast_to=BetaOrganizationUser,
        )


class AsyncUsers(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUsersWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncUsersWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUsersWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncUsersWithStreamingResponse(self)

    async def retrieve(
        self,
        user_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaOrganizationUser:
        """
        Retrieve a member of the organization by user ID.

        Args:
          user_id: ID of the User.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return await self._get(
            path_template("/v1/organizations/users/{user_id}", user_id=user_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.users.retrieve",
                span_route="/v1/organizations/users/{user_id}",
                span_attributes={"anthropic.organization.user.id": user_id},
            ),
            cast_to=BetaOrganizationUser,
        )

    async def update(
        self,
        user_id: str,
        *,
        role: Literal["billing", "claude_code_user", "developer", "managed", "user"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaOrganizationUser:
        """
        Update a member's organization role.

        Args:
          user_id: ID of the User.

          role: New role for the User.

              The accepted values depend on the organization type. Console and API
              organizations accept `user`, `developer`, `billing`, and `claude_code_user`;
              `admin` cannot be assigned through the API. Claude Enterprise organizations
              accept `user` and `managed`; changing a User's role to `managed` requires the
              `write:rbac_groups` scope in addition to `write:members`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          SandboxEgressRestrictedError:
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return await self._post(
            path_template("/v1/organizations/users/{user_id}", user_id=user_id),
            body={"role": role},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.users.update",
                span_route="/v1/organizations/users/{user_id}",
                span_attributes={"anthropic.organization.user.id": user_id},
            ),
            cast_to=BetaOrganizationUser,
        )

    def list(
        self,
        *,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        email: str | Omit = omit,
        limit: int | Omit = omit,
        roles: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaOrganizationUser, AsyncPage[BetaOrganizationUser]]:
        """
        List the organization's members.

        Args:
          after_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately after this object.

          before_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately before this object.

          email: Filter by user email.

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `1000`.

          roles: Filter to items whose `role` equals one of the supplied values. Repeatable;
              values are OR'ed together.

              Accepted values depend on the organization type: Console and API organizations
              accept `user`, `developer`, `billing`, `admin`, and `claude_code_user`; Claude
              Enterprise organizations accept `user`, `owner`, `primary_owner`,
              `membership_admin`, and `managed`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/users",
            page=AsyncPage[BetaOrganizationUser],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "after_id": after_id,
                    "before_id": before_id,
                    "email": email,
                    "limit": limit,
                    "roles": roles,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.users.list",
                span_route="/v1/organizations/users",
            ),
            model=BetaOrganizationUser,
        )

    async def remove(
        self,
        user_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> UserRemoveResponse:
        """
        Remove a member from the organization.

        Args:
          user_id: ID of the User.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          CannotRemoveLastMemberError:

          SandboxEgressRestrictedError:

          ConcurrentMembershipChangeError:
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return await self._delete(
            path_template("/v1/organizations/users/{user_id}", user_id=user_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.users.remove",
                span_route="/v1/organizations/users/{user_id}",
                span_attributes={"anthropic.organization.user.id": user_id},
            ),
            cast_to=UserRemoveResponse,
        )

    async def sign_out(
        self,
        user_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaOrganizationUser:
        """
        Sign a member out of Claude everywhere, without removing them from the
        organization. This ends their sign-in sessions and removes their trusted devices
        wherever they use Claude, including other organizations and individual plans. It
        also ends the OAuth tokens issued to them for this organization, so apps such as
        Claude Code must sign in again.

        A token can take up to an hour to stop working, though it almost always stops at
        once. The member keeps their role and can sign in again right away. To keep them
        out, remove them from the organization or, if your organization uses single
        sign-on, block them in your identity provider. Signing out does not end API
        keys, OAuth tokens that were not issued for this organization, or the member's
        Claude Code cloud sessions and routines.

        You cannot sign out the organization's primary owner or the person your API key
        or token acts for, and a request to sign out another owner, a member with owner
        permissions, or a membership admin may be refused. A refused request returns a
        `400` or `403` error that says why. If the request returns `503`, send it again
        to finish; anything already ended stays ended.

        Every request must include the beta header
        `anthropic-beta: admin-user-sign-out-2026-10-08`. A request without it returns
        `400`. Sign-out is in beta for Claude Enterprise organizations. In an
        organization where it is not enabled, a request returns `400` with `error_code`
        `organization_not_enrolled_in_beta`. In a Claude Enterprise organization, an API
        key needs the `write:members` scope; a key without it gets `403`.

        Args:
          user_id: ID of the User.

          betas: This endpoint is in beta: requests must send `admin-user-sign-out-2026-10-08` in
              this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaCannotSignOutPrimaryOwnerError:

          BetaCannotSignOutSelfError:

          BetaOrganizationNotEnrolledInBetaError:

          BetaCannotSignOutManagedMemberError:

          BetaCannotSignOutMembershipAdminError:

          BetaCannotSignOutOwnerError:

          BetaCannotSignOutPrivilegedMemberError:

          SandboxEgressRestrictedError:
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["admin-user-sign-out-2026-10-08"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "admin-user-sign-out-2026-10-08", **(extra_headers or {})}
        return await self._post(
            path_template("/v1/organizations/users/{user_id}/sign_out", user_id=user_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.users.sign_out",
                span_route="/v1/organizations/users/{user_id}/sign_out",
                span_attributes={"anthropic.organization.user.id": user_id},
            ),
            cast_to=BetaOrganizationUser,
        )


class UsersWithRawResponse:
    def __init__(self, users: Users) -> None:
        self._users = users

        self.retrieve = to_raw_response_wrapper(
            users.retrieve,
        )
        self.update = to_raw_response_wrapper(
            users.update,
        )
        self.list = to_raw_response_wrapper(
            users.list,
        )
        self.remove = to_raw_response_wrapper(
            users.remove,
        )
        self.sign_out = to_raw_response_wrapper(
            users.sign_out,
        )


class AsyncUsersWithRawResponse:
    def __init__(self, users: AsyncUsers) -> None:
        self._users = users

        self.retrieve = async_to_raw_response_wrapper(
            users.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            users.update,
        )
        self.list = async_to_raw_response_wrapper(
            users.list,
        )
        self.remove = async_to_raw_response_wrapper(
            users.remove,
        )
        self.sign_out = async_to_raw_response_wrapper(
            users.sign_out,
        )


class UsersWithStreamingResponse:
    def __init__(self, users: Users) -> None:
        self._users = users

        self.retrieve = to_streamed_response_wrapper(
            users.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            users.update,
        )
        self.list = to_streamed_response_wrapper(
            users.list,
        )
        self.remove = to_streamed_response_wrapper(
            users.remove,
        )
        self.sign_out = to_streamed_response_wrapper(
            users.sign_out,
        )


class AsyncUsersWithStreamingResponse:
    def __init__(self, users: AsyncUsers) -> None:
        self._users = users

        self.retrieve = async_to_streamed_response_wrapper(
            users.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            users.update,
        )
        self.list = async_to_streamed_response_wrapper(
            users.list,
        )
        self.remove = async_to_streamed_response_wrapper(
            users.remove,
        )
        self.sign_out = async_to_streamed_response_wrapper(
            users.sign_out,
        )
