from __future__ import annotations

import inspect
import logging
import warnings
from abc import ABC, abstractmethod
from copy import copy
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Generic,
    TypeVar,
    Callable,
    Iterator,
    Coroutine,
    AsyncIterator,
    cast,
    overload,
)
from contextlib import (
    ExitStack,
    AsyncExitStack,
    AbstractContextManager,
    aclosing,
    contextmanager,
    asynccontextmanager,
)
from collections.abc import Iterable, Sequence, Generator, AsyncGenerator
from typing_extensions import Literal, TypedDict, override

import httpx2
from opentelemetry.trace import Span

from ..._types import Body, Query, Headers, NotGiven, omit
from ..._utils import is_list, is_given, is_mapping, consume_sync_iterator, consume_async_iterator
from .._tracing import (
    ToolRun,
    tool_use_span,
    as_current_span,
    end_tool_runner_span,
    set_tool_runner_status,
    start_tool_runner_span,
)
from ..streaming import BetaMessageStream, BetaAsyncMessageStream, ParsedBetaMessageStreamEvent
from ...types.beta import (
    BetaMessage,
    BetaMessageParam,
    BetaToolUseBlock,
    BetaToolUnionParam,
    BetaUserMessageParam,
    BetaRequestToolRemovalBlockParam,
    BetaRequestToolAdditionBlockParam,
)
from ._tool_params import to_tool_params
from ..._base_client import merge_headers
from ._tool_dispatch import (
    tool_family,
    index_runnables,
    tool_error_content,
    tool_result_content,
    available_tool_names,
    partition_sync_tools,
    partition_async_tools,
)
from ._beta_functions import ToolError, BetaRunnableTool, BetaAsyncRunnableTool
from ..threads._params import ThreadFields, RunnableToolT, TurnOverrides, turn_overrides, reject_thread_param
from ._toolsets._errors import ToolsetsFixedError, ToolsetContractError
from .._parse._transform import validate_output_config_conflict
from .._stainless_helpers import helper_header, stainless_helper_header
from ._toolsets._runnable import (
    TOOLSET_CLASSES,
    BetaRunnableToolset,
    BetaAnyRunnableToolset,
    BetaAsyncRunnableToolset,
    not_executed_result,
    toolset_result_block,
)
from ._toolsets._sanitize import quoted_name
from ..threads._beta_threads import BetaMessageThread, BetaAsyncMessageThread
from ..threads._thread_state import same_message
from ...types.beta.beta_stop_reason import BetaStopReason
from ...types.beta.parsed_beta_message import ResponseFormatT, ParsedBetaMessage, ParsedBetaContentBlock
from ...types.beta.message_create_params import ParseMessageCreateParamsBase
from ...types.beta.beta_output_config_param import BetaOutputConfigParam
from ...types.beta.beta_compaction_config_param import BetaCompactionConfigParam
from ...types.beta.beta_tool_result_block_param import BetaToolResultBlockParam

if TYPE_CHECKING:
    from types import AsyncGeneratorType

    from ..._client import Anthropic, AsyncAnthropic


ThreadT = TypeVar("ThreadT", bound=BetaMessageThread[Any] | BetaAsyncMessageThread[Any])
AnyToolsetT = TypeVar("AnyToolsetT", bound=BetaAnyRunnableToolset)
RunnerItemT = TypeVar("RunnerItemT")


log = logging.getLogger(__name__)


_Step = Literal["run_tools", "resume", "stop"]

# Every stop reason maps to exactly one step. The runner tests assert this mapping
# covers `BetaStopReason`, so a newly generated value must be classified here.
_STOP_REASON_STEPS: dict[BetaStopReason, _Step] = {
    "tool_use": "run_tools",
    "pause_turn": "resume",
    # pause_after_compaction hands the turn back before the model answers; the next request continues it.
    "compaction": "resume",
    "end_turn": "stop",
    "stop_sequence": "stop",
    "max_tokens": "stop",
    "model_context_window_exceeded": "stop",
    "refusal": "stop",
}


def _determine_next_step_from_stop_reason(stop_reason: BetaStopReason | None) -> _Step:
    """Decide how the runner loop treats a finished assistant turn.

    - `run_tools`: run the turn's client tool calls, append their results and continue; stop if there are none.
    - `resume`: the turn is not finished; send it back unchanged, running no tool calls, so the server continues it.
    - `stop`: terminal; the turn is the final message and its tool_use blocks must not be executed.
    """
    if stop_reason is not None and stop_reason in _STOP_REASON_STEPS:
        return _STOP_REASON_STEPS[stop_reason]
    # Absent and unknown (forward-compatible) values stop like any other finished turn.
    return "stop"


def _reject_compaction_param(params: ParseMessageCreateParamsBase[Any]) -> None:
    compaction = params.get("compaction")
    if compaction is not None and is_given(compaction):
        raise ValueError(
            "`compaction` cannot be set on a tool runner: every request in the loop would compact again. "
            "Call `runner.compact_before_next_turn()` when the conversation should be compacted instead."
        )


def _without_format(output_config: BetaOutputConfigParam) -> Dict[str, Any]:
    return {key: value for key, value in output_config.items() if key != "format"}


def _without_compaction_incompatible_params(params: ThreadFields) -> Dict[str, Any]:
    """A compaction request returns only the compaction block, never a reply, so the API rejects the
    params that only shape a reply. The runner's later requests keep them.
    """
    trimmed: Dict[str, Any] = {**params}
    for name in ("context_management", "stop_sequences", "output_format"):
        trimmed.pop(name, None)
    tool_choice = params.get("tool_choice")
    if is_given(tool_choice) and tool_choice and tool_choice["type"] in ("any", "tool"):
        del trimmed["tool_choice"]
    output_config = params.get("output_config")
    if is_given(output_config) and output_config:
        trimmed["output_config"] = _without_format(output_config)
    fallbacks = params.get("fallbacks")
    if is_given(fallbacks) and fallbacks and not isinstance(fallbacks, str):
        trimmed["fallbacks"] = [
            {**fallback, "output_config": _without_format(fallback_output_config)}
            if (fallback_output_config := fallback.get("output_config"))
            else fallback
            for fallback in fallbacks
        ]
    return trimmed


class RequestOptions(TypedDict, total=False):
    extra_headers: Headers | None
    extra_query: Query | None
    extra_body: Body | None
    timeout: float | httpx2.Timeout | None | NotGiven


