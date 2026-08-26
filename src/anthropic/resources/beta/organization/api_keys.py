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
from ....pagination import SyncPage, AsyncPage
from ...._base_client import AsyncPaginator, make_request_options
from ....types.beta.organization import api_key_list_params, api_key_update_params
from ....types.beta.organization.beta_api_key import BetaAPIKey

__all__ = ["APIKeys", "AsyncAPIKeys"]


class APIKeys(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> APIKeysWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return APIKeysWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> APIKeysWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return APIKeysWithStreamingResponse(self)

    def retrieve(
        self,
        api_key_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaAPIKey:
        """
        Get API Key

        Args:
          api_key_id: ID of the API key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not api_key_id:
            raise ValueError(f"Expected a non-empty value for `api_key_id` but received {api_key_id!r}")
        return self._get(
            path_template("/v1/organizations/api_keys/{api_key_id}?beta=true", api_key_id=api_key_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaAPIKey,
        )

    def update(
        self,
        api_key_id: str,
        *,
        name: Optional[str] | Omit = omit,
        status: Optional[Literal["active", "archived", "inactive"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaAPIKey:
        """
        Update API Key

        Args:
          api_key_id: ID of the API key.

          name: Name of the API key.

          status: Status of the API key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not api_key_id:
            raise ValueError(f"Expected a non-empty value for `api_key_id` but received {api_key_id!r}")
        return self._post(
            path_template("/v1/organizations/api_keys/{api_key_id}?beta=true", api_key_id=api_key_id),
            body=maybe_transform(
                {
                    "name": name,
                    "status": status,
                },
                api_key_update_params.APIKeyUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaAPIKey,
        )

    def list(
        self,
        *,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        created_by_user_id: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        status: Optional[Literal["active", "archived", "expired", "inactive"]] | Omit = omit,
        workspace_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPage[BetaAPIKey]:
        """
        List API Keys

        Args:
          after_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately after this object.

          before_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately before this object.

          created_by_user_id: Filter by the ID of the User who created the object.

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `1000`.

          status: Filter by API key status.

          workspace_id: Filter by Workspace ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/api_keys?beta=true",
            page=SyncPage[BetaAPIKey],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "created_by_user_id": created_by_user_id,
                        "limit": limit,
                        "status": status,
                        "workspace_id": workspace_id,
                    },
                    api_key_list_params.APIKeyListParams,
                ),
            ),
            model=BetaAPIKey,
        )


class AsyncAPIKeys(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAPIKeysWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAPIKeysWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAPIKeysWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncAPIKeysWithStreamingResponse(self)

    async def retrieve(
        self,
        api_key_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaAPIKey:
        """
        Get API Key

        Args:
          api_key_id: ID of the API key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not api_key_id:
            raise ValueError(f"Expected a non-empty value for `api_key_id` but received {api_key_id!r}")
        return await self._get(
            path_template("/v1/organizations/api_keys/{api_key_id}?beta=true", api_key_id=api_key_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaAPIKey,
        )

    async def update(
        self,
        api_key_id: str,
        *,
        name: Optional[str] | Omit = omit,
        status: Optional[Literal["active", "archived", "inactive"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaAPIKey:
        """
        Update API Key

        Args:
          api_key_id: ID of the API key.

          name: Name of the API key.

          status: Status of the API key.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not api_key_id:
            raise ValueError(f"Expected a non-empty value for `api_key_id` but received {api_key_id!r}")
        return await self._post(
            path_template("/v1/organizations/api_keys/{api_key_id}?beta=true", api_key_id=api_key_id),
            body=await async_maybe_transform(
                {
                    "name": name,
                    "status": status,
                },
                api_key_update_params.APIKeyUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaAPIKey,
        )

    def list(
        self,
        *,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        created_by_user_id: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        status: Optional[Literal["active", "archived", "expired", "inactive"]] | Omit = omit,
        workspace_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaAPIKey, AsyncPage[BetaAPIKey]]:
        """
        List API Keys

        Args:
          after_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately after this object.

          before_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately before this object.

          created_by_user_id: Filter by the ID of the User who created the object.

          limit: Number of items to return per page.

              Defaults to `20`. Ranges from `1` to `1000`.

          status: Filter by API key status.

          workspace_id: Filter by Workspace ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/organizations/api_keys?beta=true",
            page=AsyncPage[BetaAPIKey],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "created_by_user_id": created_by_user_id,
                        "limit": limit,
                        "status": status,
                        "workspace_id": workspace_id,
                    },
                    api_key_list_params.APIKeyListParams,
                ),
            ),
            model=BetaAPIKey,
        )


class APIKeysWithRawResponse:
    def __init__(self, api_keys: APIKeys) -> None:
        self._api_keys = api_keys

        self.retrieve = to_raw_response_wrapper(
            api_keys.retrieve,
        )
        self.update = to_raw_response_wrapper(
            api_keys.update,
        )
        self.list = to_raw_response_wrapper(
            api_keys.list,
        )


class AsyncAPIKeysWithRawResponse:
    def __init__(self, api_keys: AsyncAPIKeys) -> None:
        self._api_keys = api_keys

        self.retrieve = async_to_raw_response_wrapper(
            api_keys.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            api_keys.update,
        )
        self.list = async_to_raw_response_wrapper(
            api_keys.list,
        )


class APIKeysWithStreamingResponse:
    def __init__(self, api_keys: APIKeys) -> None:
        self._api_keys = api_keys

        self.retrieve = to_streamed_response_wrapper(
            api_keys.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            api_keys.update,
        )
        self.list = to_streamed_response_wrapper(
            api_keys.list,
        )


class AsyncAPIKeysWithStreamingResponse:
    def __init__(self, api_keys: AsyncAPIKeys) -> None:
        self._api_keys = api_keys

        self.retrieve = async_to_streamed_response_wrapper(
            api_keys.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            api_keys.update,
        )
        self.list = async_to_streamed_response_wrapper(
            api_keys.list,
        )
