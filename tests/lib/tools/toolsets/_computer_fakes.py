"""In-memory computer toolsets for the computer toolset tests: a handful of members over a scripted desktop that
tracks the cursor and logs every call. The sync and async fakes drive the same `Desktop`."""

from __future__ import annotations

from typing import Any
from typing_extensions import override

from anthropic.types.beta import (
    BetaComputerKeyInput,
    BetaComputerTypeInput,
    BetaComputerWaitInput,
    BetaComputerZoomInput,
    BetaComputerScrollInput,
    BetaComputerHoldKeyInput,
    BetaComputerLeftClickInput,
    BetaComputerMouseMoveInput,
    BetaComputerScreenshotInput,
    BetaComputerLeftClickDragInput,
    BetaComputerCursorPositionInput,
)
from anthropic.tools.computer import (
    BetaScreenshotResult,
    BetaToolsetCallContext,
    BetaComputerCursorPositionResult,
    BetaAbstractComputerToolset20260801,
    BetaAsyncAbstractComputerToolset20260801,
)

PNG = "iVBORw0KGgo="


class Desktop:
    """The desktop both fakes drive: the cursor, a call log, and what each member hands back."""

    def __init__(self) -> None:
        self.cursor = (0, 0)
        self.calls: list[str] = []
        self.inputs: list[Any] = []
        self.contexts: list[BetaToolsetCallContext] = []
        self.fail: dict[str, BaseException] = {}
        self.results: dict[str, Any] = {}  # a member name -> the result to hand back instead of the usual one

    def do(self, name: str, context: BetaToolsetCallContext, input: Any) -> Any:
        self.calls.append(name)
        self.inputs.append(input)
        self.contexts.append(context)
        if name in self.fail:
            raise self.fail[name]
        return self.results.get(name)

    # member bodies -------------------------------------------------------------------------

    def screenshot(self, context: BetaToolsetCallContext, input: BetaComputerScreenshotInput) -> BetaScreenshotResult:
        return self.do("screenshot", context, input) or BetaScreenshotResult(data=PNG)

    def zoom(self, context: BetaToolsetCallContext, input: BetaComputerZoomInput) -> BetaScreenshotResult:
        return self.do("zoom", context, input) or BetaScreenshotResult(data=PNG, media_type="image/jpeg")

    def cursor_position(
        self, context: BetaToolsetCallContext, input: BetaComputerCursorPositionInput
    ) -> BetaComputerCursorPositionResult:
        x, y = self.cursor
        return self.do("cursor_position", context, input) or BetaComputerCursorPositionResult(x=x, y=y)

    def mouse_move(self, context: BetaToolsetCallContext, input: BetaComputerMouseMoveInput) -> str | None:
        self.cursor = (input.coordinate[0], input.coordinate[1])
        return self.do("mouse_move", context, input)

    def action(self, name: str, context: BetaToolsetCallContext, input: Any) -> Any:
        return self.do(name, context, input)  # a pure action may hand back one line of text


def approve(context: object) -> bool:  # noqa: ARG001
    return True


class FakeDesktop(BetaAbstractComputerToolset20260801):
    def __init__(self, desktop: Desktop | None = None, **options: Any) -> None:
        self.desktop = desktop or Desktop()
        # the toolset serves `type`, `key` and `hold_key`, so it needs a `confirm`; a test that wants none passes `None`
        # and turns `type`, `key` and `hold_key` off
        options.setdefault("confirm", approve)
        super().__init__(**options)

    @override
    def screenshot(self, context: BetaToolsetCallContext, input: BetaComputerScreenshotInput) -> BetaScreenshotResult:
        return self.desktop.screenshot(context, input)

    @override
    def zoom(self, context: BetaToolsetCallContext, input: BetaComputerZoomInput) -> BetaScreenshotResult:
        return self.desktop.zoom(context, input)

    @override
    def cursor_position(
        self, context: BetaToolsetCallContext, input: BetaComputerCursorPositionInput
    ) -> BetaComputerCursorPositionResult:
        return self.desktop.cursor_position(context, input)

    @override
    def mouse_move(self, context: BetaToolsetCallContext, input: BetaComputerMouseMoveInput) -> str | None:
        return self.desktop.mouse_move(context, input)

    @override
    def left_click(self, context: BetaToolsetCallContext, input: BetaComputerLeftClickInput) -> str | None:
        return self.desktop.action("left_click", context, input)

    @override
    def left_click_drag(self, context: BetaToolsetCallContext, input: BetaComputerLeftClickDragInput) -> None:
        self.desktop.action("left_click_drag", context, input)

    @override
    def type(self, context: BetaToolsetCallContext, input: BetaComputerTypeInput) -> None:
        self.desktop.action("type", context, input)

    @override
    def key(self, context: BetaToolsetCallContext, input: BetaComputerKeyInput) -> None:
        self.desktop.action("key", context, input)

    @override
    def hold_key(self, context: BetaToolsetCallContext, input: BetaComputerHoldKeyInput) -> None:
        self.desktop.action("hold_key", context, input)

    @override
    def scroll(self, context: BetaToolsetCallContext, input: BetaComputerScrollInput) -> None:
        self.desktop.action("scroll", context, input)

    @override
    def wait(self, context: BetaToolsetCallContext, input: BetaComputerWaitInput) -> None:
        self.desktop.action("wait", context, input)


class AsyncFakeDesktop(BetaAsyncAbstractComputerToolset20260801):
    def __init__(self, desktop: Desktop | None = None, **options: Any) -> None:
        self.desktop = desktop or Desktop()
        options.setdefault("confirm", approve)
        super().__init__(**options)

    @override
    async def screenshot(
        self, context: BetaToolsetCallContext, input: BetaComputerScreenshotInput
    ) -> BetaScreenshotResult:
        return self.desktop.screenshot(context, input)

    @override
    async def zoom(self, context: BetaToolsetCallContext, input: BetaComputerZoomInput) -> BetaScreenshotResult:
        return self.desktop.zoom(context, input)

    @override
    async def cursor_position(
        self, context: BetaToolsetCallContext, input: BetaComputerCursorPositionInput
    ) -> BetaComputerCursorPositionResult:
        return self.desktop.cursor_position(context, input)

    @override
    async def mouse_move(self, context: BetaToolsetCallContext, input: BetaComputerMouseMoveInput) -> str | None:
        return self.desktop.mouse_move(context, input)

    @override
    async def left_click(self, context: BetaToolsetCallContext, input: BetaComputerLeftClickInput) -> str | None:
        return self.desktop.action("left_click", context, input)

    @override
    async def left_click_drag(self, context: BetaToolsetCallContext, input: BetaComputerLeftClickDragInput) -> None:
        self.desktop.action("left_click_drag", context, input)

    @override
    async def type(self, context: BetaToolsetCallContext, input: BetaComputerTypeInput) -> None:
        self.desktop.action("type", context, input)

    @override
    async def key(self, context: BetaToolsetCallContext, input: BetaComputerKeyInput) -> None:
        self.desktop.action("key", context, input)

    @override
    async def hold_key(self, context: BetaToolsetCallContext, input: BetaComputerHoldKeyInput) -> None:
        self.desktop.action("hold_key", context, input)

    @override
    async def scroll(self, context: BetaToolsetCallContext, input: BetaComputerScrollInput) -> None:
        self.desktop.action("scroll", context, input)

    @override
    async def wait(self, context: BetaToolsetCallContext, input: BetaComputerWaitInput) -> None:
        self.desktop.action("wait", context, input)
