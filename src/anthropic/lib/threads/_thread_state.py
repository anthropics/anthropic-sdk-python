from __future__ import annotations

import copy
import logging
from typing import Generic, Mapping, Iterable, Sequence, cast
from collections.abc import Collection
from typing_extensions import Literal, get_args

import pydantic

from ._params import (
    THREAD_FIELDS,
    ThreadFields,
    ThreadParams,
    RunnableToolT,
    TurnOverrides,
    RequestOptions,
    CreateArguments,
    UnsupportedRequestBehavior,
    given,
    override_fields,
    override_request_options,
)
from ..._types import Omit, NotGiven, omit, not_given
from ..._utils import is_dict, is_list
from ..._compat import model_copy
from ...types.beta import BetaMessage, BetaMessageParam, BetaMessageThreadParam
from ..._exceptions import AnthropicError, APIStatusError
from ..._base_client import build_headers, merge_headers, _append_header_value
from ..._utils._json import openapi_model_dump
from .._parse._transform import merge_output_config, to_json_output_format
from .._stainless_helpers import (
    HELPER_METHOD_STREAM,
    STAINLESS_HELPER_METHOD_HEADER,
    STAINLESS_STREAM_HELPER_HEADER,
    helper_header,
)
from ..tools._tool_dispatch import tool_registry
from ..tools._beta_functions import (
    BetaFunctionTool,
    BetaAsyncFunctionTool,
    BetaBuiltinFunctionTool,
    BetaAsyncBuiltinFunctionTool,
)
from ...types.beta.parsed_beta_message import ResponseFormatT
from ...types.beta.beta_tool_union_param import BetaToolUnionParam
from ...types.beta.message_create_params import ParseMessageCreateParamsBase

log = logging.getLogger(__name__)


