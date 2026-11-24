from __future__ import annotations

from typing import List
from itertools import chain

import httpx2

from ......._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ......._utils import is_given, path_template, strip_not_given
from ......._compat import cached_property
from ......._resource import SyncAPIResource, AsyncAPIResource
from ......._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ......._base_client import make_request_options
from .......types.anthropic_beta_param import AnthropicBetaParam
from .......types.beta.organization.providers.google.projects import (
    BetaGoogleManagedProjectCMEKControlParams,
    BetaGoogleManagedProjectStorageControlParams,
)
from .......types.beta.organization.providers.google.projects.beta_google_managed_project_data_controls import (
    BetaGoogleManagedProjectDataControls,
)
from .......types.beta.organization.providers.google.projects.beta_google_managed_project_cmek_control_params import (
    BetaGoogleManagedProjectCMEKControlParams,
)
from .......types.beta.organization.providers.google.projects.beta_google_managed_project_storage_control_params import (
    BetaGoogleManagedProjectStorageControlParams,
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
        project_number: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaGoogleManagedProjectDataControls:
        """
        Get a Google Cloud project's encryption keys and storage buckets for Claude on
        Google Cloud's Agent Platform, with each region's status.

        Your organization must have proved that it owns the project.

        Args:
          project_number: The Google Cloud project's number, such as `123456789012`, not its project ID.

          betas: This endpoint is in beta: requests must send
              `google-managed-data-controls-2026-09-01` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_number:
            raise ValueError(f"Expected a non-empty value for `project_number` but received {project_number!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(
                        chain((str(e) for e in betas), ["google-managed-data-controls-2026-09-01"])
                    )
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "google-managed-data-controls-2026-09-01", **(extra_headers or {})}
        return self._get(
            path_template(
                "/v1/organizations/providers/google/projects/{project_number}/data_controls",
                project_number=project_number,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.providers.google.projects.data_controls.retrieve",
                span_route="/v1/organizations/providers/google/projects/{project_number}/data_controls",
                span_attributes={"anthropic.organization.provider.google.project.id": project_number},
            ),
            cast_to=BetaGoogleManagedProjectDataControls,
        )

    def update(
        self,
        project_number: str,
        *,
        cmek: BetaGoogleManagedProjectCMEKControlParams | Omit = omit,
        storage: BetaGoogleManagedProjectStorageControlParams | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaGoogleManagedProjectDataControls:
        """Turn a control on or off, or change the key or bucket set for a region.

        Controls
        and regions that you leave out stay as they are.

        Your organization must have proved that it owns the project. Only one
        organization at a time can have controls turned on for a project.

        **Requires a credential that identifies a user or a service account**: an OAuth
        access token with the `org:admin` scope, or an organization-scoped API key that
        belongs to a user or service account whose organization role can update these
        controls. The `admin`, `owner` and `primary_owner` roles can. An Admin API key
        gets a `403` error.

        Args:
          project_number: The Google Cloud project's number, such as `123456789012`, not its project ID.

          cmek: The customer-managed encryption key control. Leave it out to keep the control as
              it is. Send `cmek`, `storage`, or both.

          storage: The customer-owned storage control. Leave it out to keep the control as it is.
              Send `cmek`, `storage`, or both.

          betas: This endpoint is in beta: requests must send
              `google-managed-data-controls-2026-09-01` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaCMEKNotApprovedError:

          BetaExternalKeyNotFoundError:

          BetaExternalKeyProviderMismatchError:

          BetaGCPProjectNotVerifiedError:

          KeyProfileMismatchError:

          BetaOrganizationNotEligibleError:

          BetaRegionNotSupportedError:

          BetaStorageNotApprovedError:

          SandboxEgressRestrictedError:

          BetaGCPProjectControlledByAnotherOrganizationError:

          BetaStorageInUseError:

          BetaAuthorizationCheckUnavailableError:
        """
        if not project_number:
            raise ValueError(f"Expected a non-empty value for `project_number` but received {project_number!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(
                        chain((str(e) for e in betas), ["google-managed-data-controls-2026-09-01"])
                    )
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "google-managed-data-controls-2026-09-01", **(extra_headers or {})}
        return self._post(
            path_template(
                "/v1/organizations/providers/google/projects/{project_number}/data_controls",
                project_number=project_number,
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
                span_name="anthropic.organization.providers.google.projects.data_controls.update",
                span_route="/v1/organizations/providers/google/projects/{project_number}/data_controls",
                span_attributes={"anthropic.organization.provider.google.project.id": project_number},
            ),
            cast_to=BetaGoogleManagedProjectDataControls,
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
        project_number: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaGoogleManagedProjectDataControls:
        """
        Get a Google Cloud project's encryption keys and storage buckets for Claude on
        Google Cloud's Agent Platform, with each region's status.

        Your organization must have proved that it owns the project.

        Args:
          project_number: The Google Cloud project's number, such as `123456789012`, not its project ID.

          betas: This endpoint is in beta: requests must send
              `google-managed-data-controls-2026-09-01` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_number:
            raise ValueError(f"Expected a non-empty value for `project_number` but received {project_number!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(
                        chain((str(e) for e in betas), ["google-managed-data-controls-2026-09-01"])
                    )
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "google-managed-data-controls-2026-09-01", **(extra_headers or {})}
        return await self._get(
            path_template(
                "/v1/organizations/providers/google/projects/{project_number}/data_controls",
                project_number=project_number,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.providers.google.projects.data_controls.retrieve",
                span_route="/v1/organizations/providers/google/projects/{project_number}/data_controls",
                span_attributes={"anthropic.organization.provider.google.project.id": project_number},
            ),
            cast_to=BetaGoogleManagedProjectDataControls,
        )

    async def update(
        self,
        project_number: str,
        *,
        cmek: BetaGoogleManagedProjectCMEKControlParams | Omit = omit,
        storage: BetaGoogleManagedProjectStorageControlParams | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaGoogleManagedProjectDataControls:
        """Turn a control on or off, or change the key or bucket set for a region.

        Controls
        and regions that you leave out stay as they are.

        Your organization must have proved that it owns the project. Only one
        organization at a time can have controls turned on for a project.

        **Requires a credential that identifies a user or a service account**: an OAuth
        access token with the `org:admin` scope, or an organization-scoped API key that
        belongs to a user or service account whose organization role can update these
        controls. The `admin`, `owner` and `primary_owner` roles can. An Admin API key
        gets a `403` error.

        Args:
          project_number: The Google Cloud project's number, such as `123456789012`, not its project ID.

          cmek: The customer-managed encryption key control. Leave it out to keep the control as
              it is. Send `cmek`, `storage`, or both.

          storage: The customer-owned storage control. Leave it out to keep the control as it is.
              Send `cmek`, `storage`, or both.

          betas: This endpoint is in beta: requests must send
              `google-managed-data-controls-2026-09-01` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaCMEKNotApprovedError:

          BetaExternalKeyNotFoundError:

          BetaExternalKeyProviderMismatchError:

          BetaGCPProjectNotVerifiedError:

          KeyProfileMismatchError:

          BetaOrganizationNotEligibleError:

          BetaRegionNotSupportedError:

          BetaStorageNotApprovedError:

          SandboxEgressRestrictedError:

          BetaGCPProjectControlledByAnotherOrganizationError:

          BetaStorageInUseError:

          BetaAuthorizationCheckUnavailableError:
        """
        if not project_number:
            raise ValueError(f"Expected a non-empty value for `project_number` but received {project_number!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(
                        chain((str(e) for e in betas), ["google-managed-data-controls-2026-09-01"])
                    )
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "google-managed-data-controls-2026-09-01", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/v1/organizations/providers/google/projects/{project_number}/data_controls",
                project_number=project_number,
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
                span_name="anthropic.organization.providers.google.projects.data_controls.update",
                span_route="/v1/organizations/providers/google/projects/{project_number}/data_controls",
                span_attributes={"anthropic.organization.provider.google.project.id": project_number},
            ),
            cast_to=BetaGoogleManagedProjectDataControls,
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
