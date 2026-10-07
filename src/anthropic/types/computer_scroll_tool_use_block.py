from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .computer_scroll_input import ComputerScrollInput

__all__ = ["ComputerScrollToolUseBlock"]


class ComputerScrollToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: ComputerScrollInput
    """
    Scroll the screen at the specified (x, y) pixel coordinate, or the current
    cursor position if `coordinate` is omitted. Do NOT use PageUp/PageDown to
    scroll.
    """

    name: Literal["scroll"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]