class ThreadState(Generic[RunnableToolT, ResponseFormatT]):
    """A thread's local view of the conversation: the full history, which part of it the server holds and which
    reply the next turn continues from, the request fields for the next turn, and the turn in flight, if any.

    Sends nothing itself: it assembles each turn's `create()` arguments and records what the reply changes.
    """

    def __init__(
        self,
        *,
        params: ParseMessageCreateParamsBase[ResponseFormatT],
        options: RequestOptions,
        threading: bool,
        unsupported_request_behavior: UnsupportedRequestBehavior,
    ) -> None:
        self.options = options
        # Kept apart from `options`, so that no later `extra_headers` can drop it.
        self._helper_headers = helper_header("message-thread") if threading else {}
        self.unsupported_request_behavior: UnsupportedRequestBehavior = unsupported_request_behavior
        # The tools as given, `@beta_tool` functions included, and the runnable ones by name. `_fields["tools"]`
        # holds their request definitions.
        self._tools: list[BetaToolUnionParam | RunnableToolT] | None = None
        self.runnable_tools: dict[str, RunnableToolT] = {}
        self._fields: ThreadFields
        self._output_format: JSONOutputFormat[ResponseFormatT] | None = None

        self._stored: list[Entry] = []
        self._staged: list[Entry] = []
        self._thread: ThreadPosition = New() if threading else "off"
        self._turn: Turn | None = None

        self.set_params(params)

    @property
    def threading(self) -> bool:
        """Whether turns send a `thread` field at all."""
        return self._thread not in ("off", "unthreaded")

    @property
    def previous_message_id(self) -> str | None:
        """The `id` of the stored reply the next turn continues from, or `None` when it starts a new thread."""
        return self._thread.previous_message_id if isinstance(self._thread, Continue) else None

    @property
    def messages(self) -> Sequence[BetaMessageParam]:
        """Every message the server holds plus those staged for the next turn, with any edits deferred by a turn in
        flight already applied."""
        if self._turn is not None and self._turn.replacement_history is not None:
            messages = list(self._turn.replacement_history)
        else:
            messages = [entry.param for entry in (*self._stored, *self._staged)]
        if self._turn is not None:
            messages.extend(map(_to_message_param, self._turn.deferred_messages))
        return tuple(messages)

    def append(self, messages: Iterable[BetaMessageParam | BetaMessage]) -> None:
        """Stage messages for the next turn, skipping the reply just recorded and deferring while a turn is in
        flight."""
        if self._turn is not None:
            self._turn.deferred_messages.extend(messages)
            return
        for message in messages:
            if self._repeats_last_reply(message):
                continue
            self._staged.append(Given(_to_message_param(message)))

    def _repeats_last_reply(self, message: BetaMessageParam | BetaMessage) -> bool:
        """Whether `message` is the reply last recorded, as returned, or a copy of it appended right after it."""
        if isinstance(message, BetaMessage):
            last_reply = self._last_reply
            return last_reply is not None and message.id == last_reply.id
        entries = self._staged or self._stored
        return bool(entries) and isinstance(entries[-1], Reply) and same_message(message, entries[-1].param)

    @property
    def _last_reply(self) -> BetaMessage | None:
        """The most recent reply the history records."""
        for entries in (self._staged, self._stored):
            for entry in reversed(entries):
                if isinstance(entry, Reply):
                    return entry.message
        return None

    def update(
        self, overrides: TurnOverrides, *, tools: Iterable[BetaToolUnionParam | RunnableToolT] | None = None
    ) -> None:
        """Apply the given request fields, tools and request options to all later turns. They stay, whatever the turn in
        flight was given for itself."""
        self._fields = override_fields(self._fields, overrides)
        if tools is not None:
            self._tools = tools if isinstance(tools, list) else list(tools)
            self._read_tools()
        self.options = override_request_options(self.options, overrides)
        if isinstance(self._thread, Created):
            for field in CREATE_ONLY_FIELDS:
                if field in overrides or (field == "tools" and tools is not None):
                    self._thread.given_for_the_turn.pop(field, None)

    def _read_tools(self) -> None:
        """Take the runnable tools and the request definitions from the tools. A list is kept as given and read again
        for each turn, like any other field, so the turn sees an edit of it in place."""
        if self._tools is not None:
            self.runnable_tools, self._fields["tools"] = _split_tools(self._tools)

    def fork(self) -> ThreadState[RunnableToolT, ResponseFormatT]:
        """A copy with the same history, request fields, tools and options that continues from no stored reply and
        has no turn in flight."""
        fork = copy.copy(self)
        fork.runnable_tools = dict(self.runnable_tools)
        fork._fields = copy.copy(self._fields)
        fork._stored = list(self._stored)
        fork._staged = list(self._staged)
        fork._thread = New() if self.threading else self._thread
        fork._turn = None
        if self._turn is not None:
            if self._turn.replacement_history is not None:
                fork._stored = []
                fork._staged = [Given(message) for message in self._turn.replacement_history]
            fork.append(self._turn.deferred_messages)
        return fork

    def set_params(self, params: ParseMessageCreateParamsBase[ResponseFormatT]) -> None:
        """Replace the request fields, tools and output format with those of `params`, so that one it leaves out is no
        longer sent, except the container of the last reply, then `set_messages()`. The runnable tools stay registered
        until `params` give other tools."""
        params = cast(ParseMessageCreateParamsBase[ResponseFormatT], given(params))
        tools = cast("Iterable[BetaToolUnionParam | RunnableToolT] | None", params.get("tools"))
        self._fields = cast(ThreadFields, {k: v for k, v in params.items() if k in THREAD_FIELDS and k != "tools"})
        self._adopt_container(self._last_reply)
        self._tools = None
        if isinstance(self._thread, Created):
            self._thread.given_for_the_turn = TurnOverrides()
        self.update({}, tools=tools)
        output_type = cast("type[ResponseFormatT] | None", params.get("output_format"))
        self._output_format = JSONOutputFormat(output_type) if output_type is not None else None
        self.set_messages(list(params["messages"]))

    def set_messages(self, messages: list[BetaMessageParam]) -> None:
        """Take the history from `messages`: additions to the current history are staged, and any other list replaces it
        and starts a new thread."""
        if self._turn is not None:
            # A turn in flight has already sent what is staged: an edit that only appends to it is deferred like
            # `append()`, and a rewritten history replaces the thread (and anything deferred so far) once the turn ends.
            sent = [entry.param for entry in (*self._stored, *self._staged)]
            if same_messages(messages[: len(sent)], sent):
                self._turn.replacement_history = None
                self._turn.deferred_messages = list(messages[len(sent) :])
            else:
                self._turn.replacement_history = messages
                self._turn.deferred_messages = []
            return
        old_entries = [*self._stored, *self._staged]
        stored = [entry.param for entry in self._stored]
        if not same_messages(messages[: len(stored)], stored):
            self._stored = []
            if self.threading:
                self._thread = New()
        self._staged = []
        # A message that is a recorded reply keeps that record, so a history copied from `messages` or `params` and
        # edited still knows which of its messages the thread received rather than was given.
        replies = [entry for entry in old_entries if isinstance(entry, Reply)]
        for message in messages[len(self._stored) :]:
            if self._repeats_last_reply(message):
                continue
            recorded = next((entry for entry in reversed(replies) if same_message(message, entry.param)), None)
            self._staged.append(recorded or Given(message))

    @property
    def params(self) -> ThreadParams[RunnableToolT, ResponseFormatT]:
        """The thread as the arguments of one call for the whole conversation: its request fields, tools as given,
        output format, full history and `unsupported_request_behavior`. While the turn that creates the thread is in
        flight, what it was given for itself stands in for the thread's own. A new dict on each access."""
        params: ThreadParams[RunnableToolT, ResponseFormatT] = {
            **self._fields,
            "messages": list(self.messages),
            "unsupported_request_behavior": self.unsupported_request_behavior,
        }
        if self._tools is not None:
            params["tools"] = list(self._tools)
        if self._turn is not None and isinstance(self._thread, Created):
            params.update(cast("ThreadParams[RunnableToolT, ResponseFormatT]", self._thread.given_for_the_turn))
        if self._output_format is not None:
            params["output_format"] = self._output_format.output_type
        return params

    @property
    def output_format(self) -> ResponseFormatT | NotGiven:
        if self._output_format is None:
            return not_given
        # The parse helpers type the output class as `ResponseFormatT` itself rather than `type[ResponseFormatT]`.
        return cast(ResponseFormatT, self._output_format.output_type)

    @property
    def has_staged_messages(self) -> bool:
        return bool(self._staged)

    def start_turn(self, messages: Iterable[BetaMessageParam | BetaMessage]) -> None:
        """Stage `messages` and start the turn that sends them. The turn goes out even if nothing is staged then."""
        if self._turn is not None:
            raise AnthropicError("Another `send()`, `parse()` or `stream()` is already in progress on this thread")
        staged_before = len(self._staged)
        self.append(messages)
        self._turn = Turn(self._staged[staged_before:])
        self._retry_partial_turn()

    def end_turn(self) -> None:
        """Mark the turn in flight finished, take back the messages it was started with unless a reply to them
        started, and apply the history edits deferred during it."""
        turn, self._turn = self._turn, None
        if turn is None:
            raise RuntimeError("No `send()`, `parse()` or `stream()` is in progress on this thread")
        # A reply that started has moved everything staged into the stored history.
        self._staged = [entry for entry in self._staged if entry not in turn.started_with]
        if turn.replacement_history is not None:
            self.set_messages(turn.replacement_history)
        self.append(turn.deferred_messages)

    def recovers_from(self, error: APIStatusError) -> bool:
        """Whether the turn should be sent again because `error` is a thread rejection this state has now adjusted for.
        With `"continue_unthreaded"` a replay that finds the new thread lost as well stops threading, because the server
        may be unable to store the conversation."""
        continue_unthreaded = self.unsupported_request_behavior == "continue_unthreaded"
        replay_reason = _replay_reason(error)
        if replay_reason is not None and isinstance(self._thread, Continue):
            if replay_reason == "thread_not_found" and self._thread.replaces_lost_thread and continue_unthreaded:
                log.info(
                    "The server lost the thread again right after a replay; continuing without a thread: "
                    "previous_message_id=%s",
                    self.previous_message_id,
                )
                self.stop_threading()
            else:
                self._start_new_thread(replay_reason)
            return True
        unsupported = _unsupported_features(error)
        if unsupported is not None and self.threading and continue_unthreaded:
            log.info(
                "The server cannot thread this request; continuing without a thread: unsupported=%s",
                ",".join(unsupported),
            )
            self.stop_threading()
            return True
        return False

    def _start_new_thread(self, reason: NewThreadReason) -> None:
        """Stop continuing from the stored reply so the turn re-sends the full history under a new thread."""
        log.info(
            "Replaying the full message history under a new thread: reason=%s previous_message_id=%s",
            reason,
            self.previous_message_id,
        )
        self._thread = New(replaces_lost_thread=reason == "thread_not_found")

    def stop_threading(self) -> None:
        """Drop the `thread` field from this turn and every later one."""
        if self.threading:
            self._thread = "unthreaded"

    def record_reply(self, message: BetaMessage) -> None:
        """Record `message` as the turn's reply, for the next turn to continue from. A refused turn is not recorded, and
        the next turn starts a new thread, because the server may hold the refused turn. The server stores no turn that
        a fallback model wrote, so the turn after one starts a new thread as well."""
        if message.stop_reason == "refusal" and self._thread != "off":
            if self.previous_message_id is not None:
                self._start_new_thread("refusal")
            return
        self._store_turn(Reply(message))
        if isinstance(self._thread, Created):
            tools = self._thread.given_for_the_turn.get("tools")
            self.update(self._thread.given_for_the_turn, tools=None if tools == self._fields.get("tools") else tools)
        if isinstance(self._thread, (Created, Continue)):
            self._thread = Continue(
                previous_message_id=message.id,
                created_with=self._thread.created_with,
                replaces_lost_thread=isinstance(self._thread, Created) and self._thread.replaces_lost_thread,
            )
            if any(iteration.type == "fallback_message" for iteration in message.usage.iterations or ()):
                self._start_new_thread("fallback_message")
        self._adopt_container(message)

    def _adopt_container(self, reply: BetaMessage | None) -> None:
        """Continue in the container of `reply` on later turns, unless the thread already names one: container-bound
        server tools reject a follow-up request that omits the container the previous turn ran in."""
        if reply is None or reply.container is None:
            return
        container = self._fields.get("container")
        if container is None:
            self._fields["container"] = reply.container.id
        elif isinstance(container, dict) and not container.get("id"):
            self._fields["container"] = {**container, "id": reply.container.id}

    def record_partial_reply(self, snapshot: BetaMessage, completed_blocks: int) -> None:
        """Record a turn whose stream ended after `message_start` and before `message_stop`. The next turn starts a new
        thread because the server holds either the whole reply or none of it. `completed_blocks` is how many content
        blocks received `content_block_stop`."""
        if snapshot.stop_reason == "refusal" and self._thread != "off":
            self.record_reply(snapshot)
            return
        partial_reply = _partial_reply(snapshot, completed_blocks)
        self._store_turn(Reply(partial_reply, partial=True) if partial_reply is not None else None)
        if self.previous_message_id is not None:
            self._start_new_thread("stream_ended_before_message_stop")

    def _retry_partial_turn(self) -> None:
        """If nothing is staged and the history ends with a turn whose stream ended early (its messages, then its
        partial reply if any content arrived), drop the partial reply and stage those messages again so this turn
        re-sends them."""
        if self._staged or not self._stored:
            return
        tail = self._stored[-1]
        if isinstance(tail, Reply):
            if not tail.partial:
                return
            self._stored.pop()
        turn_start = self._answered_count
        self._staged = self._stored[turn_start:]
        del self._stored[turn_start:]
        log.info(
            "Re-sending the turn whose reply ended before `message_stop`: partial_reply_id=%s",
            tail.message.id if isinstance(tail, Reply) else None,
        )

    @property
    def _answered_count(self) -> int:
        """How many stored messages there are up to the last reply. Those after it were sent and never answered."""
        return max((i + 1 for i, entry in enumerate(self._stored) if isinstance(entry, Reply)), default=0)

    def _store_turn(self, reply: Reply | None) -> None:
        """Move what was staged into the stored history, followed by `reply` if there is one."""
        self._stored.extend(self._staged)
        self._staged = []
        if reply is not None:
            self._stored.append(reply)

    def create_arguments(self, overrides: TurnOverrides, *, stream: bool) -> CreateArguments:
        """Settle the `thread` field for this turn and build its `create()` keyword arguments except `stream`:
        request fields, betas, the delta or full history, and request options."""
        params = self._turn_params(overrides)
        thread = self._thread_for_turn(params, overrides)
        arguments: CreateArguments = {
            **params,
            # A `continue` sends only what the server lacks. With nothing staged after a `pause_turn` reply that is
            # nothing: the server holds the unfinished turn and resumes it from an empty `messages`.
            "messages": [
                *(() if self.previous_message_id is not None else self._stored_messages_to_send_again()),
                *(entry.param for entry in self._staged),
            ],
            **self._request_options(overrides, stream=stream),
        }
        betas = params.get("betas") or []
        if self.threading and MESSAGE_THREADS_BETA not in betas:
            arguments["betas"] = [*betas, MESSAGE_THREADS_BETA]
        if thread is not None:
            arguments["thread"] = thread
            if thread["type"] == "continue":
                for field in CREATE_ONLY_FIELDS:
                    arguments.pop(field, None)
        return arguments

    def _stored_messages_to_send_again(self) -> list[BetaMessageParam]:
        """The stored history as a turn that sends the whole history sends it: the messages up to the last reply go
        without the `cache_control` of their blocks, because each was set for the turn that sent it first, and a request
        takes only a few of them."""
        messages = [entry.param for entry in self._stored]
        if self._thread == "off":
            return messages
        answered = cast("list[BetaMessageParam]", without_cache_control(as_sent(messages[: self._answered_count])))
        return [*answered, *messages[self._answered_count :]]

    def check_next_turn(self, overrides: TurnOverrides) -> None:
        """Raise what the next turn with `overrides` would raise before it is sent."""
        if isinstance(self._thread, Continue):
            self._thread.check_create_only_fields(self._turn_params(overrides))

    def _thread_for_turn(self, params: ThreadFields, overrides: TurnOverrides) -> BetaMessageThreadParam | None:
        """The `thread` field of a turn that sends `params`, the thread's fields with `overrides`. The server takes the
        create-only fields from the thread on a `continue`, so a turn that changes one is refused, and a `create`
        records the ones it sends."""
        if self._thread == "off" or self._thread == "unthreaded":
            return None
        if isinstance(self._thread, Continue):
            self._thread.check_create_only_fields(params)
            return {"type": "continue", "previous_message_id": self._thread.previous_message_id}
        created_with = {f: params.get(f) for f in CREATE_ONLY_FIELDS if f in params}
        self._thread = Created(
            # A copy, so that an edit of them in place differs from it on the next turn.
            created_with=cast(TurnOverrides, as_sent(created_with)),
            given_for_the_turn=cast(TurnOverrides, {f: v for f, v in created_with.items() if f in overrides}),
            replaces_lost_thread=self._thread.replaces_lost_thread,
        )
        return {"type": "create"}

    def _turn_params(self, overrides: TurnOverrides) -> ThreadFields:
        """The thread's request fields with this turn's overrides, and the output format as `output_config`."""
        self._read_tools()
        params = override_fields(self._fields, overrides)
        if "tools" in overrides:
            # Read once: a `create` sends them and records them for the thread.
            params["tools"] = list(overrides["tools"])
        if self._output_format is not None:
            params["output_config"] = merge_output_config(
                params.get("output_config") or omit, self._output_format.format_param
            )
        return params

    def _request_options(self, overrides: TurnOverrides, *, stream: bool) -> RequestOptions:
        options = override_request_options(self.options, overrides)
        headers = options.get("extra_headers", {})
        if stream:
            headers = merge_headers(
                {STAINLESS_HELPER_METHOD_HEADER: HELPER_METHOD_STREAM, STAINLESS_STREAM_HELPER_HEADER: "beta.messages"},
                headers,
            )
        if self.threading:
            headers = _with_threads_beta(headers)
        options["extra_headers"] = merge_headers(headers, self._helper_headers)
        return options


