from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_computer_left_mouse_up_input import BetaComputerLeftMouseUpInput

__all__ = ["BetaComputerLeftMouseUpToolUseBlock"]


class BetaComputerLeftMouseUpToolUseBlock(BaseModel):
    id: str

    input: BetaComputerLeftMouseUpInput
    """Release the left mouse button."""

    name: Literal["left_mouse_up"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
