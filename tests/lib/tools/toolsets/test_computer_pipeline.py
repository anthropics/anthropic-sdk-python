# ruff: noqa: ARG001 -- confirm hooks ignore their arguments
"""One computer member call through `call` and `tool_result`: rendering per result kind, input checks, the
confirm gate, the refusals the model reads, and closing — on the sync and the async class."""

from __future__ import annotations

import threading
from typing import Any, cast
from typing_extensions import override

import anyio
import pytest

from anthropic.tools import (
    ToolError,
    ConfirmFailedError,
    ToolsetClosedError,
    ConfirmDeclinedError,
    ToolsetContractError,
    UnavailableMemberError,
    InvalidMemberInputError,
)
from anthropic.types.beta import BetaTextBlockParam, BetaImageBlockParam, BetaComputerKeyInput
from anthropic.tools.computer import (
    BetaToolsetCallContext,
    BetaComputerConfirmContext,
)
from anthropic.types.beta.beta_tool_use_block import BetaToolUseBlock

from ._computer_fakes import PNG, Desktop, FakeDesktop, AsyncFakeDesktop

CTX = BetaToolsetCallContext(
    tool_use=BetaToolUseBlock(type="tool_use", id="toolu_7", name="left_click", input={}, toolset_name="computer")
)


def _allow(context: BetaComputerConfirmContext) -> bool:
    return True


def _deny(context: BetaComputerConfirmContext) -> bool:
    return False


def _not_a_bool(context: BetaComputerConfirmContext) -> str:
    return "yes"


def _use(name: str, input: dict[str, Any], id: str = "toolu_1") -> BetaToolUseBlock:
    return BetaToolUseBlock(type="tool_use", id=id, name=name, input=input, toolset_name="computer")


def _error_text(desktop: FakeDesktop, name: str, input: dict[str, Any]) -> str:
    with pytest.raises(ToolError) as caught:
        desktop.call(CTX, name, input)
    return str(caught.value)


# --- rendering ------------------------------------------------------------------------------------------------


