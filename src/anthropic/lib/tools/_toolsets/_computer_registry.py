"""The computer member registry: one row per member, from which every other per-member table derives.

Member names and input models come from the generated `tool_use` union (`_computer_inputs`); what is
kept by hand here is what the generated types do not carry — each member's result kind and the
confirmation text the model reads after a pure action. Every member is on by default.
"""

from __future__ import annotations

from typing import Mapping
from typing_extensions import Literal, TypeAlias

from ._base import Member, Registry, ResultKind
from ._computer_inputs import (
    COMPUTER_INPUT_TYPES,
    COMPUTER_MEMBER_NAMES,
    BetaComputerMemberName,
    BetaComputerMemberInput,
)

__all__ = ["FAMILY", "TOOLSET_TYPE", "CONFIRM_REQUIRED", "ComputerMember", "COMPUTER", "COMPUTER_MEMBERS"]

FAMILY: Literal["computer"] = "computer"
TOOLSET_TYPE: Literal["computer_toolset_20260801"] = "computer_toolset_20260801"
# The API data marks no computer member as needing `confirm`, so unlike the browser's, this list is the SDK's own.
CONFIRM_REQUIRED: frozenset[str] = frozenset({"type", "key", "hold_key"})
"""Members that need a `confirm` callable: keyboard input goes to whichever window has focus, and what the screen
shows can steer what the model types."""

ComputerMember: TypeAlias = Member[BetaComputerMemberName, BetaComputerMemberInput]

ROWS: dict[str, "tuple[ResultKind, str | None]"] = {
    "key": ("none", "Pressed {text}."),
    "hold_key": ("none", "Held {text} for {duration}s."),
    "type": ("none", "Typed."),
    "cursor_position": ("point", None),
    "mouse_move": ("none", "Moved the mouse."),
    "left_mouse_down": ("none", "Left mouse button pressed."),
    "left_mouse_up": ("none", "Left mouse button released."),
    "left_click": ("none", "Clicked."),
    "left_click_drag": ("none", "Dragged."),
    "right_click": ("none", "Right-clicked."),
    "middle_click": ("none", "Middle-clicked."),
    "double_click": ("none", "Double-clicked."),
    "triple_click": ("none", "Triple-clicked."),
    "scroll": ("none", "Scrolled {scroll_direction}."),
    "wait": ("none", "Waited {duration}s."),
    "screenshot": ("screenshot", None),
    "zoom": ("screenshot", None),
}


def build_registry() -> dict[str, ComputerMember]:
    names: "set[str]" = set(COMPUTER_MEMBER_NAMES)
    missing = names - set(ROWS)
    extra = set(ROWS) - names
    if missing or extra:  # pragma: no cover - an import-time guard, exercised whenever codegen changes the set
        raise AssertionError(f"computer member registry drift: missing={sorted(missing)} extra={sorted(extra)}")
    table: dict[str, ComputerMember] = {}
    for name in COMPUTER_MEMBER_NAMES:
        result, text = ROWS[name]
        table[name] = ComputerMember(name=name, input=COMPUTER_INPUT_TYPES[name], result=result, text=text)
    return table


COMPUTER: Registry[BetaComputerMemberName, BetaComputerMemberInput] = Registry(
    family=FAMILY, helper_tag="computer-toolset", members=build_registry()
)
"""The computer family: its members in the generated union's order, and what it is called on the wire."""

COMPUTER_MEMBERS: Mapping[str, ComputerMember] = COMPUTER.members
"""Every computer member by name, in the generated union's order; a name the model made up is simply absent."""
