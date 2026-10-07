# ruff: noqa: ARG001 -- the confirm hook and a patched-in member ignore their arguments
"""Construction rules and the dispatch surface of the abstract computer toolset classes."""

from __future__ import annotations

import re
from typing import Any, cast
from typing_extensions import override

import pytest

from anthropic.tools import (
    ToolError,
    ToolsetConfigError,
    ToolsetContractError,
)
from anthropic.types.beta import (
    BetaComputerKeyInput,
    BetaComputerZoomInput,
    BetaComputerScreenshotInput,
    BetaComputerCursorPositionInput,
)
from anthropic.tools.computer import (
    BetaScreenshotResult,
    BetaToolsetCallContext,
    BetaComputerCursorPositionResult,
    BetaAbstractComputerToolset20260801,
    BetaAsyncAbstractComputerToolset20260801,
)
from anthropic.lib._stainless_helpers import get_helper_tag

from ._computer_fakes import FakeDesktop, AsyncFakeDesktop

CTX = BetaToolsetCallContext()


class TwoMembers(BetaAbstractComputerToolset20260801):
    @override
    def screenshot(self, context: BetaToolsetCallContext, input: BetaComputerScreenshotInput) -> BetaScreenshotResult:
        return BetaScreenshotResult(data="AAAA")

    @override
    def cursor_position(
        self, context: BetaToolsetCallContext, input: BetaComputerCursorPositionInput
    ) -> BetaComputerCursorPositionResult:
        return BetaComputerCursorPositionResult(x=3, y=4)


def _allow(context: object) -> bool:
    return True


def _disabled(entry: Any) -> list[str]:
    configs = cast("dict[str, dict[str, object]]", entry.get("configs") or {})
    return sorted(name for name, config in configs.items() if (config or {}).get("enabled") is False)


def test_a_toolset_with_no_member_enabled_sends_every_member_disabled() -> None:
    class Nothing(BetaAbstractComputerToolset20260801):
        pass

    assert len(_disabled(Nothing().to_dict())) == 17
    switched_off = TwoMembers(configs={"screenshot": {"enabled": False}, "cursor_position": {"enabled": False}})
    assert len(_disabled(switched_off.to_dict())) == 17


def test_unimplemented_members_are_sent_as_disabled_and_implemented_ones_left_to_the_api() -> None:
    entry = TwoMembers().to_dict()
    assert entry["type"] == "computer_toolset_20260801"
    disabled = _disabled(entry)
    assert "screenshot" not in disabled and "cursor_position" not in disabled
    assert len(disabled) == 15 and "left_click" in disabled and "zoom" in disabled
    # Nothing SDK-side leaks into the entry.
    assert set(entry) == {"type", "configs"}
    assert all(set(config) == {"enabled"} for config in cast(Any, entry)["configs"].values())


def test_the_callers_configs_pass_through_untouched_and_are_copied() -> None:
    configs: Any = {"screenshot": {"defer_loading": True}, "zoom": {"enabled": False, "defer_loading": True}}
    desktop = TwoMembers(configs=configs)
    entry = desktop.to_dict()
    assert entry["configs"]["screenshot"] == {"defer_loading": True}  # type: ignore[index]
    assert entry["configs"]["zoom"] == {"enabled": False, "defer_loading": True}  # type: ignore[index]
    # Enabling a member the subclass does not implement would offer the model something that can only
    # answer "not available": refused at construction.
    with pytest.raises(ToolsetConfigError, match="does not implement"):
        TwoMembers(configs={"zoom": {"enabled": True}})
    configs["screenshot"]["enabled"] = False
    assert desktop.to_dict()["configs"]["screenshot"] == {"defer_loading": True}  # type: ignore[index]
    assert desktop.to_dict() is not desktop.to_dict()


def test_an_execute_only_subclass_serves_every_member_and_turns_members_off_with_configs() -> None:
    class Forwarder(BetaAbstractComputerToolset20260801):
        @override
        def execute(self, context: BetaToolsetCallContext, name: Any, input: Any) -> Any:
            return f"forwarded {name}"

    # A class that overrides execute serves every member: the wire entry disables nothing, and the driver turns off
    # what it does not serve through configs.
    assert Forwarder(confirm=_allow).to_dict() == {"type": "computer_toolset_20260801"}
    trimmed = Forwarder(
        configs={"screenshot": {"enabled": False}, "zoom": {"enabled": False}}, confirm=_allow
    ).to_dict()
    assert _disabled(trimmed) == ["screenshot", "zoom"]

    class Hooked(TwoMembers):
        @override
        def execute(self, context: BetaToolsetCallContext, name: Any, input: Any) -> Any:
            return super().execute(context, name, input)

    assert _disabled(Hooked(confirm=_allow).to_dict()) == []
    assert Hooked(confirm=_allow).execute(
        CTX, "cursor_position", BetaComputerCursorPositionInput()
    ) == BetaComputerCursorPositionResult(x=3, y=4)
    with pytest.raises(ToolError, match="not available"):
        Hooked(confirm=_allow).execute(CTX, "zoom", BetaComputerZoomInput(region=[0, 0, 1, 1]))
    assert _disabled(Hooked(configs={"zoom": {"enabled": False}}, confirm=_allow).to_dict()) == ["zoom"]


