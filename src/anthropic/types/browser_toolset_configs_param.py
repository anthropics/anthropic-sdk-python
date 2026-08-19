# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .browser_key_config_param import BrowserKeyConfigParam
from .browser_find_config_param import BrowserFindConfigParam
from .browser_type_config_param import BrowserTypeConfigParam
from .browser_wait_config_param import BrowserWaitConfigParam
from .browser_zoom_config_param import BrowserZoomConfigParam
from .browser_hover_config_param import BrowserHoverConfigParam
from .browser_scroll_config_param import BrowserScrollConfigParam
from .browser_new_tab_config_param import BrowserNewTabConfigParam
from .browser_hold_key_config_param import BrowserHoldKeyConfigParam
from .browser_navigate_config_param import BrowserNavigateConfigParam
from .browser_close_tab_config_param import BrowserCloseTabConfigParam
from .browser_list_tabs_config_param import BrowserListTabsConfigParam
from .browser_read_page_config_param import BrowserReadPageConfigParam
from .browser_scroll_to_config_param import BrowserScrollToConfigParam
from .browser_form_input_config_param import BrowserFormInputConfigParam
from .browser_left_click_config_param import BrowserLeftClickConfigParam
from .browser_mouse_move_config_param import BrowserMouseMoveConfigParam
from .browser_screenshot_config_param import BrowserScreenshotConfigParam
from .browser_switch_tab_config_param import BrowserSwitchTabConfigParam
from .browser_file_upload_config_param import BrowserFileUploadConfigParam
from .browser_right_click_config_param import BrowserRightClickConfigParam
from .browser_double_click_config_param import BrowserDoubleClickConfigParam
from .browser_middle_click_config_param import BrowserMiddleClickConfigParam
from .browser_read_console_config_param import BrowserReadConsoleConfigParam
from .browser_read_network_config_param import BrowserReadNetworkConfigParam
from .browser_triple_click_config_param import BrowserTripleClickConfigParam
from .browser_get_page_text_config_param import BrowserGetPageTextConfigParam
from .browser_left_mouse_up_config_param import BrowserLeftMouseUpConfigParam
from .browser_javascript_exec_config_param import BrowserJavascriptExecConfigParam
from .browser_left_click_drag_config_param import BrowserLeftClickDragConfigParam
from .browser_left_mouse_down_config_param import BrowserLeftMouseDownConfigParam

__all__ = ["BrowserToolsetConfigsParam"]


class BrowserToolsetConfigsParam(TypedDict, total=False):
    """
    Per-member configuration for ``browser_toolset_20260801``: one
    optional field per member tool, keyed by the member name — the same
    name the member's ``tool_use`` blocks carry. Every member is an
    accepted key, and a member's defaults apply wherever its key is
    absent. Unknown keys are rejected: the field set is this toolset
    version's complete member set.
    """

    close_tab: Optional[BrowserCloseTabConfigParam]
    """`close_tab`'s config overrides."""

    double_click: Optional[BrowserDoubleClickConfigParam]
    """`double_click`'s config overrides."""

    file_upload: Optional[BrowserFileUploadConfigParam]
    """`file_upload`'s config overrides."""

    find: Optional[BrowserFindConfigParam]
    """`find`'s config overrides."""

    form_input: Optional[BrowserFormInputConfigParam]
    """`form_input`'s config overrides."""

    get_page_text: Optional[BrowserGetPageTextConfigParam]
    """`get_page_text`'s config overrides."""

    hold_key: Optional[BrowserHoldKeyConfigParam]
    """`hold_key`'s config overrides."""

    hover: Optional[BrowserHoverConfigParam]
    """`hover`'s config overrides."""

    javascript_exec: Optional[BrowserJavascriptExecConfigParam]
    """`javascript_exec`'s config overrides."""

    key: Optional[BrowserKeyConfigParam]
    """`key`'s config overrides."""

    left_click: Optional[BrowserLeftClickConfigParam]
    """`left_click`'s config overrides."""

    left_click_drag: Optional[BrowserLeftClickDragConfigParam]
    """`left_click_drag`'s config overrides."""

    left_mouse_down: Optional[BrowserLeftMouseDownConfigParam]
    """`left_mouse_down`'s config overrides."""

    left_mouse_up: Optional[BrowserLeftMouseUpConfigParam]
    """`left_mouse_up`'s config overrides."""

    list_tabs: Optional[BrowserListTabsConfigParam]
    """`list_tabs`'s config overrides."""

    middle_click: Optional[BrowserMiddleClickConfigParam]
    """`middle_click`'s config overrides."""

    mouse_move: Optional[BrowserMouseMoveConfigParam]
    """`mouse_move`'s config overrides."""

    navigate: Optional[BrowserNavigateConfigParam]
    """`navigate`'s config overrides."""

    new_tab: Optional[BrowserNewTabConfigParam]
    """`new_tab`'s config overrides."""

    read_console: Optional[BrowserReadConsoleConfigParam]
    """`read_console`'s config overrides."""

    read_network: Optional[BrowserReadNetworkConfigParam]
    """`read_network`'s config overrides."""

    read_page: Optional[BrowserReadPageConfigParam]
    """`read_page`'s config overrides."""

    right_click: Optional[BrowserRightClickConfigParam]
    """`right_click`'s config overrides."""

    screenshot: Optional[BrowserScreenshotConfigParam]
    """`screenshot`'s config overrides."""

    scroll: Optional[BrowserScrollConfigParam]
    """`scroll`'s config overrides."""

    scroll_to: Optional[BrowserScrollToConfigParam]
    """`scroll_to`'s config overrides."""

    switch_tab: Optional[BrowserSwitchTabConfigParam]
    """`switch_tab`'s config overrides."""

    triple_click: Optional[BrowserTripleClickConfigParam]
    """`triple_click`'s config overrides."""

    type: Optional[BrowserTypeConfigParam]
    """`type`'s config overrides."""

    wait: Optional[BrowserWaitConfigParam]
    """`wait`'s config overrides."""

    zoom: Optional[BrowserZoomConfigParam]
    """`zoom`'s config overrides."""
