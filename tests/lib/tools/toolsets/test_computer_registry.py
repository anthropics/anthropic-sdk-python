"""The computer member registry against the published toolset definition.

`computer_toolset_20260801.json` is a checked-in copy of the toolset's member set as the API defines it. The
registry derives names and inputs from the generated types and keeps result kinds and templates by hand; these
tests fail when either side moves without the other.
"""

from __future__ import annotations

import re
import json
from typing import Any, cast
from pathlib import Path
from typing_extensions import get_args

from anthropic.types.beta import (
    BetaComputerKeyInput,
    BetaComputerZoomInput,
    BetaComputerMemberName,
    BetaComputerMemberInput,
    BetaComputerScreenshotInput,
    BetaComputerLeftMouseUpInput,
    BetaComputerLeftMouseDownInput,
    BetaComputerCursorPositionInput,
    BetaComputerToolsetConfigsParam,
)
from anthropic.lib.tools._toolsets._render import TEMPLATE_FIELDS
from anthropic.lib.tools._toolsets._computer_inputs import COMPUTER_INPUT_TYPES, COMPUTER_MEMBER_NAMES
from anthropic.lib.tools._toolsets._computer_registry import COMPUTER, COMPUTER_MEMBERS

SPEC: dict[str, Any] = json.loads((Path(__file__).parent / "computer_toolset_20260801.json").read_text())


def test_member_set_matches_the_published_toolset_in_its_order() -> None:
    assert COMPUTER_MEMBER_NAMES == SPEC["members"]
    assert list(COMPUTER_MEMBERS) == SPEC["members"]
    assert len(COMPUTER_MEMBER_NAMES) == len(set(COMPUTER_MEMBER_NAMES)) == 17


def test_every_member_is_enabled_by_default() -> None:
    assert SPEC["default_disabled"] == []
    assert COMPUTER.default_disabled == frozenset()
    assert all(member.enabled_by_default for member in COMPUTER_MEMBERS.values())


def test_member_set_matches_the_generated_configs_param() -> None:
    # The wire configs object has one key per member; a member the SDK does not know could not be
    # configured, and one the API does not know would be rejected.
    assert set(BetaComputerToolsetConfigsParam.__annotations__) == set(COMPUTER_MEMBER_NAMES)


def test_static_aliases_agree_with_the_derived_tables() -> None:
    assert set(get_args(BetaComputerMemberName)) == set(COMPUTER_MEMBER_NAMES)
    assert set(cast("tuple[type, ...]", get_args(BetaComputerMemberInput))) == set(COMPUTER_INPUT_TYPES.values())
    assert COMPUTER_INPUT_TYPES["key"] is BetaComputerKeyInput
    assert COMPUTER_INPUT_TYPES["zoom"] is BetaComputerZoomInput
    assert COMPUTER_INPUT_TYPES["screenshot"] is BetaComputerScreenshotInput
    assert COMPUTER_INPUT_TYPES["cursor_position"] is BetaComputerCursorPositionInput
    assert COMPUTER_INPUT_TYPES["left_mouse_down"] is BetaComputerLeftMouseDownInput
    assert COMPUTER_INPUT_TYPES["left_mouse_up"] is BetaComputerLeftMouseUpInput


def test_result_kinds_and_confirmation_texts() -> None:
    for name, member in COMPUTER_MEMBERS.items():
        assert member.input is COMPUTER_INPUT_TYPES[name]
        if name in ("screenshot", "zoom"):
            assert member.result == "screenshot" and member.text is None
        elif name == "cursor_position":
            assert member.result == "point" and member.text is None
        else:
            assert member.result == "none"
            assert member.text, f"{name} is a pure action with nothing for the model to read"


def test_member_enabled_fails_closed() -> None:
    enabled = COMPUTER.member_enabled
    assert enabled("zoom", None) is True
    assert enabled("zoom", {"zoom": {"enabled": False}}) is False
    assert enabled("zoom", {"zoom": {"enabled": True}}) is True
    # Anything but a real boolean turns the member off rather than on.
    assert enabled("zoom", {"zoom": {"enabled": "yes"}}) is False
    assert enabled("zoom", {"zoom": {"defer_loading": True}}) is True
    assert enabled("zoom", cast(Any, {"zoom": False})) is False
    assert enabled("zoom", {"zoom": None}) is True  # None is the wire type's "defaults"


def test_every_confirmation_placeholder_has_a_template_field() -> None:
    # A `{name}` in a member's confirmation text that `_render` does not know would reach the model as written.
    placeholders = {
        name for member in COMPUTER_MEMBERS.values() if member.text for name in re.findall(r"{(\w+)}", member.text)
    }
    assert placeholders <= set(TEMPLATE_FIELDS)
    assert placeholders == {"text", "duration", "scroll_direction"}
