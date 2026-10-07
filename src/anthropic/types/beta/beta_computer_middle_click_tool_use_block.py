from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_computer_middle_click_input import BetaComputerMiddleClickInput

__all__ = ["BetaComputerMiddleClickToolUseBlock"]


class BetaComputerMiddleClickToolUseBlock(BaseModel):
    id: str

    input: BetaComputerMiddleClickInput
    """
    Click the middle mouse button at the specified (x, y) pixel coordinate, or the
    current cursor position if `coordinate` is omitted.
    """

    name: Literal["middle_click"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
