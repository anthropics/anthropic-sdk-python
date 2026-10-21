"""The computer toolset interface: `BetaAbstractComputerToolset20260801` and its async twin.

A driver subclasses one of them and overrides the members its backend supports; a member it does
not override is reported to the API as disabled and, if the model calls it anyway, answered with an
`is_error` result.
"""

from __future__ import annotations

import copy
from typing import Any, TypeVar, cast
from collections.abc import Mapping
from typing_extensions import override

from ._base import (
    BaseToolset,
    BaseSyncToolset,
    BetaToolConfigs,
    BaseAsyncToolset,
    BaseToolsetOptions,
    BetaScreenshotResult,
    parse_input,
    bounded_error,
)
from ._errors import ToolsetConfigError, UnavailableMemberError, InvalidMemberInputError
from ._render import action_line, render_result
from ._runnable import BetaToolsetContent, BetaToolsetCallContext, classify, unvalidated
from ._sanitize import FIELD_MAX, folded
from ....types.beta import (
    BetaComputerKeyInput,
    BetaComputerTypeInput,
    BetaComputerWaitInput,
    BetaComputerZoomInput,
    BetaComputerScrollInput,
    BetaComputerHoldKeyInput,
    BetaComputerLeftClickInput,
    BetaComputerMouseMoveInput,
    BetaComputerRightClickInput,
    BetaComputerDoubleClickInput,
    BetaComputerMiddleClickInput,
    BetaComputerTripleClickInput,
    BetaComputerLeftClickDragInput,
    BetaComputerToolsetConfigsParam,
    BetaComputerToolset20260801Param,
)
from .._beta_functions import ToolError, BetaFunctionToolResultType
from ._computer_inputs import (
    BetaComputerMemberName,
    BetaComputerMemberInput,
    BetaComputerScreenshotInput,
    BetaComputerLeftMouseUpInput,
    BetaComputerLeftMouseDownInput,
    BetaComputerCursorPositionInput,
)
from ._computer_results import (
    BetaComputerMemberResult,
    BetaComputerConfirmContext,
    BetaComputerConfirmCallable,
    BetaAsyncComputerConfirmCallable,
    BetaComputerCursorPositionResult,
)
from ._computer_registry import FAMILY, COMPUTER, TOOLSET_TYPE, CONFIRM_REQUIRED, ComputerMember

__all__ = ["BetaAbstractComputerToolset20260801", "BetaAsyncAbstractComputerToolset20260801"]

_ConfirmT = TypeVar("_ConfirmT", bound=BetaComputerConfirmCallable | BetaAsyncComputerConfirmCallable)


class ComputerOptions(BaseToolsetOptions[BetaComputerMemberName, BetaComputerMemberInput, _ConfirmT]):
    """The constructor options of computer toolset class `cls`, validated and resolved once at construction; a
    mistake in them raises `ToolsetConfigError` here, and so does a missing `confirm` while `type`, `key` or `hold_key`
    is enabled. The computer toolset has no options beyond the ones every family has (`BaseToolsetOptions`)."""

    def __init__(
        self,
        cls: type[BaseToolset[Any, Any, Any]],
        *,
        configs: BetaComputerToolsetConfigsParam | None,
        confirm: _ConfirmT | None,
        tool_configs: BetaToolConfigs | None,
    ) -> None:
        super().__init__(
            cls,
            registry=COMPUTER,
            default_bodies=DEFAULT_BODIES,
            configs=configs,
            confirm=confirm,
            tool_configs=tool_configs,
        )

        required = sorted(name for name in CONFIRM_REQUIRED if name in self.served and self.is_enabled(name))
        if required and confirm is None:
            # a toolset that serves `type`, `key` or `hold_key` needs a `confirm`, unless `configs` turns them off
            raise ToolsetConfigError(
                f"{required!r} requires a confirm callable: pass confirm=<callable>, or disable it in configs"
            )


