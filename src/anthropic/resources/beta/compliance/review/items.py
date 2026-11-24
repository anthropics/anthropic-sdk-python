from __future__ import annotations

from typing import List

import httpx2

from ....._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ....._utils import is_given, path_template, strip_not_given
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....._base_client import make_request_options
from .....types.anthropic_beta_param import AnthropicBetaParam
from .....types.beta.compliance.review.beta_compliance_review_item import BetaComplianceReviewItem

__all__ = ["Items", "AsyncItems"]


class Items(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ItemsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ItemsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ItemsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return ItemsWithStreamingResponse(self)

    def retrieve(
        self,
        item_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        user_profile_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaComplianceReviewItem:
        """
        Read one message that Anthropic flagged for your organization to review, with
        its request and response.

        A message that the API key can't read, or that isn't flagged, returns the same
        404 as one that doesn't exist. For a message recorded with a user profile, send
        that profile's ID in the `anthropic-user-profile-id` header. A flagged message
        can also return 404 if it belongs to another organization than the key's own, or
        to your end customer's user profile or Workspace.

        If your encryption key or storage bucket refuses the read, the API returns a 400
        with `cmek_key_disabled`, `storage_bucket_unreadable` or
        `customer_storage_refusal_unattributed` in `error.details.error_code`.

        The API key must have the `read:compliance_review_items`,
        `read:compliance_user_data` or `read:org_audit` scope. A key of an organization
        with no parent organization must have `read:compliance_review_items`.

        Args:
          item_id: The ID of the item. For a message, its ID as the client received it or as a
              review case lists it, such as `msg_...`.

          betas: Optional header to specify the beta version(s) you want to use.

          user_profile_id: The ID of the user profile that the message was recorded with (`uprof_...`).
              Send it for a message recorded with a user profile, and leave it out for a
              message recorded with none.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given,
                    "anthropic-user-profile-id": user_profile_id,
                }
            ),
            **(extra_headers or {}),
        }
        return self._get(
            path_template("/v1/compliance/review/items/{item_id}", item_id=item_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.compliance.review.items.retrieve",
                span_route="/v1/compliance/review/items/{item_id}",
                span_attributes={"anthropic.compliance.review.item.id": item_id},
            ),
            cast_to=BetaComplianceReviewItem,
        )


class AsyncItems(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncItemsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncItemsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncItemsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://platform.claude.com/docs/en/api/sdks/python
        """
        return AsyncItemsWithStreamingResponse(self)

    async def retrieve(
        self,
        item_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        user_profile_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaComplianceReviewItem:
        """
        Read one message that Anthropic flagged for your organization to review, with
        its request and response.

        A message that the API key can't read, or that isn't flagged, returns the same
        404 as one that doesn't exist. For a message recorded with a user profile, send
        that profile's ID in the `anthropic-user-profile-id` header. A flagged message
        can also return 404 if it belongs to another organization than the key's own, or
        to your end customer's user profile or Workspace.

        If your encryption key or storage bucket refuses the read, the API returns a 400
        with `cmek_key_disabled`, `storage_bucket_unreadable` or
        `customer_storage_refusal_unattributed` in `error.details.error_code`.

        The API key must have the `read:compliance_review_items`,
        `read:compliance_user_data` or `read:org_audit` scope. A key of an organization
        with no parent organization must have `read:compliance_review_items`.

        Args:
          item_id: The ID of the item. For a message, its ID as the client received it or as a
              review case lists it, such as `msg_...`.

          betas: Optional header to specify the beta version(s) you want to use.

          user_profile_id: The ID of the user profile that the message was recorded with (`uprof_...`).
              Send it for a message recorded with a user profile, and leave it out for a
              message recorded with none.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not item_id:
            raise ValueError(f"Expected a non-empty value for `item_id` but received {item_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(str(e) for e in betas) if is_given(betas) else not_given,
                    "anthropic-user-profile-id": user_profile_id,
                }
            ),
            **(extra_headers or {}),
        }
        return await self._get(
            path_template("/v1/compliance/review/items/{item_id}", item_id=item_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.compliance.review.items.retrieve",
                span_route="/v1/compliance/review/items/{item_id}",
                span_attributes={"anthropic.compliance.review.item.id": item_id},
            ),
            cast_to=BetaComplianceReviewItem,
        )


class ItemsWithRawResponse:
    def __init__(self, items: Items) -> None:
        self._items = items

        self.retrieve = to_raw_response_wrapper(
            items.retrieve,
        )


class AsyncItemsWithRawResponse:
    def __init__(self, items: AsyncItems) -> None:
        self._items = items

        self.retrieve = async_to_raw_response_wrapper(
            items.retrieve,
        )


class ItemsWithStreamingResponse:
    def __init__(self, items: Items) -> None:
        self._items = items

        self.retrieve = to_streamed_response_wrapper(
            items.retrieve,
        )


class AsyncItemsWithStreamingResponse:
    def __init__(self, items: AsyncItems) -> None:
        self._items = items

        self.retrieve = async_to_streamed_response_wrapper(
            items.retrieve,
        )