class BaseToolRunner(Generic[ThreadT, RunnableToolT, AnyToolsetT, ResponseFormatT]):
    def __init__(
        self,
        *,
        thread: ThreadT,
        options: TurnOverrides | RequestOptions,
        tools: Iterable[RunnableToolT | AnyToolsetT],
        max_iterations: int | None,
    ) -> None:
        self._thread = thread
        self._messages: Sequence[BetaMessageParam] | None = None
        """While a reply is handled, the history that `set_messages_params()` and `append_messages()` read and change:
        what the request sent, without the reply. The thread takes it over once the loop body is done with the reply.
        At any other time it is `None`, and both methods work on the thread's history."""

        self._sent_messages: Sequence[BetaMessageParam] = ()
        """The history the last request went out with."""

        self._messages_modified = False
        """Whether `append_messages()` was called while the reply was handled. The caller then owns the history of the
        turn, and the runner adds neither the reply nor its tool results."""

        self._appended_to_thread = False
        """Whether the thread itself was given messages while the last reply was handled."""

        _reject_compaction_param(self._params)
        self._options = turn_overrides(**options)
        tools_by_name, self._toolsets = index_runnables(tools)
        self._tool_overrides: dict[str, RunnableToolT | None] = {**tools_by_name}
        """Which tool runs under a name where that differs from the thread's tools: a tool the runner was given apart
        from them, the tool `add_tools()` put under it, the tool it had when `set_messages_params()` gave its
        definition, or `None` once the name was removed. The thread's own tools are left alone, so the `tools` param
        stays as sent."""

        self._helper_headers = merge_headers(
            helper_header("BetaToolRunner"),
            stainless_helper_header(
                tools=[*self._runnable_tools().values(), *self._toolsets_by_family.values()],
                messages=thread.messages,
            ),
        )
        self._cached_tool_call_response: BetaUserMessageParam | None = None
        self._max_iterations = max_iterations
        self._iteration_count = 0
        self._closed = False
        """Whether the application closed the runner. A loop that is working when it does stops before its next
        request."""

        # The compaction request goes out on a fork (`_take_compaction_thread()`), because a turn on the thread itself
        # can neither leave out one of the thread's fields nor send the whole history while the server holds a part.
        self._pending_compaction: BetaCompactionConfigParam | None = None
        self._messages_being_compacted: list[BetaMessageParam] | None = None
        self._pending_tool_changes: list[BetaRequestToolAdditionBlockParam | BetaRequestToolRemovalBlockParam] = []
        self._eager_tool_calls: EagerToolCalls | None = None
        """The tool calls of the streamed reply being handled. It is `None` without `run_tools_eagerly`."""

        self._tool_runner_span: Span | None = None
        """The span of the run, which a tool that runs while the application reads a reply is a child of too."""

        self._running_eager_tool = False
        """Whether a tool is running inside a read of a streamed reply. The loop is then suspended, and closing it
        would close the reply under that read, so a close from such a tool only stops the loop at its next step."""

    @property
    def _params(self) -> ParseMessageCreateParamsBase[ResponseFormatT]:
        """The thread's `params` that a request takes: the request fields, with `tools` as the definitions sent, and
        the whole history, `messages` included. The reply being handled is not part of it."""
        thread_params = self._thread.params
        params = {**thread_params}
        del params["unsupported_request_behavior"]
        if "tools" in thread_params:
            params["tools"] = to_tool_params(thread_params["tools"])
        if self._messages is not None:
            params["messages"] = list(self._messages)
        return cast(ParseMessageCreateParamsBase[ResponseFormatT], params)

    @property
    def _client(self) -> Anthropic | AsyncAnthropic:
        """The thread's client. It sends the runner's requests, and its options say whether the run has spans."""
        return self._thread._client

    def _start_tool_runner_span(self, client: Anthropic | AsyncAnthropic) -> Span | None:
        """Starts the `anthropic.messages.tool_runner` span of one run, or returns `None` when tracing is off."""
        self._tool_runner_span = start_tool_runner_span(client, model=self._params["model"], params=self._params)
        return self._tool_runner_span

    def _tool_use_span(
        self, client: Anthropic | AsyncAnthropic, tool: object, tool_use: BetaToolUseBlock
    ) -> AbstractContextManager[ToolRun]:
        """The span of one run of `tool` for the call `tool_use`. The result the runner sends back, an error result
        too, is made inside it."""
        return tool_use_span(
            client,
            tool,
            tool_use_id=tool_use.id,
            tool_name=tool_use.name,
            input=tool_use.input,
            toolset_name=tool_use.toolset_name,
        )

    def _turn_options(self, thread: ThreadT) -> TurnOverrides:
        """The runner's request options for a turn on `thread`. A turn's `extra_headers` replace the thread's, so the
        runner's helper tags go on top of the headers the turn sends without them."""
        headers = self._options.get("extra_headers", thread._state.options.get("extra_headers", {}))
        return {**self._options, "extra_headers": merge_headers(self._helper_headers, headers)}

    def set_messages_params(
        self,
        params: ParseMessageCreateParamsBase[ResponseFormatT]
        | Callable[[ParseMessageCreateParamsBase[ResponseFormatT]], ParseMessageCreateParamsBase[ResponseFormatT]],
    ) -> None:
        """
        Update the parameters for the next API call. This invalidates any cached tool responses. With
        `run_tools_eagerly`, a tool call of the reply that has run doesn't run again.

        The new params replace the old ones, so a field they leave out is no longer sent, except `betas`,
        `user_profile_id` and `workspace_id`, which stay as they are. `system` and the `tools` sent cannot change during
        a run: use `add_tools()` and `remove_tools()`, or create the runner with `thread=False`. A function tool or
        toolset taken out of `tools` is no longer run, and a function tool added to them is never run. Params without
        `tools` send none and leave what is run as it is.

        Args:
            params (ParsedMessageCreateParamsBase[ResponseFormatT] | Callable): Either new parameters or a function to mutate existing parameters
        """
        current_params = self._params
        if callable(params):
            params = params(current_params)
        kept = {k: v for k, v in current_params.items() if k in ("betas", "user_profile_id", "workspace_id")}
        params = cast("ParseMessageCreateParamsBase[ResponseFormatT]", {**kept, **params})
        _reject_compaction_param(params)
        reject_thread_param(params.get("thread"))
        if self._messages_being_compacted is not None and list(params["messages"]) != list(self._thread.messages):
            raise ValueError(
                "Message params can't be changed while the conversation is being compacted, because the compaction "
                "response replaces them. Make the change on the next iteration."
            )
        if self._pending_compaction is not None or self._messages_being_compacted is not None:
            self._check_can_compact(params)
        if self._messages is not None:
            self._messages = list(params["messages"])
            params = {**params, "messages": self._thread.messages}
        if "tools" in params and params["tools"] == self._params.get("tools"):
            # Given back as handed out, so the thread keeps its own, for whatever uses it after the runner.
            own_tools = self._thread.params.get("tools")
            params = cast("ParseMessageCreateParamsBase[ResponseFormatT]", {**params, "tools": own_tools})
        runnable_tools, toolsets, declared = self._runnable_tools(), self._toolsets_by_family, self._declared_tools()
        self._thread._state.set_params(params)
        withdrawn = declared - self._declared_tools() if "tools" in self._params else set[str]()
        # A definition keeps the tool that ran under its name, and a name the new `tools` leave out stops running.
        self._tool_overrides = {
            **dict.fromkeys(self._thread._state.runnable_tools),
            **self._tool_overrides,
            **runnable_tools,
            **dict.fromkeys(withdrawn),
        }
        self._toolsets = {family: toolset for family, toolset in toolsets.items() if family not in withdrawn}

    def append_messages(self, *messages: BetaMessageParam | ParsedBetaMessage[ResponseFormatT]) -> None:
        """Add one or more messages to the conversation history.

        This invalidates the cached tool response, i.e. if tools were already called, then they will
        be called again on the next loop iteration. With `run_tools_eagerly`, a tool call of the reply
        that has run doesn't run again.
        """
        if self._messages_being_compacted is not None:
            raise ValueError(
                "Message params can't be changed while the conversation is being compacted, because the compaction "
                "response replaces them. Make the change on the next iteration."
            )
        if self._messages is None:
            self._thread.append(*messages)
        else:
            self._messages = [
                *self._messages,
                *(message.to_param() if isinstance(message, BetaMessage) else message for message in messages),
            ]
            self._messages_modified = True
        self._cached_tool_call_response = None

    def compact_before_next_turn(self, compaction: BetaCompactionConfigParam | None = None) -> None:
        """Compact the conversation before the model's next turn.

        This only schedules the compaction. Once the current turn has finished, including
        any tool calls, the runner requests a summary and replaces the message history with
        the compaction response the API returns. That response is yielded like any other
        message, with `stop_reason == "compaction"`, and the runner then carries on.

        Calling this again before the compaction runs replaces the pending one. Requires
        the `compact-2026-09-04` beta.

        Args:
            compaction: The compaction config to send. Defaults to `{"type": "summarize"}`.
        """
        if self._messages_being_compacted is not None:
            return
        self._check_can_compact(self._params)
        self._pending_compaction = {"type": "summarize"} if compaction is None else compaction

    def _check_can_compact(self, params: ParseMessageCreateParamsBase[ResponseFormatT]) -> None:
        # The compaction request is sent without `context_management`, so the API can't reject this
        # combination there: it would run and bill the compaction, then reject the next request, where
        # the compaction response and the compaction edit meet.
        context_management = params.get("context_management")
        edits = context_management.get("edits") if is_given(context_management) and context_management else None
        if any(edit["type"].startswith("compact_") for edit in edits or ()):
            raise ValueError(
                "`compact_before_next_turn()` can't be used while `context_management` has a compaction edit, "
                "because the API doesn't accept a compaction block together with one. Remove the edit first."
            )

    def _take_compaction_thread(self, compaction: BetaCompactionConfigParam) -> ThreadT:
        """A fork of the thread that sends the compaction request: the whole history and the thread's fields plus
        `compaction`, minus what `_without_compaction_incompatible_params()` removes. Starts a new thread when
        threading is on."""
        self._check_can_compact(self._params)
        thread = cast(ThreadT, self._thread.fork())
        thread.update(compaction=compaction)
        # `_output_format` is added to `output_config` only when a turn is sent, so the fork drops it separately.
        thread._state._fields = cast(ThreadFields, _without_compaction_incompatible_params(thread._state._fields))
        thread._state._output_format = None
        self._pending_compaction = None
        self._messages_being_compacted = list(self._thread.messages)
        return thread

    def _prepare_compaction_after_final_turn(
        self, message: ParsedBetaMessage[ResponseFormatT]
    ) -> BetaCompactionConfigParam | None:
        compaction = self._pending_compaction
        if (
            compaction is not None
            and not self._messages_modified
            and not self._appended_to_thread
            and any(block.type == "tool_use" for block in message.content)
        ):
            # A turn that was cut short can end with tool calls that are never run, and the API
            # can't compact a conversation whose last turn has an unanswered tool call.
            log.warning(
                "The pending compaction was skipped because the last turn (stop_reason=%r) ended with tool calls "
                "whose results were not sent. Call `compact_before_next_turn()` again if you continue the "
                "conversation.",
                message.stop_reason,
            )
            self._pending_compaction = None
            return None
        return compaction

    def _register_compaction_response(
        self, thread: ThreadT, message: ParsedBetaMessage[ResponseFormatT], compacted_count: int
    ) -> bool:
        if not thread._state.threading:
            # The API could not thread the compaction request, and would reject the next request as well.
            self._thread._state.stop_threading()
        if not any(block.type == "compaction" and block.content for block in message.content):
            log.warning("Compaction produced no summary; keeping the conversation as it is.")
            return False
        # Recorded in the overrides, which outlive the history: a removal the caller wrote into it is known only from it.
        for name in self._runnable_tools().keys() - self._available_tool_names():
            self._tool_overrides[name] = None
        # The thread never received the response (the fork did), so it is staged like any replaced history. Messages
        # appended since the request went out are not in the summary, so they follow it, except the response itself:
        # appending a reply the runner yielded adds nothing.
        response = message.to_param()
        appended = self._thread.messages[compacted_count:]
        self._thread._state.set_messages([response, *(m for m in appended if not same_message(m, response))])
        return True

    def _hand_over_messages(self, reply: ParsedBetaMessage[ResponseFormatT]) -> None:
        """Give the thread the history as the loop body left it. `reply` follows it unless `append_messages()` was
        called, which leaves the history to the caller. A history that extends what the server holds continues the
        thread, and any other starts a new one."""
        # The thread already holds the reply. Anything staged after it was added during the yield.
        self._appended_to_thread = self._thread._state.has_staged_messages
        messages, self._messages = self._messages, None
        if messages is None or messages is self._sent_messages:
            return
        reply_param = reply.to_param()
        if not self._messages_modified:
            messages = [*messages, reply_param]
        added_to_thread = self._thread.messages[len(self._sent_messages) :]
        self._thread._state.set_messages([*messages, *(m for m in added_to_thread if not same_message(m, reply_param))])

    def _append_tool_results(self, results: BetaMessageParam) -> None:
        """Add `results` right after the reply, where the API takes them, ahead of messages added to the thread while
        it was handled."""
        messages = list(self._thread.messages)
        index = max(i for i, message in enumerate(messages) if message["role"] == "assistant") + 1
        self._thread._state.set_messages([*messages[:index], results, *messages[index:]])

    def add_tools(self, *tools: RunnableToolT | BetaToolUnionParam) -> None:
        """Give the model more tools without changing the `tools` param, which would miss the prompt cache.

        The definitions are sent in `tool_addition` blocks with the next request. A function tool is run straight
        away, in place of any tool of the same name, even for a call already in the message being handled. A call
        that ran while the reply streamed keeps its result. A raw definition is for server tools, such as web
        search: the tool runner never runs it, and it stops running a function tool of the same name. Requires the
        `inline-tools-2026-09-15` beta. Passing a runnable toolset, a raw definition of a toolset the runner has, or a
        tool named like one of its toolsets raises `ToolsetContractError` and adds nothing: a runner's toolsets are
        fixed when it is created, and the API rejects another tool with a toolset's name.

        Args:
            *tools: Function tools, such as `@beta_tool` functions, or raw tool definitions.
        """
        for tool in tools:
            if isinstance(tool, TOOLSET_CLASSES):
                raise ToolsetsFixedError("add", tool.toolset_name)
            # The API reads a definition of one of the runner's toolset families as replacing that toolset.
            if isinstance(tool, dict) and (family := tool_family(tool)) in self._toolsets_by_family:
                raise ToolsetsFixedError("replace", family)
            name = tool.get("name") if isinstance(tool, dict) else tool.name
            if isinstance(name, str) and name in self._toolsets_by_family:
                raise ToolsetContractError(
                    f"add_tools() can't add a tool named '{quoted_name(name)}': the runner's {quoted_name(name)} "
                    "toolset has that name; give the tool another name"
                )
        for tool in tools:
            if isinstance(tool, dict):
                definition: BetaToolUnionParam = copy(tool)
                name = tool.get("name")
                if isinstance(name, str):
                    self._tool_overrides[name] = None
            else:
                definition = tool.to_dict()
                self._tool_overrides[tool.name] = tool
            self._pending_tool_changes.append(
                {"type": "tool_addition", "tool": {"type": "tool_definition", "definition": definition}}
            )

    def remove_tools(self, *tools: RunnableToolT | str) -> None:
        """Take tools away from the model without changing the `tools` param, which would miss the prompt cache.

        The tools stop being run at once, and the model is told in `tool_removal` blocks with the next request. A
        call that ran while the reply streamed keeps its result. Requires the `inline-tools-2026-09-15` beta. Passing
        a toolset, or the name of one of the runner's toolsets, raises `ToolsetContractError` and removes nothing.

        Args:
            *tools: The tools to remove, or their names.
        """
        for tool in tools:
            if isinstance(tool, TOOLSET_CLASSES):
                raise ToolsetsFixedError("remove", tool.toolset_name)
            name = tool if isinstance(tool, str) else tool.name
            if name in self._toolsets_by_family:
                raise ToolsetsFixedError("remove", name)
        for tool in tools:
            name = tool if isinstance(tool, str) else tool.name
            self._tool_overrides[name] = None
            self._pending_tool_changes.append(
                {"type": "tool_removal", "tool": {"type": "tool_reference", "name": name}}
            )

    def _runnable_tools(self) -> dict[str, RunnableToolT]:
        """The tools the runner runs, by name: the thread's runnable tools with the overrides applied."""
        tools = cast("dict[str, RunnableToolT]", dict(self._thread._state.runnable_tools))
        for name, tool in self._tool_overrides.items():
            if tool is None:
                tools.pop(name, None)
            else:
                tools[name] = tool
        return tools

    def _declared_tools(self) -> set[str]:
        """The names of the tools in the `tools` param, and the families of its toolsets, which have no name."""
        return {tool.get("name") or tool_family(tool) for tool in self._params.get("tools", ())}

    def _send_pending_tool_changes(self, hold: bool) -> None:
        # A turn that stopped on `pause_turn` is sent back to be continued, so it has to stay last.
        if hold or not self._pending_tool_changes:
            return
        # Not `append_messages()`, which also drops the cached tool call response.
        self._thread._state.append([{"role": "system", "content": self._pending_tool_changes}])
        self._pending_tool_changes = []

    def _should_stop(self) -> bool:
        if self._closed:
            return True
        if self._max_iterations is not None and self._iteration_count >= self._max_iterations:
            return True
        return False

    def _available_tool_names(self) -> set[str]:
        """The tool names currently available, after applying any
        mid-conversation `tool_removal` / `tool_addition` blocks.

        Removal is only a hint to the model, which can still emit a `tool_use`
        for a withdrawn tool; a name absent from this set routes that call down
        the same unknown-tool path as a tool that was never declared.

        Toolsets are not in this set: a `tool_reference` names a tool,
        not a toolset, and member names are not reserved, so a toolset stays
        available for as long as it is registered.
        """
        # Changes made since the last request are not in the history yet.
        pending: BetaMessageParam = {"role": "system", "content": self._pending_tool_changes}
        messages = self._thread.messages if self._messages is None else self._messages
        return available_tool_names([*messages, pending], self._runnable_tools())

    def _toolset_for(self, tool_use: BetaToolUseBlock) -> AnyToolsetT | None:
        assert tool_use.toolset_name is not None
        toolset = self._toolsets_by_family.get(tool_use.toolset_name)
        if toolset is None:
            # both names are model output: folded to one bounded line before they reach a log
            warnings.warn(
                f"Toolset '{quoted_name(tool_use.toolset_name)}' (member '{quoted_name(tool_use.name)}') not found in tool runner. "
                f"Registered toolsets: {list(self._toolsets_by_family.keys())}. "
                f"If using a raw toolset definition, handle the tool call manually and use `append_messages()` to add the result. "
                f"Otherwise, pass a `BetaRunnableToolset` / `BetaAsyncRunnableToolset` instance.",
                UserWarning,
                stacklevel=5,  # points the warning at the user's call into generate_tool_call_response
            )
        return toolset

    @staticmethod
    def _toolset_not_found_result(tool_use: BetaToolUseBlock) -> BetaToolResultBlockParam:
        return toolset_result_block(
            tool_use,
            f"Error: Toolset '{quoted_name(tool_use.toolset_name)}' member '{quoted_name(tool_use.name)}' not found",
            is_error=True,
        )

    @property
    def _toolsets_by_family(self) -> dict[str, AnyToolsetT]:
        """The runnable toolsets among the thread's tools, read again on each access, and the ones the runner was given
        apart from them, by family (`toolset_name`). The `tools[]` entry of a toolset has no `name`, so toolsets are
        kept apart from `_runnable_tools()` and never shadow a same-named tool."""
        tools: list[object] = list(self._thread._state._tools or [])
        return {
            **{tool.toolset_name: cast(AnyToolsetT, tool) for tool in tools if isinstance(tool, TOOLSET_CLASSES)},
            **self._toolsets,
        }