class New:
    """The next turn is a `create` with the whole history. `replaces_lost_thread` says whether the server did not find
    the thread before it."""

    __slots__ = ("replaces_lost_thread",)

    def __init__(self, *, replaces_lost_thread: bool = False) -> None:
        self.replaces_lost_thread = replaces_lost_thread


class Created:
    """A `create` went out with the create-only fields `created_with`, of which `given_for_the_turn` are not the
    thread's own. The next turn is a `create` as well, unless the reply arrives first."""

    __slots__ = ("created_with", "given_for_the_turn", "replaces_lost_thread")

    def __init__(
        self, *, created_with: TurnOverrides, given_for_the_turn: TurnOverrides, replaces_lost_thread: bool
    ) -> None:
        self.created_with = created_with
        self.given_for_the_turn = given_for_the_turn
        self.replaces_lost_thread = replaces_lost_thread


class Continue:
    """The server holds the thread up to the reply `previous_message_id`, so the next turn is a `continue` with only
    what is staged. `replaces_lost_thread` says whether that is the first `continue` of a thread that replaced one the
    server did not find."""

    __slots__ = ("previous_message_id", "created_with", "replaces_lost_thread")

    def __init__(self, *, previous_message_id: str, created_with: TurnOverrides, replaces_lost_thread: bool) -> None:
        self.previous_message_id = previous_message_id
        self.created_with = created_with
        self.replaces_lost_thread = replaces_lost_thread

    def check_create_only_fields(self, params: ThreadFields) -> None:
        changed = [
            f"`{field}`" for field in CREATE_ONLY_FIELDS if as_sent(params.get(field)) != self.created_with.get(field)
        ]
        if changed:
            message = (
                f"Cannot change {' and '.join(changed)} on a thread: the server keeps the ones the thread was "
                "created with. To change them, start a new thread from `thread.params`."
            )
            if "`tools`" in changed:
                message += (
                    " To add or remove tools on this thread, send `tool_addition` or `tool_removal` blocks in a "
                    "`system` message."
                )
            raise AnthropicError(message)


