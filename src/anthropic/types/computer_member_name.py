from typing_extensions import Literal, TypeAlias

__all__ = ["ComputerMemberName", "COMPUTER_MEMBER_NAME_VALUES"]

ComputerMemberName: TypeAlias = Literal[
    "key",
    "hold_key",
    "type",
    "cursor_position",
    "mouse_move",
    "left_mouse_down",
    "left_mouse_up",
    "left_click",
    "left_click_drag",
    "right_click",
    "middle_click",
    "double_click",
    "triple_click",
    "scroll",
    "wait",
    "screenshot",
    "zoom",
]

COMPUTER_MEMBER_NAME_VALUES: tuple[ComputerMemberName, ...] = (
    "key",
    "hold_key",
    "type",
    "cursor_position",
    "mouse_move",
    "left_mouse_down",
    "left_mouse_up",
    "left_click",
    "left_click_drag",
    "right_click",
    "middle_click",
    "double_click",
    "triple_click",
    "scroll",
    "wait",
    "screenshot",
    "zoom",
)
"""The values of `ComputerMemberName`."""
