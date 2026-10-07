from typing import Union
from typing_extensions import TypeAlias

from .browser_key_input import BrowserKeyInput
from .browser_find_input import BrowserFindInput
from .browser_type_input import BrowserTypeInput
from .browser_wait_input import BrowserWaitInput
from .browser_zoom_input import BrowserZoomInput
from .browser_hover_input import BrowserHoverInput
from .browser_scroll_input import BrowserScrollInput
from .browser_new_tab_input import BrowserNewTabInput
from .browser_hold_key_input import BrowserHoldKeyInput
from .browser_navigate_input import BrowserNavigateInput
from .browser_close_tab_input import BrowserCloseTabInput
from .browser_list_tabs_input import BrowserListTabsInput
from .browser_read_page_input import BrowserReadPageInput
from .browser_scroll_to_input import BrowserScrollToInput
from .browser_form_input_input import BrowserFormInputInput
from .browser_left_click_input import BrowserLeftClickInput
from .browser_mouse_move_input import BrowserMouseMoveInput
from .browser_screenshot_input import BrowserScreenshotInput
from .browser_switch_tab_input import BrowserSwitchTabInput
from .browser_file_upload_input import BrowserFileUploadInput
from .browser_right_click_input import BrowserRightClickInput
from .browser_double_click_input import BrowserDoubleClickInput
from .browser_middle_click_input import BrowserMiddleClickInput
from .browser_read_console_input import BrowserReadConsoleInput
from .browser_read_network_input import BrowserReadNetworkInput
from .browser_triple_click_input import BrowserTripleClickInput
from .browser_get_page_text_input import BrowserGetPageTextInput
from .browser_left_mouse_up_input import BrowserLeftMouseUpInput
from .browser_javascript_exec_input import BrowserJavascriptExecInput
from .browser_left_click_drag_input import BrowserLeftClickDragInput
from .browser_left_mouse_down_input import BrowserLeftMouseDownInput

__all__ = ["BrowserMemberInput"]

BrowserMemberInput: TypeAlias = Union[
    BrowserNavigateInput,
    BrowserListTabsInput,
    BrowserNewTabInput,
    BrowserSwitchTabInput,
    BrowserCloseTabInput,
    BrowserReadPageInput,
    BrowserGetPageTextInput,
    BrowserReadConsoleInput,
    BrowserReadNetworkInput,
    BrowserFindInput,
    BrowserFormInputInput,
    BrowserFileUploadInput,
    BrowserScrollToInput,
    BrowserScreenshotInput,
    BrowserZoomInput,
    BrowserLeftClickInput,
    BrowserRightClickInput,
    BrowserMiddleClickInput,
    BrowserDoubleClickInput,
    BrowserTripleClickInput,
    BrowserHoverInput,
    BrowserLeftClickDragInput,
    BrowserLeftMouseDownInput,
    BrowserLeftMouseUpInput,
    BrowserMouseMoveInput,
    BrowserScrollInput,
    BrowserTypeInput,
    BrowserKeyInput,
    BrowserHoldKeyInput,
    BrowserWaitInput,
    BrowserJavascriptExecInput,
]