class BaseComputerToolset(BaseToolset[BetaComputerMemberName, BetaComputerMemberInput, _ConfirmT]):
    """What the synchronous and asynchronous computer toolsets share: the options resolved at construction and the
    `tools[]` entry built from them. Subclass one of the two public classes, not this one."""

    toolset_name = FAMILY

    def __init__(
        self,
        *,
        configs: BetaComputerToolsetConfigsParam | None,
        confirm: _ConfirmT | None,
        tool_configs: BetaToolConfigs | None,
    ) -> None:
        self._toolset_options: ComputerOptions[_ConfirmT] = ComputerOptions(
            type(self), configs=configs, confirm=confirm, tool_configs=tool_configs
        )
        super().__init__(self._toolset_options)

    @override
    def to_dict(self) -> BetaComputerToolset20260801Param:
        options = self._toolset_options
        # fresh copies each call: the runner keeps what to_dict() returns, so a later in-place edit must not reach it
        param = cast(BetaComputerToolset20260801Param, {**copy.deepcopy(options.tool_configs), "type": TOOLSET_TYPE})
        if options.wire_configs is not None:
            param["configs"] = cast("BetaComputerToolsetConfigsParam", copy.deepcopy(options.wire_configs))
        return param

    @property
    def configs(self) -> BetaComputerToolsetConfigsParam | None:
        """The wire `configs`: yours, plus `enabled: False` for every member this class does not serve — what
        `to_dict()` sends. A copy: nothing you do to it changes the toolset."""
        return self.to_dict().get("configs")


