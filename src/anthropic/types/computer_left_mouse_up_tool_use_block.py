from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .computer_left_mouse_up_input import ComputerLeftMouseUpInput

__all__ = ["ComputerLeftMouseUpToolUseBlock"]


class ComputerLeftMouseUpToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: ComputerLeftMouseUpInput
    """Release the left mouse button."""

    name: Literal["left_mouse_up"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]
