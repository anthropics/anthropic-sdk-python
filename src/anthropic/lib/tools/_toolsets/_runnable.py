"""Runnable-toolset contract for the toolset families (`browser_toolset_20260801`, `computer_toolset_20260801`).

A toolset is one nameless `tools[]` entry declaring a family of member tools. Each member call
is its own `tool_use` whose `name` is the member and whose `toolset_name` is the family
(`"browser"`, `"computer"`), and the `tool_result` echoes `toolset_name`. Member names are not reserved (a
custom tool may be called `navigate`, and the two families share names such as `screenshot`), so dispatch keys on
`(toolset_name, name)`, never on `name` alone.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from types import TracebackType, MappingProxyType
from typing import Any, Literal, TypeVar, ClassVar, TypeAlias, cast
from collections.abc import Mapping, Sequence
from typing_extensions import Self

import pydantic

from ._errors import ToolsetUsageError, ToolsetClosedError, ToolsetContractError
from ._sanitize import log_safe, error_text, well_formed, error_text_content
from ...._compat import PYDANTIC_V1
from ...._models import BaseModel
from ....types.beta import (
    BetaToolUseBlock,
    BetaToolResultBlockParam,
    BetaBrowserToolset20260801Param,
    BetaComputerToolset20260801Param,
)
from .._beta_functions import ToolError
from ....types.beta.beta_tool_result_block_param import Content

__all__ = [
    "ToolsetFamily",
    "BetaToolsetParam",
    "BetaToolsetContent",
    "BetaToolsetCallContext",
    "unvalidated",
    "BetaRunnableToolset",
    "BetaAsyncRunnableToolset",
    "BetaAnyRunnableToolset",
    "TOOLSET_CLASSES",
    "toolset_result_block",
    "classify",
    "hook_refusal",
    "member_error_result",
    "not_executed_result",
    "NOT_EXECUTED",
    "HALT_TEXT",
]

ToolsetFamily: TypeAlias = Literal["browser", "computer"]

BetaToolsetParam: TypeAlias = BetaBrowserToolset20260801Param | BetaComputerToolset20260801Param

BetaToolsetContent: TypeAlias = list[Content]
"""The `tool_result` content a member call renders to."""

log = logging.getLogger(__name__)


_ModelT = TypeVar("_ModelT", bound=pydantic.BaseModel)


def unvalidated(cls: type[_ModelT], **values: Any) -> _ModelT:
    """Build one of the SDK's own context or report models around objects that already exist (a parsed `tool_use`
    block, a member's input model, a driver's report) without validating: pydantic's raw constructor, so nothing is
    copied, coerced into a sibling union member, or stripped of keys the SDK does not declare. The SDK base class's
    `construct` still coerces union and typed-dict fields, which is why it is not used here."""
    if PYDANTIC_V1:
        return cast("_ModelT", pydantic.BaseModel.construct.__func__(cls, **values))  # type: ignore[attr-defined]
    return cast("_ModelT", pydantic.BaseModel.model_construct.__func__(cls, **values))  # type: ignore[attr-defined]


class BetaToolsetCallContext(BaseModel):
    """What a member receives alongside its input: the `tool_use` block the call answers
    (`context.tool_use.id`). `None` only when a member is invoked outside any model call."""

    tool_use: BetaToolUseBlock | None = None


class BaseRunnableToolset(ABC):
    toolset_name: ClassVar[ToolsetFamily]
    """The family this toolset answers for, matched against `tool_use.toolset_name`."""

    _toolset_closed: bool = False
    """Set once `close()` ran (directly or through a `with` block). A member call on a closed toolset raises
    `ToolsetClosedError` at your code instead of answering the model."""

    def _toolset_refuse_if_closed(self) -> None:
        if self._toolset_closed:
            raise ToolsetClosedError(f"this {self.toolset_name!r} toolset is closed")

    @abstractmethod
    def to_dict(self) -> BetaToolsetParam:
        """The `tools[]` entry to send. SDK-side behaviour options never appear here."""
        ...

    def _toolset_check_tool_use(self, tool_use: BetaToolUseBlock) -> None:
        # A block without `toolset_name` is a plain tool (possibly a custom tool sharing a member
        # name) and must never be routed here.
        if tool_use.toolset_name != self.toolset_name:
            raise ToolsetContractError(
                f"tool_use {tool_use.id!r} (toolset_name={tool_use.toolset_name!r}, name={tool_use.name!r}) "
                f"is not a member call of the {self.toolset_name!r} toolset"
            )


class BetaRunnableToolset(BaseRunnableToolset):
    @abstractmethod
    def call(self, context: BetaToolsetCallContext, name: str, input: Mapping[str, object]) -> str | BetaToolsetContent:
        """Execute member `name` with the raw `tool_use.input` and return the tool-result
        content. Raise `anthropic.lib.tools.ToolError` for a model-visible failure."""
        ...

    def close(self) -> None:
        """Release any resource the toolset holds (a browser, a socket, a subprocess) when you are done with it.
        The tool runner never closes a toolset, so one instance can serve several runs. Marks the toolset closed (a
        member call afterwards raises `ToolsetClosedError`), and toolsets built on the SDK's abstract classes also
        wait for queued and in-flight member calls to settle. Override it in a toolset that owns a resource and call
        `super().close()` first. `with toolset:` calls it for you."""
        self._toolset_closed = True

    def __enter__(self) -> Self:
        self._toolset_refuse_if_closed()
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
    ) -> None:
        if self._toolset_closed:
            return  # closed inside the block already, so close only once
        try:
            self.close()
        finally:
            self._toolset_closed = True

    def tool_result(self, tool_use: BetaToolUseBlock) -> BetaToolResultBlockParam:
        """Run one member `tool_use` and build its `tool_result` block, for callers driving
        `messages.create` themselves.

        Follows the tool runner's rule: a `ToolsetUsageError` propagates, a
        `ToolError` or any other exception becomes an `is_error` result.
        """
        self._toolset_check_tool_use(tool_use)
        self._toolset_refuse_if_closed()
        try:
            content = self.call(unvalidated(BetaToolsetCallContext, tool_use=tool_use), tool_use.name, tool_use.input)
        except Exception as exc:
            return member_error_result(tool_use, exc)
        return toolset_result_block(tool_use, content)


class BetaAsyncRunnableToolset(BaseRunnableToolset):
    @abstractmethod
    async def call(
        self, context: BetaToolsetCallContext, name: str, input: Mapping[str, object]
    ) -> str | BetaToolsetContent: ...

    async def close(self) -> None:
        """Release any resource the toolset holds when you are done with it. The tool runner never closes a
        toolset. The default only marks the toolset closed. Override it in a toolset that owns a resource and
        `await super().close()`. `async with toolset:` awaits it for you."""
        self._toolset_closed = True

    async def __aenter__(self) -> Self:
        self._toolset_refuse_if_closed()
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
    ) -> None:
        if self._toolset_closed:
            return
        try:
            await self.close()
        finally:
            self._toolset_closed = True

    async def tool_result(self, tool_use: BetaToolUseBlock) -> BetaToolResultBlockParam:
        self._toolset_check_tool_use(tool_use)
        self._toolset_refuse_if_closed()
        try:
            content = await self.call(
                unvalidated(BetaToolsetCallContext, tool_use=tool_use), tool_use.name, tool_use.input
            )
        except Exception as exc:
            # Cancellation is a BaseException and propagates untouched, so the call aborts rather
            # than being answered.
            return member_error_result(tool_use, exc)
        return toolset_result_block(tool_use, content)


BetaAnyRunnableToolset: TypeAlias = BetaRunnableToolset | BetaAsyncRunnableToolset
TOOLSET_CLASSES = (BetaRunnableToolset, BetaAsyncRunnableToolset)
"""The classes that identify a toolset entry in an `isinstance` check, sync or async."""


NOT_EXECUTED = "Not executed: an earlier action in this turn failed."
"""What the runner answers for a toolset member it did not run because an earlier member of the same toolset failed
in the same assistant turn: the model planned those actions as a sequence, and a later one rarely makes sense once
an earlier one did not happen."""

HALT_TEXT: Mapping[str, str] = MappingProxyType(
    {"browser": NOT_EXECUTED, "computer": "Not executed: an earlier computer action in this turn failed."}
)
"""Each family's wording of `NOT_EXECUTED`, by `toolset_name`. The wording is the API's and differs per family.
`NOT_EXECUTED` is the browser's, and the fallback for a `toolset_name` not in `HALT_TEXT`."""


