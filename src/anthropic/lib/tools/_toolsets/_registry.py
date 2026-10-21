"""The browser member registry: one row per member, from which every other per-member table derives.

Member names and input models come from the generated `tool_use` union (`_inputs`). What is
kept by hand here is what the generated types lack: each member's result kind, the
confirmation text the model reads after a pure action, and which members the API disables by
default. A test diffs the member set and the default-disabled set against the published toolset
definition so the two cannot drift silently.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing_extensions import Literal, TypeAlias

from ._base import Member, Registry, ResultKind
from ._inputs import BROWSER_INPUT_TYPES, BROWSER_MEMBER_NAMES, BetaBrowserMemberName
from ....types.beta import BetaBrowserMemberInput

__all__ = [
    "CONFIRM_REQUIRED",
    "ResultKind",
    "Member",
    "BrowserMember",
    "BROWSER",
    "BROWSER_MEMBERS",
    "BROWSER_DEFAULT_DISABLED_MEMBERS",
    "STATE_ONLY_MEMBERS",
    "member_enabled",
]

FAMILY: Literal["browser"] = "browser"
CONFIRM_REQUIRED: frozenset[str] = frozenset({"javascript_exec", "file_upload"})
"""Members whose calls wait for a person unless the application's `confirm` approves them unattended: page
content can steer what the model asks them to do, and what they do reaches outside the page."""
TOOLSET_TYPE: Literal["browser_toolset_20260801"] = "browser_toolset_20260801"

BrowserMember: TypeAlias = Member[BetaBrowserMemberName, BetaBrowserMemberInput]


# Hand-kept: result kinds, confirmation templates and default-disabled flags. Everything else about
# a member is generated.
ROWS: dict[str, tuple[ResultKind, str | None, bool]] = {
    "navigate": ("navigate", None, True),
    "screenshot": ("screenshot", None, True),
    "zoom": ("screenshot", None, True),
    "left_click": ("none", "Clicked.", True),
    "right_click": ("none", "Right-clicked.", True),
    "middle_click": ("none", "Middle-clicked.", True),
    "double_click": ("none", "Double-clicked.", True),
    "triple_click": ("none", "Triple-clicked.", True),
    "hover": ("none", "Hovered.", True),
    "left_click_drag": ("none", "Dragged.", True),
    "left_mouse_down": ("none", "Mouse button pressed.", True),
    "left_mouse_up": ("none", "Mouse button released.", True),
    "mouse_move": ("none", "Moved the mouse.", True),
    "scroll": ("none", "Scrolled {scroll_direction}.", True),
    "scroll_to": ("none", "Scrolled to {ref}.", True),
    "type": ("none", "Typed.", True),
    "key": ("none", "Pressed {text}.", True),
    "hold_key": ("none", "Held {text} for {duration}s.", True),
    "form_input": ("none", "Set the value of {ref}.", True),
    "read_page": ("text", None, True),
    "find": ("text", None, True),
    "get_page_text": ("text", None, True),
    "wait": ("none", "Waited {duration}s.", True),
    "file_upload": ("none", "Uploaded.", False),
    "read_console": ("text", None, False),
    "read_network": ("text", None, False),
    "javascript_exec": ("text", None, False),
    "new_tab": ("tab", None, True),
    "list_tabs": ("tabs", None, True),
    "switch_tab": ("tab", None, True),
    "close_tab": ("none", None, True),
}


def build_registry() -> dict[str, BrowserMember]:
    names: set[str] = set(BROWSER_MEMBER_NAMES)
    missing = names - set(ROWS)
    extra = set(ROWS) - names
    if missing or extra:  # pragma: no cover - an import-time guard, exercised whenever codegen changes the set
        raise AssertionError(f"browser member registry drift: missing={sorted(missing)} extra={sorted(extra)}")
    table: dict[str, BrowserMember] = {}
    for name in BROWSER_MEMBER_NAMES:
        result, text, enabled = ROWS[name]
        table[name] = BrowserMember(
            name=name, input=BROWSER_INPUT_TYPES[name], result=result, text=text, enabled_by_default=enabled
        )
    return table


BROWSER: Registry[BetaBrowserMemberName, BetaBrowserMemberInput] = Registry(
    family=FAMILY, helper_tag="browser-toolset", members=build_registry()
)
"""The browser family: its members in the generated union's order, and what it is called on the wire."""

BROWSER_MEMBERS: Mapping[str, BrowserMember] = BROWSER.members
"""Every browser member by name, in the generated union's order. A name the model made up is absent."""

BROWSER_DEFAULT_DISABLED_MEMBERS: frozenset[str] = BROWSER.default_disabled
"""Members the API withholds unless `configs` enables them."""

STATE_ONLY_MEMBERS: frozenset[str] = frozenset(("new_tab", "list_tabs", "switch_tab", "close_tab"))
"""The tab members, which render no content of their own, so their non-error result is exactly one `browser_state`
block, and a line meant for the model (a refused navigation) waits for the next result that can hold it. Listed by
name rather than derived from `BROWSER_MEMBERS`, so a tab member that gains a confirmation line stays in the set."""


member_enabled = BROWSER.member_enabled
"""Whether `configs` leave a browser member enabled. See `Registry.member_enabled`."""
