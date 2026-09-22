from typing import Optional

from ..._models import BaseModel
from .beta_browser_key_config import BetaBrowserKeyConfig
from .beta_browser_find_config import BetaBrowserFindConfig
from .beta_browser_type_config import BetaBrowserTypeConfig
from .beta_browser_wait_config import BetaBrowserWaitConfig
from .beta_browser_zoom_config import BetaBrowserZoomConfig
from .beta_browser_hover_config import BetaBrowserHoverConfig
from .beta_browser_scroll_config import BetaBrowserScrollConfig
from .beta_browser_new_tab_config import BetaBrowserNewTabConfig
from .beta_browser_hold_key_config import BetaBrowserHoldKeyConfig
from .beta_browser_navigate_config import BetaBrowserNavigateConfig
from .beta_browser_close_tab_config import BetaBrowserCloseTabConfig
from .beta_browser_list_tabs_config import BetaBrowserListTabsConfig
from .beta_browser_read_page_config import BetaBrowserReadPageConfig
from .beta_browser_scroll_to_config import BetaBrowserScrollToConfig
from .beta_browser_form_input_config import BetaBrowserFormInputConfig
from .beta_browser_left_click_config import BetaBrowserLeftClickConfig
from .beta_browser_mouse_move_config import BetaBrowserMouseMoveConfig
from .beta_browser_screenshot_config import BetaBrowserScreenshotConfig
from .beta_browser_switch_tab_config import BetaBrowserSwitchTabConfig
from .beta_browser_file_upload_config import BetaBrowserFileUploadConfig
from .beta_browser_right_click_config import BetaBrowserRightClickConfig
from .beta_browser_double_click_config import BetaBrowserDoubleClickConfig
from .beta_browser_middle_click_config import BetaBrowserMiddleClickConfig
from .beta_browser_read_console_config import BetaBrowserReadConsoleConfig
from .beta_browser_read_network_config import BetaBrowserReadNetworkConfig
from .beta_browser_triple_click_config import BetaBrowserTripleClickConfig
from .beta_browser_get_page_text_config import BetaBrowserGetPageTextConfig
from .beta_browser_left_mouse_up_config import BetaBrowserLeftMouseUpConfig
from .beta_browser_javascript_exec_config import BetaBrowserJavascriptExecConfig
from .beta_browser_left_click_drag_config import BetaBrowserLeftClickDragConfig
from .beta_browser_left_mouse_down_config import BetaBrowserLeftMouseDownConfig

__all__ = ["BetaBrowserToolsetConfigs"]


class BetaBrowserToolsetConfigs(BaseModel):
    """
    Per-member configuration for ``browser_toolset_20260801``: one
    optional field per member tool, keyed by the member name — the same
    name the member's ``tool_use`` blocks carry. Every member is an
    accepted key, and a member's defaults apply wherever its key is
    absent. Unknown keys are rejected: the field set is this toolset
    version's complete member set.
    """

    close_tab: Optional[BetaBrowserCloseTabConfig] = None
    """`close_tab`'s config overrides."""

    double_click: Optional[BetaBrowserDoubleClickConfig] = None
    """`double_click`'s config overrides."""

    file_upload: Optional[BetaBrowserFileUploadConfig] = None
    """`file_upload`'s config overrides."""

    find: Optional[BetaBrowserFindConfig] = None
    """`find`'s config overrides."""

    form_input: Optional[BetaBrowserFormInputConfig] = None
    """`form_input`'s config overrides."""

    get_page_text: Optional[BetaBrowserGetPageTextConfig] = None
    """`get_page_text`'s config overrides."""

    hold_key: Optional[BetaBrowserHoldKeyConfig] = None
    """`hold_key`'s config overrides."""

    hover: Optional[BetaBrowserHoverConfig] = None
    """`hover`'s config overrides."""

    javascript_exec: Optional[BetaBrowserJavascriptExecConfig] = None
    """`javascript_exec`'s config overrides."""

    key: Optional[BetaBrowserKeyConfig] = None
    """`key`'s config overrides."""

    left_click: Optional[BetaBrowserLeftClickConfig] = None
    """`left_click`'s config overrides."""

    left_click_drag: Optional[BetaBrowserLeftClickDragConfig] = None
    """`left_click_drag`'s config overrides."""

    left_mouse_down: Optional[BetaBrowserLeftMouseDownConfig] = None
    """`left_mouse_down`'s config overrides."""

    left_mouse_up: Optional[BetaBrowserLeftMouseUpConfig] = None
    """`left_mouse_up`'s config overrides."""

    list_tabs: Optional[BetaBrowserListTabsConfig] = None
    """`list_tabs`'s config overrides."""

    middle_click: Optional[BetaBrowserMiddleClickConfig] = None
    """`middle_click`'s config overrides."""

    mouse_move: Optional[BetaBrowserMouseMoveConfig] = None
    """`mouse_move`'s config overrides."""

    navigate: Optional[BetaBrowserNavigateConfig] = None
    """`navigate`'s config overrides."""

    new_tab: Optional[BetaBrowserNewTabConfig] = None
    """`new_tab`'s config overrides."""

    read_console: Optional[BetaBrowserReadConsoleConfig] = None
    """`read_console`'s config overrides."""

    read_network: Optional[BetaBrowserReadNetworkConfig] = None
    """`read_network`'s config overrides."""

    read_page: Optional[BetaBrowserReadPageConfig] = None
    """`read_page`'s config overrides."""

    right_click: Optional[BetaBrowserRightClickConfig] = None
    """`right_click`'s config overrides."""

    screenshot: Optional[BetaBrowserScreenshotConfig] = None
    """`screenshot`'s config overrides."""

    scroll: Optional[BetaBrowserScrollConfig] = None
    """`scroll`'s config overrides."""

    scroll_to: Optional[BetaBrowserScrollToConfig] = None
    """`scroll_to`'s config overrides."""

    switch_tab: Optional[BetaBrowserSwitchTabConfig] = None
    """`switch_tab`'s config overrides."""

    triple_click: Optional[BetaBrowserTripleClickConfig] = None
    """`triple_click`'s config overrides."""

    type: Optional[BetaBrowserTypeConfig] = None
    """`type`'s config overrides."""

    wait: Optional[BetaBrowserWaitConfig] = None
    """`wait`'s config overrides."""

    zoom: Optional[BetaBrowserZoomConfig] = None
    """`zoom`'s config overrides."""
