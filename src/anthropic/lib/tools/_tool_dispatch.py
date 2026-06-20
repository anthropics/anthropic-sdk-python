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

__all__ = ["tool_registry", "tool_error_content", "run_runnable_tool"]


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