ThreadPosition = Literal["off", "unthreaded"] | New | Created | Continue
"""Where the next turn stands on a server-side thread. `"off"` turns carry no `thread` field because the conversation
was never a thread, and `"unthreaded"` ones because the thread stopped threading. Both send the whole history."""


class Given:
    """A message of the history that the caller gave."""

    __slots__ = ("param",)

    def __init__(self, param: BetaMessageParam) -> None:
        self.param = param


class Reply:
    """A message of the history that the thread received from the server, and whether its stream ended before
    `message_stop`."""

    __slots__ = ("param", "message", "partial")

    def __init__(self, message: BetaMessage, *, partial: bool = False) -> None:
        self.param = _to_message_param(message)
        self.message = message
        self.partial = partial


Entry = Given | Reply


class Turn:
    """A turn in flight: the entries staged by the call that started it, and the history edits to apply once it
    ends."""

    def __init__(self, started_with: list[Entry]) -> None:
        self.started_with = started_with
        self.deferred_messages: list[BetaMessageParam | BetaMessage] = []
        self.replacement_history: list[BetaMessageParam] | None = None


class JSONOutputFormat(Generic[ResponseFormatT]):
    """An `output_format` class and the `output_config.format` param generated from its JSON schema."""

    def __init__(self, output_type: type[ResponseFormatT]) -> None:
        self.output_type = output_type
        self.format_param = to_json_output_format(output_type)


