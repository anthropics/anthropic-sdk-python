from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_computer_cursor_position_input import BetaComputerCursorPositionInput

__all__ = ["BetaComputerCursorPositionToolUseBlock"]


class BetaComputerCursorPositionToolUseBlock(BaseModel):
    id: str

    input: BetaComputerCursorPositionInput
    """Get the current (x, y) pixel coordinate of the cursor."""

    name: Literal["cursor_position"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
