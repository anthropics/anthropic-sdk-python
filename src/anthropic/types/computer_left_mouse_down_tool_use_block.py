from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .computer_left_mouse_down_input import ComputerLeftMouseDownInput

__all__ = ["ComputerLeftMouseDownToolUseBlock"]


class ComputerLeftMouseDownToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: ComputerLeftMouseDownInput
    """Press and hold the left mouse button at the current cursor position."""

    name: Literal["left_mouse_down"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]
