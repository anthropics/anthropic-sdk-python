"""The browser toolset's public surface: every name the guide documents imports from `anthropic.tools.browser`,
and the abstract classes carry the constructor options and member methods a driver overrides."""

from __future__ import annotations

import inspect
from typing import Any, cast
from typing_extensions import get_args, get_type_hints

import pytest
import pydantic

import anthropic.tools.browser as surface
from anthropic.tools import (
    ToolError,
    ToolsetUsageError,
    ConfirmFailedError,
    ToolsetClosedError,
    ToolsetConfigError,
    UnknownMemberError,
    DisabledMemberError,
    ConfirmDeclinedError,
    ToolsetContractError,
    UnavailableMemberError,
    InvalidMemberInputError,
)
from anthropic._compat import PYDANTIC_V1, field_outer_type, get_model_fields
from anthropic.lib.tools import BetaToolLike
from anthropic.types.beta import BetaBase64ImageSourceParam
from anthropic.tools.browser import (
    BetaURLContext,
    TabMissingError,
    URLRefusedError,
    BetaBrowserState,
    UploadRefusedError,
    BetaDialogDismissed,
    BetaScreenshotResult,
    BetaNavigationRefused,
    BetaAbstractBrowserToolset20260801,
    BetaAsyncAbstractBrowserToolset20260801,
)
from anthropic.lib.tools._tool_params import SupportsToDict
from anthropic.lib.tools._toolsets._inputs import BROWSER_MEMBER_NAMES
from anthropic.lib.tools._toolsets._registry import BROWSER_DEFAULT_DISABLED_MEMBERS


def test_every_documented_name_is_exported() -> None:
    for name in surface.__all__:
        assert hasattr(surface, name), name
    assert not hasattr(surface, "BROWSER_MEMBER_NAMES")
    assert not hasattr(surface, "BROWSER_DEFAULT_DISABLED_MEMBERS")


def test_the_error_family_is_one_hierarchy() -> None:
    for cls in (ToolsetClosedError, ToolsetConfigError, ToolsetContractError):
        assert issubclass(cls, ToolsetUsageError)


REFUSALS = [
    "UnknownMemberError",
    "DisabledMemberError",
    "UnavailableMemberError",
    "InvalidMemberInputError",
    "URLRefusedError",
    "TabMissingError",
    "ConfirmDeclinedError",
    "ConfirmFailedError",
    "UploadRefusedError",
]


def test_the_refusals_are_exported_tool_errors() -> None:
    classes = [
        UnknownMemberError,
        DisabledMemberError,
        UnavailableMemberError,
        InvalidMemberInputError,
        URLRefusedError,
        TabMissingError,
        ConfirmDeclinedError,
        ConfirmFailedError,
        UploadRefusedError,
    ]
    assert [cls.__name__ for cls in classes] == REFUSALS
    for cls in classes:
        assert issubclass(cls, ToolError) and cls is not ToolError


def test_the_module_exports_only_the_browser_only_errors() -> None:
    errors = [name for name in surface.__all__ if name.endswith("Error")]
    assert errors == ["URLRefusedError", "TabMissingError", "UploadRefusedError"]
    # the errors shared with the computer toolset are exported from `anthropic.tools`, not from here
    shared = set(REFUSALS) - set(errors) | {
        "ToolError",
        "ToolsetUsageError",
        "ToolsetConfigError",
        "ToolsetContractError",
    }
    for name in shared | {"ToolsetClosedError"}:
        assert not hasattr(surface, name), name


