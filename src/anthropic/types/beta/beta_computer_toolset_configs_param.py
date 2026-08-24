# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .beta_computer_key_config_param import BetaComputerKeyConfigParam
from .beta_computer_type_config_param import BetaComputerTypeConfigParam
from .beta_computer_wait_config_param import BetaComputerWaitConfigParam
from .beta_computer_zoom_config_param import BetaComputerZoomConfigParam
from .beta_computer_scroll_config_param import BetaComputerScrollConfigParam
from .beta_computer_hold_key_config_param import BetaComputerHoldKeyConfigParam
from .beta_computer_left_click_config_param import BetaComputerLeftClickConfigParam
from .beta_computer_mouse_move_config_param import BetaComputerMouseMoveConfigParam
from .beta_computer_screenshot_config_param import BetaComputerScreenshotConfigParam
from .beta_computer_right_click_config_param import BetaComputerRightClickConfigParam
from .beta_computer_double_click_config_param import BetaComputerDoubleClickConfigParam
from .beta_computer_middle_click_config_param import BetaComputerMiddleClickConfigParam
from .beta_computer_triple_click_config_param import BetaComputerTripleClickConfigParam
from .beta_computer_left_mouse_up_config_param import BetaComputerLeftMouseUpConfigParam
from .beta_computer_cursor_position_config_param import BetaComputerCursorPositionConfigParam
from .beta_computer_left_click_drag_config_param import BetaComputerLeftClickDragConfigParam
from .beta_computer_left_mouse_down_config_param import BetaComputerLeftMouseDownConfigParam

__all__ = ["BetaComputerToolsetConfigsParam"]


class BetaComputerToolsetConfigsParam(TypedDict, total=False):
    """
    Per-member configuration for ``computer_toolset_20260801``: one
    optional field per member tool, keyed by the member name — the same
    name the member's ``tool_use`` blocks carry. Every member is an
    accepted key, and a member's defaults apply wherever its key is
    absent. Unknown keys are rejected: the field set is this toolset
    version's complete member set.
    """

    cursor_position: Optional[BetaComputerCursorPositionConfigParam]
    """`cursor_position`'s config overrides."""

    double_click: Optional[BetaComputerDoubleClickConfigParam]
    """`double_click`'s config overrides."""

    hold_key: Optional[BetaComputerHoldKeyConfigParam]
    """`hold_key`'s config overrides."""

    key: Optional[BetaComputerKeyConfigParam]
    """`key`'s config overrides."""

    left_click: Optional[BetaComputerLeftClickConfigParam]
    """`left_click`'s config overrides."""

    left_click_drag: Optional[BetaComputerLeftClickDragConfigParam]
    """`left_click_drag`'s config overrides."""

    left_mouse_down: Optional[BetaComputerLeftMouseDownConfigParam]
    """`left_mouse_down`'s config overrides."""

    left_mouse_up: Optional[BetaComputerLeftMouseUpConfigParam]
    """`left_mouse_up`'s config overrides."""

    middle_click: Optional[BetaComputerMiddleClickConfigParam]
    """`middle_click`'s config overrides."""

    mouse_move: Optional[BetaComputerMouseMoveConfigParam]
    """`mouse_move`'s config overrides."""

    right_click: Optional[BetaComputerRightClickConfigParam]
    """`right_click`'s config overrides."""

    screenshot: Optional[BetaComputerScreenshotConfigParam]
    """`screenshot`'s config overrides."""

    scroll: Optional[BetaComputerScrollConfigParam]
    """`scroll`'s config overrides."""

    triple_click: Optional[BetaComputerTripleClickConfigParam]
    """`triple_click`'s config overrides."""

    type: Optional[BetaComputerTypeConfigParam]
    """`type`'s config overrides."""

    wait: Optional[BetaComputerWaitConfigParam]
    """`wait`'s config overrides."""

    zoom: Optional[BetaComputerZoomConfigParam]
    """`zoom`'s config overrides."""
