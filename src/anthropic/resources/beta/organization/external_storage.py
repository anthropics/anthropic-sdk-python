from __future__ import annotations

from typing import List, Optional
from itertools import chain

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
from ....pagination import SyncPageCursor, AsyncPageCursor
from ...._base_client import AsyncPaginator, make_request_options
from ....types.beta.organization import (
    external_storage_create_params,
)
from ....types.anthropic_beta_param import AnthropicBetaParam
from ....types.beta.organization.beta_external_storage import BetaExternalStorage
from ....types.beta.organization.beta_deleted_external_storage import BetaDeletedExternalStorage

__all__ = ["ExternalStorage", "AsyncExternalStorage"]


class ExternalStorage(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ExternalStorageWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ExternalStorageWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ExternalStorageWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ExternalStorageWithStreamingResponse(self)

    def create(
        self,
        *,
        provider_config: external_storage_create_params.ProviderConfig,
        display_name: Optional[str] | Omit = omit,
        user_profile_id: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaExternalStorage:
        """Register a bucket in the organization's own cloud account.

        It is saved as
        `pending_configuration` and verified when activated.

        Args:
          display_name: Human-friendly display name.

          user_profile_id: The user profile to bind the storage to. It can't be changed later. The storage
              can be attached only to Workspaces with this profile, and the bucket's setup
              must name the same ID.

          betas: This endpoint is in beta: requests must send `efs-2026-10-01` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaGrantRequiredError:

          BetaOrganizationNotEligibleError:

          BetaProviderNotAllowedError:

          BetaUnsupportedRegionError:

          UserProfileNotFoundError:

          SandboxEgressRestrictedError:

          BetaStorageAlreadyRegisteredError:

          BetaAuthorizationCheckUnavailableError:
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["efs-2026-10-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "efs-2026-10-01", **(extra_headers or {})}
        return self._post(
            "/v1/organizations/external_storage",
            body={
                "provider_config": provider_config,
                "display_name": display_name,
                "user_profile_id": user_profile_id,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.external_storage.create",
                span_route="/v1/organizations/external_storage",
                span_created_id="anthropic.organization.external_storage.id",
            ),
            cast_to=BetaExternalStorage,
        )

    def retrieve(
        self,
        external_storage_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaExternalStorage:
        """
        Get one External Storage in the organization.

        Args:
          external_storage_id: The External Storage ID, which starts with `estrg_`. Through Claude Platform on
              AWS, storage whose `provider_config.type` is `aws` has its bucket ARN as its ID
              instead: `arn:<partition>:s3:::<bucket_name>`, where `<partition>` is the
              partition of the bucket's region.

          betas: This endpoint is in beta: requests must send `efs-2026-10-01` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaInvalidStorageARNError:
        """
        if not external_storage_id:
            raise ValueError(
                f"Expected a non-empty value for `external_storage_id` but received {external_storage_id!r}"
            )
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["efs-2026-10-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "efs-2026-10-01", **(extra_headers or {})}
        return self._get(
            path_template(
                "/v1/organizations/external_storage/{external_storage_id}", external_storage_id=external_storage_id
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.external_storage.retrieve",
                span_route="/v1/organizations/external_storage/{external_storage_id}",
                span_attributes={"anthropic.organization.external_storage.id": external_storage_id},
            ),
            cast_to=BetaExternalStorage,
        )

    def update(
        self,
        external_storage_id: str,
        *,
        display_name: Optional[str],
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaExternalStorage:
        """
        Rename External Storage or clear its name, in any status.

        Args:
          external_storage_id: The External Storage ID, which starts with `estrg_`. Through Claude Platform on
              AWS, storage whose `provider_config.type` is `aws` has its bucket ARN as its ID
              instead: `arn:<partition>:s3:::<bucket_name>`, where `<partition>` is the
              partition of the bucket's region.

          display_name: Human-friendly display name; null clears it.

          betas: This endpoint is in beta: requests must send `efs-2026-10-01` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaInvalidStorageARNError:

          SandboxEgressRestrictedError:
        """
        if not external_storage_id:
            raise ValueError(
                f"Expected a non-empty value for `external_storage_id` but received {external_storage_id!r}"
            )
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["efs-2026-10-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "efs-2026-10-01", **(extra_headers or {})}
        return self._post(
            path_template(
                "/v1/organizations/external_storage/{external_storage_id}", external_storage_id=external_storage_id
            ),
            body={"display_name": display_name},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.external_storage.update",
                span_route="/v1/organizations/external_storage/{external_storage_id}",
                span_attributes={"anthropic.organization.external_storage.id": external_storage_id},
            ),
            cast_to=BetaExternalStorage,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        user_profile_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaExternalStorage]:
        """
        List the organization's External Storage, newest first.

        Args:
          limit: Number of results per page.

          page: Opaque cursor from a previous response's `next_page`.

          user_profile_ids: Returns only External Storage bound to one of these user profile IDs
              (`uprof_...`). An empty entry matches storage bound to no user profile. At most
              10 entries, counting repeats.

          betas: This endpoint is in beta: requests must send `efs-2026-10-01` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["efs-2026-10-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "efs-2026-10-01", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/organizations/external_storage",
            page=SyncPageCursor[BetaExternalStorage],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "page": page,
                    "user_profile_ids": user_profile_ids,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.external_storage.list",
                span_route="/v1/organizations/external_storage",
            ),
            model=BetaExternalStorage,
        )

    def delete(
        self,
        external_storage_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDeletedExternalStorage:
        """Delete External Storage.

        Storage that is pending configuration, available, or
        active but never attached is deleted at once, unless an Enterprise Frontier
        Safeguards workspace policy lists it. Other storage gets a 400 that says what to
        do next. On `draining` storage that 400 can mean this delete started a removal
        that can't be undone. To check, get the storage: if `status.removal_started` is
        true, delete it again later to finish.

        Args:
          external_storage_id: The External Storage ID, which starts with `estrg_`. Through Claude Platform on
              AWS, storage whose `provider_config.type` is `aws` has its bucket ARN as its ID
              instead: `arn:<partition>:s3:::<bucket_name>`, where `<partition>` is the
              partition of the bucket's region.

          betas: This endpoint is in beta: requests must send `efs-2026-10-01` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaExternalStorageInUseError:

          BetaExternalStorageInWorkspacePolicyError:

          BetaInvalidStorageARNError:

          SandboxEgressRestrictedError:
        """
        if not external_storage_id:
            raise ValueError(
                f"Expected a non-empty value for `external_storage_id` but received {external_storage_id!r}"
            )
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["efs-2026-10-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "efs-2026-10-01", **(extra_headers or {})}
        return self._delete(
            path_template(
                "/v1/organizations/external_storage/{external_storage_id}", external_storage_id=external_storage_id
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.external_storage.delete",
                span_route="/v1/organizations/external_storage/{external_storage_id}",
                span_attributes={"anthropic.organization.external_storage.id": external_storage_id},
            ),
            cast_to=BetaDeletedExternalStorage,
        )

    def activate(
        self,
        external_storage_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaExternalStorage:
        """Verify pending External Storage and make it available.

        Storage that is already
        available, active or draining comes back unchanged, without any check.

        Args:
          external_storage_id: The External Storage ID, which starts with `estrg_`. Through Claude Platform on
              AWS, storage whose `provider_config.type` is `aws` has its bucket ARN as its ID
              instead: `arn:<partition>:s3:::<bucket_name>`, where `<partition>` is the
              partition of the bucket's region.

          betas: This endpoint is in beta: requests must send `efs-2026-10-01` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaGrantRequiredError:

          BetaInvalidStorageARNError:

          BetaOrganizationNotEligibleError:

          BetaProviderNotAllowedError:

          BetaStorageVerificationFailedError:

          UserProfileNotFoundError:

          SandboxEgressRestrictedError:

          BetaAuthorizationCheckUnavailableError:
        """
        if not external_storage_id:
            raise ValueError(
                f"Expected a non-empty value for `external_storage_id` but received {external_storage_id!r}"
            )
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["efs-2026-10-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "efs-2026-10-01", **(extra_headers or {})}
        return self._post(
            path_template(
                "/v1/organizations/external_storage/{external_storage_id}/activate",
                external_storage_id=external_storage_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.external_storage.activate",
                span_route="/v1/organizations/external_storage/{external_storage_id}/activate",
                span_attributes={"anthropic.organization.external_storage.id": external_storage_id},
            ),
            cast_to=BetaExternalStorage,
        )


class AsyncExternalStorage(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncExternalStorageWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncExternalStorageWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncExternalStorageWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncExternalStorageWithStreamingResponse(self)

    async def create(
        self,
        *,
        provider_config: external_storage_create_params.ProviderConfig,
        display_name: Optional[str] | Omit = omit,
        user_profile_id: Optional[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaExternalStorage:
        """Register a bucket in the organization's own cloud account.

        It is saved as
        `pending_configuration` and verified when activated.

        Args:
          display_name: Human-friendly display name.

          user_profile_id: The user profile to bind the storage to. It can't be changed later. The storage
              can be attached only to Workspaces with this profile, and the bucket's setup
              must name the same ID.

          betas: This endpoint is in beta: requests must send `efs-2026-10-01` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaGrantRequiredError:

          BetaOrganizationNotEligibleError:

          BetaProviderNotAllowedError:

          BetaUnsupportedRegionError:

          UserProfileNotFoundError:

          SandboxEgressRestrictedError:

          BetaStorageAlreadyRegisteredError:

          BetaAuthorizationCheckUnavailableError:
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["efs-2026-10-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "efs-2026-10-01", **(extra_headers or {})}
        return await self._post(
            "/v1/organizations/external_storage",
            body={
                "provider_config": provider_config,
                "display_name": display_name,
                "user_profile_id": user_profile_id,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.external_storage.create",
                span_route="/v1/organizations/external_storage",
                span_created_id="anthropic.organization.external_storage.id",
            ),
            cast_to=BetaExternalStorage,
        )

    async def retrieve(
        self,
        external_storage_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaExternalStorage:
        """
        Get one External Storage in the organization.

        Args:
          external_storage_id: The External Storage ID, which starts with `estrg_`. Through Claude Platform on
              AWS, storage whose `provider_config.type` is `aws` has its bucket ARN as its ID
              instead: `arn:<partition>:s3:::<bucket_name>`, where `<partition>` is the
              partition of the bucket's region.

          betas: This endpoint is in beta: requests must send `efs-2026-10-01` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaInvalidStorageARNError:
        """
        if not external_storage_id:
            raise ValueError(
                f"Expected a non-empty value for `external_storage_id` but received {external_storage_id!r}"
            )
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["efs-2026-10-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "efs-2026-10-01", **(extra_headers or {})}
        return await self._get(
            path_template(
                "/v1/organizations/external_storage/{external_storage_id}", external_storage_id=external_storage_id
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.external_storage.retrieve",
                span_route="/v1/organizations/external_storage/{external_storage_id}",
                span_attributes={"anthropic.organization.external_storage.id": external_storage_id},
            ),
            cast_to=BetaExternalStorage,
        )

    async def update(
        self,
        external_storage_id: str,
        *,
        display_name: Optional[str],
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaExternalStorage:
        """
        Rename External Storage or clear its name, in any status.

        Args:
          external_storage_id: The External Storage ID, which starts with `estrg_`. Through Claude Platform on
              AWS, storage whose `provider_config.type` is `aws` has its bucket ARN as its ID
              instead: `arn:<partition>:s3:::<bucket_name>`, where `<partition>` is the
              partition of the bucket's region.

          display_name: Human-friendly display name; null clears it.

          betas: This endpoint is in beta: requests must send `efs-2026-10-01` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaInvalidStorageARNError:

          SandboxEgressRestrictedError:
        """
        if not external_storage_id:
            raise ValueError(
                f"Expected a non-empty value for `external_storage_id` but received {external_storage_id!r}"
            )
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["efs-2026-10-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "efs-2026-10-01", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/v1/organizations/external_storage/{external_storage_id}", external_storage_id=external_storage_id
            ),
            body={"display_name": display_name},
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.external_storage.update",
                span_route="/v1/organizations/external_storage/{external_storage_id}",
                span_attributes={"anthropic.organization.external_storage.id": external_storage_id},
            ),
            cast_to=BetaExternalStorage,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: Optional[str] | Omit = omit,
        user_profile_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaExternalStorage, AsyncPageCursor[BetaExternalStorage]]:
        """
        List the organization's External Storage, newest first.

        Args:
          limit: Number of results per page.

          page: Opaque cursor from a previous response's `next_page`.

          user_profile_ids: Returns only External Storage bound to one of these user profile IDs
              (`uprof_...`). An empty entry matches storage bound to no user profile. At most
              10 entries, counting repeats.

          betas: This endpoint is in beta: requests must send `efs-2026-10-01` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["efs-2026-10-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "efs-2026-10-01", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/organizations/external_storage",
            page=AsyncPageCursor[BetaExternalStorage],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "page": page,
                    "user_profile_ids": user_profile_ids,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.external_storage.list",
                span_route="/v1/organizations/external_storage",
            ),
            model=BetaExternalStorage,
        )

    async def delete(
        self,
        external_storage_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDeletedExternalStorage:
        """Delete External Storage.

        Storage that is pending configuration, available, or
        active but never attached is deleted at once, unless an Enterprise Frontier
        Safeguards workspace policy lists it. Other storage gets a 400 that says what to
        do next. On `draining` storage that 400 can mean this delete started a removal
        that can't be undone. To check, get the storage: if `status.removal_started` is
        true, delete it again later to finish.

        Args:
          external_storage_id: The External Storage ID, which starts with `estrg_`. Through Claude Platform on
              AWS, storage whose `provider_config.type` is `aws` has its bucket ARN as its ID
              instead: `arn:<partition>:s3:::<bucket_name>`, where `<partition>` is the
              partition of the bucket's region.

          betas: This endpoint is in beta: requests must send `efs-2026-10-01` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaExternalStorageInUseError:

          BetaExternalStorageInWorkspacePolicyError:

          BetaInvalidStorageARNError:

          SandboxEgressRestrictedError:
        """
        if not external_storage_id:
            raise ValueError(
                f"Expected a non-empty value for `external_storage_id` but received {external_storage_id!r}"
            )
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["efs-2026-10-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "efs-2026-10-01", **(extra_headers or {})}
        return await self._delete(
            path_template(
                "/v1/organizations/external_storage/{external_storage_id}", external_storage_id=external_storage_id
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.external_storage.delete",
                span_route="/v1/organizations/external_storage/{external_storage_id}",
                span_attributes={"anthropic.organization.external_storage.id": external_storage_id},
            ),
            cast_to=BetaDeletedExternalStorage,
        )

    async def activate(
        self,
        external_storage_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaExternalStorage:
        """Verify pending External Storage and make it available.

        Storage that is already
        available, active or draining comes back unchanged, without any check.

        Args:
          external_storage_id: The External Storage ID, which starts with `estrg_`. Through Claude Platform on
              AWS, storage whose `provider_config.type` is `aws` has its bucket ARN as its ID
              instead: `arn:<partition>:s3:::<bucket_name>`, where `<partition>` is the
              partition of the bucket's region.

          betas: This endpoint is in beta: requests must send `efs-2026-10-01` in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

        Raises:
          BetaGrantRequiredError:

          BetaInvalidStorageARNError:

          BetaOrganizationNotEligibleError:

          BetaProviderNotAllowedError:

          BetaStorageVerificationFailedError:

          UserProfileNotFoundError:

          SandboxEgressRestrictedError:

          BetaAuthorizationCheckUnavailableError:
        """
        if not external_storage_id:
            raise ValueError(
                f"Expected a non-empty value for `external_storage_id` but received {external_storage_id!r}"
            )
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["efs-2026-10-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "efs-2026-10-01", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/v1/organizations/external_storage/{external_storage_id}/activate",
                external_storage_id=external_storage_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.external_storage.activate",
                span_route="/v1/organizations/external_storage/{external_storage_id}/activate",
                span_attributes={"anthropic.organization.external_storage.id": external_storage_id},
            ),
            cast_to=BetaExternalStorage,
        )


class ExternalStorageWithRawResponse:
    def __init__(self, external_storage: ExternalStorage) -> None:
        self._external_storage = external_storage

        self.create = to_raw_response_wrapper(
            external_storage.create,
        )
        self.retrieve = to_raw_response_wrapper(
            external_storage.retrieve,
        )
        self.update = to_raw_response_wrapper(
            external_storage.update,
        )
        self.list = to_raw_response_wrapper(
            external_storage.list,
        )
        self.delete = to_raw_response_wrapper(
            external_storage.delete,
        )
        self.activate = to_raw_response_wrapper(
            external_storage.activate,
        )


class AsyncExternalStorageWithRawResponse:
    def __init__(self, external_storage: AsyncExternalStorage) -> None:
        self._external_storage = external_storage

        self.create = async_to_raw_response_wrapper(
            external_storage.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            external_storage.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            external_storage.update,
        )
        self.list = async_to_raw_response_wrapper(
            external_storage.list,
        )
        self.delete = async_to_raw_response_wrapper(
            external_storage.delete,
        )
        self.activate = async_to_raw_response_wrapper(
            external_storage.activate,
        )


class ExternalStorageWithStreamingResponse:
    def __init__(self, external_storage: ExternalStorage) -> None:
        self._external_storage = external_storage

        self.create = to_streamed_response_wrapper(
            external_storage.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            external_storage.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            external_storage.update,
        )
        self.list = to_streamed_response_wrapper(
            external_storage.list,
        )
        self.delete = to_streamed_response_wrapper(
            external_storage.delete,
        )
        self.activate = to_streamed_response_wrapper(
            external_storage.activate,
        )


class AsyncExternalStorageWithStreamingResponse:
    def __init__(self, external_storage: AsyncExternalStorage) -> None:
        self._external_storage = external_storage

        self.create = async_to_streamed_response_wrapper(
            external_storage.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            external_storage.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            external_storage.update,
        )
        self.list = async_to_streamed_response_wrapper(
            external_storage.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            external_storage.delete,
        )
        self.activate = async_to_streamed_response_wrapper(
            external_storage.activate,
        )
