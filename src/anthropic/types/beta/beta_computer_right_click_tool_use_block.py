from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_computer_right_click_input import BetaComputerRightClickInput

__all__ = ["BetaComputerRightClickToolUseBlock"]


class BetaComputerRightClickToolUseBlock(BaseModel):
    id: str

    input: BetaComputerRightClickInput
    """
    Click the right mouse button at the specified (x, y) pixel coordinate, or the
    current cursor position if `coordinate` is omitted.
    """

    name: Literal["right_click"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