MESSAGE_THREADS_BETA = "message-threads-2026-08-12"

# Request fields the server takes from the thread on a `continue` and rejects if the request repeats them.
CREATE_ONLY_FIELDS: Sequence[Literal["system", "tools"]] = ("system", "tools")


def _with_threads_beta(headers: Mapping[str, str | Omit]) -> dict[str, str]:
    """`headers` with the threads beta appended to a caller-set `anthropic-beta` header, which would otherwise replace
    the one `create()` builds from `betas`."""
    caller_betas = build_headers(headers)[0].get("anthropic-beta")
    if caller_betas is None:
        return merge_headers(headers)
    return merge_headers(headers, {"anthropic-beta": _append_header_value(caller_betas, MESSAGE_THREADS_BETA)})


def _replay_reason(error: APIStatusError) -> ReplayErrorCode | None:
    """The `error_code` of a rejection that a full replay under a new thread recovers from, if it is one."""
    error_code = _error_details(error).get("error_code")
    return next((code for code in _REPLAY_ERROR_CODES if code == error_code), None)


ReplayErrorCode = Literal["thread_not_found", "thread_already_continued", "thread_continue_in_flight"]

_REPLAY_ERROR_CODES: tuple[ReplayErrorCode, ...] = get_args(ReplayErrorCode)

