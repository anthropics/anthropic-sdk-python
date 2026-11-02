from __future__ import annotations

from typing import List, Optional
from itertools import chain
from typing_extensions import Literal

import httpx2

from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
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
from ....types.beta.organization.beta_organization_webhook_endpoint import BetaOrganizationWebhookEndpoint
from ....types.beta.organization.beta_new_organization_webhook_endpoint import BetaNewOrganizationWebhookEndpoint
from ....types.beta.organization.beta_deleted_organization_webhook_endpoint import (
    BetaDeletedOrganizationWebhookEndpoint,
)
from ....types.beta.organization.beta_organization_webhook_endpoint_signing_secret import (
    BetaOrganizationWebhookEndpointSigningSecret,
)

__all__ = ["Webhooks", "AsyncWebhooks"]


class Webhooks(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> WebhooksWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return WebhooksWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WebhooksWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return WebhooksWithStreamingResponse(self)

    def create(
        self,
        *,
        enabled_events: List[
            Literal["user_profile.enforcement_action_opened", "user_profile.enforcement_action_resolved"]
        ],
        url: str,
        description: str | Omit = omit,
        name: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaNewOrganizationWebhookEndpoint:
        """
        Create an organization webhook endpoint.

        An organization webhook endpoint belongs to the organization rather than to one
        of its workspaces. An organization can have at most 32 organization webhook
        endpoints, enabled or disabled.

        The response includes the endpoint's signing secret. No read returns it, so
        store it when you receive it.

        Every request must include the beta header
        `anthropic-beta: webhooks-2026-10-07`. A request without it returns `404`,
        exactly as if this API did not exist. Anthropic turns organization webhook
        endpoints on for each organization; until yours is on, requests also return
        `404`. Organization webhook endpoints are in beta and are not available to
        organizations with HIPAA readiness enabled.

        Args:
          enabled_events: The event types to deliver to the endpoint. Must list at least one.

          url: The HTTPS URL that deliveries are sent to.

          description: Notes about the endpoint.

          name: A short label for the endpoint.

          betas: This endpoint is in beta: requests must send `webhooks-2026-10-07` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["webhooks-2026-10-07"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "webhooks-2026-10-07", **(extra_headers or {})}
        return self._post(
            "/v1/organizations/webhooks",
            body={
                "enabled_events": enabled_events,
                "url": url,
                "description": description,
                "name": name,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.webhooks.create",
                span_route="/v1/organizations/webhooks",
                span_created_id="anthropic.organization.webhook.id",
            ),
            cast_to=BetaNewOrganizationWebhookEndpoint,
        )

    def retrieve(
        self,
        webhook_endpoint_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaOrganizationWebhookEndpoint:
        """
        Retrieve an organization webhook endpoint by ID.

        Every request must include the beta header
        `anthropic-beta: webhooks-2026-10-07`. A request without it returns `404`,
        exactly as if this API did not exist. Anthropic turns organization webhook
        endpoints on for each organization; until yours is on, requests also return
        `404`. Organization webhook endpoints are in beta and are not available to
        organizations with HIPAA readiness enabled.

        Args:
          webhook_endpoint_id: ID of the webhook endpoint.

          betas: This endpoint is in beta: requests must send `webhooks-2026-10-07` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not webhook_endpoint_id:
            raise ValueError(
                f"Expected a non-empty value for `webhook_endpoint_id` but received {webhook_endpoint_id!r}"
            )
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["webhooks-2026-10-07"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "webhooks-2026-10-07", **(extra_headers or {})}
        return self._get(
            path_template("/v1/organizations/webhooks/{webhook_endpoint_id}", webhook_endpoint_id=webhook_endpoint_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.webhooks.retrieve",
                span_route="/v1/organizations/webhooks/{webhook_endpoint_id}",
                span_attributes={"anthropic.organization.webhook.id": webhook_endpoint_id},
            ),
            cast_to=BetaOrganizationWebhookEndpoint,
        )

    def update(
        self,
        webhook_endpoint_id: str,
        *,
        description: str | Omit = omit,
        enabled_events: List[
            Literal["user_profile.enforcement_action_opened", "user_profile.enforcement_action_resolved"]
        ]
        | Omit = omit,
        name: str | Omit = omit,
        state: Literal["disabled", "enabled"] | Omit = omit,
        url: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaOrganizationWebhookEndpoint:
        """Update an organization webhook endpoint.

        Only the fields you send are changed.

        Every request must include the beta header
        `anthropic-beta: webhooks-2026-10-07`. A request without it returns `404`,
        exactly as if this API did not exist. Anthropic turns organization webhook
        endpoints on for each organization; until yours is on, requests also return
        `404`. Organization webhook endpoints are in beta and are not available to
        organizations with HIPAA readiness enabled.

        Args:
          webhook_endpoint_id: ID of the webhook endpoint.

          description: Notes about the endpoint.

          enabled_events: The event types to deliver to the endpoint. Replaces the whole set; an empty
              list leaves it unchanged.

          name: A short label for the endpoint.

          state: `disabled` stops deliveries. `enabled` resumes them and clears
              `disabled_reason`. Events that happen while the endpoint is disabled are never
              delivered.

          url: The HTTPS URL that deliveries are sent to.

          betas: This endpoint is in beta: requests must send `webhooks-2026-10-07` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not webhook_endpoint_id:
            raise ValueError(
                f"Expected a non-empty value for `webhook_endpoint_id` but received {webhook_endpoint_id!r}"
            )
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["webhooks-2026-10-07"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "webhooks-2026-10-07", **(extra_headers or {})}
        return self._post(
            path_template("/v1/organizations/webhooks/{webhook_endpoint_id}", webhook_endpoint_id=webhook_endpoint_id),
            body={
                "description": description,
                "enabled_events": enabled_events,
                "name": name,
                "state": state,
                "url": url,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.webhooks.update",
                span_route="/v1/organizations/webhooks/{webhook_endpoint_id}",
                span_attributes={"anthropic.organization.webhook.id": webhook_endpoint_id},
            ),
            cast_to=BetaOrganizationWebhookEndpoint,
        )

    def list(
        self,
        *,
        after_id: Optional[str] | Omit = omit,
        before_id: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        order: Optional[Literal["asc", "desc"]] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPage[BetaOrganizationWebhookEndpoint]:
        """
        List the organization's webhook endpoints.

        An organization webhook endpoint belongs to the organization rather than to one
        of its workspaces. The list does not include webhook endpoints that belong to a
        workspace.

        Every request must include the beta header
        `anthropic-beta: webhooks-2026-10-07`. A request without it returns `404`,
        exactly as if this API did not exist. Anthropic turns organization webhook
        endpoints on for each organization; until yours is on, requests also return
        `404`. Organization webhook endpoints are in beta and are not available to
        organizations with HIPAA readiness enabled.

        Args:
          after_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately after this object.

          before_id: ID of a webhook endpoint to use as a cursor. Returns the first `limit` endpoints
              that come before it in list order, not the `limit` endpoints just before it.

          limit: Number of items to return per page, up to `100`. The default, `0`, means `20`.

          order: Sort order by `created_at`. Defaults to `desc`, newest first.

          betas: This endpoint is in beta: requests must send `webhooks-2026-10-07` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["webhooks-2026-10-07"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "webhooks-2026-10-07", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/organizations/webhooks",
            page=SyncPage[BetaOrganizationWebhookEndpoint],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "after_id": after_id,
                    "before_id": before_id,
                    "limit": limit,
                    "order": order,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.webhooks.list",
                span_route="/v1/organizations/webhooks",
            ),
            model=BetaOrganizationWebhookEndpoint,
        )

    def delete(
        self,
        webhook_endpoint_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDeletedOrganizationWebhookEndpoint:
        """
        Delete an organization webhook endpoint.

        Every request must include the beta header
        `anthropic-beta: webhooks-2026-10-07`. A request without it returns `404`,
        exactly as if this API did not exist. Anthropic turns organization webhook
        endpoints on for each organization; until yours is on, requests also return
        `404`. Organization webhook endpoints are in beta and are not available to
        organizations with HIPAA readiness enabled.

        Args:
          webhook_endpoint_id: ID of the webhook endpoint.

          betas: This endpoint is in beta: requests must send `webhooks-2026-10-07` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not webhook_endpoint_id:
            raise ValueError(
                f"Expected a non-empty value for `webhook_endpoint_id` but received {webhook_endpoint_id!r}"
            )
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["webhooks-2026-10-07"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "webhooks-2026-10-07", **(extra_headers or {})}
        return self._delete(
            path_template("/v1/organizations/webhooks/{webhook_endpoint_id}", webhook_endpoint_id=webhook_endpoint_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.webhooks.delete",
                span_route="/v1/organizations/webhooks/{webhook_endpoint_id}",
                span_attributes={"anthropic.organization.webhook.id": webhook_endpoint_id},
            ),
            cast_to=BetaDeletedOrganizationWebhookEndpoint,
        )

    def regenerate_signing_secret(
        self,
        webhook_endpoint_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaOrganizationWebhookEndpointSigningSecret:
        """Replace an organization webhook endpoint's signing secret.

        The old secret stops
        working immediately. The new secret is returned only in this response.

        Every request must include the beta header
        `anthropic-beta: webhooks-2026-10-07`. A request without it returns `404`,
        exactly as if this API did not exist. Anthropic turns organization webhook
        endpoints on for each organization; until yours is on, requests also return
        `404`. Organization webhook endpoints are in beta and are not available to
        organizations with HIPAA readiness enabled.

        Args:
          webhook_endpoint_id: ID of the webhook endpoint.

          betas: This endpoint is in beta: requests must send `webhooks-2026-10-07` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not webhook_endpoint_id:
            raise ValueError(
                f"Expected a non-empty value for `webhook_endpoint_id` but received {webhook_endpoint_id!r}"
            )
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["webhooks-2026-10-07"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "webhooks-2026-10-07", **(extra_headers or {})}
        return self._post(
            path_template(
                "/v1/organizations/webhooks/{webhook_endpoint_id}/regenerate_signing_secret",
                webhook_endpoint_id=webhook_endpoint_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.webhooks.regenerate_signing_secret",
                span_route="/v1/organizations/webhooks/{webhook_endpoint_id}/regenerate_signing_secret",
                span_attributes={"anthropic.organization.webhook.id": webhook_endpoint_id},
            ),
            cast_to=BetaOrganizationWebhookEndpointSigningSecret,
        )


class AsyncWebhooks(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncWebhooksWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncWebhooksWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWebhooksWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncWebhooksWithStreamingResponse(self)

    async def create(
        self,
        *,
        enabled_events: List[
            Literal["user_profile.enforcement_action_opened", "user_profile.enforcement_action_resolved"]
        ],
        url: str,
        description: str | Omit = omit,
        name: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaNewOrganizationWebhookEndpoint:
        """
        Create an organization webhook endpoint.

        An organization webhook endpoint belongs to the organization rather than to one
        of its workspaces. An organization can have at most 32 organization webhook
        endpoints, enabled or disabled.

        The response includes the endpoint's signing secret. No read returns it, so
        store it when you receive it.

        Every request must include the beta header
        `anthropic-beta: webhooks-2026-10-07`. A request without it returns `404`,
        exactly as if this API did not exist. Anthropic turns organization webhook
        endpoints on for each organization; until yours is on, requests also return
        `404`. Organization webhook endpoints are in beta and are not available to
        organizations with HIPAA readiness enabled.

        Args:
          enabled_events: The event types to deliver to the endpoint. Must list at least one.

          url: The HTTPS URL that deliveries are sent to.

          description: Notes about the endpoint.

          name: A short label for the endpoint.

          betas: This endpoint is in beta: requests must send `webhooks-2026-10-07` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["webhooks-2026-10-07"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "webhooks-2026-10-07", **(extra_headers or {})}
        return await self._post(
            "/v1/organizations/webhooks",
            body={
                "enabled_events": enabled_events,
                "url": url,
                "description": description,
                "name": name,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.webhooks.create",
                span_route="/v1/organizations/webhooks",
                span_created_id="anthropic.organization.webhook.id",
            ),
            cast_to=BetaNewOrganizationWebhookEndpoint,
        )

    async def retrieve(
        self,
        webhook_endpoint_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaOrganizationWebhookEndpoint:
        """
        Retrieve an organization webhook endpoint by ID.

        Every request must include the beta header
        `anthropic-beta: webhooks-2026-10-07`. A request without it returns `404`,
        exactly as if this API did not exist. Anthropic turns organization webhook
        endpoints on for each organization; until yours is on, requests also return
        `404`. Organization webhook endpoints are in beta and are not available to
        organizations with HIPAA readiness enabled.

        Args:
          webhook_endpoint_id: ID of the webhook endpoint.

          betas: This endpoint is in beta: requests must send `webhooks-2026-10-07` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not webhook_endpoint_id:
            raise ValueError(
                f"Expected a non-empty value for `webhook_endpoint_id` but received {webhook_endpoint_id!r}"
            )
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["webhooks-2026-10-07"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "webhooks-2026-10-07", **(extra_headers or {})}
        return await self._get(
            path_template("/v1/organizations/webhooks/{webhook_endpoint_id}", webhook_endpoint_id=webhook_endpoint_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.webhooks.retrieve",
                span_route="/v1/organizations/webhooks/{webhook_endpoint_id}",
                span_attributes={"anthropic.organization.webhook.id": webhook_endpoint_id},
            ),
            cast_to=BetaOrganizationWebhookEndpoint,
        )

    async def update(
        self,
        webhook_endpoint_id: str,
        *,
        description: str | Omit = omit,
        enabled_events: List[
            Literal["user_profile.enforcement_action_opened", "user_profile.enforcement_action_resolved"]
        ]
        | Omit = omit,
        name: str | Omit = omit,
        state: Literal["disabled", "enabled"] | Omit = omit,
        url: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaOrganizationWebhookEndpoint:
        """Update an organization webhook endpoint.

        Only the fields you send are changed.

        Every request must include the beta header
        `anthropic-beta: webhooks-2026-10-07`. A request without it returns `404`,
        exactly as if this API did not exist. Anthropic turns organization webhook
        endpoints on for each organization; until yours is on, requests also return
        `404`. Organization webhook endpoints are in beta and are not available to
        organizations with HIPAA readiness enabled.

        Args:
          webhook_endpoint_id: ID of the webhook endpoint.

          description: Notes about the endpoint.

          enabled_events: The event types to deliver to the endpoint. Replaces the whole set; an empty
              list leaves it unchanged.

          name: A short label for the endpoint.

          state: `disabled` stops deliveries. `enabled` resumes them and clears
              `disabled_reason`. Events that happen while the endpoint is disabled are never
              delivered.

          url: The HTTPS URL that deliveries are sent to.

          betas: This endpoint is in beta: requests must send `webhooks-2026-10-07` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not webhook_endpoint_id:
            raise ValueError(
                f"Expected a non-empty value for `webhook_endpoint_id` but received {webhook_endpoint_id!r}"
            )
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["webhooks-2026-10-07"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "webhooks-2026-10-07", **(extra_headers or {})}
        return await self._post(
            path_template("/v1/organizations/webhooks/{webhook_endpoint_id}", webhook_endpoint_id=webhook_endpoint_id),
            body={
                "description": description,
                "enabled_events": enabled_events,
                "name": name,
                "state": state,
                "url": url,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.webhooks.update",
                span_route="/v1/organizations/webhooks/{webhook_endpoint_id}",
                span_attributes={"anthropic.organization.webhook.id": webhook_endpoint_id},
            ),
            cast_to=BetaOrganizationWebhookEndpoint,
        )

    def list(
        self,
        *,
        after_id: Optional[str] | Omit = omit,
        before_id: Optional[str] | Omit = omit,
        limit: int | Omit = omit,
        order: Optional[Literal["asc", "desc"]] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaOrganizationWebhookEndpoint, AsyncPage[BetaOrganizationWebhookEndpoint]]:
        """
        List the organization's webhook endpoints.

        An organization webhook endpoint belongs to the organization rather than to one
        of its workspaces. The list does not include webhook endpoints that belong to a
        workspace.

        Every request must include the beta header
        `anthropic-beta: webhooks-2026-10-07`. A request without it returns `404`,
        exactly as if this API did not exist. Anthropic turns organization webhook
        endpoints on for each organization; until yours is on, requests also return
        `404`. Organization webhook endpoints are in beta and are not available to
        organizations with HIPAA readiness enabled.

        Args:
          after_id: ID of the object to use as a cursor for pagination. When provided, returns the
              page of results immediately after this object.

          before_id: ID of a webhook endpoint to use as a cursor. Returns the first `limit` endpoints
              that come before it in list order, not the `limit` endpoints just before it.

          limit: Number of items to return per page, up to `100`. The default, `0`, means `20`.

          order: Sort order by `created_at`. Defaults to `desc`, newest first.

          betas: This endpoint is in beta: requests must send `webhooks-2026-10-07` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["webhooks-2026-10-07"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "webhooks-2026-10-07", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/organizations/webhooks",
            page=AsyncPage[BetaOrganizationWebhookEndpoint],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "after_id": after_id,
                    "before_id": before_id,
                    "limit": limit,
                    "order": order,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.webhooks.list",
                span_route="/v1/organizations/webhooks",
            ),
            model=BetaOrganizationWebhookEndpoint,
        )

    async def delete(
        self,
        webhook_endpoint_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDeletedOrganizationWebhookEndpoint:
        """
        Delete an organization webhook endpoint.

        Every request must include the beta header
        `anthropic-beta: webhooks-2026-10-07`. A request without it returns `404`,
        exactly as if this API did not exist. Anthropic turns organization webhook
        endpoints on for each organization; until yours is on, requests also return
        `404`. Organization webhook endpoints are in beta and are not available to
        organizations with HIPAA readiness enabled.

        Args:
          webhook_endpoint_id: ID of the webhook endpoint.

          betas: This endpoint is in beta: requests must send `webhooks-2026-10-07` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not webhook_endpoint_id:
            raise ValueError(
                f"Expected a non-empty value for `webhook_endpoint_id` but received {webhook_endpoint_id!r}"
            )
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["webhooks-2026-10-07"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "webhooks-2026-10-07", **(extra_headers or {})}
        return await self._delete(
            path_template("/v1/organizations/webhooks/{webhook_endpoint_id}", webhook_endpoint_id=webhook_endpoint_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.webhooks.delete",
                span_route="/v1/organizations/webhooks/{webhook_endpoint_id}",
                span_attributes={"anthropic.organization.webhook.id": webhook_endpoint_id},
            ),
            cast_to=BetaDeletedOrganizationWebhookEndpoint,
        )

    async def regenerate_signing_secret(
        self,
        webhook_endpoint_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaOrganizationWebhookEndpointSigningSecret:
        """Replace an organization webhook endpoint's signing secret.

        The old secret stops
        working immediately. The new secret is returned only in this response.

        Every request must include the beta header
        `anthropic-beta: webhooks-2026-10-07`. A request without it returns `404`,
        exactly as if this API did not exist. Anthropic turns organization webhook
        endpoints on for each organization; until yours is on, requests also return
        `404`. Organization webhook endpoints are in beta and are not available to
        organizations with HIPAA readiness enabled.

        Args:
          webhook_endpoint_id: ID of the webhook endpoint.

          betas: This endpoint is in beta: requests must send `webhooks-2026-10-07` in this
              header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not webhook_endpoint_id:
            raise ValueError(
                f"Expected a non-empty value for `webhook_endpoint_id` but received {webhook_endpoint_id!r}"
            )
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["webhooks-2026-10-07"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "webhooks-2026-10-07", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/v1/organizations/webhooks/{webhook_endpoint_id}/regenerate_signing_secret",
                webhook_endpoint_id=webhook_endpoint_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.webhooks.regenerate_signing_secret",
                span_route="/v1/organizations/webhooks/{webhook_endpoint_id}/regenerate_signing_secret",
                span_attributes={"anthropic.organization.webhook.id": webhook_endpoint_id},
            ),
            cast_to=BetaOrganizationWebhookEndpointSigningSecret,
        )


class WebhooksWithRawResponse:
    def __init__(self, webhooks: Webhooks) -> None:
        self._webhooks = webhooks

        self.create = to_raw_response_wrapper(
            webhooks.create,
        )
        self.retrieve = to_raw_response_wrapper(
            webhooks.retrieve,
        )
        self.update = to_raw_response_wrapper(
            webhooks.update,
        )
        self.list = to_raw_response_wrapper(
            webhooks.list,
        )
        self.delete = to_raw_response_wrapper(
            webhooks.delete,
        )
        self.regenerate_signing_secret = to_raw_response_wrapper(
            webhooks.regenerate_signing_secret,
        )


class AsyncWebhooksWithRawResponse:
    def __init__(self, webhooks: AsyncWebhooks) -> None:
        self._webhooks = webhooks

        self.create = async_to_raw_response_wrapper(
            webhooks.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            webhooks.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            webhooks.update,
        )
        self.list = async_to_raw_response_wrapper(
            webhooks.list,
        )
        self.delete = async_to_raw_response_wrapper(
            webhooks.delete,
        )
        self.regenerate_signing_secret = async_to_raw_response_wrapper(
            webhooks.regenerate_signing_secret,
        )


class WebhooksWithStreamingResponse:
    def __init__(self, webhooks: Webhooks) -> None:
        self._webhooks = webhooks

        self.create = to_streamed_response_wrapper(
            webhooks.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            webhooks.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            webhooks.update,
        )
        self.list = to_streamed_response_wrapper(
            webhooks.list,
        )
        self.delete = to_streamed_response_wrapper(
            webhooks.delete,
        )
        self.regenerate_signing_secret = to_streamed_response_wrapper(
            webhooks.regenerate_signing_secret,
        )


class AsyncWebhooksWithStreamingResponse:
    def __init__(self, webhooks: AsyncWebhooks) -> None:
        self._webhooks = webhooks

        self.create = async_to_streamed_response_wrapper(
            webhooks.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            webhooks.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            webhooks.update,
        )
        self.list = async_to_streamed_response_wrapper(
            webhooks.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            webhooks.delete,
        )
        self.regenerate_signing_secret = async_to_streamed_response_wrapper(
            webhooks.regenerate_signing_secret,
        )
