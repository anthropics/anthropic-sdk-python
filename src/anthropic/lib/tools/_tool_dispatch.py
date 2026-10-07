"""Shared tool-dispatch helpers for the tool runners.

Both `client.beta.messages.tool_runner` (the Messages tool runner) and
`client.beta.sessions.events.tool_runner` (the sessions-side
`anthropic.lib.tools._beta_session_runner.SessionToolRunner`) do the
same three small things: index the supplied tools by name, run a runnable tool
over a JSON input, and turn an exception raised by a tool into tool-result
content. Those steps are factored out here so the two runners stay consistent
instead of each carrying its own copy. Consumed by the runner helpers only.
"""

from __future__ import annotations

import re
import inspect
from typing import Union, TypeVar, Iterable, Awaitable, cast, overload
from typing_extensions import Literal, Protocol

from anyio.to_thread import run_sync

from ..._utils import is_dict
from ...types.beta import BetaToolUnionParam
from ._beta_functions import (
    ToolError,
    BetaFunctionTool,
    BetaRunnableTool,
    BetaAsyncFunctionTool,
    BetaAsyncRunnableTool,
    BetaBuiltinFunctionTool,
    BetaFunctionToolResultType,
    BetaAsyncBuiltinFunctionTool,
)
from ._toolsets._errors import ToolsetContractError
from ._toolsets._runnable import (
    TOOLSET_CLASSES,
    BetaRunnableToolset,
    BetaAnyRunnableToolset,
    BetaAsyncRunnableToolset,
)
from ._toolsets._sanitize import error_text, well_formed
from ...types.beta.beta_message_param import BetaMessageParam
from ...types.beta.beta_compaction_block import BetaCompactionBlock
from ...types.beta.beta_content_block_param import BetaContentBlockParam
from ...types.beta.beta_tool_result_block_param import Content as BetaContent
from ...types.beta.beta_request_tool_removal_block_param import BetaRequestToolRemovalBlockParam
from ...types.beta.beta_request_tool_addition_block_param import (
    Tool as _ToolChangeTool,
    BetaRequestToolAdditionBlockParam,
)

__all__ = [
    "tool_registry",
    "index_runnables",
    "partition_sync_tools",
    "partition_async_tools",
    "wrong_flavour_error",
    "tool_error_content",
    "tool_result_content",
    "run_runnable_tool",
    "available_tool_names",
    "tool_family",
]

_SYNC_RUNNABLES = (BetaFunctionTool, BetaBuiltinFunctionTool, BetaRunnableToolset)
_ASYNC_RUNNABLES = (BetaAsyncFunctionTool, BetaAsyncBuiltinFunctionTool, BetaAsyncRunnableToolset)


def wrong_flavour_error(tool: object, *, expected: Literal["sync", "async"]) -> Exception:
    """The error for a sync tool or toolset handed to the async runner (or the reverse), raised when the
    runner is built. A toolset mismatch is a `ToolsetContractError`."""
    if expected == "sync":
        message = (
            f"Received an async tool or toolset ({type(tool).__name__}) in the synchronous tool_runner. Create the "
            "runner from an AsyncAnthropic client (and await its result), or pass a synchronous tool or "
            "toolset here."
        )
    else:
        message = (
            f"Received a synchronous tool or toolset ({type(tool).__name__}) in the asynchronous tool_runner. Create "
            "the runner from an Anthropic client, or pass an async tool or toolset here."
        )
    if isinstance(tool, TOOLSET_CLASSES):
        return ToolsetContractError(message)
    return TypeError(message)


def partition_sync_tools(
    tools: Iterable[BetaRunnableTool | BetaRunnableToolset | BetaToolUnionParam],
) -> tuple[list[BetaRunnableTool | BetaRunnableToolset], list[BetaToolUnionParam]]:
    """Split a synchronous `tool_runner`'s `tools` argument into the runnable objects the runner dispatches (function
    tools and toolsets) and the raw `tools[]` params that go on the wire as given. An async runnable raises
    `wrong_flavour_error`."""
    runnable: list[BetaRunnableTool | BetaRunnableToolset] = []
    raw: list[BetaToolUnionParam] = []
    for tool in tools:
        if isinstance(tool, _SYNC_RUNNABLES):
            runnable.append(tool)
        elif isinstance(tool, _ASYNC_RUNNABLES):
            raise wrong_flavour_error(tool, expected="sync")
        else:
            raw.append(tool)
    return runnable, raw


