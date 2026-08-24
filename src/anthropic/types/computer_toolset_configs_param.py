# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .computer_key_config_param import ComputerKeyConfigParam
from .computer_type_config_param import ComputerTypeConfigParam
from .computer_wait_config_param import ComputerWaitConfigParam
from .computer_zoom_config_param import ComputerZoomConfigParam
from .computer_scroll_config_param import ComputerScrollConfigParam
from .computer_hold_key_config_param import ComputerHoldKeyConfigParam
from .computer_left_click_config_param import ComputerLeftClickConfigParam
from .computer_mouse_move_config_param import ComputerMouseMoveConfigParam
from .computer_screenshot_config_param import ComputerScreenshotConfigParam
from .computer_right_click_config_param import ComputerRightClickConfigParam
from .computer_double_click_config_param import ComputerDoubleClickConfigParam
from .computer_middle_click_config_param import ComputerMiddleClickConfigParam
from .computer_triple_click_config_param import ComputerTripleClickConfigParam
from .computer_left_mouse_up_config_param import ComputerLeftMouseUpConfigParam
from .computer_cursor_position_config_param import ComputerCursorPositionConfigParam
from .computer_left_click_drag_config_param import ComputerLeftClickDragConfigParam
from .computer_left_mouse_down_config_param import ComputerLeftMouseDownConfigParam

__all__ = ["ComputerToolsetConfigsParam"]


class ComputerToolsetConfigsParam(TypedDict, total=False):
    """
    Per-member configuration for ``computer_toolset_20260801``: one
    optional field per member tool, keyed by the member name — the same
    name the member's ``tool_use`` blocks carry. Every member is an
    accepted key, and a member's defaults apply wherever its key is
    absent. Unknown keys are rejected: the field set is this toolset
    version's complete member set.
    """

    cursor_position: Optional[ComputerCursorPositionConfigParam]
    """`cursor_position`'s config overrides."""

    double_click: Optional[ComputerDoubleClickConfigParam]
    """`double_click`'s config overrides."""

    hold_key: Optional[ComputerHoldKeyConfigParam]
    """`hold_key`'s config overrides."""

    key: Optional[ComputerKeyConfigParam]
    """`key`'s config overrides."""

    left_click: Optional[ComputerLeftClickConfigParam]
    """`left_click`'s config overrides."""

    left_click_drag: Optional[ComputerLeftClickDragConfigParam]
    """`left_click_drag`'s config overrides."""

    left_mouse_down: Optional[ComputerLeftMouseDownConfigParam]
    """`left_mouse_down`'s config overrides."""

    left_mouse_up: Optional[ComputerLeftMouseUpConfigParam]
    """`left_mouse_up`'s config overrides."""

    middle_click: Optional[ComputerMiddleClickConfigParam]
    """`middle_click`'s config overrides."""

    mouse_move: Optional[ComputerMouseMoveConfigParam]
    """`mouse_move`'s config overrides."""

    right_click: Optional[ComputerRightClickConfigParam]
    """`right_click`'s config overrides."""

    screenshot: Optional[ComputerScreenshotConfigParam]
    """`screenshot`'s config overrides."""

    scroll: Optional[ComputerScrollConfigParam]
    """`scroll`'s config overrides."""

    triple_click: Optional[ComputerTripleClickConfigParam]
    """`triple_click`'s config overrides."""

    type: Optional[ComputerTypeConfigParam]
    """`type`'s config overrides."""

    wait: Optional[ComputerWaitConfigParam]
    """`wait`'s config overrides."""

    zoom: Optional[ComputerZoomConfigParam]
    """`zoom`'s config overrides."""
