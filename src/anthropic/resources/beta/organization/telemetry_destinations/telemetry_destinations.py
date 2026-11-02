from __future__ import annotations

from typing import Dict, List, Optional
from itertools import chain

import httpx2

from ....._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ....._utils import is_given, path_template, strip_not_given
from .workspaces import (
    Workspaces,
    AsyncWorkspaces,
    WorkspacesWithRawResponse,
    AsyncWorkspacesWithRawResponse,
    WorkspacesWithStreamingResponse,
    AsyncWorkspacesWithStreamingResponse,
)
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .....pagination import SyncPageCursor, AsyncPageCursor
from ....._base_client import AsyncPaginator, make_request_options
from .....types.beta.organization import (
    BetaTelemetryDestinationStateParams,
    BetaTelemetryDestinationTracesParams,
    BetaTelemetryDestinationWorkspacesParams,
)
from .....types.anthropic_beta_param import AnthropicBetaParam
from .....types.beta.organization.beta_telemetry_destination import BetaTelemetryDestination
from .....types.beta.organization.beta_deleted_telemetry_destination import BetaDeletedTelemetryDestination
from .....types.beta.organization.beta_telemetry_destination_state_params import BetaTelemetryDestinationStateParams
from .....types.beta.organization.beta_telemetry_destination_test_response import BetaTelemetryDestinationTestResponse
from .....types.beta.organization.beta_telemetry_destination_traces_params import BetaTelemetryDestinationTracesParams
from .....types.beta.organization.beta_telemetry_destination_workspaces_params import (
    BetaTelemetryDestinationWorkspacesParams,
)

__all__ = ["TelemetryDestinations", "AsyncTelemetryDestinations"]