class BetaAbstractComputerToolset20260801(
    BaseComputerToolset[BetaComputerConfirmCallable],
    BaseSyncToolset[BetaComputerMemberName, BetaComputerMemberInput, BetaComputerConfirmCallable],
):
    """The synchronous computer toolset for `computer_toolset_20260801`.

    Subclass it and override the members your desktop supports. Each takes `(context, input)` and returns the
    result type in its signature:

    - A pure action (a click, typing, scrolling) returns nothing, or one line of text. The SDK folds that text to
      one line and bounds its length. The model reads it in a text block of its own, after the SDK's fixed
      acknowledgment (`Clicked.`).
    - `screenshot` and `zoom` return an image that already fits the model's image limits.
    - `cursor_position` returns the cursor in screenshot pixels.

    Read "Running a computer toolset safely" in the SDK guide (`computer-toolset.md`) before deploying one.
    """

    _toolset_twin = "BetaAsyncAbstractComputerToolset20260801"

    def __init__(
        self,
        *,
        configs: BetaComputerToolsetConfigsParam | None = None,
        confirm: BetaComputerConfirmCallable | None = None,
        tool_configs: BetaToolConfigs | None = None,
    ) -> None:
        """A computer toolset with the given options; a mistake in them raises `ToolsetConfigError` here.

        Args:
            configs: The `configs` object of the `tools[]` entry, sent as given:
                `{"<member>": {"enabled": bool, "defer_loading": bool}}`. This is how a member is
                switched on or off; the SDK adds `enabled: False` for every member the subclass
                does not implement and never dispatches a disabled member. A subclass that overrides
                `execute` serves every member; turn off the ones it does not serve here. Every member is on by
                default.
            confirm: `(context) -> bool`, called before every member call the SDK is about to run (never for a
                call already refused). Required while `type`, `key` or `hold_key` is enabled, and optional
                otherwise. Return `True` to run the call, `False` to answer the model with a refusal; decide by
                `context.member` which members actually prompt a person. `context` also carries the parsed `input`.
            tool_configs: Optional fields set on the `tools[]` entry itself rather than on a member:
                `{"cache_control": {"type": "ephemeral"}}`.
        """
        super().__init__(configs=configs, confirm=confirm, tool_configs=tool_configs)

    @override
    def _toolset_run(
        self, context: BetaToolsetCallContext, name: str, input: Mapping[str, object]
    ) -> BetaToolsetContent:
        try:
            member = self._toolset_options.resolve(name)
            parsed = parse_computer_input(member, input)
            self._toolset_confirm(member.name, confirm_context(context, member, parsed))
            try:
                result = self.execute(context, member.name, parsed)
            except Exception as exc:
                # The driver's own error text reaches the model, cut to the field limit.
                error = bounded_error(classify(exc))
                if error is exc:
                    raise
                raise error from exc
            return render_result(member, parsed, bounded_result(member, result))
        except ToolError as exc:
            raise ToolError(raised_content(bounded_error(exc))) from exc

    def execute(
        self, context: BetaToolsetCallContext, name: BetaComputerMemberName, input: BetaComputerMemberInput
    ) -> BetaComputerMemberResult:
        """Dispatch one member call to its method. Override it, calling `super().execute(context, name, input)`, for
        before/after hooks around every member; `confirm` has already run and the result is rendered from what the
        override returns."""
        return self._toolset_member_method(name)(context, input)

    def key(self, context: BetaToolsetCallContext, input: BetaComputerKeyInput) -> str | None:
        raise UnavailableMemberError("key", family=FAMILY)

    def hold_key(self, context: BetaToolsetCallContext, input: BetaComputerHoldKeyInput) -> str | None:
        raise UnavailableMemberError("hold_key", family=FAMILY)

    def type(self, context: BetaToolsetCallContext, input: BetaComputerTypeInput) -> str | None:
        raise UnavailableMemberError("type", family=FAMILY)

    def cursor_position(
        self, context: BetaToolsetCallContext, input: BetaComputerCursorPositionInput
    ) -> BetaComputerCursorPositionResult:
        raise UnavailableMemberError("cursor_position", family=FAMILY)

    def mouse_move(self, context: BetaToolsetCallContext, input: BetaComputerMouseMoveInput) -> str | None:
        raise UnavailableMemberError("mouse_move", family=FAMILY)

    def left_mouse_down(self, context: BetaToolsetCallContext, input: BetaComputerLeftMouseDownInput) -> str | None:
        raise UnavailableMemberError("left_mouse_down", family=FAMILY)

    def left_mouse_up(self, context: BetaToolsetCallContext, input: BetaComputerLeftMouseUpInput) -> str | None:
        raise UnavailableMemberError("left_mouse_up", family=FAMILY)

    def left_click(self, context: BetaToolsetCallContext, input: BetaComputerLeftClickInput) -> str | None:
        raise UnavailableMemberError("left_click", family=FAMILY)

    def left_click_drag(self, context: BetaToolsetCallContext, input: BetaComputerLeftClickDragInput) -> str | None:
        raise UnavailableMemberError("left_click_drag", family=FAMILY)

    def right_click(self, context: BetaToolsetCallContext, input: BetaComputerRightClickInput) -> str | None:
        raise UnavailableMemberError("right_click", family=FAMILY)

    def middle_click(self, context: BetaToolsetCallContext, input: BetaComputerMiddleClickInput) -> str | None:
        raise UnavailableMemberError("middle_click", family=FAMILY)

    def double_click(self, context: BetaToolsetCallContext, input: BetaComputerDoubleClickInput) -> str | None:
        raise UnavailableMemberError("double_click", family=FAMILY)

    def triple_click(self, context: BetaToolsetCallContext, input: BetaComputerTripleClickInput) -> str | None:
        raise UnavailableMemberError("triple_click", family=FAMILY)

    def scroll(self, context: BetaToolsetCallContext, input: BetaComputerScrollInput) -> str | None:
        raise UnavailableMemberError("scroll", family=FAMILY)

    def wait(self, context: BetaToolsetCallContext, input: BetaComputerWaitInput) -> str | None:
        raise UnavailableMemberError("wait", family=FAMILY)

    def screenshot(self, context: BetaToolsetCallContext, input: BetaComputerScreenshotInput) -> BetaScreenshotResult:
        raise UnavailableMemberError("screenshot", family=FAMILY)

    def zoom(self, context: BetaToolsetCallContext, input: BetaComputerZoomInput) -> BetaScreenshotResult:
        raise UnavailableMemberError("zoom", family=FAMILY)