NewThreadReason = ReplayErrorCode | Literal["stream_ended_before_message_stop", "refusal", "fallback_message"]


def _unsupported_features(error: APIStatusError) -> list[str] | None:
    """The `unsupported` values of a `thread_unsupported_request` rejection, none if it lists none, or `None` for any
    other error."""
    details = _error_details(error)
    if details.get("error_code") != "thread_unsupported_request":
        return None
    unsupported = details.get("unsupported")
    return [str(feature) for feature in unsupported] if is_list(unsupported) else []


def _error_details(error: APIStatusError) -> dict[object, object]:
    """The `error.details` object of the response body, or an empty one when the body has none."""
    body = error.body
    error_body = body.get("error") if is_dict(body) else None
    details = error_body.get("details") if is_dict(error_body) else None
    return details if is_dict(details) else {}


def _partial_reply(snapshot: BetaMessage, completed_blocks: int) -> BetaMessage | None:
    """The part of a streamed reply worth keeping when the stream ended early, or `None` if nothing is. An unfinished
    block stays only if it is `text`, because the `input` or `signature` of any other is incomplete."""
    content = list(snapshot.content[:completed_blocks])
    unfinished = snapshot.content[completed_blocks] if completed_blocks < len(snapshot.content) else None
    if unfinished is not None and unfinished.type == "text" and unfinished.text:
        content.append(unfinished)
    if not content:
        return None
    partial_reply = model_copy(snapshot)
    partial_reply.content = content
    return partial_reply


