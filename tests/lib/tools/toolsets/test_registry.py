"""The member registry against the published toolset definition.

`BROWSER_TOOLSET_MEMBERS` is the toolset's member table, generated from the API's definition. The
registry derives names and inputs from the generated types. It keeps result kinds, templates and
default-disabled flags by hand. These tests fail when either side moves without the other.
"""

from __future__ import annotations

import re
from typing import Any, cast
from typing_extensions import get_args, get_type_hints

from anthropic._data import BROWSER_TOOLSET_MEMBERS
from anthropic.types.beta import (
    BetaBrowserMemberName,
    BetaBrowserMemberInput,
    BetaBrowserNewTabInput,
    BetaBrowserListTabsInput,
    BetaBrowserNavigateInput,
    BetaBrowserStateChangeParam,
    BetaBrowserToolsetConfigsParam,
)
from anthropic.lib.tools._toolsets._inputs import BROWSER_INPUT_TYPES, BROWSER_MEMBER_NAMES
from anthropic.lib.tools._toolsets._render import DOWNLOAD_TYPES, TEMPLATE_FIELDS
from anthropic.lib.tools._toolsets._registry import (
    ROWS,
    BROWSER_MEMBERS,
    CONFIRM_REQUIRED,
    STATE_ONLY_MEMBERS,
    BROWSER_DEFAULT_DISABLED_MEMBERS,
    member_enabled,
)


def test_member_set_matches_the_published_toolset() -> None:
    assert set(BROWSER_MEMBER_NAMES) == set(BROWSER_TOOLSET_MEMBERS)
    assert set(BROWSER_MEMBERS) == set(BROWSER_TOOLSET_MEMBERS)
    assert len(BROWSER_MEMBER_NAMES) == len(set(BROWSER_MEMBER_NAMES)) == 31


def test_default_disabled_members_match_the_published_toolset() -> None:
    assert BROWSER_DEFAULT_DISABLED_MEMBERS == frozenset(
        name for name, member in BROWSER_TOOLSET_MEMBERS.items() if not member["enabled_by_default"]
    )


def test_result_kinds_confirmations_and_default_flags_match_the_published_toolset() -> None:
    generated = {
        name: (member["result"], member["confirmation"], member["enabled_by_default"])
        for name, member in BROWSER_TOOLSET_MEMBERS.items()
    }
    assert ROWS == generated, (
        "ROWS in lib/tools/_toolsets/_registry.py has drifted from the generated BROWSER_TOOLSET_MEMBERS: "
        "update ROWS to match (result kind, confirmation text, enabled by default)"
    )


def test_members_that_need_a_confirm_match_the_published_toolset() -> None:
    generated = frozenset(name for name, member in BROWSER_TOOLSET_MEMBERS.items() if member["confirm_required"])
    assert CONFIRM_REQUIRED == generated, (
        "CONFIRM_REQUIRED in lib/tools/_toolsets/_registry.py has drifted from the generated BROWSER_TOOLSET_MEMBERS: "
        "update it to the members marked confirm_required, because a member missing from it runs without a `confirm`"
    )


def test_member_set_matches_the_generated_configs_param() -> None:
    # The wire configs object has one key per member; a member the SDK does not know could not be
    # configured, and one the API does not know would be rejected.
    assert set(BetaBrowserToolsetConfigsParam.__annotations__) == set(BROWSER_MEMBER_NAMES)


def test_static_aliases_agree_with_the_derived_tables() -> None:
    assert set(get_args(BetaBrowserMemberName)) == set(BROWSER_MEMBER_NAMES)
    assert set(cast("tuple[type, ...]", get_args(BetaBrowserMemberInput))) == set(BROWSER_INPUT_TYPES.values())
    assert BROWSER_INPUT_TYPES["navigate"] is BetaBrowserNavigateInput
    # The two property-less members have no generated model; the SDK's stand-ins fill the slots.
    assert BROWSER_INPUT_TYPES["new_tab"] is BetaBrowserNewTabInput
    assert BROWSER_INPUT_TYPES["list_tabs"] is BetaBrowserListTabsInput


def test_every_pure_action_has_confirmation_text_and_tab_members_render_state_only() -> None:
    for name, member in BROWSER_MEMBERS.items():
        assert member.input is BROWSER_INPUT_TYPES[name]
        if name in STATE_ONLY_MEMBERS:
            # The API produces the text for these from the browser_state block; the SDK adds none.
            assert member.text is None
            assert member.result in ("tab", "tabs", "none")
        elif member.result == "none":
            assert member.text, f"{name} is a pure action with nothing for the model to read"


def test_derived_member_sets() -> None:
    # The tab members render no content of their own.
    assert STATE_ONLY_MEMBERS == {"new_tab", "list_tabs", "switch_tab", "close_tab"}


def test_member_enabled_fails_closed() -> None:
    assert member_enabled("navigate", None) is True
    assert member_enabled("javascript_exec", None) is False
    assert member_enabled("javascript_exec", {"javascript_exec": {"enabled": True}}) is True
    assert member_enabled("navigate", {"navigate": {"enabled": False}}) is False

    # Anything but a real boolean turns the member off rather than on.
    assert member_enabled("javascript_exec", {"javascript_exec": {"enabled": "yes"}}) is False
    assert member_enabled("navigate", {"navigate": {"enabled": 1}}) is False
    assert member_enabled("navigate", {"navigate": {"defer_loading": True}}) is True

    # An entry that is neither a mapping nor None reads as off too, so `{"navigate": False}` cannot leave navigate on.
    assert member_enabled("navigate", cast(Any, {"navigate": False})) is False
    assert member_enabled("navigate", cast(Any, {"navigate": "off"})) is False
    assert member_enabled("navigate", {"navigate": None}) is True  # None is the wire type's "defaults"


def test_every_confirmation_placeholder_has_a_template_field() -> None:
    # A `{name}` in a member's confirmation text that `_render` does not know would reach the model as written.
    placeholders = {
        name for member in BROWSER_MEMBERS.values() if member.text for name in re.findall(r"{(\w+)}", member.text)
    }
    assert placeholders == set(TEMPLATE_FIELDS)


def test_every_state_change_kind_is_either_tab_opened_or_a_download_kind() -> None:
    """A new change kind with a `url` in the generated union must be added to DOWNLOAD_TYPES, or the SDK neither
    bounds its `url` nor checks its `path` and `error` against the file policy."""
    kinds = {get_args(get_type_hints(variant)["type"])[0] for variant in get_args(BetaBrowserStateChangeParam)}
    assert kinds == {"tab_opened", *DOWNLOAD_TYPES}
