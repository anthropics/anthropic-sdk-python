from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_computer_left_mouse_down_input import BetaComputerLeftMouseDownInput

__all__ = ["BetaComputerLeftMouseDownToolUseBlock"]


class BetaComputerLeftMouseDownToolUseBlock(BaseModel):
    id: str

    input: BetaComputerLeftMouseDownInput
    """Press and hold the left mouse button at the current cursor position."""

    name: Literal["left_mouse_down"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
