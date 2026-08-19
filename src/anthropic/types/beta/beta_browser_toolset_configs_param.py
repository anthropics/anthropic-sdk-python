# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .beta_browser_key_config_param import BetaBrowserKeyConfigParam
from .beta_browser_find_config_param import BetaBrowserFindConfigParam
from .beta_browser_type_config_param import BetaBrowserTypeConfigParam
from .beta_browser_wait_config_param import BetaBrowserWaitConfigParam
from .beta_browser_zoom_config_param import BetaBrowserZoomConfigParam
from .beta_browser_hover_config_param import BetaBrowserHoverConfigParam
from .beta_browser_scroll_config_param import BetaBrowserScrollConfigParam
from .beta_browser_new_tab_config_param import BetaBrowserNewTabConfigParam
from .beta_browser_hold_key_config_param import BetaBrowserHoldKeyConfigParam
from .beta_browser_navigate_config_param import BetaBrowserNavigateConfigParam
from .beta_browser_close_tab_config_param import BetaBrowserCloseTabConfigParam
from .beta_browser_list_tabs_config_param import BetaBrowserListTabsConfigParam
from .beta_browser_read_page_config_param import BetaBrowserReadPageConfigParam
from .beta_browser_scroll_to_config_param import BetaBrowserScrollToConfigParam
from .beta_browser_form_input_config_param import BetaBrowserFormInputConfigParam
from .beta_browser_left_click_config_param import BetaBrowserLeftClickConfigParam
from .beta_browser_mouse_move_config_param import BetaBrowserMouseMoveConfigParam
from .beta_browser_screenshot_config_param import BetaBrowserScreenshotConfigParam
from .beta_browser_switch_tab_config_param import BetaBrowserSwitchTabConfigParam
from .beta_browser_file_upload_config_param import BetaBrowserFileUploadConfigParam
from .beta_browser_right_click_config_param import BetaBrowserRightClickConfigParam
from .beta_browser_double_click_config_param import BetaBrowserDoubleClickConfigParam
from .beta_browser_middle_click_config_param import BetaBrowserMiddleClickConfigParam
from .beta_browser_read_console_config_param import BetaBrowserReadConsoleConfigParam
from .beta_browser_read_network_config_param import BetaBrowserReadNetworkConfigParam
from .beta_browser_triple_click_config_param import BetaBrowserTripleClickConfigParam
from .beta_browser_get_page_text_config_param import BetaBrowserGetPageTextConfigParam
from .beta_browser_left_mouse_up_config_param import BetaBrowserLeftMouseUpConfigParam
from .beta_browser_javascript_exec_config_param import BetaBrowserJavascriptExecConfigParam
from .beta_browser_left_click_drag_config_param import BetaBrowserLeftClickDragConfigParam
from .beta_browser_left_mouse_down_config_param import BetaBrowserLeftMouseDownConfigParam

__all__ = ["BetaBrowserToolsetConfigsParam"]


class BetaBrowserToolsetConfigsParam(TypedDict, total=False):
    """
    Per-member configuration for ``browser_toolset_20260801``: one
    optional field per member tool, keyed by the member name — the same
    name the member's ``tool_use`` blocks carry. Every member is an
    accepted key, and a member's defaults apply wherever its key is
    absent. Unknown keys are rejected: the field set is this toolset
    version's complete member set.
    """

    close_tab: Optional[BetaBrowserCloseTabConfigParam]
    """`close_tab`'s config overrides."""

    double_click: Optional[BetaBrowserDoubleClickConfigParam]
    """`double_click`'s config overrides."""

    file_upload: Optional[BetaBrowserFileUploadConfigParam]
    """`file_upload`'s config overrides."""

    find: Optional[BetaBrowserFindConfigParam]
    """`find`'s config overrides."""

    form_input: Optional[BetaBrowserFormInputConfigParam]
    """`form_input`'s config overrides."""

    get_page_text: Optional[BetaBrowserGetPageTextConfigParam]
    """`get_page_text`'s config overrides."""

    hold_key: Optional[BetaBrowserHoldKeyConfigParam]
    """`hold_key`'s config overrides."""

    hover: Optional[BetaBrowserHoverConfigParam]
    """`hover`'s config overrides."""

    javascript_exec: Optional[BetaBrowserJavascriptExecConfigParam]
    """`javascript_exec`'s config overrides."""

    key: Optional[BetaBrowserKeyConfigParam]
    """`key`'s config overrides."""

    left_click: Optional[BetaBrowserLeftClickConfigParam]
    """`left_click`'s config overrides."""

    left_click_drag: Optional[BetaBrowserLeftClickDragConfigParam]
    """`left_click_drag`'s config overrides."""

    left_mouse_down: Optional[BetaBrowserLeftMouseDownConfigParam]
    """`left_mouse_down`'s config overrides."""

    left_mouse_up: Optional[BetaBrowserLeftMouseUpConfigParam]
    """`left_mouse_up`'s config overrides."""

    list_tabs: Optional[BetaBrowserListTabsConfigParam]
    """`list_tabs`'s config overrides."""

    middle_click: Optional[BetaBrowserMiddleClickConfigParam]
    """`middle_click`'s config overrides."""

    mouse_move: Optional[BetaBrowserMouseMoveConfigParam]
    """`mouse_move`'s config overrides."""

    navigate: Optional[BetaBrowserNavigateConfigParam]
    """`navigate`'s config overrides."""

    new_tab: Optional[BetaBrowserNewTabConfigParam]
    """`new_tab`'s config overrides."""

    read_console: Optional[BetaBrowserReadConsoleConfigParam]
    """`read_console`'s config overrides."""

    read_network: Optional[BetaBrowserReadNetworkConfigParam]
    """`read_network`'s config overrides."""

    read_page: Optional[BetaBrowserReadPageConfigParam]
    """`read_page`'s config overrides."""

    right_click: Optional[BetaBrowserRightClickConfigParam]
    """`right_click`'s config overrides."""

    screenshot: Optional[BetaBrowserScreenshotConfigParam]
    """`screenshot`'s config overrides."""

    scroll: Optional[BetaBrowserScrollConfigParam]
    """`scroll`'s config overrides."""

    scroll_to: Optional[BetaBrowserScrollToConfigParam]
    """`scroll_to`'s config overrides."""

    switch_tab: Optional[BetaBrowserSwitchTabConfigParam]
    """`switch_tab`'s config overrides."""

    triple_click: Optional[BetaBrowserTripleClickConfigParam]
    """`triple_click`'s config overrides."""

    type: Optional[BetaBrowserTypeConfigParam]
    """`type`'s config overrides."""

    wait: Optional[BetaBrowserWaitConfigParam]
    """`wait`'s config overrides."""

    zoom: Optional[BetaBrowserZoomConfigParam]
    """`zoom`'s config overrides."""
