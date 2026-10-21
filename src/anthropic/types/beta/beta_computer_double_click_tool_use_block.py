from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_computer_double_click_input import BetaComputerDoubleClickInput

__all__ = ["BetaComputerDoubleClickToolUseBlock"]


class BetaComputerDoubleClickToolUseBlock(BaseModel):
    id: str

    input: BetaComputerDoubleClickInput
    """
    Double-click the left mouse button at the specified (x, y) pixel coordinate, or
    the current cursor position if `coordinate` is omitted.
    """

    name: Literal["double_click"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