class BetaAsyncAbstractComputerToolset20260801(
    BaseComputerToolset[BetaAsyncComputerConfirmCallable],
    BaseAsyncToolset[BetaComputerMemberName, BetaComputerMemberInput, BetaAsyncComputerConfirmCallable],
):
    """The asynchronous computer toolset for `computer_toolset_20260801`, for `AsyncAnthropic`.

    Identical to `BetaAbstractComputerToolset20260801` except that members are async (a sync one is a contract
    error), `confirm` may be either, and `close` (also the async context-manager exit) is awaited.
    """

    _toolset_twin = "BetaAbstractComputerToolset20260801"

    def __init__(
        self,
        *,
        configs: BetaComputerToolsetConfigsParam | None = None,
        confirm: BetaAsyncComputerConfirmCallable | None = None,
        tool_configs: BetaToolConfigs | None = None,
    ) -> None:
        """An asynchronous computer toolset with the given options; `confirm` may be a plain or an `async` callable
        here. A mistake in the options raises `ToolsetConfigError`.

        Args:
            configs: The `configs` object of the `tools[]` entry, sent as given:
                `{"<member>": {"enabled": bool, "defer_loading": bool}}`. This is how a member is
                switched on or off; the SDK adds `enabled: False` for every member the subclass
                does not implement and never dispatches a disabled member. A subclass that overrides
                `execute` serves every member; turn off the ones it does not serve here. Every member is on by
                default.
            confirm: `(context) -> bool`, called before every member call the SDK is about to run (never for a
                call already refused). Required while `type`, `key` or `hold_key` is enabled, and optional
                otherwise. Return `True` to run the call, `False` to answer the model with a refusal; decide by
                `context.member` which members actually prompt a person. `context` also carries the parsed `input`.
            tool_configs: Optional fields set on the `tools[]` entry itself rather than on a member:
                `{"cache_control": {"type": "ephemeral"}}`.
        """
        super().__init__(configs=configs, confirm=confirm, tool_configs=tool_configs)

    @override
    async def _toolset_run(
        self, context: BetaToolsetCallContext, name: str, input: Mapping[str, object]
    ) -> BetaToolsetContent:
        try:
            member = self._toolset_options.resolve(name)
            parsed = parse_computer_input(member, input)
            await self._toolset_confirm(member.name, confirm_context(context, member, parsed))
            try:
                result = await self.execute(context, member.name, parsed)
            except Exception as exc:
                error = bounded_error(classify(exc))
                if error is exc:
                    raise
                raise error from exc
            return render_result(member, parsed, bounded_result(member, result))
        except ToolError as exc:
            raise ToolError(raised_content(bounded_error(exc))) from exc

    async def execute(
        self, context: BetaToolsetCallContext, name: BetaComputerMemberName, input: BetaComputerMemberInput
    ) -> BetaComputerMemberResult:
        """Dispatch one member call to its method; see the synchronous class's `execute`. Members are
        async here; one written sync is a contract error."""
        return await self._toolset_member_method(name)(context, input)

    async def key(self, context: BetaToolsetCallContext, input: BetaComputerKeyInput) -> str | None:
        raise UnavailableMemberError("key", family=FAMILY)

    async def hold_key(self, context: BetaToolsetCallContext, input: BetaComputerHoldKeyInput) -> str | None:
        raise UnavailableMemberError("hold_key", family=FAMILY)

    async def type(self, context: BetaToolsetCallContext, input: BetaComputerTypeInput) -> str | None:
        raise UnavailableMemberError("type", family=FAMILY)

    async def cursor_position(
        self, context: BetaToolsetCallContext, input: BetaComputerCursorPositionInput
    ) -> BetaComputerCursorPositionResult:
        raise UnavailableMemberError("cursor_position", family=FAMILY)

    async def mouse_move(self, context: BetaToolsetCallContext, input: BetaComputerMouseMoveInput) -> str | None:
        raise UnavailableMemberError("mouse_move", family=FAMILY)

    async def left_mouse_down(
        self, context: BetaToolsetCallContext, input: BetaComputerLeftMouseDownInput
    ) -> str | None:
        raise UnavailableMemberError("left_mouse_down", family=FAMILY)

    async def left_mouse_up(self, context: BetaToolsetCallContext, input: BetaComputerLeftMouseUpInput) -> str | None:
        raise UnavailableMemberError("left_mouse_up", family=FAMILY)

    async def left_click(self, context: BetaToolsetCallContext, input: BetaComputerLeftClickInput) -> str | None:
        raise UnavailableMemberError("left_click", family=FAMILY)

    async def left_click_drag(
        self, context: BetaToolsetCallContext, input: BetaComputerLeftClickDragInput
    ) -> str | None:
        raise UnavailableMemberError("left_click_drag", family=FAMILY)

    async def right_click(self, context: BetaToolsetCallContext, input: BetaComputerRightClickInput) -> str | None:
        raise UnavailableMemberError("right_click", family=FAMILY)

    async def middle_click(self, context: BetaToolsetCallContext, input: BetaComputerMiddleClickInput) -> str | None:
        raise UnavailableMemberError("middle_click", family=FAMILY)

    async def double_click(self, context: BetaToolsetCallContext, input: BetaComputerDoubleClickInput) -> str | None:
        raise UnavailableMemberError("double_click", family=FAMILY)

    async def triple_click(self, context: BetaToolsetCallContext, input: BetaComputerTripleClickInput) -> str | None:
        raise UnavailableMemberError("triple_click", family=FAMILY)

    async def scroll(self, context: BetaToolsetCallContext, input: BetaComputerScrollInput) -> str | None:
        raise UnavailableMemberError("scroll", family=FAMILY)

    async def wait(self, context: BetaToolsetCallContext, input: BetaComputerWaitInput) -> str | None:
        raise UnavailableMemberError("wait", family=FAMILY)

    async def screenshot(
        self, context: BetaToolsetCallContext, input: BetaComputerScreenshotInput
    ) -> BetaScreenshotResult:
        raise UnavailableMemberError("screenshot", family=FAMILY)

    async def zoom(self, context: BetaToolsetCallContext, input: BetaComputerZoomInput) -> BetaScreenshotResult:
        raise UnavailableMemberError("zoom", family=FAMILY)