class BaseSyncToolRunner(
    BaseToolRunner[BetaMessageThread[ResponseFormatT], BetaRunnableTool, BetaRunnableToolset, ResponseFormatT],
    Generic[RunnerItemT, ResponseFormatT],
    ABC,
):
    def __init__(
        self,
        *,
        thread: BetaMessageThread[ResponseFormatT] | None,
        params: ParseMessageCreateParamsBase[ResponseFormatT] | None,
        options: TurnOverrides | RequestOptions,
        tools: Iterable[BetaRunnableTool | BetaRunnableToolset] | None,
        client: Anthropic | None,
        max_iterations: int | None,
    ) -> None:
        if thread is None and params is not None and tools is not None and client is not None:
            validate_output_config_conflict(params.get("output_config", omit), params.get("output_format"))
            tools = list(tools)
            partition_sync_tools(tools)
            thread = BetaMessageThread[ResponseFormatT]._for_tool_runner(client, params)
        elif thread is None or params is not None or tools is not None or client is not None:
            raise constructor_arguments_error(thread=thread, params=params, tools=tools, client=client)

        super().__init__(thread=thread, options=options, tools=tools or (), max_iterations=max_iterations)
        self._iterator = self.__run__()
        self._last_message: (
            Callable[[], ParsedBetaMessage[ResponseFormatT]] | ParsedBetaMessage[ResponseFormatT] | None
        ) = None

    def __next__(self) -> RunnerItemT:
        return self._iterator.__next__()

    def __iter__(self) -> Iterator[RunnerItemT]:
        for item in self._iterator:
            yield item

    def close(self) -> None:
        """Stop the runner early and end its span. Use it when you won't resume the runner with `until_done()`.

        Iterating a closed runner yields nothing. Closing a runner that is done has no effect.
        """
        self._closed = True
        # A loop that is working, such as one whose tool calls this, cannot be closed from inside. It stops at its next
        # step, as does one whose tool runs while the application reads a reply.
        if not self._running_eager_tool and inspect.getgeneratorstate(self._iterator) != inspect.GEN_RUNNING:
            self._iterator.close()

    @abstractmethod
    @contextmanager
    def _handle_request(self, thread: BetaMessageThread[ResponseFormatT]) -> Iterator[RunnerItemT]:
        raise NotImplementedError()
        yield  # type: ignore[unreachable]

    def _compact(self, compaction: BetaCompactionConfigParam) -> Iterator[RunnerItemT]:
        last_message = self._last_message
        thread = self._take_compaction_thread(compaction)
        compacted_count = len(self._thread.messages)
        try:
            with self._handle_request(thread) as item:
                yield item
                message = self._get_last_message()
                assert message is not None
        finally:
            self._messages_being_compacted = None
        if not self._register_compaction_response(thread, message, compacted_count):
            # `until_done()` still returns the turn the run ended on.
            self._last_message = last_message

    def _compact_after_final_turn(self, message: ParsedBetaMessage[ResponseFormatT]) -> Iterator[RunnerItemT]:
        compaction = self._prepare_compaction_after_final_turn(message)
        if compaction is not None:
            yield from self._compact(compaction)

    def __run__(self) -> Generator[RunnerItemT, None, None]:
        tool_runner_span = self._start_tool_runner_span(self._client)
        steps = self._steps()
        try:
            try:
                while True:
                    # The runner's own code runs with its span current. Each step enters the span again, because the
                    # application resumes the runner from its own context.
                    with as_current_span(tool_runner_span):
                        try:
                            item = next(steps)
                        except StopIteration:
                            break
                    # Outside the span, so that the application's code between iterations keeps its own context.
                    yield item
                # A closed runner stops here too, and closing leaves the status unset.
                if not self._closed:
                    set_tool_runner_status(tool_runner_span)
            except BaseException as err:
                # Closing a suspended runner raises `GeneratorExit` here, which leaves the status unset.
                set_tool_runner_status(tool_runner_span, err)
                raise
            finally:
                # Closing the request is the runner's code too, so it runs with the span current.
                with as_current_span(tool_runner_span):
                    steps.close()
        finally:
            end_tool_runner_span(tool_runner_span)

    def _steps(self) -> Generator[RunnerItemT, None, None]:
        """The runner's loop. `__run__` drives it, one step for each item."""
        stop_reason: BetaStopReason | None = None
        while not self._should_stop():
            self._send_pending_tool_changes(hold=stop_reason == "pause_turn")
            # The API can't compact a conversation that ends mid-turn, so a paused turn is resumed first.
            turn_paused = _determine_next_step_from_stop_reason(stop_reason) == "resume"
            compaction = None if turn_paused else self._pending_compaction
            if compaction is not None:
                yield from self._compact(compaction)
                continue

            self._sent_messages = self._messages = self._thread.messages
            with self._handle_request(self._thread) as item:
                yield item
                message = self._get_last_message()
                assert message is not None

            stop_reason = message.stop_reason
            next_step = _determine_next_step_from_stop_reason(stop_reason)
            if next_step != "stop":
                # No tool runs for a turn the thread refuses to send. A history the caller rewrote starts a new thread,
                # which takes any fields, so this comes first.
                self._thread._state.check_next_turn(self._options)

            self._hand_over_messages(message)
            self._iteration_count += 1

            if next_step == "stop":
                log.debug("Turn ended with stop_reason %r, exiting from tool runner loop.", message.stop_reason)
                yield from self._compact_after_final_turn(message)
                break

            # On "resume" there is nothing to append: the history already holds the unfinished reply, or is the caller's.
            if next_step == "run_tools":
                response = self.generate_tool_call_response()
                if response is None and not self._appended_to_thread:
                    log.debug("Tool call was not requested, exiting from tool runner loop.")
                    yield from self._compact_after_final_turn(message)
                    break
                if response is not None and not self._messages_modified:
                    self._append_tool_results(response)

            self._messages_modified = False
            self._cached_tool_call_response = None

    def until_done(self) -> ParsedBetaMessage[ResponseFormatT]:
        """
        Consumes the tool runner stream and returns the last message if it has not been consumed yet.
        If it has, it simply returns the last message.
        """
        consume_sync_iterator(self)
        last_message = self._get_last_message()
        assert last_message is not None
        return last_message

    def generate_tool_call_response(self) -> BetaUserMessageParam | None:
        """Generate a MessageParam by calling tool functions with any tool use blocks from the last message.

        Note the tool call response is cached, repeated calls to this method will return the same response.
        With `run_tools_eagerly`, it reuses the results of the reply's calls that have run and runs the rest,
        including the ones `defer_tool_call()` is holding, so that no call runs twice.

        None can be returned if no tool call was applicable.
        """
        if self._cached_tool_call_response is not None:
            log.debug("Returning cached tool call response.")
            return self._cached_tool_call_response
        response = self._generate_tool_call_response()
        self._cached_tool_call_response = response
        return response

    def _generate_tool_call_response(self) -> BetaUserMessageParam | None:
        content = self._get_last_assistant_message_content()
        if not content:
            return None

        tool_use_blocks = [block for block in content if block.type == "tool_use"]
        if not tool_use_blocks:
            return None

        results: list[BetaToolResultBlockParam] = []
        tools_by_name = self._runnable_tools()
        available = self._available_tool_names()
        failed_toolsets: set[str] = set()  # a toolset whose member failed this turn: its later members are not run
        eager_calls = self._eager_tool_calls

        for tool_use in tool_use_blocks:
            if tool_use.toolset_name is not None:
                if tool_use.toolset_name in failed_toolsets:
                    results.append(not_executed_result(tool_use))
                    continue
                # With `run_tools_eagerly`, the result of a member that ran while the reply streamed is kept, so that
                # it doesn't run twice.
                member_result = eager_calls.results.get(tool_use.id) if eager_calls is not None else None
                if member_result is None:
                    member_result = self._run_toolset_member(tool_use)
                    if eager_calls is not None:
                        eager_calls.record(tool_use, member_result)
                if member_result.get("is_error") and tool_use.toolset_name in self._toolsets_by_family:
                    failed_toolsets.add(tool_use.toolset_name)
                results.append(member_result)
                continue

            result: BetaToolResultBlockParam | None = None
            if eager_calls is not None:
                result = eager_calls.results.get(tool_use.id)
            if result is None:
                tool = tools_by_name.get(tool_use.name) if tool_use.name in available else None
                if tool is None and tool_use.name in self._toolsets_by_family:
                    failed_toolsets.add(tool_use.name)
                    results.append(malformed_toolset_call_result(tool_use))
                    continue
                if tool is None:
                    warnings.warn(
                        f"Tool '{tool_use.name}' not found in tool runner. "
                        f"Available tools: {list(tools_by_name)}. "
                        f"If using a raw tool definition, handle the tool call manually and use `append_messages()` to add the result. "
                        f"Otherwise, pass the tool using `beta_tool(func)` or a `@beta_tool` decorated function.",
                        UserWarning,
                        stacklevel=3,
                    )
                    result = {
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": f"Error: Tool '{tool_use.name}' not found",
                        "is_error": True,
                    }
                else:
                    with self._tool_use_span(self._client, tool, tool_use) as run:
                        run.result = result = self._run_tool(tool, tool_use)

                if eager_calls is not None:
                    eager_calls.record(tool_use, result)

            results.append(result)

        return {"role": "user", "content": results}

    def _run_tool(self, tool: BetaRunnableTool, tool_use: BetaToolUseBlock) -> BetaToolResultBlockParam:
        try:
            return {
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": tool_result_content(tool.call(tool_use.input)),
            }
        except ToolError as exc:
            return {
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": tool_error_content(exc),
                "is_error": True,
            }
        except Exception as exc:
            log.exception(f"Error occurred while calling tool: {tool.name}", exc_info=exc)
            return {
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": tool_error_content(exc),
                "is_error": True,
            }

    def _run_toolset_member(self, tool_use: BetaToolUseBlock) -> BetaToolResultBlockParam:
        toolset = self._toolset_for(tool_use)
        if toolset is None:
            return self._toolset_not_found_result(tool_use)
        with self._tool_use_span(self._client, toolset, tool_use) as run:
            run.result = result = toolset.tool_result(tool_use)
        return result

    def _get_last_message(self) -> ParsedBetaMessage[ResponseFormatT] | None:
        if callable(self._last_message):
            return self._last_message()
        return self._last_message

    def _get_last_assistant_message(self) -> ParsedBetaMessage[ResponseFormatT] | None:
        last_message = self._get_last_message()
        if last_message is None or last_message.role != "assistant" or not last_message.content:
            return None

        return last_message

    def _get_last_assistant_message_content(self) -> list[ParsedBetaContentBlock[ResponseFormatT]] | None:
        last_assistant_message = self._get_last_assistant_message()
        if last_assistant_message is None:
            return None

        return last_assistant_message.content


