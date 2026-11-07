from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .computer_double_click_input import ComputerDoubleClickInput

__all__ = ["ComputerDoubleClickToolUseBlock"]


class ComputerDoubleClickToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: ComputerDoubleClickInput
    """
    Double-click the left mouse button at the specified (x, y) pixel coordinate, or
    the current cursor position if `coordinate` is omitted.
    """

    name: Literal["double_click"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]
