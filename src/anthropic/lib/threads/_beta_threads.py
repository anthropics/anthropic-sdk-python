from __future__ import annotations

from typing import TYPE_CHECKING, Union, Generic, TypeVar, Iterable, Optional, Sequence, overload
from typing_extensions import Self, Unpack, Literal

import httpx2

from ._params import (
    ThreadParams,
    RunnableToolT,
    TurnOverrides,
    UnsupportedRequestBehavior,
    turn_overrides,
    request_options,
    thread_arguments,
    reject_thread_param,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import is_given
from ..._models import add_response_ids
from ..._streaming import Stream, AsyncStream
from ...types.beta import (
    BetaMessage,
    BetaMessageParam,
    ThreadSendParams,
    BetaToolUnionParam,
    ThreadCreateParams,
    BetaRawMessageStreamEvent,
)
from ..._exceptions import AnthropicError, APIStatusError
from ._thread_state import ThreadState
from ._stream_managers import ThreadMessageStreamManager, AsyncThreadMessageStreamManager
from .._parse._response import parse_beta_response
from .._parse._transform import validate_output_config_conflict
from ...types.model_param import ModelParam
from ..tools._beta_functions import BetaRunnableTool, BetaAsyncRunnableTool
from ..streaming._beta_messages import BetaMessageStreamManager, BetaAsyncMessageStreamManager
from ...types.beta.parsed_beta_message import ResponseFormatT, ParsedBetaMessage
from ...types.beta.message_create_params import ParseMessageCreateParamsBase

if TYPE_CHECKING:
    from ..._client import Anthropic, AsyncAnthropic
    from ..tools._beta_runner import (
        BetaToolRunner,
        BetaAsyncToolRunner,
        BetaStreamingToolRunner,
        BetaAsyncStreamingToolRunner,
    )


__all__ = ["BetaMessageThread", "BetaAsyncMessageThread", "UnsupportedRequestBehavior"]


ClientT = TypeVar("ClientT", bound="Anthropic | AsyncAnthropic")


class BaseMessageThread(Generic[ClientT, RunnableToolT, ResponseFormatT]):
    """The part of a thread that sends nothing, which the sync and the async thread share."""

    _client: ClientT
    _state: ThreadState[RunnableToolT, ResponseFormatT]

    @classmethod
    def _from_state(cls, client: ClientT, state: ThreadState[RunnableToolT, ResponseFormatT]) -> Self:
        thread = cls.__new__(cls)
        thread._client = client
        thread._state = state
        return thread

    @classmethod
    def _for_tool_runner(cls, client: ClientT, params: ParseMessageCreateParamsBase[ResponseFormatT]) -> Self:
        """The thread of a tool runner that is made from the params of its requests. It sends no `thread` field on a
        client without message threads or when `params` have `thread` as `False`, and it stops sending one when the
        server cannot thread a request."""
        thread: object = params.get("thread")
        reject_thread_param(thread)
        return cls._from_state(
            client,
            ThreadState(
                params=params,
                options={},
                threading=thread is not False and client._supports_message_threads,
                unsupported_request_behavior="continue_unthreaded",
            ),
        )

    @property
    def messages(self) -> Sequence[BetaMessageParam]:
        """The full conversation: every message the server holds plus those staged for the next turn."""
        return self._state.messages

    @property
    def previous_message_id(self) -> str | None:
        """The response `id` the next turn continues from, or `None` when the next turn starts a new thread."""
        return self._state.previous_message_id

    @property
    def params(self) -> ThreadParams[RunnableToolT, ResponseFormatT]:
        """The arguments of a `client.beta.messages.thread()` call for the whole conversation, in a new dict."""
        return self._state.params

    def append(self, *messages: BetaMessageParam | BetaMessage) -> None:
        """Stage messages for the next turn without sending anything."""
        self._state.append(messages)

    def update(
        self,
        *,
        tools: Iterable[Union[BetaToolUnionParam, RunnableToolT]] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
        **params: Unpack[ThreadSendParams],
    ) -> None:
        """Change the request fields and request options of all later turns without sending anything. `system` and
        `tools` cannot change once a turn has created the thread."""
        overrides = turn_overrides(
            **params,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        self._state.update(overrides, tools=tools if is_given(tools) else None)

    def fork(self) -> Self:
        """Return a new, independent thread with a copy of this one's history, request fields, tools and request
        options, and no `previous_message_id`. Sends nothing."""
        return self._from_state(self._client, self._state.fork())

    def _parse_reply(self, reply: BetaMessage) -> ParsedBetaMessage[ResponseFormatT]:
        parsed = parse_beta_response(output_format=self._state.output_format, response=reply)
        add_response_ids(parsed, request_id=reply._request_id, workspace_id=reply._workspace_id)
        return parsed


class BetaMessageThread(BaseMessageThread["Anthropic", BetaRunnableTool, ResponseFormatT]):
    """A conversation the server holds between turns, so each request sends only the new messages.

    Create one with `client.beta.messages.thread(...)`. A thread runs one turn at a time.
    """

    def __init__(
        self,
        client: Anthropic,
        *,
        max_tokens: int,
        model: ModelParam,
        messages: Iterable[BetaMessageParam] | Omit = omit,
        tools: Iterable[BetaRunnableTool | BetaToolUnionParam] | Omit = omit,
        output_format: Optional[type[ResponseFormatT]] | Omit = omit,
        unsupported_request_behavior: UnsupportedRequestBehavior = "error",
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
        **params: Unpack[ThreadCreateParams],
    ) -> None:
        """Start a thread on `client` with the arguments of `client.beta.messages.thread()`. Sends nothing."""
        _check_message_threads_supported(client)
        validate_output_config_conflict(params.get("output_config", omit), output_format)
        self._client = client
        self._state = ThreadState(
            params=thread_arguments(
                params,
                max_tokens=max_tokens,
                model=model,
                messages=messages,
                tools=tools,
                output_format=output_format,
            ),
            options=request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            threading=True,
            unsupported_request_behavior=unsupported_request_behavior,
        )

    def send(
        self,
        *messages: BetaMessageParam | BetaMessage,
        tools: Iterable[BetaToolUnionParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
        **params: Unpack[ThreadSendParams],
    ) -> BetaMessage:
        """Send the staged messages and `messages` as one turn and return the reply. Keyword arguments apply to this
        turn only. Raises `AnthropicError` while another `send()` / `parse()` / `stream()` on this thread is in
        progress."""
        return self._send(
            messages,
            turn_overrides(
                **params,
                tools=tools,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )

    def parse(
        self,
        *messages: BetaMessageParam | BetaMessage,
        tools: Iterable[BetaToolUnionParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
        **params: Unpack[ThreadSendParams],
    ) -> ParsedBetaMessage[ResponseFormatT]:
        """Like `send()`, and parses the reply against the thread's `output_format` into `parsed_output`."""
        overrides = turn_overrides(
            **params,
            tools=tools,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._parse_reply(self._send(messages, overrides))

    def stream(
        self,
        *messages: BetaMessageParam | BetaMessage,
        tools: Iterable[BetaToolUnionParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
        **params: Unpack[ThreadSendParams],
    ) -> BetaMessageStreamManager[ResponseFormatT]:
        """Like `send()`, and returns the reply's stream. The turn is in progress until the stream ends or is closed."""
        return ThreadMessageStreamManager(
            self,
            messages,
            turn_overrides(
                **params,
                tools=tools,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )

    @overload
    def tool_runner(
        self,
        *,
        max_iterations: int | Omit = omit,
        stream: Literal[False] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaToolRunner[ResponseFormatT]: ...

    @overload
    def tool_runner(
        self,
        *,
        max_iterations: int | Omit = omit,
        stream: Literal[True],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaStreamingToolRunner[ResponseFormatT]: ...

    @overload
    def tool_runner(
        self,
        *,
        max_iterations: int | Omit = omit,
        stream: bool,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaToolRunner[ResponseFormatT] | BetaStreamingToolRunner[ResponseFormatT]: ...

    def tool_runner(
        self,
        *,
        max_iterations: int | Omit = omit,
        stream: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaToolRunner[ResponseFormatT] | BetaStreamingToolRunner[ResponseFormatT]:
        """Run the tool loop over this thread: call its `@beta_tool` functions whenever the model asks for one, until
        a reply makes no tool call. The replies and tool results become part of the thread's history."""
        from ..tools._beta_runner import BetaToolRunner, BetaStreamingToolRunner

        runner_class = BetaStreamingToolRunner[ResponseFormatT] if stream else BetaToolRunner[ResponseFormatT]
        return runner_class(
            thread=self,
            options=turn_overrides(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            max_iterations=max_iterations if is_given(max_iterations) else None,
        )

    def _send(self, messages: Iterable[BetaMessageParam | BetaMessage], overrides: TurnOverrides) -> BetaMessage:
        self._state.start_turn(messages)
        try:
            message = self._create_with_recovery(overrides, stream=False)
            self._state.record_reply(message)
            return message
        finally:
            self._state.end_turn()

    def _open_stream(
        self, messages: Iterable[BetaMessageParam | BetaMessage], overrides: TurnOverrides
    ) -> Stream[BetaRawMessageStreamEvent]:
        self._state.start_turn(messages)
        try:
            return self._create_with_recovery(overrides, stream=True)
        except BaseException:
            self._state.end_turn()
            raise

    @overload
    def _create_with_recovery(self, overrides: TurnOverrides, *, stream: Literal[False]) -> BetaMessage: ...

    @overload
    def _create_with_recovery(
        self, overrides: TurnOverrides, *, stream: Literal[True]
    ) -> Stream[BetaRawMessageStreamEvent]: ...

    def _create_with_recovery(
        self, overrides: TurnOverrides, *, stream: bool
    ) -> BetaMessage | Stream[BetaRawMessageStreamEvent]:
        """One `create()` call for this turn, re-sent as long as the state can recover from the rejection."""
        while True:
            arguments = self._state.create_arguments(overrides, stream=stream)
            try:
                if stream:
                    return self._client.beta.messages.create(**arguments, stream=True)
                return self._client.beta.messages.create(**arguments)
            except APIStatusError as error:
                if not self._state.recovers_from(error):
                    raise


class BetaAsyncMessageThread(BaseMessageThread["AsyncAnthropic", BetaAsyncRunnableTool, ResponseFormatT]):
    """A conversation the server holds between turns, so each request sends only the new messages.

    Create one with `client.beta.messages.thread(...)` on `AsyncAnthropic`. A thread runs one turn at a time.
    """

    def __init__(
        self,
        client: AsyncAnthropic,
        *,
        max_tokens: int,
        model: ModelParam,
        messages: Iterable[BetaMessageParam] | Omit = omit,
        tools: Iterable[BetaAsyncRunnableTool | BetaToolUnionParam] | Omit = omit,
        output_format: Optional[type[ResponseFormatT]] | Omit = omit,
        unsupported_request_behavior: UnsupportedRequestBehavior = "error",
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
        **params: Unpack[ThreadCreateParams],
    ) -> None:
        """Start a thread on `client` with the arguments of `client.beta.messages.thread()`. Sends nothing."""
        _check_message_threads_supported(client)
        validate_output_config_conflict(params.get("output_config", omit), output_format)
        self._client = client
        self._state = ThreadState(
            params=thread_arguments(
                params,
                max_tokens=max_tokens,
                model=model,
                messages=messages,
                tools=tools,
                output_format=output_format,
            ),
            options=request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            threading=True,
            unsupported_request_behavior=unsupported_request_behavior,
        )

    async def send(
        self,
        *messages: BetaMessageParam | BetaMessage,
        tools: Iterable[BetaToolUnionParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
        **params: Unpack[ThreadSendParams],
    ) -> BetaMessage:
        """Send the staged messages and `messages` as one turn and return the reply. Keyword arguments apply to this
        turn only. Raises `AnthropicError` while another `send()` / `parse()` / `stream()` on this thread is in
        progress."""
        return await self._send(
            messages,
            turn_overrides(
                **params,
                tools=tools,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )

    async def parse(
        self,
        *messages: BetaMessageParam | BetaMessage,
        tools: Iterable[BetaToolUnionParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
        **params: Unpack[ThreadSendParams],
    ) -> ParsedBetaMessage[ResponseFormatT]:
        """Like `send()`, and parses the reply against the thread's `output_format` into `parsed_output`."""
        overrides = turn_overrides(
            **params,
            tools=tools,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._parse_reply(await self._send(messages, overrides))

    def stream(
        self,
        *messages: BetaMessageParam | BetaMessage,
        tools: Iterable[BetaToolUnionParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
        **params: Unpack[ThreadSendParams],
    ) -> BetaAsyncMessageStreamManager[ResponseFormatT]:
        """Like `send()`, and returns the reply's stream. The turn is in progress until the stream ends or is closed."""
        return AsyncThreadMessageStreamManager(
            self,
            messages,
            turn_overrides(
                **params,
                tools=tools,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
        )

    @overload
    def tool_runner(
        self,
        *,
        max_iterations: int | Omit = omit,
        stream: Literal[False] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaAsyncToolRunner[ResponseFormatT]: ...

    @overload
    def tool_runner(
        self,
        *,
        max_iterations: int | Omit = omit,
        stream: Literal[True],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaAsyncStreamingToolRunner[ResponseFormatT]: ...

    @overload
    def tool_runner(
        self,
        *,
        max_iterations: int | Omit = omit,
        stream: bool,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaAsyncToolRunner[ResponseFormatT] | BetaAsyncStreamingToolRunner[ResponseFormatT]: ...

    def tool_runner(
        self,
        *,
        max_iterations: int | Omit = omit,
        stream: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx2.Timeout | None | NotGiven = not_given,
    ) -> BetaAsyncToolRunner[ResponseFormatT] | BetaAsyncStreamingToolRunner[ResponseFormatT]:
        """Run the tool loop over this thread: call its `@beta_async_tool` functions whenever the model asks for one,
        until a reply makes no tool call. The replies and tool results become part of the thread's history."""
        from ..tools._beta_runner import BetaAsyncToolRunner, BetaAsyncStreamingToolRunner

        runner_class = BetaAsyncStreamingToolRunner[ResponseFormatT] if stream else BetaAsyncToolRunner[ResponseFormatT]
        return runner_class(
            thread=self,
            options=turn_overrides(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            max_iterations=max_iterations if is_given(max_iterations) else None,
        )

    async def _send(self, messages: Iterable[BetaMessageParam | BetaMessage], overrides: TurnOverrides) -> BetaMessage:
        self._state.start_turn(messages)
        try:
            message = await self._create_with_recovery(overrides, stream=False)
            self._state.record_reply(message)
            return message
        finally:
            self._state.end_turn()

    async def _open_stream(
        self, messages: Iterable[BetaMessageParam | BetaMessage], overrides: TurnOverrides
    ) -> AsyncStream[BetaRawMessageStreamEvent]:
        self._state.start_turn(messages)
        try:
            return await self._create_with_recovery(overrides, stream=True)
        except BaseException:
            self._state.end_turn()
            raise

    @overload
    async def _create_with_recovery(self, overrides: TurnOverrides, *, stream: Literal[False]) -> BetaMessage: ...

    @overload
    async def _create_with_recovery(
        self, overrides: TurnOverrides, *, stream: Literal[True]
    ) -> AsyncStream[BetaRawMessageStreamEvent]: ...

    async def _create_with_recovery(
        self, overrides: TurnOverrides, *, stream: bool
    ) -> BetaMessage | AsyncStream[BetaRawMessageStreamEvent]:
        """One `create()` call for this turn, re-sent as long as the state can recover from the rejection."""
        while True:
            arguments = self._state.create_arguments(overrides, stream=stream)
            try:
                if stream:
                    return await self._client.beta.messages.create(**arguments, stream=True)
                return await self._client.beta.messages.create(**arguments)
            except APIStatusError as error:
                if not self._state.recovers_from(error):
                    raise


def _check_message_threads_supported(client: Anthropic | AsyncAnthropic) -> None:
    if not client._supports_message_threads:
        raise AnthropicError(
            "Message threads are not available on this client; use `client.beta.messages.create()` with the full `messages` instead"
        )
