from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .computer_right_click_input import ComputerRightClickInput

__all__ = ["ComputerRightClickToolUseBlock"]


class ComputerRightClickToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: ComputerRightClickInput
    """
    Click the right mouse button at the specified (x, y) pixel coordinate, or the
    current cursor position if `coordinate` is omitted.
    """

    name: Literal["right_click"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]