class BetaToolRunner(BaseSyncToolRunner[ParsedBetaMessage[ResponseFormatT], ResponseFormatT]):
    @overload
    def __init__(
        self,
        *,
        thread: BetaMessageThread[ResponseFormatT],
        options: TurnOverrides,
        max_iterations: int | None = None,
    ) -> None: ...

    @overload
    def __init__(
        self,
        *,
        params: ParseMessageCreateParamsBase[ResponseFormatT],
        options: RequestOptions,
        tools: Iterable[BetaRunnableTool | BetaRunnableToolset],
        client: Anthropic,
        max_iterations: int | None = None,
    ) -> None: ...

    def __init__(
        self,
        *,
        thread: BetaMessageThread[ResponseFormatT] | None = None,
        params: ParseMessageCreateParamsBase[ResponseFormatT] | None = None,
        options: TurnOverrides | RequestOptions,
        tools: Iterable[BetaRunnableTool | BetaRunnableToolset] | None = None,
        client: Anthropic | None = None,
        max_iterations: int | None = None,
    ) -> None:
        """Run the tool loop over `thread`, or over the thread that `client.beta.messages.tool_runner()` makes for
        `params`. Pass either `thread`, or `params`, `tools` and `client`.

        Args:
            thread: The message thread to run the loop over. The runner runs the thread's tools.
            params: The params of the requests. Their `tools` are the tool definitions to send.
            options: The request options of every request.
            tools: The tools and toolsets to run.
            client: The client that sends the requests.
            max_iterations: How many replies the loop asks for at most. There is no limit by default.
        """
        super().__init__(
            thread=thread, params=params, options=options, tools=tools, client=client, max_iterations=max_iterations
        )

    @override
    @contextmanager
    def _handle_request(
        self, thread: BetaMessageThread[ResponseFormatT]
    ) -> Iterator[ParsedBetaMessage[ResponseFormatT]]:
        message = thread.parse(**self._turn_options(thread))
        self._last_message = message
        yield message


