# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal

import httpx2

from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import path_template, maybe_transform, async_maybe_transform
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
from ....types.beta.organization import external_key_list_params, external_key_create_params, external_key_update_params
from ....types.beta.organization.beta_external_key import BetaExternalKey
from ....types.beta.organization.external_key_delete_response import ExternalKeyDeleteResponse
from ....types.beta.organization.external_key_validate_response import ExternalKeyValidateResponse

__all__ = ["ExternalKeys", "AsyncExternalKeys"]


class ExternalKeys(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ExternalKeysWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return ExternalKeysWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ExternalKeysWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return ExternalKeysWithStreamingResponse(self)

    def create(
        self,
        *,
        provider_config: external_key_create_params.ProviderConfig,
        display_name: Optional[str] | Omit = omit,
        geo: Literal["us"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaExternalKey:
        """
        Create an external key config owned by the caller's organization.

        Args:
          provider_config: KMS provider identity and auth coordinates.

          display_name: Human-friendly display name.

          geo: Data residency geo. Only `us` is supported.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/organizations/external_keys?beta=true",
            body=maybe_transform(
                {
                    "provider_config": provider_config,
                    "display_name": display_name,
                    "geo": geo,
                },
                external_key_create_params.ExternalKeyCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaExternalKey,
        )

    def retrieve(
        self,
        external_key_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaExternalKey:
        """
        Retrieve a single external key config in the caller's organization by ID.

        Args:
          external_key_id: ID of the External Key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not external_key_id:
            raise ValueError(f"Expected a non-empty value for `external_key_id` but received {external_key_id!r}")
        return self._get(
            path_template(
                "/v1/organizations/external_keys/{external_key_id}?beta=true", external_key_id=external_key_id
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaExternalKey,
        )

    def update(
        self,
        external_key_id: str,
        *,
        display_name: Optional[str] | Omit = omit,
        geo: Optional[Literal["us"]] | Omit = omit,
        provider_config: Optional[external_key_update_params.ProviderConfig] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaExternalKey:
        """Partially update an external key config.

        Omitted fields are left unchanged.

        `display_name` is always editable. `geo` and `provider_config` cannot be changed
        once any workspace references this config, because previously encrypted data
        requires the original key identity to decrypt.

        Args:
          external_key_id: ID of the External Key.

          display_name: Human-friendly display name.

          geo: Data residency geo. Only `us` is supported.

          provider_config: KMS provider identity and auth coordinates.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not external_key_id:
            raise ValueError(f"Expected a non-empty value for `external_key_id` but received {external_key_id!r}")
        return self._post(
            path_template(
                "/v1/organizations/external_keys/{external_key_id}?beta=true", external_key_id=external_key_id
            ),
            body=maybe_transform(
                {
                    "display_name": display_name,
                    "geo": geo,
                    "provider_config": provider_config,
                },
                external_key_update_params.ExternalKeyUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaExternalKey,
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
    ) -> SyncPageCursor[BetaExternalKey]:
        """
        List external key configs in the caller's organization.

        Results are ordered by creation time (newest first). Use the `next_page` cursor
        from the response to fetch subsequent pages.

        Args:
          limit: Number of results per page.

          page: Opaque cursor from a previous response's `next_page`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/external_keys?beta=true",
            page=SyncPageCursor[BetaExternalKey],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                    },
                    external_key_list_params.ExternalKeyListParams,
                ),
            ),
            model=BetaExternalKey,
        )

    def delete(
        self,
        external_key_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> ExternalKeyDeleteResponse:
        """
        Delete an external key config.

        The request is rejected if any workspace still references this config.

        Args:
          external_key_id: ID of the External Key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not external_key_id:
            raise ValueError(f"Expected a non-empty value for `external_key_id` but received {external_key_id!r}")
        return self._delete(
            path_template(
                "/v1/organizations/external_keys/{external_key_id}?beta=true", external_key_id=external_key_id
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExternalKeyDeleteResponse,
        )

    def validate(
        self,
        external_key_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> ExternalKeyValidateResponse:
        """
        Validate an external key config against the customer's KMS.

        Anthropic performs an encrypt/decrypt roundtrip against the configured KMS key
        and waits up to 30 seconds for the result. The response status is `success` if
        the roundtrip succeeded, or `failure` with an error message if it failed or
        timed out.

        Args:
          external_key_id: ID of the External Key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not external_key_id:
            raise ValueError(f"Expected a non-empty value for `external_key_id` but received {external_key_id!r}")
        return self._post(
            path_template(
                "/v1/organizations/external_keys/{external_key_id}/validate?beta=true", external_key_id=external_key_id
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExternalKeyValidateResponse,
        )


class AsyncExternalKeys(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncExternalKeysWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncExternalKeysWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncExternalKeysWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncExternalKeysWithStreamingResponse(self)

    async def create(
        self,
        *,
        provider_config: external_key_create_params.ProviderConfig,
        display_name: Optional[str] | Omit = omit,
        geo: Literal["us"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaExternalKey:
        """
        Create an external key config owned by the caller's organization.

        Args:
          provider_config: KMS provider identity and auth coordinates.

          display_name: Human-friendly display name.

          geo: Data residency geo. Only `us` is supported.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/organizations/external_keys?beta=true",
            body=await async_maybe_transform(
                {
                    "provider_config": provider_config,
                    "display_name": display_name,
                    "geo": geo,
                },
                external_key_create_params.ExternalKeyCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaExternalKey,
        )

    async def retrieve(
        self,
        external_key_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaExternalKey:
        """
        Retrieve a single external key config in the caller's organization by ID.

        Args:
          external_key_id: ID of the External Key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not external_key_id:
            raise ValueError(f"Expected a non-empty value for `external_key_id` but received {external_key_id!r}")
        return await self._get(
            path_template(
                "/v1/organizations/external_keys/{external_key_id}?beta=true", external_key_id=external_key_id
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaExternalKey,
        )

    async def update(
        self,
        external_key_id: str,
        *,
        display_name: Optional[str] | Omit = omit,
        geo: Optional[Literal["us"]] | Omit = omit,
        provider_config: Optional[external_key_update_params.ProviderConfig] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaExternalKey:
        """Partially update an external key config.

        Omitted fields are left unchanged.

        `display_name` is always editable. `geo` and `provider_config` cannot be changed
        once any workspace references this config, because previously encrypted data
        requires the original key identity to decrypt.

        Args:
          external_key_id: ID of the External Key.

          display_name: Human-friendly display name.

          geo: Data residency geo. Only `us` is supported.

          provider_config: KMS provider identity and auth coordinates.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not external_key_id:
            raise ValueError(f"Expected a non-empty value for `external_key_id` but received {external_key_id!r}")
        return await self._post(
            path_template(
                "/v1/organizations/external_keys/{external_key_id}?beta=true", external_key_id=external_key_id
            ),
            body=await async_maybe_transform(
                {
                    "display_name": display_name,
                    "geo": geo,
                    "provider_config": provider_config,
                },
                external_key_update_params.ExternalKeyUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaExternalKey,
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
    ) -> AsyncPaginator[BetaExternalKey, AsyncPageCursor[BetaExternalKey]]:
        """
        List external key configs in the caller's organization.

        Results are ordered by creation time (newest first). Use the `next_page` cursor
        from the response to fetch subsequent pages.

        Args:
          limit: Number of results per page.

          page: Opaque cursor from a previous response's `next_page`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/external_keys?beta=true",
            page=AsyncPageCursor[BetaExternalKey],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                    },
                    external_key_list_params.ExternalKeyListParams,
                ),
            ),
            model=BetaExternalKey,
        )

    async def delete(
        self,
        external_key_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> ExternalKeyDeleteResponse:
        """
        Delete an external key config.

        The request is rejected if any workspace still references this config.

        Args:
          external_key_id: ID of the External Key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not external_key_id:
            raise ValueError(f"Expected a non-empty value for `external_key_id` but received {external_key_id!r}")
        return await self._delete(
            path_template(
                "/v1/organizations/external_keys/{external_key_id}?beta=true", external_key_id=external_key_id
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExternalKeyDeleteResponse,
        )

    async def validate(
        self,
        external_key_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> ExternalKeyValidateResponse:
        """
        Validate an external key config against the customer's KMS.

        Anthropic performs an encrypt/decrypt roundtrip against the configured KMS key
        and waits up to 30 seconds for the result. The response status is `success` if
        the roundtrip succeeded, or `failure` with an error message if it failed or
        timed out.

        Args:
          external_key_id: ID of the External Key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not external_key_id:
            raise ValueError(f"Expected a non-empty value for `external_key_id` but received {external_key_id!r}")
        return await self._post(
            path_template(
                "/v1/organizations/external_keys/{external_key_id}/validate?beta=true", external_key_id=external_key_id
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExternalKeyValidateResponse,
        )


class ExternalKeysWithRawResponse:
    def __init__(self, external_keys: ExternalKeys) -> None:
        self._external_keys = external_keys

        self.create = to_raw_response_wrapper(
            external_keys.create,
        )
        self.retrieve = to_raw_response_wrapper(
            external_keys.retrieve,
        )
        self.update = to_raw_response_wrapper(
            external_keys.update,
        )
        self.list = to_raw_response_wrapper(
            external_keys.list,
        )
        self.delete = to_raw_response_wrapper(
            external_keys.delete,
        )
        self.validate = to_raw_response_wrapper(
            external_keys.validate,
        )


class AsyncExternalKeysWithRawResponse:
    def __init__(self, external_keys: AsyncExternalKeys) -> None:
        self._external_keys = external_keys

        self.create = async_to_raw_response_wrapper(
            external_keys.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            external_keys.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            external_keys.update,
        )
        self.list = async_to_raw_response_wrapper(
            external_keys.list,
        )
        self.delete = async_to_raw_response_wrapper(
            external_keys.delete,
        )
        self.validate = async_to_raw_response_wrapper(
            external_keys.validate,
        )


class ExternalKeysWithStreamingResponse:
    def __init__(self, external_keys: ExternalKeys) -> None:
        self._external_keys = external_keys

        self.create = to_streamed_response_wrapper(
            external_keys.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            external_keys.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            external_keys.update,
        )
        self.list = to_streamed_response_wrapper(
            external_keys.list,
        )
        self.delete = to_streamed_response_wrapper(
            external_keys.delete,
        )
        self.validate = to_streamed_response_wrapper(
            external_keys.validate,
        )


class AsyncExternalKeysWithStreamingResponse:
    def __init__(self, external_keys: AsyncExternalKeys) -> None:
        self._external_keys = external_keys

        self.create = async_to_streamed_response_wrapper(
            external_keys.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            external_keys.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            external_keys.update,
        )
        self.list = async_to_streamed_response_wrapper(
            external_keys.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            external_keys.delete,
        )
        self.validate = async_to_streamed_response_wrapper(
            external_keys.validate,
        )