def partition_async_tools(
    tools: Iterable[BetaAsyncRunnableTool | BetaAsyncRunnableToolset | BetaToolUnionParam],
) -> tuple[list[BetaAsyncRunnableTool | BetaAsyncRunnableToolset], list[BetaToolUnionParam]]:
    """The async twin of `partition_sync_tools`: a synchronous runnable raises `wrong_flavour_error`."""
    runnable: list[BetaAsyncRunnableTool | BetaAsyncRunnableToolset] = []
    raw: list[BetaToolUnionParam] = []
    for tool in tools:
        if isinstance(tool, _ASYNC_RUNNABLES):
            runnable.append(tool)
        elif isinstance(tool, _SYNC_RUNNABLES):
            raise wrong_flavour_error(tool, expected="async")
        else:
            raw.append(tool)
    return runnable, raw


class _NamedTool(Protocol):
    """Anything with a `name` — the shape `tool_registry` indexes on."""

    @property
    def name(self) -> str: ...


class _CallableTool(Protocol):
    """A runnable tool: `call` may be sync or async (it returns either the
    result or an awaitable of it)."""

    def call(self, input: object) -> Union[BetaFunctionToolResultType, Awaitable[BetaFunctionToolResultType]]: ...


NamedToolT = TypeVar("NamedToolT", bound=_NamedTool)
ToolsetT = TypeVar("ToolsetT", bound=BetaAnyRunnableToolset)


def tool_registry(tools: Iterable[NamedToolT]) -> dict[str, NamedToolT]:
    """Index the named `tools` by their `name`. On a duplicate name the later tool wins."""
    return {tool.name: tool for tool in tools}


def index_runnables(
    tools: Iterable[NamedToolT | ToolsetT],
) -> tuple[dict[str, NamedToolT], dict[str, ToolsetT]]:
    """Index a runner's tools by `name` and its toolsets by family (`toolset_name`).

    A toolset's `tools[]` entry has no `name`, so toolsets are indexed apart and never shadow a
    same-named custom tool. On a duplicate key the later one wins.
    """
    by_name: dict[str, NamedToolT] = {}
    by_family: dict[str, ToolsetT] = {}
    for tool in tools:
        if isinstance(tool, TOOLSET_CLASSES):
            by_family[tool.toolset_name] = tool
        else:
            by_name[tool.name] = tool
    return by_name, by_family


def available_tool_names(messages: Iterable[BetaMessageParam], tool_names: Iterable[str]) -> set[str]:
    """Fold mid-conversation `tool_removal` / `tool_addition` blocks over
    the locally runnable `tool_names`.

    These blocks arrive in `role: "system"` messages, and in the
    `tool_changes` of a `compaction` block, which stands in for the system
    messages of the turns it summarized. A `tool_reference` or a by-value
    `tool_definition` can name a locally runnable tool; MCP references
    execute server-side, so they (and any unknown block or tool type) are
    ignored rather than raising.
    """
    available = set(tool_names)
    for message in messages:
        content = message["content"]
        if isinstance(content, str):
            continue
        for block in content:
            if message["role"] == "system":
                _apply_tool_change(block, available)
            elif message["role"] == "assistant":
                for change in _compaction_tool_changes(block):
                    _apply_tool_change(change, available)
    return available


def _compaction_tool_changes(block: BetaContentBlockParam) -> Iterable[BetaContentBlockParam]:
    """The ``tool_changes`` of a ``compaction`` block, whichever shape it has in history.

    A caller-written block is a dict; one the runner echoed from a response is
    still the response model, with response-model entries.
    """
    if isinstance(block, BetaCompactionBlock):
        return [cast(BetaContentBlockParam, change.to_dict()) for change in block.tool_changes or ()]
    if isinstance(block, dict) and block["type"] == "compaction":
        return block.get("tool_changes") or ()
    return ()


