from __future__ import annotations

from typing import List
from itertools import chain

import httpx2

from ......_types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ......_utils import is_given, path_template, strip_not_given
from ......_compat import cached_property
from ......_resource import SyncAPIResource, AsyncAPIResource
from ......_response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ......_base_client import make_request_options
from ......types.anthropic_beta_param import AnthropicBetaParam
from ......types.beta.user_profiles.providers.google import (
    BetaGoogleManagedCMEKControlParams,
    BetaGoogleManagedStorageControlParams,
)
from ......types.beta.user_profiles.providers.google.beta_google_managed_data_controls import (
    BetaGoogleManagedDataControls,
)
from ......types.beta.user_profiles.providers.google.beta_google_managed_cmek_control_params import (
    BetaGoogleManagedCMEKControlParams,
)
from ......types.beta.user_profiles.providers.google.beta_google_managed_storage_control_params import (
    BetaGoogleManagedStorageControlParams,
)

__all__ = ["DataControls", "AsyncDataControls"]


class DataControls(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DataControlsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return DataControlsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DataControlsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return DataControlsWithStreamingResponse(self)

    def retrieve(
        self,
        user_profile_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaGoogleManagedDataControls:
        """
        Get the profile's encryption keys and storage buckets for Claude on Google
        Cloud's Agent Platform, with each region's status.

        Args:
          user_profile_id: The ID of the user profile whose Google-managed data controls to retrieve
              (`uprof_...`).

          betas: This endpoint is in beta: requests must send
              `google-managed-data-controls-2026-09-01` in this header.

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
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(
                        chain(
                            (str(e) for e in betas),
                            ["user-profiles-2026-09-04,google-managed-data-controls-2026-09-01"],
                        )
                    )
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {
            "anthropic-beta": "user-profiles-2026-09-04,google-managed-data-controls-2026-09-01",
            **(extra_headers or {}),
        }
        return self._get(
            path_template(
                "/v1/user_profiles/{user_profile_id}/providers/google/data_controls", user_profile_id=user_profile_id
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.user_profiles.providers.google.data_controls.retrieve",
                span_route="/v1/user_profiles/{user_profile_id}/providers/google/data_controls",
                span_attributes={"anthropic.user_profile.id": user_profile_id},
            ),
            cast_to=BetaGoogleManagedDataControls,
        )

    def update(
        self,
        user_profile_id: str,
        *,
        cmek: BetaGoogleManagedCMEKControlParams | Omit = omit,
        storage: BetaGoogleManagedStorageControlParams | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaGoogleManagedDataControls:
        """Turn a control on or off, or change the key or bucket set for a region.

        Controls
        and regions that you leave out stay as they are.

        Args:
          user_profile_id: The ID of the user profile whose Google-managed data controls to update
              (`uprof_...`).

          cmek: The customer-managed encryption key control. Leave it out to keep the control as
              it is. Send `cmek`, `storage`, or both.

          storage: The customer-owned storage control. Leave it out to keep the control as it is.
              Send `cmek`, `storage`, or both.

          betas: This endpoint is in beta: requests must send
              `google-managed-data-controls-2026-09-01` in this header.

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
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(
                        chain(
                            (str(e) for e in betas),
                            ["user-profiles-2026-09-04,google-managed-data-controls-2026-09-01"],
                        )
                    )
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {
            "anthropic-beta": "user-profiles-2026-09-04,google-managed-data-controls-2026-09-01",
            **(extra_headers or {}),
        }
        return self._post(
            path_template(
                "/v1/user_profiles/{user_profile_id}/providers/google/data_controls", user_profile_id=user_profile_id
            ),
            body={
                "cmek": cmek,
                "storage": storage,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.user_profiles.providers.google.data_controls.update",
                span_route="/v1/user_profiles/{user_profile_id}/providers/google/data_controls",
                span_attributes={"anthropic.user_profile.id": user_profile_id},
            ),
            cast_to=BetaGoogleManagedDataControls,
        )


class AsyncDataControls(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDataControlsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncDataControlsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDataControlsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncDataControlsWithStreamingResponse(self)

    async def retrieve(
        self,
        user_profile_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaGoogleManagedDataControls:
        """
        Get the profile's encryption keys and storage buckets for Claude on Google
        Cloud's Agent Platform, with each region's status.

        Args:
          user_profile_id: The ID of the user profile whose Google-managed data controls to retrieve
              (`uprof_...`).

          betas: This endpoint is in beta: requests must send
              `google-managed-data-controls-2026-09-01` in this header.

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
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(
                        chain(
                            (str(e) for e in betas),
                            ["user-profiles-2026-09-04,google-managed-data-controls-2026-09-01"],
                        )
                    )
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {
            "anthropic-beta": "user-profiles-2026-09-04,google-managed-data-controls-2026-09-01",
            **(extra_headers or {}),
        }
        return await self._get(
            path_template(
                "/v1/user_profiles/{user_profile_id}/providers/google/data_controls", user_profile_id=user_profile_id
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.user_profiles.providers.google.data_controls.retrieve",
                span_route="/v1/user_profiles/{user_profile_id}/providers/google/data_controls",
                span_attributes={"anthropic.user_profile.id": user_profile_id},
            ),
            cast_to=BetaGoogleManagedDataControls,
        )

    async def update(
        self,
        user_profile_id: str,
        *,
        cmek: BetaGoogleManagedCMEKControlParams | Omit = omit,
        storage: BetaGoogleManagedStorageControlParams | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaGoogleManagedDataControls:
        """Turn a control on or off, or change the key or bucket set for a region.

        Controls
        and regions that you leave out stay as they are.

        Args:
          user_profile_id: The ID of the user profile whose Google-managed data controls to update
              (`uprof_...`).

          cmek: The customer-managed encryption key control. Leave it out to keep the control as
              it is. Send `cmek`, `storage`, or both.

          storage: The customer-owned storage control. Leave it out to keep the control as it is.
              Send `cmek`, `storage`, or both.

          betas: This endpoint is in beta: requests must send
              `google-managed-data-controls-2026-09-01` in this header.

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
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(
                        chain(
                            (str(e) for e in betas),
                            ["user-profiles-2026-09-04,google-managed-data-controls-2026-09-01"],
                        )
                    )
                    if is_given(betas)
                    else not_given,
                    "anthropic-workspace-id": workspace_id,
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {
            "anthropic-beta": "user-profiles-2026-09-04,google-managed-data-controls-2026-09-01",
            **(extra_headers or {}),
        }
        return await self._post(
            path_template(
                "/v1/user_profiles/{user_profile_id}/providers/google/data_controls", user_profile_id=user_profile_id
            ),
            body={
                "cmek": cmek,
                "storage": storage,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.user_profiles.providers.google.data_controls.update",
                span_route="/v1/user_profiles/{user_profile_id}/providers/google/data_controls",
                span_attributes={"anthropic.user_profile.id": user_profile_id},
            ),
            cast_to=BetaGoogleManagedDataControls,
        )


class DataControlsWithRawResponse:
    def __init__(self, data_controls: DataControls) -> None:
        self._data_controls = data_controls

        self.retrieve = to_raw_response_wrapper(
            data_controls.retrieve,
        )
        self.update = to_raw_response_wrapper(
            data_controls.update,
        )


class AsyncDataControlsWithRawResponse:
    def __init__(self, data_controls: AsyncDataControls) -> None:
        self._data_controls = data_controls

        self.retrieve = async_to_raw_response_wrapper(
            data_controls.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            data_controls.update,
        )


class DataControlsWithStreamingResponse:
    def __init__(self, data_controls: DataControls) -> None:
        self._data_controls = data_controls

        self.retrieve = to_streamed_response_wrapper(
            data_controls.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            data_controls.update,
        )


class AsyncDataControlsWithStreamingResponse:
    def __init__(self, data_controls: AsyncDataControls) -> None:
        self._data_controls = data_controls

        self.retrieve = async_to_streamed_response_wrapper(
            data_controls.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            data_controls.update,
        )
