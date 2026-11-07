from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_computer_scroll_input import BetaComputerScrollInput

__all__ = ["BetaComputerScrollToolUseBlock"]


class BetaComputerScrollToolUseBlock(BaseModel):
    id: str

    input: BetaComputerScrollInput
    """
    Scroll the screen at the specified (x, y) pixel coordinate, or the current
    cursor position if `coordinate` is omitted. Do NOT use PageUp/PageDown to
    scroll.
    """

    name: Literal["scroll"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
