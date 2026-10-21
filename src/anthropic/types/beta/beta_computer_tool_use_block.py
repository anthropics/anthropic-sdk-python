from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .beta_computer_key_tool_use_block import BetaComputerKeyToolUseBlock
from .beta_computer_type_tool_use_block import BetaComputerTypeToolUseBlock
from .beta_computer_wait_tool_use_block import BetaComputerWaitToolUseBlock
from .beta_computer_zoom_tool_use_block import BetaComputerZoomToolUseBlock
from .beta_computer_scroll_tool_use_block import BetaComputerScrollToolUseBlock
from .beta_computer_hold_key_tool_use_block import BetaComputerHoldKeyToolUseBlock
from .beta_computer_left_click_tool_use_block import BetaComputerLeftClickToolUseBlock
from .beta_computer_mouse_move_tool_use_block import BetaComputerMouseMoveToolUseBlock
from .beta_computer_screenshot_tool_use_block import BetaComputerScreenshotToolUseBlock
from .beta_computer_right_click_tool_use_block import BetaComputerRightClickToolUseBlock
from .beta_computer_double_click_tool_use_block import BetaComputerDoubleClickToolUseBlock
from .beta_computer_middle_click_tool_use_block import BetaComputerMiddleClickToolUseBlock
from .beta_computer_triple_click_tool_use_block import BetaComputerTripleClickToolUseBlock
from .beta_computer_left_mouse_up_tool_use_block import BetaComputerLeftMouseUpToolUseBlock
from .beta_computer_cursor_position_tool_use_block import BetaComputerCursorPositionToolUseBlock
from .beta_computer_left_click_drag_tool_use_block import BetaComputerLeftClickDragToolUseBlock
from .beta_computer_left_mouse_down_tool_use_block import BetaComputerLeftMouseDownToolUseBlock

__all__ = ["BetaComputerToolUseBlock"]

BetaComputerToolUseBlock: TypeAlias = Annotated[
    Union[
        BetaComputerKeyToolUseBlock,
        BetaComputerHoldKeyToolUseBlock,
        BetaComputerTypeToolUseBlock,
        BetaComputerCursorPositionToolUseBlock,
        BetaComputerMouseMoveToolUseBlock,
        BetaComputerLeftMouseDownToolUseBlock,
        BetaComputerLeftMouseUpToolUseBlock,
        BetaComputerLeftClickToolUseBlock,
        BetaComputerLeftClickDragToolUseBlock,
        BetaComputerRightClickToolUseBlock,
        BetaComputerMiddleClickToolUseBlock,
        BetaComputerDoubleClickToolUseBlock,
        BetaComputerTripleClickToolUseBlock,
        BetaComputerScrollToolUseBlock,
        BetaComputerWaitToolUseBlock,
        BetaComputerScreenshotToolUseBlock,
        BetaComputerZoomToolUseBlock,
    ],
    UnionDiscriminator("name"),
]
