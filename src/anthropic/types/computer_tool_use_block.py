from typing import Union
from typing_extensions import Annotated, TypeAlias

from .._models import UnionDiscriminator
from .computer_key_tool_use_block import ComputerKeyToolUseBlock
from .computer_type_tool_use_block import ComputerTypeToolUseBlock
from .computer_wait_tool_use_block import ComputerWaitToolUseBlock
from .computer_zoom_tool_use_block import ComputerZoomToolUseBlock
from .computer_scroll_tool_use_block import ComputerScrollToolUseBlock
from .computer_hold_key_tool_use_block import ComputerHoldKeyToolUseBlock
from .computer_left_click_tool_use_block import ComputerLeftClickToolUseBlock
from .computer_mouse_move_tool_use_block import ComputerMouseMoveToolUseBlock
from .computer_screenshot_tool_use_block import ComputerScreenshotToolUseBlock
from .computer_right_click_tool_use_block import ComputerRightClickToolUseBlock
from .computer_double_click_tool_use_block import ComputerDoubleClickToolUseBlock
from .computer_middle_click_tool_use_block import ComputerMiddleClickToolUseBlock
from .computer_triple_click_tool_use_block import ComputerTripleClickToolUseBlock
from .computer_left_mouse_up_tool_use_block import ComputerLeftMouseUpToolUseBlock
from .computer_cursor_position_tool_use_block import ComputerCursorPositionToolUseBlock
from .computer_left_click_drag_tool_use_block import ComputerLeftClickDragToolUseBlock
from .computer_left_mouse_down_tool_use_block import ComputerLeftMouseDownToolUseBlock

__all__ = ["ComputerToolUseBlock"]

ComputerToolUseBlock: TypeAlias = Annotated[
    Union[
        ComputerKeyToolUseBlock,
        ComputerHoldKeyToolUseBlock,
        ComputerTypeToolUseBlock,
        ComputerCursorPositionToolUseBlock,
        ComputerMouseMoveToolUseBlock,
        ComputerLeftMouseDownToolUseBlock,
        ComputerLeftMouseUpToolUseBlock,
        ComputerLeftClickToolUseBlock,
        ComputerLeftClickDragToolUseBlock,
        ComputerRightClickToolUseBlock,
        ComputerMiddleClickToolUseBlock,
        ComputerDoubleClickToolUseBlock,
        ComputerTripleClickToolUseBlock,
        ComputerScrollToolUseBlock,
        ComputerWaitToolUseBlock,
        ComputerScreenshotToolUseBlock,
        ComputerZoomToolUseBlock,
    ],
    UnionDiscriminator("name"),
]