def test_a_null_configs_entry_leaves_the_member_at_its_defaults_and_goes_to_the_api_as_given() -> None:
    entry = cast(Any, TwoMembers(configs={"screenshot": None}).to_dict())
    assert entry["configs"]["screenshot"] is None and "screenshot" not in _disabled(entry)
    assert TwoMembers(configs={"screenshot": None}).call(CTX, "screenshot", {})


def test_tool_configs_go_onto_the_entry_and_the_helper_tag_does_not() -> None:
    desktop = TwoMembers(tool_configs={"cache_control": {"type": "ephemeral"}})
    assert desktop.to_dict().get("cache_control") == {"type": "ephemeral"}
    assert get_helper_tag(desktop) == "computer-toolset"
    assert "computer-toolset" not in str(desktop.to_dict())
    cast(Any, desktop.to_dict())["cache_control"]["ttl"] = "1h"
    assert desktop.to_dict().get("cache_control") == {"type": "ephemeral"}


def test_execute_dispatches_to_the_member_method_and_refuses_unknown_names() -> None:
    desktop = TwoMembers()
    assert desktop.execute(CTX, "screenshot", BetaComputerScreenshotInput()) == BetaScreenshotResult(data="AAAA")
    with pytest.raises(ToolError) as unknown:
        desktop.execute(CTX, "__init__", BetaComputerScreenshotInput())  # type: ignore[arg-type]
    assert str(unknown.value) == "Error: unknown computer toolset member '__init__'"
    # A member the subclass did not implement answers the model rather than raising into the runner.
    with pytest.raises(ToolError) as unavailable:
        desktop.execute(CTX, "key", BetaComputerKeyInput(text="a"))
    assert str(unavailable.value) == "The computer toolset member 'key' is not available in this environment."


def test_an_async_member_on_the_sync_class_is_a_contract_error() -> None:
    class Mixed(TwoMembers):
        @override
        async def key(self, context: BetaToolsetCallContext, input: BetaComputerKeyInput) -> str | None:  # type: ignore[override]
            return None

    # reported when the toolset is built, before any call
    with pytest.raises(
        ToolsetContractError,
        match="computer member 'key' is async on the synchronous toolset.*BetaAsyncAbstractComputer",
    ):
        Mixed()

    async def prompt(context: Any) -> bool:
        return True

    with pytest.raises(ToolsetContractError, match="confirm is async on the synchronous toolset"):
        TwoMembers(confirm=prompt)  # type: ignore[arg-type]


async def test_async_execute_awaits_async_members_and_a_sync_one_is_a_contract_error() -> None:
    class Points(BetaAsyncAbstractComputerToolset20260801):
        @override
        async def cursor_position(
            self, context: BetaToolsetCallContext, input: BetaComputerCursorPositionInput
        ) -> BetaComputerCursorPositionResult:
            return BetaComputerCursorPositionResult(x=1, y=2)

    desktop = Points()
    assert await desktop.execute(
        CTX, "cursor_position", BetaComputerCursorPositionInput()
    ) == BetaComputerCursorPositionResult(x=1, y=2)
    with pytest.raises(ToolError, match="^The computer toolset member 'zoom' is not available in this environment\\.$"):
        await desktop.execute(CTX, "zoom", BetaComputerZoomInput(region=[0, 0, 1, 1]))

    class SyncMember(Points):
        @override
        def key(self, context: BetaToolsetCallContext, input: BetaComputerKeyInput) -> str | None:  # type: ignore[override]
            return None

    # a member written sync on the async class is reported when the toolset is built rather than run on the event loop
    with pytest.raises(
        ToolsetContractError,
        match="computer member 'key' is sync on the asynchronous toolset.*BetaAbstractComputer",
    ):
        SyncMember()