class BetaStreamingToolRunner(BaseSyncToolRunner[BetaMessageStream[ResponseFormatT], ResponseFormatT]):
    @overload
    def __init__(
        self,
        *,
        thread: BetaMessageThread[ResponseFormatT],
        options: TurnOverrides,
        max_iterations: int | None = None,
        run_tools_eagerly: bool = False,
    ) -> None: ...

    @overload
    def __init__(
        self,
        *,
        params: ParseMessageCreateParamsBase[ResponseFormatT],
        options: RequestOptions,
        tools: Iterable[BetaRunnableTool | BetaRunnableToolset],
        client: Anthropic,
        max_iterations: int | None = None,
        run_tools_eagerly: bool = False,
    ) -> None: ...

    def __init__(
        self,
        *,
        thread: BetaMessageThread[ResponseFormatT] | None = None,
        params: ParseMessageCreateParamsBase[ResponseFormatT] | None = None,
        options: TurnOverrides | RequestOptions,
        tools: Iterable[BetaRunnableTool | BetaRunnableToolset] | None = None,
        client: Anthropic | None = None,
        max_iterations: int | None = None,
        run_tools_eagerly: bool = False,
    ) -> None:
        """Run the tool loop over `thread`, or over the thread that `client.beta.messages.tool_runner()` makes for
        `params`. Pass either `thread`, or `params`, `tools` and `client`.

        Args:
            thread: The message thread to run the loop over. The runner runs the thread's tools.
            params: The params of the requests. Their `tools` are the tool definitions to send.
            options: The request options of every request.
            tools: The tools and toolsets to run.
            client: The client that sends the requests.
            max_iterations: How many replies the loop asks for at most. There is no limit by default.
            run_tools_eagerly: Run each tool as soon as its call is complete, before the reply finishes. See
                `client.beta.messages.tool_runner()`.
        """
        super().__init__(
            thread=thread, params=params, options=options, tools=tools, client=client, max_iterations=max_iterations
        )
        self._run_tools_eagerly = run_tools_eagerly

    def defer_tool_call(self, tool_use: BetaToolUseBlock | str) -> None:
        """Hold a tool call of the current reply until you are done with the reply, which is when it runs without
        `run_tools_eagerly`: at the end of the loop body, or when you call `generate_tool_call_response()`.

        With `run_tools_eagerly` the runner otherwise runs each call while the reply streams, once the model has
        moved on from it: when the next block starts, or the reply stops with `tool_use`. The call runs when you ask
        for the event after that one, so you can hold it while you handle any event up to and including that one.
        The other calls of the reply still run early, except the later calls of the same toolset, which a toolset
        runs in order. It does nothing for a call that has run, outside the loop body, and without
        `run_tools_eagerly`.

        ```py
        for stream in runner:
            for event in stream:
                if event.type == "content_block_start" and event.content_block.type == "tool_use":
                    if event.content_block.name == "delete_file":
                        runner.defer_tool_call(event.content_block)
            # No `delete_file` call has run yet.
        ```

        Args:
            tool_use: The `tool_use` block of the call, or its id.
        """
        if self._eager_tool_calls is not None:
            self._eager_tool_calls.hold(tool_use)

    @property
    def deferred_tool_calls(self) -> list[BetaToolUseBlock]:
        """The tool calls of the current reply that `defer_tool_call()` is holding, in the model's order, as their
        `tool_use` blocks.

        A call is in the list once its block has finished streaming, so read the list when you are done with the
        stream. A call that has run is not in it. It is empty without `run_tools_eagerly`.

        Held calls are listed whatever the reply's `stop_reason`, because `generate_tool_call_response()` runs them
        whatever it is. After `max_tokens` the input of the last call can be cut off.

        ```py
        for stream in runner:
            for event in stream:
                if event.type == "content_block_start" and event.content_block.type == "tool_use":
                    if event.content_block.name == "delete_file":
                        runner.defer_tool_call(event.content_block)

            held = runner.deferred_tool_calls
            if held and not confirm(held):
                break
        ```
        """
        return [] if self._eager_tool_calls is None else self._eager_tool_calls.held()

    @override
    @contextmanager
    def _handle_request(
        self, thread: BetaMessageThread[ResponseFormatT]
    ) -> Iterator[BetaMessageStream[ResponseFormatT]]:
        with ExitStack() as stack:
            stream = stack.enter_context(thread.stream(**self._turn_options(thread)))
            self._last_message = stream.get_final_message
            if self._run_tools_eagerly:
                self._eager_tool_calls = EagerToolCalls()
                stream._iterator = self._run_tools_while_streaming(stream._iterator, self._eager_tool_calls)
            yield stream

    def _run_tools_while_streaming(
        self, events: Iterator[ParsedBetaMessageStreamEvent[ResponseFormatT]], calls: EagerToolCalls
    ) -> Iterator[ParsedBetaMessageStreamEvent[ResponseFormatT]]:
        """Passes on the reply's events, and runs each tool call once the reader is done with the event that shows
        the model has moved on from it. Asking for the next event is how the reader says it is done with the one it
        holds."""
        moved_on_from: BetaToolUseBlock | None = None
        # The next event is read first, so that no call runs once reading the reply has failed.
        for event in events:
            if moved_on_from is not None:
                name = moved_on_from.name
                family = moved_on_from.toolset_name
                tool = (
                    self._runnable_tools().get(name)
                    if family is None and name in self._available_tool_names()
                    else None
                )
                if family is None and tool is None and name in self._toolsets_by_family:
                    # A call named like a toolset, with no `toolset_name`, is a malformed toolset call.
                    family = name
                    calls.waiting_toolsets.add(family)
                if family is not None:
                    # A toolset runs its calls in the model's order. So once one of its calls waits for the tool
                    # response, or fails, its later calls wait for the tool response too.
                    if calls.is_held(moved_on_from):
                        calls.waiting_toolsets.add(family)
                    if family not in calls.waiting_toolsets:
                        self._running_eager_tool = True
                        try:
                            # The application resumed the reply from its own context, as it resumes the loop.
                            with as_current_span(self._tool_runner_span):
                                member_result = self._run_toolset_member(moved_on_from)
                        finally:
                            self._running_eager_tool = False
                        calls.record(moved_on_from, member_result)
                        if member_result.get("is_error"):
                            calls.waiting_toolsets.add(family)
                # A call to a tool the runner doesn't have gets its error result with the tool response.
                elif tool is not None and not calls.is_held(moved_on_from):
                    self._running_eager_tool = True
                    try:
                        # The application resumed the reply from its own context, as it resumes the loop.
                        with as_current_span(self._tool_runner_span):
                            with self._tool_use_span(self._client, tool, moved_on_from) as run:
                                run.result = result = self._run_tool(tool, moved_on_from)
                    finally:
                        self._running_eager_tool = False
                    calls.record(moved_on_from, result)

            moved_on_from = calls.track(event)
            yield event