def not_executed_result(tool_use: BetaToolUseBlock) -> BetaToolResultBlockParam:
    return toolset_result_block(tool_use, HALT_TEXT.get(tool_use.toolset_name or "", NOT_EXECUTED), is_error=True)


def classify(exc: Exception) -> ToolError:
    """The rule for an exception out of a member call, at the `execute` boundary and in the runner alike: a
    `ToolsetUsageError` propagates, a `ToolError` is the member's own refusal, and anything else a driver raises,
    its `TypeError` included, becomes a refusal the model reads, so the loop continues. The text is returned whole,
    so it can be checked before it is cut. Cancellation is a `BaseException` and never reaches here."""
    if isinstance(exc, ToolsetUsageError):
        raise exc
    if isinstance(exc, ToolError):
        return exc
    # A browser toolset member's error reads as the type and the message, not `repr`: `repr` writes a line break as
    # `\n`, which hides the break from the path check, and shows constructor arguments that the message leaves out.
    name = type(exc).__name__
    try:
        message = str(exc)
    except Exception:
        message = ""  # a broken `__str__` still gives the model the type
    return ToolError(well_formed(f"{name}: {message}" if message else name))


def hook_refusal(exc: Exception, fallback: ToolError) -> ToolError:
    """The rule for an exception out of a developer hook (`confirm`, `url_policy`, the file policy): a
    `ToolsetUsageError` stops the run, a `ToolError` is the hook's own refusal and is returned as raised, and
    anything else fails closed as `fallback`: its own message may contain the address or path being withheld,
    so the model reads the fallback's text instead and the traceback goes to the log."""
    error = classify(exc)
    if error is not exc:
        log.exception("A toolset hook raised; failing closed with %r", str(fallback), exc_info=exc)
        error = fallback
    return error