def _apply_tool_change(block: BetaContentBlockParam, available: set[str]) -> None:
    """Apply a single `tool_removal` / `tool_addition` block to `available`."""
    if not isinstance(block, dict):
        # `BetaContentBlockParam` also admits response-side content-block
        # models; `tool_removal` / `tool_addition` are request-only
        # TypedDicts, so a non-dict block is never one of them.
        return
    if block["type"] == "tool_removal" or block["type"] == "tool_addition":
        _apply_tool_reference_change(block, available)


def _apply_tool_reference_change(
    block: Union[BetaRequestToolRemovalBlockParam, BetaRequestToolAdditionBlockParam], available: set[str]
) -> None:
    """Fold one `tool_removal` / `tool_addition` block into `available`."""
    name = _changed_tool_name(block["tool"])
    if name is None:
        return
    if block["type"] == "tool_removal":
        available.discard(name)  # removing an absent name is a set no-op
    else:
        available.add(name)  # add unconditionally: dispatch still requires a registry hit


def _changed_tool_name(tool: _ToolChangeTool) -> str | None:
    """The locally runnable tool name a tool-change ``tool`` resolves to.

    `tool_reference` names one directly and `tool_definition` carries one
    by value; MCP references execute server-side, and unknown types are
    ignored (forward compatibility), so those resolve to `None`.
    """
    if tool["type"] == "tool_reference":
        return tool["name"]
    if tool["type"] == "tool_definition":
        # Not every `tools[]` entry has a `name` (e.g. `mcp_toolset`); those are never locally runnable.
        name = cast("dict[str, object]", tool["definition"]).get("name")
        return name if isinstance(name, str) else None
    return None


def tool_family(definition: BetaToolUnionParam) -> str:
    """A tool definition's family, as the API computes it for a toolset: its `type` ("custom" when absent) without a
    trailing `_YYYYMMDD` date and then without `_toolset`. `browser_toolset_20260801` and any later dated version are
    "browser"."""
    return re.sub(r"_\d{8}$", "", definition.get("type") or "custom").removesuffix("_toolset")


def tool_error_content(exc: BaseException) -> BetaFunctionToolResultType:
    """Render an exception raised by a tool as tool-result content.

    A `ToolError` has its own structured content, made well formed but
    never cut. Anything else is rendered with `repr` (which, unlike `str`, keeps
    the exception type), well formed and cut to the field limit so the next
    request can include it whatever the exception's text holds. The caller owns
    the `is_error` flag and any logging.
    """
    if isinstance(exc, ToolError):
        return tool_result_content(exc.content)
    return error_text(exc)


@overload
def tool_result_content(content: None) -> None: ...
@overload
def tool_result_content(content: BetaFunctionToolResultType) -> BetaFunctionToolResultType: ...
def tool_result_content(content: BetaFunctionToolResultType | None) -> BetaFunctionToolResultType | None:
    """A tool's result, or a `ToolError`'s content, in a form the next request
    can encode: an unpaired surrogate in a string, or in a text block's text, is
    folded to U+FFFD. Nothing is cut and no block is dropped, so the length and
    shape stay the tool's own. A tool that returns `None` (whatever its
    annotation says) sends `content: null`.
    """
    if content is None:
        return None
    if isinstance(content, str):
        return well_formed(content)

    blocks = list(content)
    for i, block in enumerate(blocks):
        if is_dict(block) and block.get("type") == "text":
            text = block.get("text")
            if isinstance(text, str) and (fixed := well_formed(text)) != text:
                blocks[i] = cast(BetaContent, {**block, "text": fixed})
    return blocks


async def run_runnable_tool(tool: _CallableTool, input: dict[str, object]) -> BetaFunctionToolResultType:
    """Call `tool` with `input`, awaiting the result if the tool is async.

    Sync tools run on a worker thread. If the caller cancels (for example on a
    timeout), the thread is left to finish on its own and its result is
    dropped.
    """
    if isinstance(tool, (BetaFunctionTool, BetaBuiltinFunctionTool)):
        return await run_sync(tool.call, input, abandon_on_cancel=True)
    result = tool.call(input)
    if inspect.isawaitable(result):
        return await result
    return result