class TelemetryDestinations(SyncAPIResource):
    @cached_property
    def workspaces(self) -> Workspaces:
        return Workspaces(self._client)

    @cached_property
    def with_raw_response(self) -> TelemetryDestinationsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return TelemetryDestinationsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TelemetryDestinationsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return TelemetryDestinationsWithStreamingResponse(self)

    def create(
        self,
        *,
        endpoint_url: str,
        workspaces: BetaTelemetryDestinationWorkspacesParams,
        display_name: Optional[str] | Omit = omit,
        headers: Dict[str, str] | Omit = omit,
        traces: BetaTelemetryDestinationTracesParams | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaTelemetryDestination:
        """
        Register an OpenTelemetry destination for the organization.

        The destination starts in state `enabled`. An organization can have at most 10
        destinations, including disabled ones.

        See the
        [OpenTelemetry export guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry#add-a-destination)
        to learn more about adding a destination.

        Args:
          endpoint_url: The base URL of your collector's OTLP/HTTP endpoint, for example
              `https://gateway.example.com`.

              The URL must use `https` and a hostname, not an IP address. The port, if given,
              must be 443. The URL must not contain a query string, a fragment, or a username
              and password. At most 2,048 characters.

              A path prefix, such as `/otlp`, is allowed. Don't include the per-signal path
              (`/v1/traces`), because the API appends it on delivery. If your collector takes
              traces on another path, also set `traces.endpoint_url`.

          workspaces: Which of the organization's workspaces the destination covers.

          display_name: Human-readable name for the destination. Optional. 1 to 255 characters.

          headers: Request headers that the API sends with every delivery, typically your
              collector's authentication header (for example `authorization`).

              The API stores the values encrypted and never returns them. Reads show only
              `header_names`.

              At most 20 headers. Names are at most 128 characters. Two names can't differ
              only in case. Values are printable ASCII, at most 4,096 characters, and can't
              begin or end with a space. Names and values together are at most 16,384 bytes.

              Reserved names are rejected, for example `host`, `cookie`, `user-agent`, and
              names that start with `content-`, `proxy-`, `x-forwarded-`, or `anthropic-`. For
              this check, `_` in a name counts as `-`.

          traces: The settings for the traces that the destination receives. If you leave it out,
              every setting takes its default.

          betas: This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["telemetry-destinations-2026-08-11"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "telemetry-destinations-2026-08-11", **(extra_headers or {})}
        return self._post(
            "/v1/organizations/telemetry_destinations",
            body={
                "endpoint_url": endpoint_url,
                "workspaces": workspaces,
                "display_name": display_name,
                "headers": headers,
                "traces": traces,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.telemetry_destinations.create",
                span_route="/v1/organizations/telemetry_destinations",
                span_created_id="anthropic.organization.telemetry_destination.id",
            ),
            cast_to=BetaTelemetryDestination,
        )

    def retrieve(
        self,
        destination_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaTelemetryDestination:
        """
        Read a destination's configuration, state, and most recent delivery results.

        See the
        [OpenTelemetry export guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry#delivery-and-health)
        to learn how the API delivers spans and when it disables a destination.

        Args:
          destination_id: ID of the destination (`tdst_...`).

          betas: This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not destination_id:
            raise ValueError(f"Expected a non-empty value for `destination_id` but received {destination_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["telemetry-destinations-2026-08-11"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "telemetry-destinations-2026-08-11", **(extra_headers or {})}
        return self._get(
            path_template("/v1/organizations/telemetry_destinations/{destination_id}", destination_id=destination_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.telemetry_destinations.retrieve",
                span_route="/v1/organizations/telemetry_destinations/{destination_id}",
                span_attributes={"anthropic.organization.telemetry_destination.id": destination_id},
            ),
            cast_to=BetaTelemetryDestination,
        )

    def update(
        self,
        destination_id: str,
        *,
        display_name: Optional[str] | Omit = omit,
        endpoint_url: str | Omit = omit,
        headers: Optional[Dict[str, Optional[str]]] | Omit = omit,
        state: BetaTelemetryDestinationStateParams | Omit = omit,
        traces: Optional[BetaTelemetryDestinationTracesParams] | Omit = omit,
        workspaces: BetaTelemetryDestinationWorkspacesParams | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaTelemetryDestination:
        """
        Change a telemetry destination's settings, its state, or which workspaces it
        covers.

        Send at least one field. Omitted fields keep their stored values, except the
        registered headers, which a change of the endpoint's hostname or port removes.
        Only `display_name`, `traces`, `traces.endpoint_url`, `traces.content_mode`,
        `traces.max_content_bytes`, and individual `headers` values accept `null`.

        If another request changes the destination while the update runs, the API
        returns a 409 `conflict_error`. Read the destination again, then retry the
        update.

        See the
        [OpenTelemetry export guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry#delivery-and-health)
        to learn more about changing a destination.

        Args:
          destination_id: ID of the destination (`tdst_...`).

          display_name: New human-readable name, 1 to 255 characters. Null clears it.

          endpoint_url: The new base URL of the destination's OTLP/HTTP endpoint. The same rules as on
              create apply.

              A change of hostname or port first removes every registered header, so send the
              headers for the new endpoint in the same request. When the destination has a
              `traces.endpoint_url`, such a change must also set `traces.endpoint_url` to a
              URL with the new hostname and port, or to `null`. A change of the path alone
              keeps the headers.

          headers: Headers to set or remove. The API merges them into the destination's headers by
              name.

              Names compare case-insensitively. A string value sets or replaces that header. A
              `null` value removes it. Headers that you omit don't change. The field itself
              can't be `null`.

              A request that sets a header value must also include `endpoint_url`. The current
              URL is accepted.

              The resulting set must stay within the same limits as on create. When the
              request sets a value, each stored value that it doesn't set counts as 4,096
              bytes toward the 16,384-byte limit, because you can't read its real length. So
              to change one header of a destination that has four or more other headers, send
              the values of the others again in the same request.

          state: Whether the destination receives deliveries after the update. The field can't be
              `null`.

          traces: The traces settings to change. Omitted settings keep their stored values.

              `null` sets every traces setting to its create default.

          workspaces: The new workspace scope, in the same form as on create. The field can't be
              `null`.

              The API refuses an update that changes the type or sends `workspace_ids` while
              the destination's list has more than 750 workspaces. Remove workspaces one at a
              time until 750 or fewer remain, then send the update again.

          betas: This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not destination_id:
            raise ValueError(f"Expected a non-empty value for `destination_id` but received {destination_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["telemetry-destinations-2026-08-11"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "telemetry-destinations-2026-08-11", **(extra_headers or {})}
        return self._post(
            path_template("/v1/organizations/telemetry_destinations/{destination_id}", destination_id=destination_id),
            body={
                "display_name": display_name,
                "endpoint_url": endpoint_url,
                "headers": headers,
                "state": state,
                "traces": traces,
                "workspaces": workspaces,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.telemetry_destinations.update",
                span_route="/v1/organizations/telemetry_destinations/{destination_id}",
                span_attributes={"anthropic.organization.telemetry_destination.id": destination_id},
            ),
            cast_to=BetaTelemetryDestination,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        workspace_ids: SequenceNotStr[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaTelemetryDestination]:
        """
        List the organization's destinations, newest first, optionally only those that
        cover given workspaces.

        See the
        [OpenTelemetry export guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry#set-up-api-tracing)
        to learn more about destinations.

        Args:
          limit: Number of destinations to return per page, between 1 and 1,000. Defaults to 20.

          page: Opaque cursor from a previous response's `next_page`. Leave it out to get the
              first page.

          workspace_ids: Return only the destinations that cover at least one of these workspaces
              (`wrkspc_...`).

              Send at most 100 IDs, as `workspace_ids[]`. A destination covers a workspace
              when its `workspaces.type` is `all`, when its `include` list has the workspace,
              or when its `exclude` list doesn't have it. Destinations in either state can
              match. An ID that isn't the ID of one of the organization's workspaces doesn't
              match any destination, not even one whose type is `all`.

          betas: This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["telemetry-destinations-2026-08-11"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "telemetry-destinations-2026-08-11", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/organizations/telemetry_destinations",
            page=SyncPageCursor[BetaTelemetryDestination],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "page": page,
                    "workspace_ids": workspace_ids,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.telemetry_destinations.list",
                span_route="/v1/organizations/telemetry_destinations",
            ),
            model=BetaTelemetryDestination,
        )

    def delete(
        self,
        destination_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDeletedTelemetryDestination:
        """
        Delete a destination and its workspace list.

        The API stops sending spans to the destination. The spans of the workspaces it
        covered still go to the other destinations that cover them. A deleted
        destination can't be read, listed, or restored.

        See the
        [OpenTelemetry export guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry#delivery-and-health)
        to learn more about managing a destination.

        Args:
          destination_id: ID of the destination (`tdst_...`).

          betas: This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not destination_id:
            raise ValueError(f"Expected a non-empty value for `destination_id` but received {destination_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["telemetry-destinations-2026-08-11"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "telemetry-destinations-2026-08-11", **(extra_headers or {})}
        return self._delete(
            path_template("/v1/organizations/telemetry_destinations/{destination_id}", destination_id=destination_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.telemetry_destinations.delete",
                span_route="/v1/organizations/telemetry_destinations/{destination_id}",
                span_attributes={"anthropic.organization.telemetry_destination.id": destination_id},
            ),
            cast_to=BetaDeletedTelemetryDestination,
        )

    def test(
        self,
        destination_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaTelemetryDestinationTestResponse:
        """
        Send one test span, named `anthropic.test`, to the destination with its
        registered headers, once and without retries, and report the destination's
        answer. The response is 200 whether or not the destination answered with a 2xx
        status: its `result` has the type `success`, or the type `failure` and the
        reason in `error`. The destination's configuration, `state` and
        `delivery_health` do not change. A disabled destination can be tested too. Wait
        10 seconds between tests of one destination; a request that comes sooner may be
        answered with status 429.

        Args:
          destination_id: ID of the destination to test (starts with `tdst_`).

          betas: This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not destination_id:
            raise ValueError(f"Expected a non-empty value for `destination_id` but received {destination_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["telemetry-destinations-2026-08-11"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "telemetry-destinations-2026-08-11", **(extra_headers or {})}
        return self._post(
            path_template(
                "/v1/organizations/telemetry_destinations/{destination_id}/test", destination_id=destination_id
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.telemetry_destinations.test",
                span_route="/v1/organizations/telemetry_destinations/{destination_id}/test",
                span_attributes={"anthropic.organization.telemetry_destination.id": destination_id},
            ),
            cast_to=BetaTelemetryDestinationTestResponse,
        )


class AsyncTelemetryDestinations(AsyncAPIResource):
    @cached_property
    def workspaces(self) -> AsyncWorkspaces:
        return AsyncWorkspaces(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTelemetryDestinationsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTelemetryDestinationsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTelemetryDestinationsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncTelemetryDestinationsWithStreamingResponse(self)

    async def create(
        self,
        *,
        endpoint_url: str,
        workspaces: BetaTelemetryDestinationWorkspacesParams,
        display_name: Optional[str] | Omit = omit,
        headers: Dict[str, str] | Omit = omit,
        traces: BetaTelemetryDestinationTracesParams | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaTelemetryDestination:
        """
        Register an OpenTelemetry destination for the organization.

        The destination starts in state `enabled`. An organization can have at most 10
        destinations, including disabled ones.

        See the
        [OpenTelemetry export guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry#add-a-destination)
        to learn more about adding a destination.

        Args:
          endpoint_url: The base URL of your collector's OTLP/HTTP endpoint, for example
              `https://gateway.example.com`.

              The URL must use `https` and a hostname, not an IP address. The port, if given,
              must be 443. The URL must not contain a query string, a fragment, or a username
              and password. At most 2,048 characters.

              A path prefix, such as `/otlp`, is allowed. Don't include the per-signal path
              (`/v1/traces`), because the API appends it on delivery. If your collector takes
              traces on another path, also set `traces.endpoint_url`.

          workspaces: Which of the organization's workspaces the destination covers.

          display_name: Human-readable name for the destination. Optional. 1 to 255 characters.

          headers: Request headers that the API sends with every delivery, typically your
              collector's authentication header (for example `authorization`).

              The API stores the values encrypted and never returns them. Reads show only
              `header_names`.

              At most 20 headers. Names are at most 128 characters. Two names can't differ
              only in case. Values are printable ASCII, at most 4,096 characters, and can't
              begin or end with a space. Names and values together are at most 16,384 bytes.

              Reserved names are rejected, for example `host`, `cookie`, `user-agent`, and
              names that start with `content-`, `proxy-`, `x-forwarded-`, or `anthropic-`. For
              this check, `_` in a name counts as `-`.

          traces: The settings for the traces that the destination receives. If you leave it out,
              every setting takes its default.

          betas: This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["telemetry-destinations-2026-08-11"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "telemetry-destinations-2026-08-11", **(extra_headers or {})}
        return await self._post(
            "/v1/organizations/telemetry_destinations",
            body={
                "endpoint_url": endpoint_url,
                "workspaces": workspaces,
                "display_name": display_name,
                "headers": headers,
                "traces": traces,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.telemetry_destinations.create",
                span_route="/v1/organizations/telemetry_destinations",
                span_created_id="anthropic.organization.telemetry_destination.id",
            ),
            cast_to=BetaTelemetryDestination,
        )

    async def retrieve(
        self,
        destination_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaTelemetryDestination:
        """
        Read a destination's configuration, state, and most recent delivery results.

        See the
        [OpenTelemetry export guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry#delivery-and-health)
        to learn how the API delivers spans and when it disables a destination.

        Args:
          destination_id: ID of the destination (`tdst_...`).

          betas: This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not destination_id:
            raise ValueError(f"Expected a non-empty value for `destination_id` but received {destination_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["telemetry-destinations-2026-08-11"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "telemetry-destinations-2026-08-11", **(extra_headers or {})}
        return await self._get(
            path_template("/v1/organizations/telemetry_destinations/{destination_id}", destination_id=destination_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.telemetry_destinations.retrieve",
                span_route="/v1/organizations/telemetry_destinations/{destination_id}",
                span_attributes={"anthropic.organization.telemetry_destination.id": destination_id},
            ),
            cast_to=BetaTelemetryDestination,
        )

    async def update(
        self,
        destination_id: str,
        *,
        display_name: Optional[str] | Omit = omit,
        endpoint_url: str | Omit = omit,
        headers: Optional[Dict[str, Optional[str]]] | Omit = omit,
        state: BetaTelemetryDestinationStateParams | Omit = omit,
        traces: Optional[BetaTelemetryDestinationTracesParams] | Omit = omit,
        workspaces: BetaTelemetryDestinationWorkspacesParams | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaTelemetryDestination:
        """
        Change a telemetry destination's settings, its state, or which workspaces it
        covers.

        Send at least one field. Omitted fields keep their stored values, except the
        registered headers, which a change of the endpoint's hostname or port removes.
        Only `display_name`, `traces`, `traces.endpoint_url`, `traces.content_mode`,
        `traces.max_content_bytes`, and individual `headers` values accept `null`.

        If another request changes the destination while the update runs, the API
        returns a 409 `conflict_error`. Read the destination again, then retry the
        update.

        See the
        [OpenTelemetry export guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry#delivery-and-health)
        to learn more about changing a destination.

        Args:
          destination_id: ID of the destination (`tdst_...`).

          display_name: New human-readable name, 1 to 255 characters. Null clears it.

          endpoint_url: The new base URL of the destination's OTLP/HTTP endpoint. The same rules as on
              create apply.

              A change of hostname or port first removes every registered header, so send the
              headers for the new endpoint in the same request. When the destination has a
              `traces.endpoint_url`, such a change must also set `traces.endpoint_url` to a
              URL with the new hostname and port, or to `null`. A change of the path alone
              keeps the headers.

          headers: Headers to set or remove. The API merges them into the destination's headers by
              name.

              Names compare case-insensitively. A string value sets or replaces that header. A
              `null` value removes it. Headers that you omit don't change. The field itself
              can't be `null`.

              A request that sets a header value must also include `endpoint_url`. The current
              URL is accepted.

              The resulting set must stay within the same limits as on create. When the
              request sets a value, each stored value that it doesn't set counts as 4,096
              bytes toward the 16,384-byte limit, because you can't read its real length. So
              to change one header of a destination that has four or more other headers, send
              the values of the others again in the same request.

          state: Whether the destination receives deliveries after the update. The field can't be
              `null`.

          traces: The traces settings to change. Omitted settings keep their stored values.

              `null` sets every traces setting to its create default.

          workspaces: The new workspace scope, in the same form as on create. The field can't be
              `null`.

              The API refuses an update that changes the type or sends `workspace_ids` while
              the destination's list has more than 750 workspaces. Remove workspaces one at a
              time until 750 or fewer remain, then send the update again.

          betas: This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not destination_id:
            raise ValueError(f"Expected a non-empty value for `destination_id` but received {destination_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["telemetry-destinations-2026-08-11"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "telemetry-destinations-2026-08-11", **(extra_headers or {})}
        return await self._post(
            path_template("/v1/organizations/telemetry_destinations/{destination_id}", destination_id=destination_id),
            body={
                "display_name": display_name,
                "endpoint_url": endpoint_url,
                "headers": headers,
                "state": state,
                "traces": traces,
                "workspaces": workspaces,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.telemetry_destinations.update",
                span_route="/v1/organizations/telemetry_destinations/{destination_id}",
                span_attributes={"anthropic.organization.telemetry_destination.id": destination_id},
            ),
            cast_to=BetaTelemetryDestination,
        )

    def list(
        self,
        *,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        workspace_ids: SequenceNotStr[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaTelemetryDestination, AsyncPageCursor[BetaTelemetryDestination]]:
        """
        List the organization's destinations, newest first, optionally only those that
        cover given workspaces.

        See the
        [OpenTelemetry export guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry#set-up-api-tracing)
        to learn more about destinations.

        Args:
          limit: Number of destinations to return per page, between 1 and 1,000. Defaults to 20.

          page: Opaque cursor from a previous response's `next_page`. Leave it out to get the
              first page.

          workspace_ids: Return only the destinations that cover at least one of these workspaces
              (`wrkspc_...`).

              Send at most 100 IDs, as `workspace_ids[]`. A destination covers a workspace
              when its `workspaces.type` is `all`, when its `include` list has the workspace,
              or when its `exclude` list doesn't have it. Destinations in either state can
              match. An ID that isn't the ID of one of the organization's workspaces doesn't
              match any destination, not even one whose type is `all`.

          betas: This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["telemetry-destinations-2026-08-11"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "telemetry-destinations-2026-08-11", **(extra_headers or {})}
        return self._get_api_list(
            "/v1/organizations/telemetry_destinations",
            page=AsyncPageCursor[BetaTelemetryDestination],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query={
                    "limit": limit,
                    "page": page,
                    "workspace_ids": workspace_ids,
                },
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.telemetry_destinations.list",
                span_route="/v1/organizations/telemetry_destinations",
            ),
            model=BetaTelemetryDestination,
        )

    async def delete(
        self,
        destination_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaDeletedTelemetryDestination:
        """
        Delete a destination and its workspace list.

        The API stops sending spans to the destination. The spans of the workspaces it
        covered still go to the other destinations that cover them. A deleted
        destination can't be read, listed, or restored.

        See the
        [OpenTelemetry export guide](https://platform.claude.com/docs/en/manage-claude/opentelemetry#delivery-and-health)
        to learn more about managing a destination.

        Args:
          destination_id: ID of the destination (`tdst_...`).

          betas: This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not destination_id:
            raise ValueError(f"Expected a non-empty value for `destination_id` but received {destination_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["telemetry-destinations-2026-08-11"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "telemetry-destinations-2026-08-11", **(extra_headers or {})}
        return await self._delete(
            path_template("/v1/organizations/telemetry_destinations/{destination_id}", destination_id=destination_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.telemetry_destinations.delete",
                span_route="/v1/organizations/telemetry_destinations/{destination_id}",
                span_attributes={"anthropic.organization.telemetry_destination.id": destination_id},
            ),
            cast_to=BetaDeletedTelemetryDestination,
        )

    async def test(
        self,
        destination_id: str,
        *,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaTelemetryDestinationTestResponse:
        """
        Send one test span, named `anthropic.test`, to the destination with its
        registered headers, once and without retries, and report the destination's
        answer. The response is 200 whether or not the destination answered with a 2xx
        status: its `result` has the type `success`, or the type `failure` and the
        reason in `error`. The destination's configuration, `state` and
        `delivery_health` do not change. A disabled destination can be tested too. Wait
        10 seconds between tests of one destination; a request that comes sooner may be
        answered with status 429.

        Args:
          destination_id: ID of the destination to test (starts with `tdst_`).

          betas: This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
              in this header.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not destination_id:
            raise ValueError(f"Expected a non-empty value for `destination_id` but received {destination_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["telemetry-destinations-2026-08-11"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "telemetry-destinations-2026-08-11", **(extra_headers or {})}
        return await self._post(
            path_template(
                "/v1/organizations/telemetry_destinations/{destination_id}/test", destination_id=destination_id
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                qualifiers={"beta": "true"},
                span_name="anthropic.organization.telemetry_destinations.test",
                span_route="/v1/organizations/telemetry_destinations/{destination_id}/test",
                span_attributes={"anthropic.organization.telemetry_destination.id": destination_id},
            ),
            cast_to=BetaTelemetryDestinationTestResponse,
        )


class TelemetryDestinationsWithRawResponse:
    def __init__(self, telemetry_destinations: TelemetryDestinations) -> None:
        self._telemetry_destinations = telemetry_destinations

        self.create = to_raw_response_wrapper(
            telemetry_destinations.create,
        )
        self.retrieve = to_raw_response_wrapper(
            telemetry_destinations.retrieve,
        )
        self.update = to_raw_response_wrapper(
            telemetry_destinations.update,
        )
        self.list = to_raw_response_wrapper(
            telemetry_destinations.list,
        )
        self.delete = to_raw_response_wrapper(
            telemetry_destinations.delete,
        )
        self.test = to_raw_response_wrapper(
            telemetry_destinations.test,
        )

    @cached_property
    def workspaces(self) -> WorkspacesWithRawResponse:
        return WorkspacesWithRawResponse(self._telemetry_destinations.workspaces)


class AsyncTelemetryDestinationsWithRawResponse:
    def __init__(self, telemetry_destinations: AsyncTelemetryDestinations) -> None:
        self._telemetry_destinations = telemetry_destinations

        self.create = async_to_raw_response_wrapper(
            telemetry_destinations.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            telemetry_destinations.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            telemetry_destinations.update,
        )
        self.list = async_to_raw_response_wrapper(
            telemetry_destinations.list,
        )
        self.delete = async_to_raw_response_wrapper(
            telemetry_destinations.delete,
        )
        self.test = async_to_raw_response_wrapper(
            telemetry_destinations.test,
        )

    @cached_property
    def workspaces(self) -> AsyncWorkspacesWithRawResponse:
        return AsyncWorkspacesWithRawResponse(self._telemetry_destinations.workspaces)


class TelemetryDestinationsWithStreamingResponse:
    def __init__(self, telemetry_destinations: TelemetryDestinations) -> None:
        self._telemetry_destinations = telemetry_destinations

        self.create = to_streamed_response_wrapper(
            telemetry_destinations.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            telemetry_destinations.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            telemetry_destinations.update,
        )
        self.list = to_streamed_response_wrapper(
            telemetry_destinations.list,
        )
        self.delete = to_streamed_response_wrapper(
            telemetry_destinations.delete,
        )
        self.test = to_streamed_response_wrapper(
            telemetry_destinations.test,
        )

    @cached_property
    def workspaces(self) -> WorkspacesWithStreamingResponse:
        return WorkspacesWithStreamingResponse(self._telemetry_destinations.workspaces)


class AsyncTelemetryDestinationsWithStreamingResponse:
    def __init__(self, telemetry_destinations: AsyncTelemetryDestinations) -> None:
        self._telemetry_destinations = telemetry_destinations

        self.create = async_to_streamed_response_wrapper(
            telemetry_destinations.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            telemetry_destinations.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            telemetry_destinations.update,
        )
        self.list = async_to_streamed_response_wrapper(
            telemetry_destinations.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            telemetry_destinations.delete,
        )
        self.test = async_to_streamed_response_wrapper(
            telemetry_destinations.test,
        )

    @cached_property
    def workspaces(self) -> AsyncWorkspacesWithStreamingResponse:
        return AsyncWorkspacesWithStreamingResponse(self._telemetry_destinations.workspaces)
