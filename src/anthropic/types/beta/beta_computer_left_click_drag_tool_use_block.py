from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_computer_left_click_drag_input import BetaComputerLeftClickDragInput

__all__ = ["BetaComputerLeftClickDragToolUseBlock"]


class BetaComputerLeftClickDragToolUseBlock(BaseModel):
    id: str

    input: BetaComputerLeftClickDragInput
    """Click and drag the cursor from `start_coordinate` to `coordinate`."""

    name: Literal["left_click_drag"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