def member_error_result(tool_use: BetaToolUseBlock, exc: Exception) -> BetaToolResultBlockParam:
    """`classify` for the runner: the refusal as an `is_error` result, an unexpected exception logged first."""
    error = classify(exc)
    content = error.content
    if error is not exc:
        # The names are model output and the exception text may contain page content: the log line gets the names with
        # control characters folded (no forged log records), the model gets the text bounded.
        log.exception(
            "Error occurred while calling toolset member: %s/%s",
            log_safe(tool_use.toolset_name),
            log_safe(tool_use.name),
            exc_info=exc,
        )
        content = error_text(exc)
    return toolset_result_block(tool_use, error_text_content(content), is_error=True)


def toolset_result_block(
    tool_use: BetaToolUseBlock,
    content: str | Sequence[Content],
    *,
    is_error: bool = False,
) -> BetaToolResultBlockParam:
    """The `tool_result` answering a member `tool_use`. `toolset_name` is required on a member
    result (the API rejects a mismatch), so it is echoed on error paths too."""
    if is_error and not content:
        # The API rejects an is_error result with empty content, ending the loop instead of showing
        # the model the error. An empty ToolError (str(TimeoutError()) is "") reaches here.
        content = "The tool call failed with an empty error message."
    block: BetaToolResultBlockParam = {
        "type": "tool_result",
        "tool_use_id": tool_use.id,
        "toolset_name": tool_use.toolset_name,
        "content": content,
    }
    if is_error:
        block["is_error"] = True
    return block
