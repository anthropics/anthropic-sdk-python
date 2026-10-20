from __future__ import annotations

from typing import Dict, Optional

import httpx2

from ...types import (
    UserProfileListOrder,
    UserProfileAccessType,
    UserProfileListOrderBy,
    UserProfileExternalUserDetailsParams,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, strip_not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .action_urls import (
    ActionURLs,
    AsyncActionURLs,
    ActionURLsWithRawResponse,
    AsyncActionURLsWithRawResponse,
    ActionURLsWithStreamingResponse,
    AsyncActionURLsWithStreamingResponse,
)
from ...pagination import SyncPageCursor, AsyncPageCursor
from ..._base_client import AsyncPaginator, make_request_options
from ...types.user_profile import UserProfile
from ...types.deleted_user_profile import DeletedUserProfile
from ...types.user_profile_list_order import UserProfileListOrder
from ...types.user_profile_access_type import UserProfileAccessType
from ...types.user_profile_list_order_by import UserProfileListOrderBy
from ...types.user_profile_external_user_details_params import UserProfileExternalUserDetailsParams

__all__ = ["UserProfiles", "AsyncUserProfiles"]


class UserProfiles(SyncAPIResource):
    @cached_property
    def action_urls(self) -> ActionURLs:
        return ActionURLs(self._client)

    @cached_property
    def with_raw_response(self) -> UserProfilesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return UserProfilesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UserProfilesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return UserProfilesWithStreamingResponse(self)

    def create(
        self,
        *,
        access_type: UserProfileAccessType | Omit = omit,
        external_user_details: UserProfileExternalUserDetailsParams | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> UserProfile:
        """
        Create User Profile

        Args:
          access_type: How the platform uses the API for this entity. `application` (default): the
              profile represents an individual end-user of the platform's product.
              `passthrough`: the profile identifies a company the platform resells Claude
              access to.

          external_user_details: Details about the entity this profile represents, as the platform states them.
              Every field is optional. Not accepted under the legacy
              `user-profiles-2026-03-24` and `user-profiles-2026-08-18` beta headers, which
              take the top-level `external_id` (and, under `user-profiles-2026-08-18`,
              `external_user_onboarded_at`) instead.

          metadata: Free-form key-value data to attach to this user profile. Maximum 16 keys, with
              keys up to 64 characters and values up to 512 characters. Values must be
              non-empty strings.

          name: Optional for all profiles. Real-world name of the entity this profile represents
              (company or individual); for a company the platform resells Claude access to
              (`access_type` `passthrough`), that company's name where known. Maximum 255
              characters.

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"anthropic-workspace-id": workspace_id}), **(extra_headers or {})}
        return self._post(
            "/v1/user_profiles",
            body={
                "access_type": access_type,
                "external_user_details": external_user_details,
                "metadata": metadata,
                "name": name,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.user_profiles.create",
                span_route="/v1/user_profiles",
                span_created_id="anthropic.user_profile.id",
            ),
            cast_to=UserProfile,
        )

    def retrieve(
        self,
        user_profile_id: str,
        *,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> UserProfile:
        """
        Get User Profile

        Args:
          user_profile_id: The ID of the user profile to get (`uprof_...`).

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_profile_id:
            raise ValueError(f"Expected a non-empty value for `user_profile_id` but received {user_profile_id!r}")
        extra_headers = {**strip_not_given({"anthropic-workspace-id": workspace_id}), **(extra_headers or {})}
        return self._get(
            path_template("/v1/user_profiles/{user_profile_id}", user_profile_id=user_profile_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.user_profiles.retrieve",
                span_route="/v1/user_profiles/{user_profile_id}",
                span_attributes={"anthropic.user_profile.id": user_profile_id},
            ),
            cast_to=UserProfile,
        )

    def update(
        self,
        user_profile_id: str,
        *,
        access_type: Optional[UserProfileAccessType] | Omit = omit,
        external_user_details: UserProfileExternalUserDetailsParams | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> UserProfile:
        """
        Update User Profile

        Args:
          user_profile_id: The ID of the user profile to update (`uprof_...`).

          access_type: If present, replaces the stored access type. Omit to leave unchanged.

          external_user_details: Details about the entity this profile represents, as the platform states them.
              Each field sent replaces the stored value; omit a field to leave it unchanged.
              Once set, a value cannot be cleared and `null` is rejected. Not accepted under
              the legacy `user-profiles-2026-03-24` and `user-profiles-2026-08-18` beta
              headers.

          metadata: Key-value pairs to merge into the stored metadata. Keys provided overwrite
              existing values. To remove a key, set its value to an empty string. Keys not
              provided are left unchanged. Maximum 16 keys, with keys up to 64 characters and
              values up to 512 characters.

          name: If present, replaces the stored name. Omit to leave unchanged. Maximum 255
              characters.

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_profile_id:
            raise ValueError(f"Expected a non-empty value for `user_profile_id` but received {user_profile_id!r}")
        extra_headers = {**strip_not_given({"anthropic-workspace-id": workspace_id}), **(extra_headers or {})}
        return self._post(
            path_template("/v1/user_profiles/{user_profile_id}", user_profile_id=user_profile_id),
            body={
                "access_type": access_type,
                "external_user_details": external_user_details,
                "metadata": metadata,
                "name": name,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.user_profiles.update",
                span_route="/v1/user_profiles/{user_profile_id}",
                span_attributes={"anthropic.user_profile.id": user_profile_id},
            ),
            cast_to=UserProfile,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        order: UserProfileListOrder | Omit = omit,
        order_by: UserProfileListOrderBy | Omit = omit,
        page: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[UserProfile]:
        """
        List User Profiles

        Args:
          limit: The maximum number of user profiles to return, from 1 to 100. Defaults to 20.

          order: The sort direction, applied to the field that `order_by` selects. Defaults to
              `desc`.

          order_by: The field to sort user profiles by, in the direction that `order` sets. Defaults
              to `created_at`.

          page: The cursor for the page to return, taken from `next_page` in a previous
              response.

              Leave it out to get the first page.

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"anthropic-workspace-id": workspace_id}), **(extra_headers or {})}
        return self._get_api_list(
            "/v1/user_profiles",
            page=SyncPageCursor[UserProfile],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "order": order,
                    "order_by": order_by,
                    "page": page,
                },
                span_name="anthropic.user_profiles.list",
                span_route="/v1/user_profiles",
            ),
            model=UserProfile,
        )

    def delete(
        self,
        user_profile_id: str,
        *,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedUserProfile:
        """
        Delete User Profile

        Args:
          user_profile_id: The ID of the user profile to delete (`uprof_...`).

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_profile_id:
            raise ValueError(f"Expected a non-empty value for `user_profile_id` but received {user_profile_id!r}")
        extra_headers = {**strip_not_given({"anthropic-workspace-id": workspace_id}), **(extra_headers or {})}
        return self._delete(
            path_template("/v1/user_profiles/{user_profile_id}", user_profile_id=user_profile_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.user_profiles.delete",
                span_route="/v1/user_profiles/{user_profile_id}",
                span_attributes={"anthropic.user_profile.id": user_profile_id},
            ),
            cast_to=DeletedUserProfile,
        )


class AsyncUserProfiles(AsyncAPIResource):
    @cached_property
    def action_urls(self) -> AsyncActionURLs:
        return AsyncActionURLs(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncUserProfilesWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncUserProfilesWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUserProfilesWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncUserProfilesWithStreamingResponse(self)

    async def create(
        self,
        *,
        access_type: UserProfileAccessType | Omit = omit,
        external_user_details: UserProfileExternalUserDetailsParams | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> UserProfile:
        """
        Create User Profile

        Args:
          access_type: How the platform uses the API for this entity. `application` (default): the
              profile represents an individual end-user of the platform's product.
              `passthrough`: the profile identifies a company the platform resells Claude
              access to.

          external_user_details: Details about the entity this profile represents, as the platform states them.
              Every field is optional. Not accepted under the legacy
              `user-profiles-2026-03-24` and `user-profiles-2026-08-18` beta headers, which
              take the top-level `external_id` (and, under `user-profiles-2026-08-18`,
              `external_user_onboarded_at`) instead.

          metadata: Free-form key-value data to attach to this user profile. Maximum 16 keys, with
              keys up to 64 characters and values up to 512 characters. Values must be
              non-empty strings.

          name: Optional for all profiles. Real-world name of the entity this profile represents
              (company or individual); for a company the platform resells Claude access to
              (`access_type` `passthrough`), that company's name where known. Maximum 255
              characters.

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"anthropic-workspace-id": workspace_id}), **(extra_headers or {})}
        return await self._post(
            "/v1/user_profiles",
            body={
                "access_type": access_type,
                "external_user_details": external_user_details,
                "metadata": metadata,
                "name": name,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.user_profiles.create",
                span_route="/v1/user_profiles",
                span_created_id="anthropic.user_profile.id",
            ),
            cast_to=UserProfile,
        )

    async def retrieve(
        self,
        user_profile_id: str,
        *,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> UserProfile:
        """
        Get User Profile

        Args:
          user_profile_id: The ID of the user profile to get (`uprof_...`).

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_profile_id:
            raise ValueError(f"Expected a non-empty value for `user_profile_id` but received {user_profile_id!r}")
        extra_headers = {**strip_not_given({"anthropic-workspace-id": workspace_id}), **(extra_headers or {})}
        return await self._get(
            path_template("/v1/user_profiles/{user_profile_id}", user_profile_id=user_profile_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.user_profiles.retrieve",
                span_route="/v1/user_profiles/{user_profile_id}",
                span_attributes={"anthropic.user_profile.id": user_profile_id},
            ),
            cast_to=UserProfile,
        )

    async def update(
        self,
        user_profile_id: str,
        *,
        access_type: Optional[UserProfileAccessType] | Omit = omit,
        external_user_details: UserProfileExternalUserDetailsParams | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> UserProfile:
        """
        Update User Profile

        Args:
          user_profile_id: The ID of the user profile to update (`uprof_...`).

          access_type: If present, replaces the stored access type. Omit to leave unchanged.

          external_user_details: Details about the entity this profile represents, as the platform states them.
              Each field sent replaces the stored value; omit a field to leave it unchanged.
              Once set, a value cannot be cleared and `null` is rejected. Not accepted under
              the legacy `user-profiles-2026-03-24` and `user-profiles-2026-08-18` beta
              headers.

          metadata: Key-value pairs to merge into the stored metadata. Keys provided overwrite
              existing values. To remove a key, set its value to an empty string. Keys not
              provided are left unchanged. Maximum 16 keys, with keys up to 64 characters and
              values up to 512 characters.

          name: If present, replaces the stored name. Omit to leave unchanged. Maximum 255
              characters.

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_profile_id:
            raise ValueError(f"Expected a non-empty value for `user_profile_id` but received {user_profile_id!r}")
        extra_headers = {**strip_not_given({"anthropic-workspace-id": workspace_id}), **(extra_headers or {})}
        return await self._post(
            path_template("/v1/user_profiles/{user_profile_id}", user_profile_id=user_profile_id),
            body={
                "access_type": access_type,
                "external_user_details": external_user_details,
                "metadata": metadata,
                "name": name,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.user_profiles.update",
                span_route="/v1/user_profiles/{user_profile_id}",
                span_attributes={"anthropic.user_profile.id": user_profile_id},
            ),
            cast_to=UserProfile,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        order: UserProfileListOrder | Omit = omit,
        order_by: UserProfileListOrderBy | Omit = omit,
        page: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[UserProfile, AsyncPageCursor[UserProfile]]:
        """
        List User Profiles

        Args:
          limit: The maximum number of user profiles to return, from 1 to 100. Defaults to 20.

          order: The sort direction, applied to the field that `order_by` selects. Defaults to
              `desc`.

          order_by: The field to sort user profiles by, in the direction that `order` sets. Defaults
              to `created_at`.

          page: The cursor for the page to return, taken from `next_page` in a previous
              response.

              Leave it out to get the first page.

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"anthropic-workspace-id": workspace_id}), **(extra_headers or {})}
        return self._get_api_list(
            "/v1/user_profiles",
            page=AsyncPageCursor[UserProfile],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "order": order,
                    "order_by": order_by,
                    "page": page,
                },
                span_name="anthropic.user_profiles.list",
                span_route="/v1/user_profiles",
            ),
            model=UserProfile,
        )

    async def delete(
        self,
        user_profile_id: str,
        *,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> DeletedUserProfile:
        """
        Delete User Profile

        Args:
          user_profile_id: The ID of the user profile to delete (`uprof_...`).

          workspace_id: Optional header to select the Workspace for this request. The value is a
              Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

              Only needed for credentials that can act on more than one Workspace. A
              credential that belongs to a specific Workspace may omit it; if sent, it must
              match that Workspace.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_profile_id:
            raise ValueError(f"Expected a non-empty value for `user_profile_id` but received {user_profile_id!r}")
        extra_headers = {**strip_not_given({"anthropic-workspace-id": workspace_id}), **(extra_headers or {})}
        return await self._delete(
            path_template("/v1/user_profiles/{user_profile_id}", user_profile_id=user_profile_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                span_name="anthropic.user_profiles.delete",
                span_route="/v1/user_profiles/{user_profile_id}",
                span_attributes={"anthropic.user_profile.id": user_profile_id},
            ),
            cast_to=DeletedUserProfile,
        )


class UserProfilesWithRawResponse:
    def __init__(self, user_profiles: UserProfiles) -> None:
        self._user_profiles = user_profiles

        self.create = to_raw_response_wrapper(
            user_profiles.create,
        )
        self.retrieve = to_raw_response_wrapper(
            user_profiles.retrieve,
        )
        self.update = to_raw_response_wrapper(
            user_profiles.update,
        )
        self.list = to_raw_response_wrapper(
            user_profiles.list,
        )
        self.delete = to_raw_response_wrapper(
            user_profiles.delete,
        )

    @cached_property
    def action_urls(self) -> ActionURLsWithRawResponse:
        return ActionURLsWithRawResponse(self._user_profiles.action_urls)


class AsyncUserProfilesWithRawResponse:
    def __init__(self, user_profiles: AsyncUserProfiles) -> None:
        self._user_profiles = user_profiles

        self.create = async_to_raw_response_wrapper(
            user_profiles.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            user_profiles.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            user_profiles.update,
        )
        self.list = async_to_raw_response_wrapper(
            user_profiles.list,
        )
        self.delete = async_to_raw_response_wrapper(
            user_profiles.delete,
        )

    @cached_property
    def action_urls(self) -> AsyncActionURLsWithRawResponse:
        return AsyncActionURLsWithRawResponse(self._user_profiles.action_urls)


class UserProfilesWithStreamingResponse:
    def __init__(self, user_profiles: UserProfiles) -> None:
        self._user_profiles = user_profiles

        self.create = to_streamed_response_wrapper(
            user_profiles.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            user_profiles.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            user_profiles.update,
        )
        self.list = to_streamed_response_wrapper(
            user_profiles.list,
        )
        self.delete = to_streamed_response_wrapper(
            user_profiles.delete,
        )

    @cached_property
    def action_urls(self) -> ActionURLsWithStreamingResponse:
        return ActionURLsWithStreamingResponse(self._user_profiles.action_urls)


class AsyncUserProfilesWithStreamingResponse:
    def __init__(self, user_profiles: AsyncUserProfiles) -> None:
        self._user_profiles = user_profiles

        self.create = async_to_streamed_response_wrapper(
            user_profiles.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            user_profiles.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            user_profiles.update,
        )
        self.list = async_to_streamed_response_wrapper(
            user_profiles.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            user_profiles.delete,
        )

    @cached_property
    def action_urls(self) -> AsyncActionURLsWithStreamingResponse:
        return AsyncActionURLsWithStreamingResponse(self._user_profiles.action_urls)