def test_a_screenshot_renders_as_one_image_block() -> None:
    desktop = FakeDesktop()
    assert desktop.call(CTX, "screenshot", {}) == [
        {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": PNG}}
    ]
    # zoom is rendered the same way, with the media type the driver reported
    assert desktop.call(CTX, "zoom", {"region": [0, 0, 10, 10]}) == [
        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": PNG}}
    ]
    assert desktop.desktop.inputs[-1].region == [0, 0, 10, 10]
    # anything but the result model is the driver's bug: a ValueError, which reaches the model as an error result
    desktop.desktop.results["screenshot"] = "BBBB"
    with pytest.raises(ValueError, match="screenshot returned str, not its result model"):
        desktop.call(CTX, "screenshot", {})


def test_cursor_position_renders_as_a_text_line() -> None:
    desktop = FakeDesktop()
    assert desktop.call(CTX, "cursor_position", {}) == [{"type": "text", "text": "X=0,Y=0"}]
    desktop.call(CTX, "mouse_move", {"coordinate": [120, 45]})
    assert desktop.call(CTX, "cursor_position", {}) == [{"type": "text", "text": "X=120,Y=45"}]
    desktop.desktop.results["cursor_position"] = (1, 2)  # not the result model: the driver's bug, named
    with pytest.raises(ValueError, match="cursor_position returned tuple, not its result model"):
        desktop.call(CTX, "cursor_position", {})


def test_a_pure_action_renders_its_acknowledgment_then_the_line_it_returned() -> None:
    desktop = FakeDesktop()
    assert desktop.call(CTX, "left_click", {"coordinate": [1, 2]}) == [{"type": "text", "text": "Clicked."}]
    assert desktop.call(CTX, "mouse_move", {"coordinate": [1, 2]}) == [{"type": "text", "text": "Moved the mouse."}]
    assert desktop.call(CTX, "key", {"text": "ctrl+s"}) == [{"type": "text", "text": "Pressed ctrl+s."}]
    assert desktop.call(CTX, "hold_key", {"text": "shift", "duration": 2}) == [
        {"type": "text", "text": "Held shift for 2s."}
    ]
    assert desktop.call(CTX, "type", {"text": "hello"}) == [{"type": "text", "text": "Typed."}]
    assert desktop.call(CTX, "scroll", {"scroll_direction": "down", "scroll_amount": 3}) == [
        {"type": "text", "text": "Scrolled down."}
    ]
    assert desktop.call(CTX, "wait", {"duration": 3}) == [{"type": "text", "text": "Waited 3s."}]

    class Buttons(FakeDesktop):
        @override
        def execute(self, context: BetaToolsetCallContext, name: Any, input: Any) -> Any:
            return None

    buttons = Buttons()
    assert buttons.call(CTX, "left_mouse_down", {}) == [{"type": "text", "text": "Left mouse button pressed."}]
    assert buttons.call(CTX, "left_mouse_up", {}) == [{"type": "text", "text": "Left mouse button released."}]
    assert buttons.call(CTX, "left_click_drag", {"start_coordinate": [1, 1], "coordinate": [2, 2]}) == [
        {"type": "text", "text": "Dragged."}
    ]
    # a line the action returned follows the acknowledgment, folded to one line and bounded
    desktop.desktop.results["left_click"] = "Window\n\u202efocused" + "x" * 5000
    blocks = desktop.call(CTX, "left_click", {})
    assert blocks[0] == {"type": "text", "text": "Clicked."}
    line = cast(Any, blocks[1])["text"]
    assert line.startswith("Window focusedx") and len(line) == 4096
    desktop.desktop.results["left_click"] = ""  # blank: the acknowledgment only
    assert desktop.call(CTX, "left_click", {}) == [{"type": "text", "text": "Clicked."}]


def test_a_line_that_folds_to_nothing_renders_as_the_acknowledgment_alone() -> None:
    # Whitespace and control characters fold away, and a text block that would carry nothing is not sent.
    desktop = FakeDesktop()
    desktop.desktop.results["left_click"] = "\n \t\x00"
    assert desktop.call(CTX, "left_click", {}) == [{"type": "text", "text": "Clicked."}]
    block = desktop.tool_result(_use("left_click", {}))
    assert block.get("content") == [{"type": "text", "text": "Clicked."}] and "is_error" not in block


async def test_a_line_that_folds_to_nothing_renders_as_the_acknowledgment_alone_on_the_async_class() -> None:
    desktop = AsyncFakeDesktop()
    desktop.desktop.results["left_click"] = " \u2028 "
    assert await desktop.call(CTX, "left_click", {}) == [{"type": "text", "text": "Clicked."}]


def test_a_template_value_the_model_wrote_stays_data() -> None:
    desktop = FakeDesktop()
    assert desktop.call(CTX, "key", {"text": "{duration}\n{text}"}) == [
        {"type": "text", "text": "Pressed {duration} {text}."}
    ]


# --- inputs ---------------------------------------------------------------------------------------------------


def test_inputs_are_parsed_into_the_generated_models_and_undeclared_keys_are_kept() -> None:
    desktop = FakeDesktop()
    desktop.call(CTX, "key", {"text": "a", "repeat": 3, "tab_id": "t1"})
    parsed = desktop.desktop.inputs[-1]
    assert isinstance(parsed, BetaComputerKeyInput) and parsed.repeat == 3
    assert cast(Any, parsed).tab_id == "t1"  # a key the schema lacks stays on the parsed input
    # the member sees the same tool_use the call answers
    assert desktop.desktop.contexts[-1].tool_use is CTX.tool_use


def test_a_bad_field_is_refused_without_echoing_the_value() -> None:
    desktop = FakeDesktop()
    text = _error_text(desktop, "wait", {"duration": "long"})
    assert text.startswith("invalid input for computer member 'wait': duration: ") and "long" not in text
    assert (
        _error_text(desktop, "mouse_move", {})
        .lower()
        .startswith("invalid input for computer member 'mouse_move': coordinate: field required")
    )
    assert _error_text(desktop, "scroll", {"scroll_direction": "sideways", "scroll_amount": 1}).startswith(
        "invalid input for computer member 'scroll': scroll_direction: "
    )
    assert desktop.desktop.calls == []


def test_coordinate_lists_must_have_the_shape_the_model_was_told() -> None:
    desktop = FakeDesktop()
    assert _error_text(desktop, "mouse_move", {"coordinate": [1]}) == (
        "invalid input for computer member 'mouse_move': coordinate: expected [x, y]"
    )
    assert _error_text(desktop, "zoom", {"region": [0, 0, 1]}) == (
        "invalid input for computer member 'zoom': region: expected [x0, y0, x1, y1]"
    )
    assert _error_text(desktop, "left_click_drag", {"start_coordinate": [1], "coordinate": [1, 2, 3]}) == (
        "invalid input for computer member 'left_click_drag': coordinate: expected [x, y]; "
        "start_coordinate: expected [x, y]"
    )
    assert _error_text(desktop, "mouse_move", {"coordinate": [1, "b"]}).startswith(
        "invalid input for computer member 'mouse_move': coordinate.1: "
    )
    # an omitted optional coordinate means "at the cursor" and is not checked
    desktop.call(CTX, "left_click", {})
    assert desktop.desktop.inputs[-1].coordinate is None
    assert desktop.desktop.calls == ["left_click"]


def test_no_numeric_bound_is_applied_beyond_the_generated_types() -> None:
    # The tool's schema tells the model these limits, but nothing enforces them; a driver that needs a cap
    # applies its own.
    desktop = FakeDesktop()
    assert desktop.call(CTX, "wait", {"duration": 1000}) == [{"type": "text", "text": "Waited 1000s."}]
    assert desktop.call(CTX, "key", {"text": "a", "repeat": 500}) == [{"type": "text", "text": "Pressed a."}]
    assert desktop.desktop.inputs[-1].repeat == 500


# --- refusals and errors --------------------------------------------------------------------------------------


def test_member_resolution_refusals() -> None:
    desktop = FakeDesktop(configs={"zoom": {"enabled": False}})
    assert _error_text(desktop, "teleport", {}) == "Error: unknown computer toolset member 'teleport'"
    assert _error_text(desktop, "zoom", {"region": [0, 0, 1, 1]}) == (
        "The 'zoom' action is not permitted by this application's permissions and cannot be used in this session."
    )
    assert _error_text(desktop, "double_click", {}) == (
        "The computer toolset member 'double_click' is not available in this environment."
    )
    with pytest.raises(ToolError) as caught:
        desktop.call(CTX, "double_click", {})
    assert isinstance(caught.value.__cause__, UnavailableMemberError)
    with pytest.raises(ToolError) as invalid:
        desktop.call(CTX, "wait", {})
    assert isinstance(invalid.value.__cause__, InvalidMemberInputError)
    assert desktop.desktop.calls == []


def test_a_driver_error_reaches_the_model_as_text_and_a_refusal_is_relayed() -> None:
    desktop = FakeDesktop()
    desktop.desktop.fail["left_click"] = RuntimeError("the display went away")
    with pytest.raises(ToolError) as caught:
        desktop.call(CTX, "left_click", {})
    assert caught.value.content == [{"type": "text", "text": "RuntimeError: the display went away"}]
    assert isinstance(caught.value.__cause__, ToolError) and isinstance(caught.value.__cause__.__cause__, RuntimeError)
    desktop.desktop.fail["left_click"] = ToolError("Nothing to click here.")
    with pytest.raises(ToolError) as relayed:
        desktop.call(CTX, "left_click", {})
    assert relayed.value.content == [{"type": "text", "text": "Nothing to click here."}]
    # a driver's text can carry a screen-sized payload: cut to the field limit, whether raised as ToolError or not
    desktop.desktop.fail["left_click"] = RuntimeError("x" * 5000)
    assert len(_error_text(desktop, "left_click", {})) == 4096
    desktop.desktop.fail["left_click"] = ToolError("y" * 5000)
    assert _error_text(desktop, "left_click", {}) == "y" * 4096
    assert len(cast(Any, desktop.tool_result(_use("left_click", {})))["content"][0]["text"]) == 4096
    # a usage error is the driver's bug and propagates
    desktop.desktop.fail["left_click"] = ToolsetContractError("misused")
    with pytest.raises(ToolsetContractError, match="misused"):
        desktop.call(CTX, "left_click", {})


_IMAGE: BetaImageBlockParam = {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": PNG}}
_RAISED: list[BetaTextBlockParam | BetaImageBlockParam] = [
    {"type": "text", "text": "No button here."},
    _IMAGE,
    {"type": "text", "text": ""},
]


def test_call_raises_a_tool_errors_blocks_as_they_are_and_tool_result_keeps_only_the_text() -> None:
    # The API rejects an error result that holds a non-text block. `tool_result()` keeps only the non-empty text blocks.
    desktop = FakeDesktop()
    desktop.desktop.fail["left_click"] = ToolError(_RAISED)
    with pytest.raises(ToolError) as caught:
        desktop.call(CTX, "left_click", {})
    assert caught.value.content == _RAISED
    assert cast(Any, desktop.tool_result(_use("left_click", {})))["content"] == [
        {"type": "text", "text": "No button here."}
    ]


async def test_call_raises_a_tool_errors_blocks_as_they_are_on_the_async_class() -> None:
    desktop = AsyncFakeDesktop()
    desktop.desktop.fail["left_click"] = ToolError(_RAISED)
    with pytest.raises(ToolError) as caught:
        await desktop.call(CTX, "left_click", {})
    assert caught.value.content == _RAISED
    result = cast(Any, await desktop.tool_result(_use("left_click", {})))
    assert result["content"] == [{"type": "text", "text": "No button here."}]


class _NoMessage(Exception):
    @override
    def __str__(self) -> str:
        raise ValueError("no message")


@pytest.mark.parametrize(
    ("raised", "expected"),
    [
        (OSError("display :3 is gone"), "OSError: display :3 is gone"),
        (TimeoutError(), "TimeoutError"),
        (_NoMessage(), "_NoMessage"),
    ],
)
async def test_a_driver_exception_reads_as_its_type_and_message(raised: Exception, expected: str) -> None:
    # an empty message, or a `__str__` that raises, gives the type name alone
    desktop, async_desktop = FakeDesktop(), AsyncFakeDesktop()
    desktop.desktop.fail["left_click"] = async_desktop.desktop.fail["left_click"] = raised
    assert cast(Any, desktop.tool_result(_use("left_click", {})))["content"] == [{"type": "text", "text": expected}]
    result = cast(Any, await async_desktop.tool_result(_use("left_click", {})))
    assert result["content"] == [{"type": "text", "text": expected}]


def test_tool_result_builds_the_block_and_never_raises_a_tool_error() -> None:
    desktop = FakeDesktop()
    ok = desktop.tool_result(_use("cursor_position", {}))
    assert ok == {
        "type": "tool_result",
        "tool_use_id": "toolu_1",
        "toolset_name": "computer",
        "content": [{"type": "text", "text": "X=0,Y=0"}],
    }
    failed = desktop.tool_result(_use("teleport", {}, id="toolu_2"))
    assert failed == {
        "type": "tool_result",
        "tool_use_id": "toolu_2",
        "toolset_name": "computer",
        "content": [{"type": "text", "text": "Error: unknown computer toolset member 'teleport'"}],
        "is_error": True,
    }
    # a browser block is not a computer member call, whatever its name
    with pytest.raises(ToolsetContractError, match="not a member call of the 'computer' toolset"):
        desktop.tool_result(
            BetaToolUseBlock(type="tool_use", id="x", name="screenshot", input={}, toolset_name="browser")
        )


# --- confirm ----------------------------------------------------------------------------------------------------


def test_confirm_sees_every_call_with_the_member_and_its_parsed_input() -> None:
    seen: list[BetaComputerConfirmContext] = []

    def confirm(context: BetaComputerConfirmContext) -> bool:
        seen.append(context)
        return context.member != "type"

    desktop = FakeDesktop(confirm=confirm)
    desktop.call(CTX, "key", {"text": "a"})
    assert _error_text(desktop, "type", {"text": "secret"}) == (
        "The user did not grant permission to run 'type'. Do not retry it unless the user asks you to."
    )
    assert [c.member for c in seen] == ["key", "type"]
    assert seen[1].input.to_dict() == {"text": "secret"} and seen[1].tool_use is CTX.tool_use
    assert desktop.desktop.calls == ["key"]  # the declined call never reached the driver
    # a refused call is never shown: nothing to approve
    _error_text(desktop, "teleport", {})
    assert len(seen) == 2


def test_a_confirm_that_raises_refuses_the_call_and_an_answer_other_than_true_declines() -> None:
    def failing(context: BetaComputerConfirmContext) -> bool:
        raise RuntimeError("no terminal")

    desktop = FakeDesktop(confirm=failing)
    with pytest.raises(ToolError) as caught:
        desktop.call(CTX, "key", {"text": "a"})
    assert isinstance(caught.value.__cause__, ConfirmFailedError)
    assert str(caught.value).startswith("Permission to run 'key' could not be obtained")

    def refusing(context: BetaComputerConfirmContext) -> bool:
        raise ToolError("Ask again later.")

    assert _error_text(FakeDesktop(confirm=refusing), "key", {"text": "a"}) == "Ask again later."

    def long_refusal(context: BetaComputerConfirmContext) -> bool:
        raise ToolError("r" * 5000)

    # A refusal raised before the call is held to the field limit, and so is a parse error on a long input.
    assert _error_text(FakeDesktop(confirm=long_refusal), "key", {"text": "a"}) == "r" * 4096
    assert len(_error_text(FakeDesktop(), "mouse_move", {"coordinate": ["x"] * 5000})) <= 4096
    for confirm in (_deny, _not_a_bool):  # only `True` runs the call
        with pytest.raises(ToolError) as declined:
            FakeDesktop(confirm=confirm).call(CTX, "key", {"text": "a"})
        assert isinstance(declined.value.__cause__, ConfirmDeclinedError)


def test_the_gate_runs_before_an_execute_override() -> None:
    class Hooked(FakeDesktop):
        @override
        def execute(self, context: BetaToolsetCallContext, name: Any, input: Any) -> Any:
            self.desktop.calls.append(f"execute:{name}")
            return super().execute(context, name, input)

    desktop = Hooked(confirm=_deny)
    _error_text(desktop, "key", {"text": "a"})
    assert desktop.desktop.calls == []


async def test_the_async_class_cuts_a_refusal_raised_before_the_call() -> None:
    async def long_refusal(context: BetaComputerConfirmContext) -> bool:
        raise ToolError("r" * 5000)

    with pytest.raises(ToolError) as caught:
        await AsyncFakeDesktop(confirm=long_refusal).call(CTX, "key", {"text": "a"})
    assert str(caught.value) == "r" * 4096


async def test_async_confirm_may_be_a_coroutine_or_a_plain_function() -> None:
    async def coroutine(context: BetaComputerConfirmContext) -> bool:
        return context.member == "key"

    desktop = AsyncFakeDesktop(confirm=coroutine)
    assert await desktop.call(CTX, "key", {"text": "a"}) == [{"type": "text", "text": "Pressed a."}]
    with pytest.raises(ToolError) as caught:
        await desktop.call(CTX, "type", {"text": "b"})
    assert isinstance(caught.value.__cause__, ConfirmDeclinedError)
    plain = AsyncFakeDesktop(confirm=_allow)
    assert await plain.call(CTX, "type", {"text": "b"}) == [{"type": "text", "text": "Typed."}]


_KEYBOARD_OFF = {name: {"enabled": False} for name in ("type", "key", "hold_key")}


def test_a_toolset_with_the_keyboard_off_runs_its_calls_with_no_confirm() -> None:
    desktop = FakeDesktop(confirm=None, configs=_KEYBOARD_OFF)

    assert desktop.call(CTX, "left_click", {"coordinate": [1, 2]}) == [{"type": "text", "text": "Clicked."}]
    assert desktop.call(CTX, "cursor_position", {}) == [{"type": "text", "text": "X=0,Y=0"}]
    assert desktop.desktop.calls == ["left_click", "cursor_position"]


async def test_the_async_class_with_the_keyboard_off_runs_its_calls_with_no_confirm() -> None:
    desktop = AsyncFakeDesktop(confirm=None, configs=_KEYBOARD_OFF)

    assert await desktop.call(CTX, "left_click", {"coordinate": [1, 2]}) == [{"type": "text", "text": "Clicked."}]
    assert desktop.desktop.calls == ["left_click"]


# --- the async class, closing, serialization ------------------------------------------------------------------


def test_an_async_execute_override_on_the_sync_class_is_a_contract_error() -> None:
    class Coroutine(FakeDesktop):
        @override
        async def execute(self, context: BetaToolsetCallContext, name: Any, input: Any) -> Any:  # type: ignore[override]
            return None

    with pytest.raises(ToolsetContractError, match="execute is async on the synchronous toolset"):
        Coroutine()


async def test_a_plain_execute_override_on_the_async_class_is_a_contract_error() -> None:
    # reported when the toolset is built, as for the browser toolset: the override never runs
    class Plain(AsyncFakeDesktop):
        @override
        def execute(self, context: BetaToolsetCallContext, name: Any, input: Any) -> Any:
            return None

    with pytest.raises(ToolsetContractError, match="execute is sync on the asynchronous toolset"):
        Plain()


async def test_the_async_class_renders_and_refuses_the_same_way() -> None:
    desktop = AsyncFakeDesktop()
    assert await desktop.call(CTX, "screenshot", {}) == [
        {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": PNG}}
    ]
    assert await desktop.call(CTX, "cursor_position", {}) == [{"type": "text", "text": "X=0,Y=0"}]
    assert await desktop.call(CTX, "scroll", {"scroll_direction": "up", "scroll_amount": 2}) == [
        {"type": "text", "text": "Scrolled up."}
    ]
    with pytest.raises(ToolError, match="expected \\[x, y\\]"):
        await desktop.call(CTX, "mouse_move", {"coordinate": [1, 2, 3]})
    desktop.desktop.fail["key"] = RuntimeError("boom")
    with pytest.raises(ToolError, match=r"^RuntimeError: boom$"):
        await desktop.call(CTX, "key", {"text": "a"})
    desktop.desktop.fail["key"] = ToolError("Nothing to press.")
    with pytest.raises(ToolError, match="^Nothing to press\\.$"):
        await desktop.call(CTX, "key", {"text": "a"})
    result = await desktop.tool_result(_use("triple_click", {}))
    assert result["is_error"] is True and "not available" in str(result["content"])  # type: ignore[typeddict-item]


def test_a_closed_toolset_refuses_calls_and_a_member_cannot_nest_call() -> None:
    desktop = FakeDesktop()
    with desktop:
        desktop.call(CTX, "key", {"text": "a"})
    with pytest.raises(ToolsetClosedError):
        desktop.call(CTX, "key", {"text": "a"})
    with pytest.raises(ToolsetClosedError):
        with desktop:
            pass

    class Nesting(FakeDesktop):
        @override
        def key(self, context: BetaToolsetCallContext, input: BetaComputerKeyInput) -> None:
            self.call(context, "type", {"text": input.text})

    with pytest.raises(ToolsetContractError, match="call\\(\\) was invoked from inside a member"):
        Nesting().call(CTX, "key", {"text": "a"})


def test_close_waits_for_the_call_in_flight() -> None:
    started, release = threading.Event(), threading.Event()
    shared = Desktop()

    class Slow(FakeDesktop):
        @override
        def key(self, context: BetaToolsetCallContext, input: BetaComputerKeyInput) -> None:
            started.set()
            release.wait(5)
            self.desktop.action("key", context, input)

    desktop = Slow(shared)
    worker = threading.Thread(target=lambda: desktop.call(CTX, "key", {"text": "a"}))
    worker.start()
    assert started.wait(5)
    closer = threading.Thread(target=desktop.close)
    closer.start()
    closer.join(0.2)
    assert closer.is_alive()  # close waits for the member to finish
    release.set()
    worker.join(5)
    closer.join(5)
    assert not closer.is_alive() and shared.calls == ["key"]


async def test_async_calls_run_one_at_a_time_and_close_waits() -> None:
    order: list[str] = []

    class Slow(AsyncFakeDesktop):
        @override
        async def key(self, context: BetaToolsetCallContext, input: BetaComputerKeyInput) -> None:
            order.append(f"start {input.text}")
            await anyio.sleep(0.05)
            order.append(f"end {input.text}")

    desktop = Slow()
    async with anyio.create_task_group() as tg:
        tg.start_soon(desktop.call, CTX, "key", {"text": "a"})
        tg.start_soon(desktop.call, CTX, "key", {"text": "b"})
        await anyio.sleep(0.01)
        await desktop.close()
        order.append("closed")
    assert order[-1] == "closed" and order[:4] in (
        ["start a", "end a", "start b", "end b"],
        ["start b", "end b", "start a", "end a"],
    )
    with pytest.raises(ToolsetClosedError):
        await desktop.call(CTX, "key", {"text": "c"})