class BaseAsyncToolRunner(
    BaseToolRunner[
        BetaAsyncMessageThread[ResponseFormatT], BetaAsyncRunnableTool, BetaAsyncRunnableToolset, ResponseFormatT
    ],
    Generic[RunnerItemT, ResponseFormatT],
    ABC,
):
    def __init__(
        self,
        *,
        thread: BetaAsyncMessageThread[ResponseFormatT] | None,
        params: ParseMessageCreateParamsBase[ResponseFormatT] | None,
        options: TurnOverrides | RequestOptions,
        tools: Iterable[BetaAsyncRunnableTool | BetaAsyncRunnableToolset] | None,
        client: AsyncAnthropic | None,
        max_iterations: int | None,
    ) -> None:
        if thread is None and params is not None and tools is not None and client is not None:
            validate_output_config_conflict(params.get("output_config", omit), params.get("output_format"))
            tools = list(tools)
            partition_async_tools(tools)
            thread = BetaAsyncMessageThread[ResponseFormatT]._for_tool_runner(client, params)
        elif thread is None or params is not None or tools is not None or client is not None:
            raise constructor_arguments_error(thread=thread, params=params, tools=tools, client=client)

        super().__init__(thread=thread, options=options, tools=tools or (), max_iterations=max_iterations)
        self._iterator = self.__run__()
        self._last_message: (
            Callable[[], Coroutine[None, None, ParsedBetaMessage[ResponseFormatT]]]
            | ParsedBetaMessage[ResponseFormatT]
            | None
        ) = None

    async def __anext__(self) -> RunnerItemT:
        # A close from another task can still be unwinding the loop, which cannot be asked for an item meanwhile.
        # No lock is needed: neither `close` nor this check awaits before it acts on `_closed`.
        if self._closed and cast("AsyncGeneratorType[RunnerItemT, None]", self._iterator).ag_running:
            raise StopAsyncIteration
        return await self._iterator.__anext__()

    async def __aiter__(self) -> AsyncIterator[RunnerItemT]:
        while True:
            try:
                item = await self.__anext__()
            except StopAsyncIteration:
                return
            yield item

    async def close(self) -> None:
        """Stop the runner early and end its span. Use it when you won't resume the runner with `until_done()`.

        Iterating a closed runner yields nothing. Closing a runner that is done has no effect.
        """
        self._closed = True
        # A loop that another task is driving, or is already closing, cannot be closed concurrently. It stops at its
        # next step, as does one whose tool runs while the application reads a reply.
        if (
            not self._running_eager_tool
            and not cast("AsyncGeneratorType[RunnerItemT, None]", self._iterator).ag_running
        ):
            await self._iterator.aclose()

    @abstractmethod
    @asynccontextmanager
    async def _handle_request(self, thread: BetaAsyncMessageThread[ResponseFormatT]) -> AsyncIterator[RunnerItemT]:
        raise NotImplementedError()
        yield  # type: ignore[unreachable]

    async def _compact(self, compaction: BetaCompactionConfigParam) -> AsyncGenerator[RunnerItemT, None]:
        last_message = self._last_message
        thread = self._take_compaction_thread(compaction)
        compacted_count = len(self._thread.messages)
        try:
            async with self._handle_request(thread) as item:
                yield item
                message = await self._get_last_message()
                assert message is not None
        finally:
            self._messages_being_compacted = None
        if not self._register_compaction_response(thread, message, compacted_count):
            # `until_done()` still returns the turn the run ended on.
            self._last_message = last_message

    async def _compact_after_final_turn(
        self, message: ParsedBetaMessage[ResponseFormatT]
    ) -> AsyncGenerator[RunnerItemT, None]:
        compaction = self._prepare_compaction_after_final_turn(message)
        if compaction is not None:
            # Closing the runner closes the compaction request with it, as `yield from` does in the sync runner.
            async with aclosing(self._compact(compaction)) as items:
                async for item in items:
                    yield item

    async def __run__(self) -> AsyncGenerator[RunnerItemT, None]:
        tool_runner_span = self._start_tool_runner_span(self._client)
        steps = self._steps()
        try:
            try:
                while True:
                    # The runner's own code runs with its span current. Each step enters the span again, because the
                    # application resumes the runner from its own context.
                    with as_current_span(tool_runner_span):
                        try:
                            item = await steps.__anext__()
                        except StopAsyncIteration:
                            break
                    # Outside the span, so that the application's code between iterations keeps its own context.
                    yield item
                # A closed runner stops here too, and closing leaves the status unset.
                if not self._closed:
                    set_tool_runner_status(tool_runner_span)
            except BaseException as err:
                # Closing a suspended runner raises `GeneratorExit` here, which leaves the status unset.
                set_tool_runner_status(tool_runner_span, err)
                raise
            finally:
                # Closing the request is the runner's code too, so it runs with the span current. The status is
                # settled by now: at the end of the event loop this can fail, when the loop is closing `steps` itself.
                with as_current_span(tool_runner_span):
                    await steps.aclose()
        finally:
            end_tool_runner_span(tool_runner_span)

    async def _steps(self) -> AsyncGenerator[RunnerItemT, None]:
        """The runner's loop. `__run__` drives it, one step for each item."""
        stop_reason: BetaStopReason | None = None
        while not self._should_stop():
            self._send_pending_tool_changes(hold=stop_reason == "pause_turn")
            # The API can't compact a conversation that ends mid-turn, so a paused turn is resumed first.
            turn_paused = _determine_next_step_from_stop_reason(stop_reason) == "resume"
            compaction = None if turn_paused else self._pending_compaction
            if compaction is not None:
                async with aclosing(self._compact(compaction)) as items:
                    async for item in items:
                        yield item
                continue

            self._sent_messages = self._messages = self._thread.messages
            async with self._handle_request(self._thread) as item:
                yield item
                message = await self._get_last_message()
                assert message is not None

            stop_reason = message.stop_reason
            next_step = _determine_next_step_from_stop_reason(stop_reason)
            if next_step != "stop":
                # No tool runs for a turn the thread refuses to send. A history the caller rewrote starts a new thread,
                # which takes any fields, so this comes first.
                self._thread._state.check_next_turn(self._options)

            self._hand_over_messages(message)
            self._iteration_count += 1

            if next_step == "stop":
                log.debug("Turn ended with stop_reason %r, exiting from tool runner loop.", message.stop_reason)
                async with aclosing(self._compact_after_final_turn(message)) as items:
                    async for item in items:
                        yield item
                break

            # On "resume" there is nothing to append: the history already holds the unfinished reply, or is the caller's.
            if next_step == "run_tools":
                response = await self.generate_tool_call_response()
                if response is None and not self._appended_to_thread:
                    log.debug("Tool call was not requested, exiting from tool runner loop.")
                    async with aclosing(self._compact_after_final_turn(message)) as items:
                        async for item in items:
                            yield item
                    break
                if response is not None and not self._messages_modified:
                    self._append_tool_results(response)

            self._messages_modified = False
            self._cached_tool_call_response = None

    async def until_done(self) -> ParsedBetaMessage[ResponseFormatT]:
        """
        Consumes the tool runner stream and returns the last message if it has not been consumed yet.
        If it has, it simply returns the last message.
        """
        await consume_async_iterator(self)
        last_message = await self._get_last_message()
        assert last_message is not None
        return last_message

    async def generate_tool_call_response(self) -> BetaUserMessageParam | None:
        """Generate a MessageParam by calling tool functions with any tool use blocks from the last message.

        Note the tool call response is cached, repeated calls to this method will return the same response.
        With `run_tools_eagerly`, it reuses the results of the reply's calls that have run and runs the rest,
        including the ones `defer_tool_call()` is holding, so that no call runs twice.

        None can be returned if no tool call was applicable.
        """
        if self._cached_tool_call_response is not None:
            log.debug("Returning cached tool call response.")
            return self._cached_tool_call_response

        response = await self._generate_tool_call_response()
        self._cached_tool_call_response = response
        return response

    async def _get_last_message(self) -> ParsedBetaMessage[ResponseFormatT] | None:
        if callable(self._last_message):
            return await self._last_message()
        return self._last_message

    async def _get_last_assistant_message(self) -> ParsedBetaMessage[ResponseFormatT] | None:
        last_message = await self._get_last_message()
        if last_message is None or last_message.role != "assistant" or not last_message.content:
            return None

        return last_message

    async def _get_last_assistant_message_content(self) -> list[ParsedBetaContentBlock[ResponseFormatT]] | None:
        last_assistant_message = await self._get_last_assistant_message()
        if last_assistant_message is None:
            return None

        return last_assistant_message.content

    async def _generate_tool_call_response(self) -> BetaUserMessageParam | None:
        content = await self._get_last_assistant_message_content()
        if not content:
            return None

        tool_use_blocks = [block for block in content if block.type == "tool_use"]
        if not tool_use_blocks:
            return None

        results: list[BetaToolResultBlockParam] = []
        tools_by_name = self._runnable_tools()
        available = self._available_tool_names()
        failed_toolsets: set[str] = set()  # a toolset whose member failed this turn: its later members are not run
        eager_calls = self._eager_tool_calls

        for tool_use in tool_use_blocks:
            if tool_use.toolset_name is not None:
                if tool_use.toolset_name in failed_toolsets:
                    results.append(not_executed_result(tool_use))
                    continue
                # With `run_tools_eagerly`, the result of a member that ran while the reply streamed is kept, so that
                # it doesn't run twice.
                member_result = eager_calls.results.get(tool_use.id) if eager_calls is not None else None
                if member_result is None:
                    member_result = await self._run_toolset_member(tool_use)
                    if eager_calls is not None:
                        eager_calls.record(tool_use, member_result)
                if member_result.get("is_error") and tool_use.toolset_name in self._toolsets_by_family:
                    failed_toolsets.add(tool_use.toolset_name)
                results.append(member_result)
                continue

            result: BetaToolResultBlockParam | None = None
            if eager_calls is not None:
                result = eager_calls.results.get(tool_use.id)
            if result is None:
                tool = tools_by_name.get(tool_use.name) if tool_use.name in available else None
                if tool is None and tool_use.name in self._toolsets_by_family:
                    failed_toolsets.add(tool_use.name)
                    results.append(malformed_toolset_call_result(tool_use))
                    continue
                if tool is None:
                    warnings.warn(
                        f"Tool '{tool_use.name}' not found in tool runner. "
                        f"Available tools: {list(tools_by_name)}. "
                        f"If using a raw tool definition, handle the tool call manually and use `append_messages()` to add the result. "
                        f"Otherwise, pass the tool using `beta_async_tool(func)` or a `@beta_async_tool` decorated function.",
                        UserWarning,
                        stacklevel=3,
                    )
                    result = {
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": f"Error: Tool '{tool_use.name}' not found",
                        "is_error": True,
                    }
                else:
                    with self._tool_use_span(self._client, tool, tool_use) as run:
                        run.result = result = await self._run_tool(tool, tool_use)

                if eager_calls is not None:
                    eager_calls.record(tool_use, result)

            results.append(result)

        return {"role": "user", "content": results}

    async def _run_tool(self, tool: BetaAsyncRunnableTool, tool_use: BetaToolUseBlock) -> BetaToolResultBlockParam:
        try:
            return {
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": tool_result_content(await tool.call(tool_use.input)),
            }
        except ToolError as exc:
            return {
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": tool_error_content(exc),
                "is_error": True,
            }
        except Exception as exc:
            log.exception(f"Error occurred while calling tool: {tool.name}", exc_info=exc)
            return {
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": tool_error_content(exc),
                "is_error": True,
            }

    async def _run_toolset_member(self, tool_use: BetaToolUseBlock) -> BetaToolResultBlockParam:
        toolset = self._toolset_for(tool_use)
        if toolset is None:
            return self._toolset_not_found_result(tool_use)
        with self._tool_use_span(self._client, toolset, tool_use) as run:
            run.result = result = await toolset.tool_result(tool_use)
        return result


