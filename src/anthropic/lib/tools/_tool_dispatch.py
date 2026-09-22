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

import inspect
from typing import Union, TypeVar, Iterable, Awaitable, cast
from typing_extensions import Protocol

from anyio.to_thread import run_sync

from ._beta_functions import ToolError, BetaFunctionTool, BetaBuiltinFunctionTool, BetaFunctionToolResultType
from ...types.beta.beta_message_param import BetaMessageParam
from ...types.beta.beta_compaction_block import BetaCompactionBlock
from ...types.beta.beta_content_block_param import BetaContentBlockParam
from ...types.beta.beta_request_tool_removal_block_param import BetaRequestToolRemovalBlockParam
from ...types.beta.beta_request_tool_addition_block_param import (
    Tool as _ToolChangeTool,
    BetaRequestToolAdditionBlockParam,
)

__all__ = ["tool_registry", "tool_error_content", "run_runnable_tool", "available_tool_names"]


class _NamedTool(Protocol):
    """Anything with a `name` — the shape `tool_registry` indexes on."""

    @property
    def name(self) -> str: ...


class _CallableTool(Protocol):
    """A runnable tool: `call` may be sync or async (it returns either the
    result or an awaitable of it)."""

    def call(self, input: object) -> Union[BetaFunctionToolResultType, Awaitable[BetaFunctionToolResultType]]: ...


NamedToolT = TypeVar("NamedToolT", bound=_NamedTool)


def tool_registry(tools: Iterable[NamedToolT]) -> dict[str, NamedToolT]:
    """Index `tools` by their `name` for O(1) dispatch lookup.

    On a duplicate name the later tool wins, matching a plain dict comprehension.
    """
    return {tool.name: tool for tool in tools}


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


def tool_error_content(exc: BaseException) -> BetaFunctionToolResultType:
    """Render an exception raised by a tool as tool-result content.

    A `ToolError` carries its own structured content; anything else is
    rendered with `repr` (which, unlike `str`, keeps the exception type).
    The caller owns the `is_error` flag and any logging.
    """
    if isinstance(exc, ToolError):
        return exc.content
    return repr(exc)


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
