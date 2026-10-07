from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .computer_left_click_drag_input import ComputerLeftClickDragInput

__all__ = ["ComputerLeftClickDragToolUseBlock"]


class ComputerLeftClickDragToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: ComputerLeftClickDragInput
    """Click and drag the cursor from `start_coordinate` to `coordinate`."""

    name: Literal["left_click_drag"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]
