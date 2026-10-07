from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .beta_browser_key_tool_use_block import BetaBrowserKeyToolUseBlock
from .beta_browser_find_tool_use_block import BetaBrowserFindToolUseBlock
from .beta_browser_type_tool_use_block import BetaBrowserTypeToolUseBlock
from .beta_browser_wait_tool_use_block import BetaBrowserWaitToolUseBlock
from .beta_browser_zoom_tool_use_block import BetaBrowserZoomToolUseBlock
from .beta_browser_hover_tool_use_block import BetaBrowserHoverToolUseBlock
from .beta_browser_scroll_tool_use_block import BetaBrowserScrollToolUseBlock
from .beta_browser_new_tab_tool_use_block import BetaBrowserNewTabToolUseBlock
from .beta_browser_hold_key_tool_use_block import BetaBrowserHoldKeyToolUseBlock
from .beta_browser_navigate_tool_use_block import BetaBrowserNavigateToolUseBlock
from .beta_browser_close_tab_tool_use_block import BetaBrowserCloseTabToolUseBlock
from .beta_browser_list_tabs_tool_use_block import BetaBrowserListTabsToolUseBlock
from .beta_browser_read_page_tool_use_block import BetaBrowserReadPageToolUseBlock
from .beta_browser_scroll_to_tool_use_block import BetaBrowserScrollToToolUseBlock
from .beta_browser_form_input_tool_use_block import BetaBrowserFormInputToolUseBlock
from .beta_browser_left_click_tool_use_block import BetaBrowserLeftClickToolUseBlock
from .beta_browser_mouse_move_tool_use_block import BetaBrowserMouseMoveToolUseBlock
from .beta_browser_screenshot_tool_use_block import BetaBrowserScreenshotToolUseBlock
from .beta_browser_switch_tab_tool_use_block import BetaBrowserSwitchTabToolUseBlock
from .beta_browser_file_upload_tool_use_block import BetaBrowserFileUploadToolUseBlock
from .beta_browser_right_click_tool_use_block import BetaBrowserRightClickToolUseBlock
from .beta_browser_double_click_tool_use_block import BetaBrowserDoubleClickToolUseBlock
from .beta_browser_middle_click_tool_use_block import BetaBrowserMiddleClickToolUseBlock
from .beta_browser_read_console_tool_use_block import BetaBrowserReadConsoleToolUseBlock
from .beta_browser_read_network_tool_use_block import BetaBrowserReadNetworkToolUseBlock
from .beta_browser_triple_click_tool_use_block import BetaBrowserTripleClickToolUseBlock
from .beta_browser_get_page_text_tool_use_block import BetaBrowserGetPageTextToolUseBlock
from .beta_browser_left_mouse_up_tool_use_block import BetaBrowserLeftMouseUpToolUseBlock
from .beta_browser_javascript_exec_tool_use_block import BetaBrowserJavascriptExecToolUseBlock
from .beta_browser_left_click_drag_tool_use_block import BetaBrowserLeftClickDragToolUseBlock
from .beta_browser_left_mouse_down_tool_use_block import BetaBrowserLeftMouseDownToolUseBlock

__all__ = ["BetaBrowserToolUseBlock"]

BetaBrowserToolUseBlock: TypeAlias = Annotated[
    Union[
        BetaBrowserNavigateToolUseBlock,
        BetaBrowserListTabsToolUseBlock,
        BetaBrowserNewTabToolUseBlock,
        BetaBrowserSwitchTabToolUseBlock,
        BetaBrowserCloseTabToolUseBlock,
        BetaBrowserReadPageToolUseBlock,
        BetaBrowserGetPageTextToolUseBlock,
        BetaBrowserReadConsoleToolUseBlock,
        BetaBrowserReadNetworkToolUseBlock,
        BetaBrowserFindToolUseBlock,
        BetaBrowserFormInputToolUseBlock,
        BetaBrowserFileUploadToolUseBlock,
        BetaBrowserScrollToToolUseBlock,
        BetaBrowserScreenshotToolUseBlock,
        BetaBrowserZoomToolUseBlock,
        BetaBrowserLeftClickToolUseBlock,
        BetaBrowserRightClickToolUseBlock,
        BetaBrowserMiddleClickToolUseBlock,
        BetaBrowserDoubleClickToolUseBlock,
        BetaBrowserTripleClickToolUseBlock,
        BetaBrowserHoverToolUseBlock,
        BetaBrowserLeftClickDragToolUseBlock,
        BetaBrowserLeftMouseDownToolUseBlock,
        BetaBrowserLeftMouseUpToolUseBlock,
        BetaBrowserMouseMoveToolUseBlock,
        BetaBrowserScrollToolUseBlock,
        BetaBrowserTypeToolUseBlock,
        BetaBrowserKeyToolUseBlock,
        BetaBrowserHoldKeyToolUseBlock,
        BetaBrowserWaitToolUseBlock,
        BetaBrowserJavascriptExecToolUseBlock,
    ],
    UnionDiscriminator("name"),
]
