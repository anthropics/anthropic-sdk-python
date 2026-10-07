from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .computer_middle_click_input import ComputerMiddleClickInput

__all__ = ["ComputerMiddleClickToolUseBlock"]


class ComputerMiddleClickToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: ComputerMiddleClickInput
    """
    Click the middle mouse button at the specified (x, y) pixel coordinate, or the
    current cursor position if `coordinate` is omitted.
    """

    name: Literal["middle_click"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]
