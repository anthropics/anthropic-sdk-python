"""The computer toolset's public surface: every name the guide documents imports from `anthropic.tools.computer`,
the abstract classes carry the constructor options and member methods a driver overrides, and what is shared with
the browser toolset is the same object in both modules."""

from __future__ import annotations

import inspect
from typing_extensions import get_args, get_type_hints

import anthropic.tools as tools
import anthropic.types.beta as beta
import anthropic.tools.browser as browser
import anthropic.tools.computer as surface
from anthropic.tools import (
    ToolError,
    ToolsetUsageError,
    ToolsetClosedError,
    ToolsetConfigError,
    ToolsetContractError,
)
from anthropic._compat import field_outer_type, get_model_fields
from anthropic.types.beta import BetaBase64ImageSourceParam
from anthropic.tools.computer import (
    BetaScreenshotResult,
    BetaComputerCursorPositionResult,
    BetaAbstractComputerToolset20260801,
    BetaAsyncAbstractComputerToolset20260801,
)
from anthropic.lib.tools._toolsets._render import image_block
from anthropic.lib.tools._toolsets._computer_inputs import COMPUTER_MEMBER_NAMES

REFUSALS = [
    "UnknownMemberError",
    "DisabledMemberError",
    "UnavailableMemberError",
    "InvalidMemberInputError",
    "ConfirmDeclinedError",
    "ConfirmFailedError",
]


def test_every_documented_name_is_exported() -> None:
    for name in surface.__all__:
        assert hasattr(surface, name), name
        assert getattr(tools, name) is getattr(surface, name), name  # re-exported by the package too
    assert not hasattr(surface, "COMPUTER_MEMBER_NAMES")
    assert not hasattr(tools, "COMPUTER_MEMBER_NAMES")
    generated = {name for name in dir(beta) if name.startswith("BetaComputer")}
    assert generated.isdisjoint(dir(surface)), "import generated types from anthropic.types.beta only"
    assert generated.isdisjoint(dir(tools))


def test_the_error_family_is_one_hierarchy_shared_with_the_browser_toolset() -> None:
    for cls in (ToolsetClosedError, ToolsetConfigError, ToolsetContractError):
        assert issubclass(cls, ToolsetUsageError)
    for name in REFUSALS:
        cls = getattr(tools, name)
        assert issubclass(cls, ToolError) and cls is not ToolError
    # the shared errors are exported from `anthropic.tools` only, as for the browser toolset
    shared = ["ToolError", "ToolsetUsageError", "ToolsetClosedError", "ToolsetConfigError", "ToolsetContractError"]
    for name in (*shared, *REFUSALS):
        assert hasattr(tools, name), name
        assert not hasattr(surface, name) and not hasattr(browser, name), name
    for name in ("BetaToolsetCallContext", "BetaToolsetContent", "BetaToolConfigs"):
        assert getattr(surface, name) is getattr(browser, name)


def test_the_abstract_classes_declare_every_member_and_the_constructor_options() -> None:
    for cls in (BetaAbstractComputerToolset20260801, BetaAsyncAbstractComputerToolset20260801):
        assert set(inspect.signature(cls.__init__).parameters) - {"self"} == {"configs", "confirm", "tool_configs"}
        for member in COMPUTER_MEMBER_NAMES:
            assert callable(getattr(cls, member)), member
        for method in ("call", "execute", "to_dict", "tool_result", "close"):
            assert callable(getattr(cls, method)), method
    sync_members = {
        m
        for m in COMPUTER_MEMBER_NAMES
        if not inspect.iscoroutinefunction(getattr(BetaAbstractComputerToolset20260801, m))
    }
    async_members = {
        m
        for m in COMPUTER_MEMBER_NAMES
        if inspect.iscoroutinefunction(getattr(BetaAsyncAbstractComputerToolset20260801, m))
    }
    assert sync_members == async_members == set(COMPUTER_MEMBER_NAMES)


def test_value_types_construct() -> None:
    assert BetaScreenshotResult(data="AAAA").media_type == "image/png"
    assert BetaComputerCursorPositionResult(x=1, y=2).to_dict() == {"x": 1, "y": 2}


def test_a_toolset_instance_is_a_tool_like() -> None:
    from anthropic.lib.tools._tool_params import SupportsToDict

    assert issubclass(BetaAbstractComputerToolset20260801, SupportsToDict)


def test_image_media_types_track_the_generated_image_source() -> None:
    # BetaScreenshotResult.media_type (_computer_results.py) and image_block's media_type (_render.py) copy
    # BetaBase64ImageSourceParam's media types by hand. When this fails, make both Literals match it.
    expected = set(get_args(get_type_hints(BetaBase64ImageSourceParam)["media_type"]))
    assert set(get_args(field_outer_type(get_model_fields(BetaScreenshotResult)["media_type"]))) == expected
    assert set(get_args(get_type_hints(image_block)["media_type"])) == expected
