from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_computer_left_click_input import BetaComputerLeftClickInput

__all__ = ["BetaComputerLeftClickToolUseBlock"]


class BetaComputerLeftClickToolUseBlock(BaseModel):
    id: str

    input: BetaComputerLeftClickInput
    """
    Click the left mouse button at the specified (x, y) pixel coordinate, or the
    current cursor position if `coordinate` is omitted.
    """

    name: Literal["left_click"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
