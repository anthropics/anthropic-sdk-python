from typing import Union
from typing_extensions import Annotated, TypeAlias

from .._models import UnionDiscriminator
from .browser_key_tool_use_block import BrowserKeyToolUseBlock
from .browser_find_tool_use_block import BrowserFindToolUseBlock
from .browser_type_tool_use_block import BrowserTypeToolUseBlock
from .browser_wait_tool_use_block import BrowserWaitToolUseBlock
from .browser_zoom_tool_use_block import BrowserZoomToolUseBlock
from .browser_hover_tool_use_block import BrowserHoverToolUseBlock
from .browser_scroll_tool_use_block import BrowserScrollToolUseBlock
from .browser_new_tab_tool_use_block import BrowserNewTabToolUseBlock
from .browser_hold_key_tool_use_block import BrowserHoldKeyToolUseBlock
from .browser_navigate_tool_use_block import BrowserNavigateToolUseBlock
from .browser_close_tab_tool_use_block import BrowserCloseTabToolUseBlock
from .browser_list_tabs_tool_use_block import BrowserListTabsToolUseBlock
from .browser_read_page_tool_use_block import BrowserReadPageToolUseBlock
from .browser_scroll_to_tool_use_block import BrowserScrollToToolUseBlock
from .browser_form_input_tool_use_block import BrowserFormInputToolUseBlock
from .browser_left_click_tool_use_block import BrowserLeftClickToolUseBlock
from .browser_mouse_move_tool_use_block import BrowserMouseMoveToolUseBlock
from .browser_screenshot_tool_use_block import BrowserScreenshotToolUseBlock
from .browser_switch_tab_tool_use_block import BrowserSwitchTabToolUseBlock
from .browser_file_upload_tool_use_block import BrowserFileUploadToolUseBlock
from .browser_right_click_tool_use_block import BrowserRightClickToolUseBlock
from .browser_double_click_tool_use_block import BrowserDoubleClickToolUseBlock
from .browser_middle_click_tool_use_block import BrowserMiddleClickToolUseBlock
from .browser_read_console_tool_use_block import BrowserReadConsoleToolUseBlock
from .browser_read_network_tool_use_block import BrowserReadNetworkToolUseBlock
from .browser_triple_click_tool_use_block import BrowserTripleClickToolUseBlock
from .browser_get_page_text_tool_use_block import BrowserGetPageTextToolUseBlock
from .browser_left_mouse_up_tool_use_block import BrowserLeftMouseUpToolUseBlock
from .browser_javascript_exec_tool_use_block import BrowserJavascriptExecToolUseBlock
from .browser_left_click_drag_tool_use_block import BrowserLeftClickDragToolUseBlock
from .browser_left_mouse_down_tool_use_block import BrowserLeftMouseDownToolUseBlock

__all__ = ["BrowserToolUseBlock"]

BrowserToolUseBlock: TypeAlias = Annotated[
    Union[
        BrowserNavigateToolUseBlock,
        BrowserListTabsToolUseBlock,
        BrowserNewTabToolUseBlock,
        BrowserSwitchTabToolUseBlock,
        BrowserCloseTabToolUseBlock,
        BrowserReadPageToolUseBlock,
        BrowserGetPageTextToolUseBlock,
        BrowserReadConsoleToolUseBlock,
        BrowserReadNetworkToolUseBlock,
        BrowserFindToolUseBlock,
        BrowserFormInputToolUseBlock,
        BrowserFileUploadToolUseBlock,
        BrowserScrollToToolUseBlock,
        BrowserScreenshotToolUseBlock,
        BrowserZoomToolUseBlock,
        BrowserLeftClickToolUseBlock,
        BrowserRightClickToolUseBlock,
        BrowserMiddleClickToolUseBlock,
        BrowserDoubleClickToolUseBlock,
        BrowserTripleClickToolUseBlock,
        BrowserHoverToolUseBlock,
        BrowserLeftClickDragToolUseBlock,
        BrowserLeftMouseDownToolUseBlock,
        BrowserLeftMouseUpToolUseBlock,
        BrowserMouseMoveToolUseBlock,
        BrowserScrollToolUseBlock,
        BrowserTypeToolUseBlock,
        BrowserKeyToolUseBlock,
        BrowserHoldKeyToolUseBlock,
        BrowserWaitToolUseBlock,
        BrowserJavascriptExecToolUseBlock,
    ],
    UnionDiscriminator("name"),
]
