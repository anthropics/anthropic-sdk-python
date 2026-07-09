# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Union, Iterable, cast
from datetime import datetime
from itertools import chain
from typing_extensions import Literal

import httpx

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ...._client import AsyncAnthropic
    from ....lib.tools._beta_session_runner import SessionToolRunner, BetaAnyRunnableTool

from .... import _legacy_response
from ...._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ...._utils import is_given, path_template, maybe_transform, strip_not_given, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from ...._streaming import Stream, AsyncStream
from ....pagination import SyncPageCursor, AsyncPageCursor
from ...._base_client import AsyncPaginator, make_request_options
from ....types.beta.sessions import event_list_params, event_send_params, event_stream_params
from ....types.anthropic_beta_param import AnthropicBetaParam
from ....types.beta.beta_managed_agents_delta_type import BetaManagedAgentsDeltaType
from ....types.beta.sessions.beta_managed_agents_event_params import BetaManagedAgentsEventParams
from ....types.beta.sessions.beta_managed_agents_session_event import BetaManagedAgentsSessionEvent
from ....types.beta.sessions.beta_managed_agents_send_session_events import BetaManagedAgentsSendSessionEvents
from ....types.beta.sessions.beta_managed_agents_stream_session_events import BetaManagedAgentsStreamSessionEvents

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
        session_id: str,
        *,
        created_at_gt: Union[str, datetime] | Omit = omit,
        created_at_gte: Union[str, datetime] | Omit = omit,
        created_at_lt: Union[str, datetime] | Omit = omit,
        created_at_lte: Union[str, datetime] | Omit = omit,
        limit: int | Omit = omit,
        order: Literal["asc", "desc"] | Omit = omit,
        page: str | Omit = omit,
        types: SequenceNotStr[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageCursor[BetaManagedAgentsSessionEvent]:
        """
        List Events

        Args:
          created_at_gt: Return events created after this time (exclusive).

          created_at_gte: Return events created at or after this time (inclusive).

          created_at_lt: Return events created before this time (exclusive).

          created_at_lte: Return events created at or before this time (inclusive).

          limit: Query parameter for limit

          order: Sort direction for results, ordered by created_at. Defaults to asc
              (chronological).

          page: Opaque pagination cursor from a previous response's next_page.

          types: Filter by event type. Values match the `type` field on returned events (for
              example, `user.message` or `agent.tool_use`). Omit to return all event types.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
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
            path_template("/v1/sessions/{session_id}/events?beta=true", session_id=session_id),
            page=SyncPageCursor[BetaManagedAgentsSessionEvent],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "created_at_gt": created_at_gt,
                        "created_at_gte": created_at_gte,
                        "created_at_lt": created_at_lt,
                        "created_at_lte": created_at_lte,
                        "limit": limit,
                        "order": order,
                        "page": page,
                        "types": types,
                    },
                    event_list_params.EventListParams,
                ),
            ),
            model=cast(
                Any, BetaManagedAgentsSessionEvent
            ),  # Union types cannot be passed in as arguments in the type system
        )

    def send(
        self,
        session_id: str,
        *,
        events: Iterable[BetaManagedAgentsEventParams],
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsSendSessionEvents:
        """
        Send Events

        Args:
          events: Events to send to the `session`.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
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
        return self._post(
            path_template("/v1/sessions/{session_id}/events?beta=true", session_id=session_id),
            body=maybe_transform({"events": events}, event_send_params.EventSendParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaManagedAgentsSendSessionEvents,
        )

    def stream(
        self,
        session_id: str,
        *,
        event_deltas: List[BetaManagedAgentsDeltaType] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Stream[BetaManagedAgentsStreamSessionEvents]:
        """
        Stream Events

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
            path_template("/v1/sessions/{session_id}/events/stream?beta=true", session_id=session_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"event_deltas": event_deltas}, event_stream_params.EventStreamParams),
            ),
            cast_to=cast(
                Any, BetaManagedAgentsStreamSessionEvents
            ),  # Union types cannot be passed in as arguments in the type system
            stream=True,
            stream_cls=Stream[BetaManagedAgentsStreamSessionEvents],
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
        session_id: str,
        *,
        created_at_gt: Union[str, datetime] | Omit = omit,
        created_at_gte: Union[str, datetime] | Omit = omit,
        created_at_lt: Union[str, datetime] | Omit = omit,
        created_at_lte: Union[str, datetime] | Omit = omit,
        limit: int | Omit = omit,
        order: Literal["asc", "desc"] | Omit = omit,
        page: str | Omit = omit,
        types: SequenceNotStr[str] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BetaManagedAgentsSessionEvent, AsyncPageCursor[BetaManagedAgentsSessionEvent]]:
        """
        List Events

        Args:
          created_at_gt: Return events created after this time (exclusive).

          created_at_gte: Return events created at or after this time (inclusive).

          created_at_lt: Return events created before this time (exclusive).

          created_at_lte: Return events created at or before this time (inclusive).

          limit: Query parameter for limit

          order: Sort direction for results, ordered by created_at. Defaults to asc
              (chronological).

          page: Opaque pagination cursor from a previous response's next_page.

          types: Filter by event type. Values match the `type` field on returned events (for
              example, `user.message` or `agent.tool_use`). Omit to return all event types.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
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
            path_template("/v1/sessions/{session_id}/events?beta=true", session_id=session_id),
            page=AsyncPageCursor[BetaManagedAgentsSessionEvent],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "created_at_gt": created_at_gt,
                        "created_at_gte": created_at_gte,
                        "created_at_lt": created_at_lt,
                        "created_at_lte": created_at_lte,
                        "limit": limit,
                        "order": order,
                        "page": page,
                        "types": types,
                    },
                    event_list_params.EventListParams,
                ),
            ),
            model=cast(
                Any, BetaManagedAgentsSessionEvent
            ),  # Union types cannot be passed in as arguments in the type system
        )

    async def send(
        self,
        session_id: str,
        *,
        events: Iterable[BetaManagedAgentsEventParams],
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BetaManagedAgentsSendSessionEvents:
        """
        Send Events

        Args:
          events: Events to send to the `session`.

          betas: Optional header to specify the beta version(s) you want to use.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
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
        return await self._post(
            path_template("/v1/sessions/{session_id}/events?beta=true", session_id=session_id),
            body=await async_maybe_transform({"events": events}, event_send_params.EventSendParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BetaManagedAgentsSendSessionEvents,
        )

    async def stream(
        self,
        session_id: str,
        *,
        event_deltas: List[BetaManagedAgentsDeltaType] | Omit = omit,
        betas: List[AnthropicBetaParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncStream[BetaManagedAgentsStreamSessionEvents]:
        """
        Stream Events

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
            path_template("/v1/sessions/{session_id}/events/stream?beta=true", session_id=session_id),
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
                Any, BetaManagedAgentsStreamSessionEvents
            ),  # Union types cannot be passed in as arguments in the type system
            stream=True,
            stream_cls=AsyncStream[BetaManagedAgentsStreamSessionEvents],
        )

    def tool_runner(
        self,
        session_id: str,
        *,
        tools: Sequence[BetaAnyRunnableTool],
        max_idle: float | None | NotGiven = not_given,
        environment_key: str | None = None,
        extra_headers: Headers | None = None,
    ) -> SessionToolRunner:
        """Dispatch a self-hosted session's tool-call events.

        The sessions-side counterpart to ``client.beta.messages.tool_runner``:
        returns a :class:`~anthropic.lib.environments.SessionToolRunner` — an
        async iterable that attaches to the session's event stream, reconciles
        against the events-list endpoint, runs the matching tool from ``tools``
        for each tool-call event, posts the matching result event back, and
        yields one :class:`~anthropic.lib.environments.DispatchedToolCall` per
        completed call. It handles both tool-call kinds: ``agent.tool_use``
        (built-in agent-toolset tools) answered with ``user.tool_result``, and
        ``agent.custom_tool_use`` (custom, user-defined tools) answered with
        ``user.custom_tool_result``. A call the server gated behind user
        confirmation (``evaluated_permission`` ``ask``, e.g. a tool configured
        with the ``always_ask`` permission policy) is held until the matching
        ``user.tool_confirmation`` event arrives — executed on ``allow``,
        never executed on ``deny`` (the denied call is still yielded with
        ``confirmation="deny"`` so it can be observed). Internally drives
        event-stream reconnect (with capped backoff) via an anyio task group
        so it works under both ``asyncio`` and ``trio``.

        Iteration ends when the session terminates (``session.status_terminated``
        / ``session.deleted``), when the consumer breaks out of the loop, or —
        once the session has gone idle with ``stop_reason`` ``end_turn`` —
        ``max_idle`` seconds elapse with no new event (any new event resets that
        countdown; it re-arms on the next ``end_turn`` idle). ``max_idle=None``
        disables that last condition. It does **not** touch the work-item lease —
        wrap it in an :class:`~anthropic.lib.environments.EnvironmentWorker` if
        you need heartbeating / force-stop.

        Usage::

            from anthropic.lib.tools.agent_toolset import AgentToolContext, beta_agent_toolset_20260401

            async with AgentToolContext(workdir=...) as env:
                async for call in client.beta.sessions.events.tool_runner(
                    work.data.id,
                    tools=[*beta_agent_toolset_20260401(env), my_tool],
                ):
                    ...

        Args:
          session_id: The session whose events stream we attach to. Passed
            positionally, matching ``list`` / ``send`` / ``stream`` on this
            resource.
          tools: Registry of tool callables the runner will execute when the
            agent emits matching ``agent.tool_use`` / ``agent.custom_tool_use``
            events — the same :class:`~anthropic.lib.tools.BetaAsyncFunctionTool`
            shape ``client.beta.messages.tool_runner`` accepts.
          max_idle: Seconds to keep running after the session goes idle with
            ``stop_reason`` ``end_turn`` before stopping; any new event resets
            the countdown. Defaults to ``DEFAULT_MAX_IDLE`` (60s) when not
            given. ``None`` disables it.
          environment_key: The self-hosted environment key. When set, the
            runner builds a Bearer-only scoped sub-client keyed to that
            environment for the event stream / list / send calls; leave it
            unset to authenticate those calls with the parent client's own
            credentials.
          extra_headers: Optional headers passed through per request on every
            call the runner makes (event stream / list / send). They are
            threaded into each call's ``extra_headers=`` and never assigned
            onto the client, so client state is not mutated. Auth and
            ``x-stainless-helper`` are supplied by the runner's scoped
            sub-client (and the parent client's ``default_headers`` propagate
            via its ``client.copy()``); a header given here overrides the
            scoped client's same-named default for that request, so use it for
            caller passthrough (e.g. trace ids), not to set auth.
        """
        # DEFAULT_MAX_IDLE resolved here rather than as a literal signature
        # default so the value can't drift from the constant; the lazy import
        # also keeps the host-only environment lib out of ``import anthropic``.
        from ....lib.tools._beta_session_runner import DEFAULT_MAX_IDLE, SessionToolRunner

        if not is_given(max_idle):
            max_idle = DEFAULT_MAX_IDLE

        return SessionToolRunner(
            cast("AsyncAnthropic", self._client),
            session_id,
            tools=tools,
            max_idle=max_idle,
            environment_key=environment_key,
            extra_headers=extra_headers,
        )


class EventsWithRawResponse:
    def __init__(self, events: Events) -> None:
        self._events = events

        self.list = _legacy_response.to_raw_response_wrapper(
            events.list,
        )
        self.send = _legacy_response.to_raw_response_wrapper(
            events.send,
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
        self.send = _legacy_response.async_to_raw_response_wrapper(
            events.send,
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
        self.send = to_streamed_response_wrapper(
            events.send,
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
        self.send = async_to_streamed_response_wrapper(
            events.send,
        )
        self.stream = async_to_streamed_response_wrapper(
            events.stream,
        )