def test_override_detection_sees_intermediate_classes_and_dynamic_assignment() -> None:
    class Middle(TwoMembers):
        pass

    class Leaf(Middle):
        @override
        def key(self, context: BetaToolsetCallContext, input: BetaComputerKeyInput) -> str | None:
            return None

    assert {"screenshot", "cursor_position", "key"}.isdisjoint(_disabled(Leaf(confirm=_allow).to_dict()))

    def wait(self: Any, context: Any, input: Any) -> None:
        return None

    Patched = type("Patched", (TwoMembers,), {"wait": wait})
    assert "wait" not in _disabled(Patched().to_dict())


def test_options_do_not_leak_into_the_entry() -> None:
    assert set(TwoMembers(confirm=_allow).to_dict()) == {"type", "configs"}


def test_configs_is_a_read_only_copy_of_what_to_dict_sends() -> None:
    class AsyncOne(BetaAsyncAbstractComputerToolset20260801):
        @override
        async def screenshot(
            self, context: BetaToolsetCallContext, input: BetaComputerScreenshotInput
        ) -> BetaScreenshotResult:
            return BetaScreenshotResult(data="AAAA")

    for desktop in (TwoMembers(configs={"zoom": {"enabled": False}}), AsyncOne()):
        configs: Any = desktop.configs
        assert configs is not None and configs == cast(Any, desktop.to_dict())["configs"]
        assert configs["left_click"] == {"enabled": False}  # not implemented, so withheld from the model
        configs["left_click"] = {"enabled": True}  # a copy: nothing the toolset holds changes
        assert cast(Any, desktop.configs)["left_click"] == {"enabled": False}
        with pytest.raises(AttributeError):
            desktop.configs = {}  # type: ignore[misc]


# --- keyboard input needs a confirm ------------------------------------------------------------

KEYBOARD = ("type", "key", "hold_key")


def _serving(*members: str, twin: bool = False) -> Any:
    """A toolset class that serves `members` and nothing else, on the synchronous class or (`twin`) the async one."""

    def serve(self: Any, context: Any, input: Any) -> None:
        return None

    async def serve_async(self: Any, context: Any, input: Any) -> None:
        return None

    base: Any = BetaAsyncAbstractComputerToolset20260801 if twin else BetaAbstractComputerToolset20260801
    return type("Serving", (base,), {name: serve_async if twin else serve for name in members})


@pytest.mark.parametrize("twin", [False, True], ids=["sync", "async"])
@pytest.mark.parametrize("member", KEYBOARD)
def test_a_toolset_that_serves_keyboard_input_will_not_build_without_a_confirm(member: str, twin: bool) -> None:
    Desktop = _serving(member, twin=twin)

    for options in ({}, {"confirm": None}):
        with pytest.raises(ToolsetConfigError, match=re.escape(f"['{member}'] requires a confirm callable")):
            Desktop(**options)
    assert Desktop(confirm=_allow).to_dict()["type"] == "computer_toolset_20260801"


def test_the_refusal_names_the_keyboard_members_still_enabled_and_says_how_to_go_on() -> None:
    class Forwarder(BetaAbstractComputerToolset20260801):  # an `execute` override serves every member
        @override
        def execute(self, context: BetaToolsetCallContext, name: Any, input: Any) -> Any:
            return None

    def refused(**options: Any) -> str:
        with pytest.raises(ToolsetConfigError) as raised:
            Forwarder(**options)
        return str(raised.value)

    how = "requires a confirm callable: pass confirm=<callable>, or disable it in configs"
    assert refused() == f"['hold_key', 'key', 'type'] {how}"
    assert refused(configs={"type": {"enabled": False}, "hold_key": {"enabled": False}}) == f"['key'] {how}"


@pytest.mark.parametrize("Desktop", [FakeDesktop, AsyncFakeDesktop], ids=["sync", "async"])
def test_a_toolset_with_all_three_keyboard_members_disabled_needs_no_confirm(Desktop: Any) -> None:
    off = {name: {"enabled": False} for name in KEYBOARD}

    desktop = Desktop(configs=off, confirm=None)

    assert all(desktop.configs[name] == {"enabled": False} for name in KEYBOARD)
    with pytest.raises(ToolsetConfigError, match=re.escape("['hold_key', 'key', 'type'] requires")):
        Desktop(confirm=None)


@pytest.mark.parametrize("twin", [False, True], ids=["sync", "async"])
def test_members_that_do_not_type_need_no_confirm(twin: bool) -> None:
    others = ("screenshot", "zoom", "cursor_position", "mouse_move", "left_click", "left_click_drag", "scroll", "wait")

    _serving(*others, twin=twin)()
