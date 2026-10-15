from typing import Union
from typing_extensions import TypeAlias

from .computer_key_input import ComputerKeyInput
from .computer_type_input import ComputerTypeInput
from .computer_wait_input import ComputerWaitInput
from .computer_zoom_input import ComputerZoomInput
from .computer_scroll_input import ComputerScrollInput
from .computer_hold_key_input import ComputerHoldKeyInput
from .computer_left_click_input import ComputerLeftClickInput
from .computer_mouse_move_input import ComputerMouseMoveInput
from .computer_screenshot_input import ComputerScreenshotInput
from .computer_right_click_input import ComputerRightClickInput
from .computer_double_click_input import ComputerDoubleClickInput
from .computer_middle_click_input import ComputerMiddleClickInput
from .computer_triple_click_input import ComputerTripleClickInput
from .computer_left_mouse_up_input import ComputerLeftMouseUpInput
from .computer_cursor_position_input import ComputerCursorPositionInput
from .computer_left_click_drag_input import ComputerLeftClickDragInput
from .computer_left_mouse_down_input import ComputerLeftMouseDownInput

__all__ = ["ComputerMemberInput"]

ComputerMemberInput: TypeAlias = Union[
    ComputerKeyInput,
    ComputerHoldKeyInput,
    ComputerTypeInput,
    ComputerCursorPositionInput,
    ComputerMouseMoveInput,
    ComputerLeftMouseDownInput,
    ComputerLeftMouseUpInput,
    ComputerLeftClickInput,
    ComputerLeftClickDragInput,
    ComputerRightClickInput,
    ComputerMiddleClickInput,
    ComputerDoubleClickInput,
    ComputerTripleClickInput,
    ComputerScrollInput,
    ComputerWaitInput,
    ComputerScreenshotInput,
    ComputerZoomInput,
]
