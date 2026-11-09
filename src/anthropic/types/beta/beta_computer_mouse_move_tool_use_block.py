from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_computer_mouse_move_input import BetaComputerMouseMoveInput

__all__ = ["BetaComputerMouseMoveToolUseBlock"]


class BetaComputerMouseMoveToolUseBlock(BaseModel):
    id: str

    input: BetaComputerMouseMoveInput
    """Move the cursor to a specified (x, y) pixel coordinate.

    Use this ONLY to hover without clicking; otherwise use a click action directly.
    """

    name: Literal["mouse_move"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
