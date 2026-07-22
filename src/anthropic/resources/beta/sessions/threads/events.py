# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, List, cast
from itertools import chain

import httpx

from ..... import _legacy_response
from ....._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ....._utils import is_given, path_template, maybe_transform, strip_not_given, async_maybe_transform
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ....._streaming import Stream, AsyncStream
from .....pagination import SyncPageCursor, AsyncPageCursor
from ....._base_client import AsyncPaginator, make_request_options
from .....types.anthropic_beta_param import AnthropicBetaParam
from .....types.beta.sessions.threads import event_list_params, event_stream_params
from .....types.beta.beta_managed_agents_delta_type import BetaManagedAgentsDeltaType
from .....types.beta.sessions.beta_managed_agents_session_event import BetaManagedAgentsSessionEvent
from .....types.beta.sessions.beta_managed_agents_stream_session_thread_events import (
    BetaManagedAgentsStreamSessionThreadEvents,
)

__all__ = ["Events", "AsyncEvents"]


class Events(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EventsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return EventsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EventsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return EventsWithStreamingResponse(self)

    def list(
        self,
        thread_id: str,
        *,
        session_id: str,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaManagedAgentsSessionEvent]:
        """
        List Session Thread Events

        Args:
          limit: Query parameter for limit

          page: Query parameter for page

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return self._get_api_list(
            path_template(
                "/v1/sessions/{session_id}/threads/{thread_id}/events?beta=true",
                session_id=session_id,
                thread_id=thread_id,
            ),
            page=SyncPageCursor[BetaManagedAgentsSessionEvent],
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
                    event_list_params.EventListParams,
                ),
            ),
            model=cast(
                Any, BetaManagedAgentsSessionEvent
            ),  # Union types cannot be passed in as arguments in the type system
        )

    def stream(
        self,
        thread_id: str,
        *,
        session_id: str,
        event_deltas: List[BetaManagedAgentsDeltaType] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Stream[BetaManagedAgentsStreamSessionThreadEvents]:
        """
        Stream Session Thread Events

        Args:
          event_deltas: When set, this connection also receives streaming deltas (`event_start`,
              `event_delta`) while an event is being produced, before the event itself
              arrives. Deltas are best-effort; when the final event is produced it carries the
              complete content. A model request that ends early (an error or interrupt)
              produces no final event — its terminal `span.model_request_end` closes the
              preview. Accepts one or more event types to preview and may be repeated:
              `agent.message` streams `content_delta` fragments; `agent.thinking` is
              start-only — a signal that the agent has begun extended thinking, concluded by
              the `agent.thinking` event itself. Only previews of the requested event types
              are sent.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return self._get(
            path_template(
                "/v1/sessions/{session_id}/threads/{thread_id}/stream?beta=true",
                session_id=session_id,
                thread_id=thread_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"event_deltas": event_deltas}, event_stream_params.EventStreamParams),
            ),
            cast_to=cast(
                Any, BetaManagedAgentsStreamSessionThreadEvents
            ),  # Union types cannot be passed in as arguments in the type system
            stream=True,
            stream_cls=Stream[BetaManagedAgentsStreamSessionThreadEvents],
        )


class AsyncEvents(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEventsWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEventsWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEventsWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/anthropics/anthropic-sdk-python#with_streaming_response
        """
        return AsyncEventsWithStreamingResponse(self)

    def list(
        self,
        thread_id: str,
        *,
        session_id: str,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaManagedAgentsSessionEvent, AsyncPageCursor[BetaManagedAgentsSessionEvent]]:
        """
        List Session Thread Events

        Args:
          limit: Query parameter for limit

          page: Query parameter for page

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return self._get_api_list(
            path_template(
                "/v1/sessions/{session_id}/threads/{thread_id}/events?beta=true",
                session_id=session_id,
                thread_id=thread_id,
            ),
            page=AsyncPageCursor[BetaManagedAgentsSessionEvent],
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
                    event_list_params.EventListParams,
                ),
            ),
            model=cast(
                Any, BetaManagedAgentsSessionEvent
            ),  # Union types cannot be passed in as arguments in the type system
        )

    async def stream(
        self,
        thread_id: str,
        *,
        session_id: str,
        event_deltas: List[BetaManagedAgentsDeltaType] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncStream[BetaManagedAgentsStreamSessionThreadEvents]:
        """
        Stream Session Thread Events

        Args:
          event_deltas: When set, this connection also receives streaming deltas (`event_start`,
              `event_delta`) while an event is being produced, before the event itself
              arrives. Deltas are best-effort; when the final event is produced it carries the
              complete content. A model request that ends early (an error or interrupt)
              produces no final event — its terminal `span.model_request_end` closes the
              preview. Accepts one or more event types to preview and may be repeated:
              `agent.message` streams `content_delta` fragments; `agent.thinking` is
              start-only — a signal that the agent has begun extended thinking, concluded by
              the `agent.thinking` event itself. Only previews of the requested event types
              are sent.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        extra_headers = {
            **strip_not_given(
                {
                    "anthropic-beta": ",".join(chain((str(e) for e in betas), ["managed-agents-2026-04-01"]))
                    if is_given(betas)
                    else not_given
                }
            ),
            **(extra_headers or {}),
        }
        extra_headers = {"anthropic-beta": "managed-agents-2026-04-01", **(extra_headers or {})}
        return await self._get(
            path_template(
                "/v1/sessions/{session_id}/threads/{thread_id}/stream?beta=true",
                session_id=session_id,
                thread_id=thread_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"event_deltas": event_deltas}, event_stream_params.EventStreamParams
                ),
            ),
            cast_to=cast(
                Any, BetaManagedAgentsStreamSessionThreadEvents
            ),  # Union types cannot be passed in as arguments in the type system
            stream=True,
            stream_cls=AsyncStream[BetaManagedAgentsStreamSessionThreadEvents],
        )


class EventsWithRawResponse:
    def __init__(self, events: Events) -> None:
        self._events = events

        self.list = _legacy_response.to_raw_response_wrapper(
            events.list,
        )
        self.stream = _legacy_response.to_raw_response_wrapper(
            events.stream,
        )


class AsyncEventsWithRawResponse:
    def __init__(self, events: AsyncEvents) -> None:
        self._events = events

        self.list = _legacy_response.async_to_raw_response_wrapper(
            events.list,
        )
        self.stream = _legacy_response.async_to_raw_response_wrapper(
            events.stream,
        )


class EventsWithStreamingResponse:
    def __init__(self, events: Events) -> None:
        self._events = events

        self.list = to_streamed_response_wrapper(
            events.list,
        )
        self.stream = to_streamed_response_wrapper(
            events.stream,
        )


class AsyncEventsWithStreamingResponse:
    def __init__(self, events: AsyncEvents) -> None:
        self._events = events

        self.list = async_to_streamed_response_wrapper(
            events.list,
        )
        self.stream = async_to_streamed_response_wrapper(
            events.stream,
        )