class BetaAsyncToolRunner(BaseAsyncToolRunner[ParsedBetaMessage[ResponseFormatT], ResponseFormatT]):
    @overload
    def __init__(
        self,
        *,
        thread: BetaAsyncMessageThread[ResponseFormatT],
        options: TurnOverrides,
        max_iterations: int | None = None,
    ) -> None: ...

    @overload
    def __init__(
        self,
        *,
        params: ParseMessageCreateParamsBase[ResponseFormatT],
        options: RequestOptions,
        tools: Iterable[BetaAsyncRunnableTool | BetaAsyncRunnableToolset],
        client: AsyncAnthropic,
        max_iterations: int | None = None,
    ) -> None: ...

    def __init__(
        self,
        *,
        thread: BetaAsyncMessageThread[ResponseFormatT] | None = None,
        params: ParseMessageCreateParamsBase[ResponseFormatT] | None = None,
        options: TurnOverrides | RequestOptions,
        tools: Iterable[BetaAsyncRunnableTool | BetaAsyncRunnableToolset] | None = None,
        client: AsyncAnthropic | None = None,
        max_iterations: int | None = None,
    ) -> None:
        """Run the tool loop over `thread`, or over the thread that `client.beta.messages.tool_runner()` makes for
        `params`. Pass either `thread`, or `params`, `tools` and `client`.

        Args:
            thread: The message thread to run the loop over. The runner runs the thread's tools.
            params: The params of the requests. Their `tools` are the tool definitions to send.
            options: The request options of every request.
            tools: The tools and toolsets to run.
            client: The client that sends the requests.
            max_iterations: How many replies the loop asks for at most. There is no limit by default.
        """
        super().__init__(
            thread=thread, params=params, options=options, tools=tools, client=client, max_iterations=max_iterations
        )

    @override
    @asynccontextmanager
    async def _handle_request(
        self, thread: BetaAsyncMessageThread[ResponseFormatT]
    ) -> AsyncIterator[ParsedBetaMessage[ResponseFormatT]]:
        message = await thread.parse(**self._turn_options(thread))
        self._last_message = message
        yield message