DEFAULT_BODIES: frozenset[object] = frozenset(
    getattr(cls, name)
    for cls in (BetaAbstractComputerToolset20260801, BetaAsyncAbstractComputerToolset20260801)
    for name in (*COMPUTER.names, "execute")
)
"""The two abstract classes' own member and `execute` bodies: a subclass whose attribute is still one of these did
not override it."""

SHAPES = (("coordinate", "[x, y]", 2), ("start_coordinate", "[x, y]", 2), ("region", "[x0, y0, x1, y1]", 4))
"""The list-valued input fields, the shape the model is told to send, and the length that shape has."""


def parse_computer_input(member: ComputerMember, raw: Mapping[str, object]) -> BetaComputerMemberInput:
    """`parse_input` for a computer member, plus the shape of each coordinate list: the generated models type them
    as lists of integers of any length, and a driver indexes them."""
    parsed = parse_input(member, raw, family=FAMILY)
    problems = [
        f"{field}: expected {shape}"
        for field, shape, length in SHAPES
        if (value := getattr(parsed, field, None)) is not None and len(value) != length
    ]
    if problems:
        raise InvalidMemberInputError(member.name, "; ".join(problems), family=FAMILY)
    return parsed


def bounded_result(member: ComputerMember, result: BetaComputerMemberResult) -> BetaComputerMemberResult:
    """`result` as it is rendered: the line a pure action returned is folded to one line and cut, so one that is only
    whitespace or control characters becomes the empty string and renders as the acknowledgment alone, as the browser
    toolset's does, instead of as a text block that carries nothing. Anything else is kept as returned."""
    line = action_line(member, result)
    return result if line is None else folded(line)[:FIELD_MAX]


def raised_content(error: ToolError) -> BetaFunctionToolResultType:
    """The content `call()` raises for a refusal or failure. A string becomes one text block. A list of blocks is kept
    as raised, images included. `tool_result()` later keeps only the text blocks."""
    content = error.content
    return [{"type": "text", "text": content}] if isinstance(content, str) else content


def confirm_context(
    context: BetaToolsetCallContext, member: ComputerMember, input: BetaComputerMemberInput
) -> BetaComputerConfirmContext:
    """What the `confirm` callable is told: the member, its parsed input and the `tool_use` being answered. Built
    from values the pipeline already holds, so nothing here is validated again."""
    return unvalidated(BetaComputerConfirmContext, tool_use=context.tool_use, member=member.name, input=input)
