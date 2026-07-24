"""Shared tool-dispatch helpers for the tool runners.

Both ``client.beta.messages.tool_runner`` (the Messages tool runner) and
``client.beta.sessions.events.tool_runner`` (the sessions-side
:class:`~anthropic.lib.tools._beta_session_runner.SessionToolRunner`) do the
same three small things: index the supplied tools by name, run a runnable tool
over a JSON input, and turn an exception raised by a tool into tool-result
content. Those steps are factored out here so the two runners stay consistent
instead of each carrying its own copy. Consumed by the runner helpers only.
"""

from __future__ import annotations

import inspect
from typing import Union, TypeVar, Iterable, Awaitable
from typing_extensions import Protocol

from ._beta_functions import ToolError, BetaFunctionToolResultType
from ...types.beta.beta_message_param import BetaMessageParam
from ...types.beta.beta_content_block_param import BetaContentBlockParam
from ...types.beta.beta_request_tool_removal_block_param import (
    Tool as _ToolChangeReference,
    BetaRequestToolRemovalBlockParam,
)
from ...types.beta.beta_request_tool_addition_block_param import BetaRequestToolAdditionBlockParam

__all__ = ["tool_registry", "tool_error_content", "run_runnable_tool", "available_tool_names"]


class _NamedTool(Protocol):
    """Anything with a ``name`` — the shape :func:`tool_registry` indexes on."""

    @property
    def name(self) -> str: ...


class _CallableTool(Protocol):
    """A runnable tool: ``call`` may be sync or async (it returns either the
    result or an awaitable of it)."""

    def call(self, input: object) -> Union[BetaFunctionToolResultType, Awaitable[BetaFunctionToolResultType]]: ...


NamedToolT = TypeVar("NamedToolT", bound=_NamedTool)


def tool_registry(tools: Iterable[NamedToolT]) -> dict[str, NamedToolT]:
    """Index ``tools`` by their ``name`` for O(1) dispatch lookup.

    On a duplicate name the later tool wins, matching a plain dict comprehension.
    """
    return {tool.name: tool for tool in tools}


def available_tool_names(messages: Iterable[BetaMessageParam], tool_names: Iterable[str]) -> set[str]:
    """Fold mid-conversation ``tool_removal`` / ``tool_addition`` blocks over
    the locally runnable ``tool_names``.

    Only ``role: "system"`` messages carry these blocks, and only a
    ``tool_reference`` can name a locally runnable tool — MCP references are
    executed server-side, so they (and any unknown block/reference type) are
    ignored rather than raising.
    """
    available = set(tool_names)
    for message in messages:
        content = message["content"]
        if message["role"] != "system" or isinstance(content, str):
            continue
        for block in content:
            _apply_tool_change(block, available)
    return available


def _apply_tool_change(block: BetaContentBlockParam, available: set[str]) -> None:
    """Apply a single ``tool_removal`` / ``tool_addition`` block to ``available``.

    A ``mid_conv_system`` block's ``content`` is limited by the API schema to
    ``text`` / ``tool_addition`` / ``tool_removal``, so exactly one level is
    walked (no deeper nesting exists); every other block type is a no-op.
    """
    if not isinstance(block, dict):
        # ``BetaContentBlockParam`` also admits response-side content-block
        # models; ``tool_removal`` / ``tool_addition`` are request-only
        # TypedDicts, so a non-dict block is never one of them.
        return
    if block["type"] == "tool_removal" or block["type"] == "tool_addition":
        _apply_tool_reference_change(block, available)
    elif block["type"] == "mid_conv_system":
        for inner in block["content"]:
            # schema-bounded to text/tool_addition/tool_removal: one level, no recursion
            if inner["type"] == "tool_removal" or inner["type"] == "tool_addition":
                _apply_tool_reference_change(inner, available)
    else:
        pass  # other/unknown block types are ignored (forward compatibility)


def _apply_tool_reference_change(
    block: Union[BetaRequestToolRemovalBlockParam, BetaRequestToolAdditionBlockParam], available: set[str]
) -> None:
    """Fold one ``tool_removal`` / ``tool_addition`` block into ``available``."""
    name = _referenced_tool_name(block["tool"])
    if name is None:
        return
    if block["type"] == "tool_removal":
        available.discard(name)  # removing an absent name is a set no-op
    else:
        available.add(name)  # add unconditionally: dispatch still requires a registry hit


def _referenced_tool_name(ref: _ToolChangeReference) -> str | None:
    """The locally runnable tool name a tool-change reference resolves to.

    Only ``tool_reference`` names a runnable tool; ``mcp_tool_reference`` /
    ``mcp_toolset_reference`` execute server-side and unknown reference types
    are ignored (forward compatibility), so all of those resolve to ``None``.
    """
    if ref["type"] == "tool_reference":
        return ref["name"]
    return None


def tool_error_content(exc: BaseException) -> BetaFunctionToolResultType:
    """Render an exception raised by a tool as tool-result content.

    A :class:`ToolError` carries its own structured content; anything else is
    rendered with ``repr`` (which, unlike ``str``, keeps the exception type).
    The caller owns the ``is_error`` flag and any logging.
    """
    if isinstance(exc, ToolError):
        return exc.content
    return repr(exc)


async def run_runnable_tool(tool: _CallableTool, input: dict[str, object]) -> BetaFunctionToolResultType:
    """Call ``tool`` with ``input``, awaiting the result if the tool is async.

    Bridges the sync (:class:`~anthropic.lib.tools.BetaFunctionTool`) and async
    (:class:`~anthropic.lib.tools.BetaAsyncFunctionTool`) runnable-tool shapes
    behind a single ``await``.
    """
    result = tool.call(input)
    if inspect.isawaitable(result):
        return await result
    return result
