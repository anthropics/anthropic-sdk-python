# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx2

from ...._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ...._utils import path_template, maybe_transform, async_maybe_transform
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
from ....types.beta.organization import invite_list_params, invite_create_params
from ....types.beta.organization.invite_delete_response import InviteDeleteResponse
from ....types.beta.organization.beta_organization_invite import BetaOrganizationInvite

__all__ = ["Invites", "AsyncInvites"]


class Invites(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> InvitesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return InvitesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> InvitesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return InvitesWithStreamingResponse(self)

    def create(
        self,
        *,
        email: str,
        role: Literal["billing", "claude_code_user", "developer", "managed", "user"],
        rbac_group_ids: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaOrganizationInvite:
        """
        Invite a user to join the organization by email.

        On plans that draw members from a finite pool of purchased seats, the invite
        automatically consumes a seat from the lowest tier with availability; there is
        no seat-tier parameter. When no seat is free the request fails with a 400 error
        rather than purchasing a seat.

        Args:
          email: Email of the User.

          role: Role for the invited User.

              The accepted values depend on the organization type. Console and API
              organizations accept `user`, `developer`, `billing`, and `claude_code_user`;
              `admin` cannot be assigned through the API. Claude Enterprise organizations
              accept `user` and `managed`.

          rbac_group_ids: RBAC group IDs to assign to the User when the Invite is accepted. A non-empty
              array is accepted only for a Claude Enterprise organization with RBAC groups,
              and requires the key to carry the `write:rbac_groups` scope.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/organizations/invites?beta=true",
            body=maybe_transform(
                {
                    "email": email,
                    "role": role,
                    "rbac_group_ids": rbac_group_ids,
                },
                invite_create_params.InviteCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaOrganizationInvite,
        )

    def retrieve(
        self,
        invite_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaOrganizationInvite:
        """
        Retrieve an invite by ID.

        Args:
          invite_id: ID of the Invite.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not invite_id:
            raise ValueError(f"Expected a non-empty value for `invite_id` but received {invite_id!r}")
        return self._get(
            path_template("/v1/organizations/invites/{invite_id}?beta=true", invite_id=invite_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaOrganizationInvite,
        )

    def list(
        self,
        *,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        email: str | Omit = omit,
        limit: int | Omit = omit,
        roles: SequenceNotStr[str] | Omit = omit,
        statuses: List[Literal["accepted", "expired", "pending"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPage[BetaOrganizationInvite]:
        """
        List the organization's invites.

        Args:
          after_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately after this object.

          before_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately before this object.

          email: Filter by the email address the Invite was sent to. Matches the same way as the
              Users list's `email` filter (normalized, case-insensitive).

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `1000`.

          roles: Filter to items whose `role` equals one of the supplied values. Repeatable;
              values are OR'ed together.

              Accepted values depend on the organization type: Console and API organizations
              accept `user`, `developer`, `billing`, `admin`, and `claude_code_user`; Claude
              Enterprise organizations accept `user`, `owner`, `primary_owner`,
              `membership_admin`, and `managed`.

          statuses: Filter by Invite status. Repeatable; values are OR'ed together. Omit to return
              `pending`, `accepted`, and `expired` Invites alike.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/invites?beta=true",
            page=SyncPage[BetaOrganizationInvite],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "email": email,
                        "limit": limit,
                        "roles": roles,
                        "statuses": statuses,
                    },
                    invite_list_params.InviteListParams,
                ),
            ),
            model=BetaOrganizationInvite,
        )

    def delete(
        self,
        invite_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> InviteDeleteResponse:
        """
        Delete a pending invite.

        Args:
          invite_id: ID of the Invite.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not invite_id:
            raise ValueError(f"Expected a non-empty value for `invite_id` but received {invite_id!r}")
        return self._delete(
            path_template("/v1/organizations/invites/{invite_id}?beta=true", invite_id=invite_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InviteDeleteResponse,
        )


class AsyncInvites(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncInvitesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncInvitesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncInvitesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncInvitesWithStreamingResponse(self)

    async def create(
        self,
        *,
        email: str,
        role: Literal["billing", "claude_code_user", "developer", "managed", "user"],
        rbac_group_ids: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaOrganizationInvite:
        """
        Invite a user to join the organization by email.

        On plans that draw members from a finite pool of purchased seats, the invite
        automatically consumes a seat from the lowest tier with availability; there is
        no seat-tier parameter. When no seat is free the request fails with a 400 error
        rather than purchasing a seat.

        Args:
          email: Email of the User.

          role: Role for the invited User.

              The accepted values depend on the organization type. Console and API
              organizations accept `user`, `developer`, `billing`, and `claude_code_user`;
              `admin` cannot be assigned through the API. Claude Enterprise organizations
              accept `user` and `managed`.

          rbac_group_ids: RBAC group IDs to assign to the User when the Invite is accepted. A non-empty
              array is accepted only for a Claude Enterprise organization with RBAC groups,
              and requires the key to carry the `write:rbac_groups` scope.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/organizations/invites?beta=true",
            body=await async_maybe_transform(
                {
                    "email": email,
                    "role": role,
                    "rbac_group_ids": rbac_group_ids,
                },
                invite_create_params.InviteCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaOrganizationInvite,
        )

    async def retrieve(
        self,
        invite_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaOrganizationInvite:
        """
        Retrieve an invite by ID.

        Args:
          invite_id: ID of the Invite.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not invite_id:
            raise ValueError(f"Expected a non-empty value for `invite_id` but received {invite_id!r}")
        return await self._get(
            path_template("/v1/organizations/invites/{invite_id}?beta=true", invite_id=invite_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaOrganizationInvite,
        )

    def list(
        self,
        *,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        email: str | Omit = omit,
        limit: int | Omit = omit,
        roles: SequenceNotStr[str] | Omit = omit,
        statuses: List[Literal["accepted", "expired", "pending"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaOrganizationInvite, AsyncPage[BetaOrganizationInvite]]:
        """
        List the organization's invites.

        Args:
          after_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately after this object.

          before_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately before this object.

          email: Filter by the email address the Invite was sent to. Matches the same way as the
              Users list's `email` filter (normalized, case-insensitive).

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `1000`.

          roles: Filter to items whose `role` equals one of the supplied values. Repeatable;
              values are OR'ed together.

              Accepted values depend on the organization type: Console and API organizations
              accept `user`, `developer`, `billing`, `admin`, and `claude_code_user`; Claude
              Enterprise organizations accept `user`, `owner`, `primary_owner`,
              `membership_admin`, and `managed`.

          statuses: Filter by Invite status. Repeatable; values are OR'ed together. Omit to return
              `pending`, `accepted`, and `expired` Invites alike.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/invites?beta=true",
            page=AsyncPage[BetaOrganizationInvite],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "email": email,
                        "limit": limit,
                        "roles": roles,
                        "statuses": statuses,
                    },
                    invite_list_params.InviteListParams,
                ),
            ),
            model=BetaOrganizationInvite,
        )

    async def delete(
        self,
        invite_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> InviteDeleteResponse:
        """
        Delete a pending invite.

        Args:
          invite_id: ID of the Invite.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not invite_id:
            raise ValueError(f"Expected a non-empty value for `invite_id` but received {invite_id!r}")
        return await self._delete(
            path_template("/v1/organizations/invites/{invite_id}?beta=true", invite_id=invite_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InviteDeleteResponse,
        )


class InvitesWithRawResponse:
    def __init__(self, invites: Invites) -> None:
        self._invites = invites

        self.create = to_raw_response_wrapper(
            invites.create,
        )
        self.retrieve = to_raw_response_wrapper(
            invites.retrieve,
        )
        self.list = to_raw_response_wrapper(
            invites.list,
        )
        self.delete = to_raw_response_wrapper(
            invites.delete,
        )


class AsyncInvitesWithRawResponse:
    def __init__(self, invites: AsyncInvites) -> None:
        self._invites = invites

        self.create = async_to_raw_response_wrapper(
            invites.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            invites.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            invites.list,
        )
        self.delete = async_to_raw_response_wrapper(
            invites.delete,
        )


class InvitesWithStreamingResponse:
    def __init__(self, invites: Invites) -> None:
        self._invites = invites

        self.create = to_streamed_response_wrapper(
            invites.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            invites.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            invites.list,
        )
        self.delete = to_streamed_response_wrapper(
            invites.delete,
        )


class AsyncInvitesWithStreamingResponse:
    def __init__(self, invites: AsyncInvites) -> None:
        self._invites = invites

        self.create = async_to_streamed_response_wrapper(
            invites.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            invites.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            invites.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            invites.delete,
        )