def test_the_abstract_classes_declare_every_member_and_the_constructor_options() -> None:
    options = {"configs", "confirm", "url_policy", "file_policy", "tool_configs"}
    for cls in (BetaAbstractBrowserToolset20260801, BetaAsyncAbstractBrowserToolset20260801):
        params = set(inspect.signature(cls.__init__).parameters) - {"self"}
        assert params == options
        for member in BROWSER_MEMBER_NAMES:
            assert callable(getattr(cls, member)), member
        for method in ("call", "execute", "to_dict", "tool_result", "_browser_state"):
            assert callable(getattr(cls, method)), method
        assert getattr(cls._browser_state, "__isabstractmethod__", False)
    assert BROWSER_DEFAULT_DISABLED_MEMBERS <= set(BROWSER_MEMBER_NAMES)
    sync_members = {
        m
        for m in BROWSER_MEMBER_NAMES
        if not inspect.iscoroutinefunction(getattr(BetaAbstractBrowserToolset20260801, m))
    }
    async_members = {
        m
        for m in BROWSER_MEMBER_NAMES
        if inspect.iscoroutinefunction(getattr(BetaAsyncAbstractBrowserToolset20260801, m))
    }
    assert sync_members == async_members == set(BROWSER_MEMBER_NAMES)


def test_value_types_construct() -> None:
    from anthropic._compat import get_model_fields

    assert BetaBrowserState(tabs=[]).state_changes == []
    assert set(get_model_fields(BetaURLContext)) == {"member", "tab_id", "tool_use_id"}


def test_state_changes_are_told_apart_by_their_type() -> None:
    # A wire change written as a dict comes back as an equal dict, extra keys and all; the SDK's own kinds arrive as
    # instances or as dicts carrying their `type`. Every entry is matched by `type` alone, never by the keys it shares.
    download: Any = {
        "type": "download_completed",
        "download_id": "d1",
        "url": "https://a.test/f",
        "filename": "f",
        "x": 1,
    }
    opened: Any = {"type": "tab_opened", "tab_id": "tab_2", "url": "https://a.test/"}
    refused = BetaNavigationRefused()
    dialog: Any = {"type": "dialog_dismissed", "kind": "confirm", "message": "Sure?"}

    state = BetaBrowserState(tabs=[], state_changes=[download, opened, refused, dialog])
    assert state.state_changes[:2] == [download, opened]
    assert [type(c) for c in state.state_changes] == [dict, dict, BetaNavigationRefused, BetaDialogDismissed]
    assert state.state_changes[3] == BetaDialogDismissed(kind="confirm", message="Sure?")

    def errors(change: dict[str, Any]) -> list[Any]:
        with pytest.raises(pydantic.ValidationError) as caught:
            BetaBrowserState(tabs=[], state_changes=[cast(Any, change)])
        return caught.value.errors()

    (missing,) = errors({"download_id": "d1", "url": "https://a.test/f"})
    assert "'type'" in missing["msg"]
    (empty,) = errors({})  # an SDK kind written as a dict without its `type`
    assert "'type'" in empty["msg"]
    (unknown,) = errors({"type": "made_up", "url": "https://a.test/"})

    tags = (
        "tab_opened",
        "download_started",
        "download_completed",
        "download_failed",
        "navigation_refused",
        "dialog_dismissed",
    )
    assert all(tag in unknown["msg"] for tag in tags)

    if not PYDANTIC_V1:  # pydantic v1 does not enforce a generated param's `Required` keys
        (typo,) = errors({"type": "download_completed", "downlaod_id": "d1", "url": "https://a.test/f"})
        assert typo["loc"][-1] == "download_id" and "required" in typo["msg"].lower()


def test_a_toolset_instance_is_a_tool_like() -> None:
    assert BetaToolLike is not None
    assert issubclass(BetaAbstractBrowserToolset20260801, SupportsToDict)


def test_screenshot_media_types_track_the_generated_image_source() -> None:
    # BetaScreenshotResult.media_type lists the generated image source's media types by hand. When this fails,
    # make that Literal in _results.py match the generated one.
    generated = get_type_hints(BetaBase64ImageSourceParam)["media_type"]
    declared = field_outer_type(get_model_fields(BetaScreenshotResult)["media_type"])
    assert set(get_args(declared)) == set(get_args(generated))