def same_messages(a: Sequence[BetaMessageParam], b: Sequence[BetaMessageParam]) -> bool:
    return len(a) == len(b) and all(map(same_message, a, b))


def same_message(a: BetaMessageParam, b: BetaMessageParam) -> bool:
    """Whether `a` and `b` are sent as the same message. A recorded reply holds its content blocks as models, and the
    caller gives the same blocks back as dicts or as the blocks of the parsed reply, which compare unequal to them."""
    return a is b or (a["role"] == b["role"] and as_sent(a) == as_sent(b))


def as_sent(value: object) -> object:
    """A copy of `value` with every model in it dumped as a request body sends it."""
    if isinstance(value, pydantic.BaseModel):
        return openapi_model_dump(value)
    if isinstance(value, Mapping):
        return {key: as_sent(item) for key, item in cast("Mapping[object, object]", value).items()}
    if isinstance(value, Collection) and not isinstance(value, (str, bytes, bytearray)):
        return [as_sent(item) for item in cast("Collection[object]", value)]
    return value


def without_cache_control(value: object) -> object:
    """A copy of `value`, which `as_sent()` returned, without the `cache_control` of any block in it, however deep. Only
    the keys that hold blocks are followed, so free-form data such as a tool's `input` stays as it is."""
    if is_dict(value):
        return {
            key: without_cache_control(item) if key in KEYS_THAT_HOLD_BLOCKS else item
            for key, item in value.items()
            if key != "cache_control"
        }
    if is_list(value):
        return [without_cache_control(item) for item in value]
    return value


KEYS_THAT_HOLD_BLOCKS = ("content", "source", "tool", "definition", "tool_references")


def _split_tools(
    tools: Iterable[BetaToolUnionParam | RunnableToolT],
) -> tuple[dict[str, RunnableToolT], list[BetaToolUnionParam]]:
    runnable_tools: list[RunnableToolT] = []
    definitions: list[BetaToolUnionParam] = []
    for tool in tools:
        if isinstance(tool, RUNNABLE_TOOL_TYPES):
            runnable_tools.append(tool)
            definitions.append(tool.to_dict())
        else:
            definitions.append(tool)
    return tool_registry(runnable_tools), definitions


RUNNABLE_TOOL_TYPES = (BetaFunctionTool, BetaBuiltinFunctionTool, BetaAsyncFunctionTool, BetaAsyncBuiltinFunctionTool)


def _to_message_param(message: BetaMessageParam | BetaMessage) -> BetaMessageParam:
    if isinstance(message, BetaMessage):
        return {"role": message.role, "content": message.content}
    return message
