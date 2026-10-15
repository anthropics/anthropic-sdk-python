from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .computer_left_click_input import ComputerLeftClickInput

__all__ = ["ComputerLeftClickToolUseBlock"]


class ComputerLeftClickToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: ComputerLeftClickInput
    """
    Click the left mouse button at the specified (x, y) pixel coordinate, or the
    current cursor position if `coordinate` is omitted.
    """

    name: Literal["left_click"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]