class BetaAsyncStreamingToolRunner(BaseAsyncToolRunner[BetaAsyncMessageStream[ResponseFormatT], ResponseFormatT]):
    @overload
    def __init__(
        self,
        *,
        thread: BetaAsyncMessageThread[ResponseFormatT],
        options: TurnOverrides,
        max_iterations: int | None = None,
        run_tools_eagerly: bool = False,
    ) -> None: ...

    @overload
    def __init__(
        self,
        *,
        params: ParseMessageCreateParamsBase[ResponseFormatT],
        options: RequestOptions,
        tools: Iterable[BetaAsyncRunnableTool | BetaAsyncRunnableToolset],
        client: AsyncAnthropic,
        max_iterations: int | None = None,
        run_tools_eagerly: bool = False,
    ) -> None: ...

    def __init__(
        self,
        *,
        thread: BetaAsyncMessageThread[ResponseFormatT] | None = None,
        params: ParseMessageCreateParamsBase[ResponseFormatT] | None = None,
        options: TurnOverrides | RequestOptions,
        tools: Iterable[BetaAsyncRunnableTool | BetaAsyncRunnableToolset] | None = None,
        client: AsyncAnthropic | None = None,
        max_iterations: int | None = None,
        run_tools_eagerly: bool = False,
    ) -> None:
        """Run the tool loop over `thread`, or over the thread that `client.beta.messages.tool_runner()` makes for
        `params`. Pass either `thread`, or `params`, `tools` and `client`.

        Args:
            thread: The message thread to run the loop over. The runner runs the thread's tools.
            params: The params of the requests. Their `tools` are the tool definitions to send.
            options: The request options of every request.
            tools: The tools and toolsets to run.
            client: The client that sends the requests.
            max_iterations: How many replies the loop asks for at most. There is no limit by default.
            run_tools_eagerly: Run each tool as soon as its call is complete, before the reply finishes. See
                `client.beta.messages.tool_runner()`.
        """
        super().__init__(
            thread=thread, params=params, options=options, tools=tools, client=client, max_iterations=max_iterations
        )
        self._run_tools_eagerly = run_tools_eagerly

    def defer_tool_call(self, tool_use: BetaToolUseBlock | str) -> None:
        """Hold a tool call of the current reply until you are done with the reply, which is when it runs without
        `run_tools_eagerly`: at the end of the loop body, or when you call `generate_tool_call_response()`.

        With `run_tools_eagerly` the runner otherwise runs each call while the reply streams, once the model has
        moved on from it: when the next block starts, or the reply stops with `tool_use`. The call runs when you ask
        for the event after that one, so you can hold it while you handle any event up to and including that one.
        The other calls of the reply still run early, except the later calls of the same toolset, which a toolset
        runs in order. It does nothing for a call that has run, outside the loop body, and without
        `run_tools_eagerly`.

        ```py
        async for stream in runner:
            async for event in stream:
                if event.type == "content_block_start" and event.content_block.type == "tool_use":
                    if event.content_block.name == "delete_file":
                        runner.defer_tool_call(event.content_block)
            # No `delete_file` call has run yet.
        ```

        Args:
            tool_use: The `tool_use` block of the call, or its id.
        """
        if self._eager_tool_calls is not None:
            self._eager_tool_calls.hold(tool_use)

    @property
    def deferred_tool_calls(self) -> list[BetaToolUseBlock]:
        """The tool calls of the current reply that `defer_tool_call()` is holding, in the model's order, as their
        `tool_use` blocks.

        A call is in the list once its block has finished streaming, so read the list when you are done with the
        stream. A call that has run is not in it. It is empty without `run_tools_eagerly`.

        Held calls are listed whatever the reply's `stop_reason`, because `generate_tool_call_response()` runs them
        whatever it is. After `max_tokens` the input of the last call can be cut off.

        ```py
        async for stream in runner:
            async for event in stream:
                if event.type == "content_block_start" and event.content_block.type == "tool_use":
                    if event.content_block.name == "delete_file":
                        runner.defer_tool_call(event.content_block)

            held = runner.deferred_tool_calls
            if held and not await confirm(held):
                break
        ```
        """
        return [] if self._eager_tool_calls is None else self._eager_tool_calls.held()

    @override
    @asynccontextmanager
    async def _handle_request(
        self, thread: BetaAsyncMessageThread[ResponseFormatT]
    ) -> AsyncIterator[BetaAsyncMessageStream[ResponseFormatT]]:
        async with AsyncExitStack() as stack:
            stream = await stack.enter_async_context(thread.stream(**self._turn_options(thread)))
            self._last_message = stream.get_final_message
            if self._run_tools_eagerly:
                self._eager_tool_calls = EagerToolCalls()
                stream._iterator = self._run_tools_while_streaming(stream._iterator, self._eager_tool_calls)
            yield stream

    async def _run_tools_while_streaming(
        self, events: AsyncIterator[ParsedBetaMessageStreamEvent[ResponseFormatT]], calls: EagerToolCalls
    ) -> AsyncIterator[ParsedBetaMessageStreamEvent[ResponseFormatT]]:
        """Passes on the reply's events, and runs each tool call once the reader is done with the event that shows
        the model has moved on from it. Asking for the next event is how the reader says it is done with the one it
        holds."""
        moved_on_from: BetaToolUseBlock | None = None
        # The next event is read first, so that no call runs once reading the reply has failed.
        async for event in events:
            if moved_on_from is not None:
                name = moved_on_from.name
                family = moved_on_from.toolset_name
                tool = (
                    self._runnable_tools().get(name)
                    if family is None and name in self._available_tool_names()
                    else None
                )
                if family is None and tool is None and name in self._toolsets_by_family:
                    # A call named like a toolset, with no `toolset_name`, is a malformed toolset call.
                    family = name
                    calls.waiting_toolsets.add(family)
                if family is not None:
                    # A toolset runs its calls in the model's order. So once one of its calls waits for the tool
                    # response, or fails, its later calls wait for the tool response too.
                    if calls.is_held(moved_on_from):
                        calls.waiting_toolsets.add(family)
                    if family not in calls.waiting_toolsets:
                        self._running_eager_tool = True
                        try:
                            # The application resumed the reply from its own context, as it resumes the loop.
                            with as_current_span(self._tool_runner_span):
                                member_result = await self._run_toolset_member(moved_on_from)
                        finally:
                            self._running_eager_tool = False
                        calls.record(moved_on_from, member_result)
                        if member_result.get("is_error"):
                            calls.waiting_toolsets.add(family)
                # A call to a tool the runner doesn't have gets its error result with the tool response.
                elif tool is not None and not calls.is_held(moved_on_from):
                    self._running_eager_tool = True
                    try:
                        # The application resumed the reply from its own context, as it resumes the loop.
                        with as_current_span(self._tool_runner_span):
                            with self._tool_use_span(self._client, tool, moved_on_from) as run:
                                run.result = result = await self._run_tool(tool, moved_on_from)
                    finally:
                        self._running_eager_tool = False
                    calls.record(moved_on_from, result)

            moved_on_from = calls.track(event)
            yield event


class EagerToolCalls:
    """The tool calls of one streamed reply, for a tool runner with `run_tools_eagerly`."""

    def __init__(self) -> None:
        self.results: dict[str, BetaToolResultBlockParam] = {}
        """The result of each call that has run, by `tool_use` id."""

        self._finished: list[BetaToolUseBlock] = []
        """The `tool_use` blocks that have finished streaming, in the model's order."""

        self._held_ids: set[str] = set()
        """The ids of the calls that `defer_tool_call()` is holding."""

        self.waiting_toolsets: set[str] = set()
        """The toolsets that have a call waiting for the tool response. Their later calls wait for it too."""

        self._closed: BetaToolUseBlock | None = None
        """The last `tool_use` block to close, until the model moves on from it."""

        self._fallback = False
        """Whether a refusal has handed the reply to a fallback model."""

    def hold(self, tool_use: BetaToolUseBlock | str) -> None:
        tool_use_id = tool_use if isinstance(tool_use, str) else tool_use.id
        if tool_use_id not in self.results:
            self._held_ids.add(tool_use_id)

    def is_held(self, tool_use: BetaToolUseBlock) -> bool:
        return tool_use.id in self._held_ids

    def held(self) -> list[BetaToolUseBlock]:
        return [tool_use for tool_use in self._finished if tool_use.id in self._held_ids]

    def record(self, tool_use: BetaToolUseBlock, result: BetaToolResultBlockParam) -> None:
        self._held_ids.discard(tool_use.id)
        self.results[tool_use.id] = result

    def track(self, event: ParsedBetaMessageStreamEvent[Any]) -> BetaToolUseBlock | None:
        """Follows the reply, and returns the call that `event` shows the model has moved on from, if any.

        A call's own `content_block_stop` isn't enough, because a reply that is cut off closes its last call too.
        After a `fallback` block no call is returned, so the rest wait for the reply to end.
        """
        if event.type == "content_block_stop":
            if event.content_block.type == "tool_use":
                self._finished.append(event.content_block)
                self._closed = None if self._fallback else event.content_block
            return None

        if event.type == "content_block_start" and event.content_block.type == "fallback":
            # The refusal that led to the fallback may have cut off the call before it.
            self._fallback = True
            self._closed = None
            return None

        moved_on = event.type == "content_block_start" or (
            event.type == "message_delta" and event.delta.stop_reason == "tool_use"
        )
        if not moved_on:
            return None

        moved_on_from, self._closed = self._closed, None
        return moved_on_from


def constructor_arguments_error(**arguments: object) -> TypeError:
    """The error for a tool runner constructor call that has neither of the two sets of `arguments`, or both."""
    given = [f"`{name}`" for name, value in arguments.items() if value is not None]
    return TypeError(
        "A tool runner takes either `thread`, or `params`, `tools` and `client`, "
        f"but got {', '.join(given) or 'none of them'}."
    )


MAX_NAMED_ACTIONS = 10


def malformed_toolset_call_result(tool_use: BetaToolUseBlock) -> BetaToolResultBlockParam:
    """Build the error result for a call that is named after a toolset in the run but has no `toolset_name`.

    Its input holds actions for that toolset in a form the runner cannot run. The text says what is wrong and names
    the actions where it can. Apart from action names, it does not repeat the model's input.
    """
    detail = malformed_call_detail(tool_use.input)
    return {
        "type": "tool_result",
        "tool_use_id": tool_use.id,
        "content": f"Error: the '{quoted_name(tool_use.name)}' toolset could not run this call{detail}; "
        "nothing in the batch was executed",
        "is_error": True,
    }


def malformed_call_detail(input: Dict[str, object]) -> str:
    if "actions" not in input:
        action = input.get("action")
        if isinstance(action, str):
            return f": the call has no 'actions' list (action: '{quoted_name(action)}')"
        return ": the call has no 'actions' list"
    actions = input["actions"]
    if isinstance(actions, str):
        return ": 'actions' is text, not a list of actions"
    if not is_list(actions):
        return ": 'actions' is not a list of actions"
    if not actions:
        return ": the 'actions' list is empty"
    names: List[str] = []
    for i, entry in enumerate(actions):
        name = entry.get("action") if is_mapping(entry) else None
        if not isinstance(name, str):
            return f": action {i} must be an object with a string 'action' field"
        names.append(f"'{quoted_name(name)}'")
    more = len(names) - MAX_NAMED_ACTIONS
    shown = ", ".join(names[:MAX_NAMED_ACTIONS]) + (f", and {more} more" if more > 0 else "")
    return f": its actions could not be run as sent (actions: {shown})"
