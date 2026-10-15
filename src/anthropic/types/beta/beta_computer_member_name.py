from typing_extensions import Literal, TypeAlias

__all__ = ["BetaComputerMemberName", "BETA_COMPUTER_MEMBER_NAME_VALUES"]

BetaComputerMemberName: TypeAlias = Literal[
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

BETA_COMPUTER_MEMBER_NAME_VALUES: tuple[BetaComputerMemberName, ...] = (
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
"""The values of `BetaComputerMemberName`."""
