from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_computer_triple_click_input import BetaComputerTripleClickInput

__all__ = ["BetaComputerTripleClickToolUseBlock"]


class BetaComputerTripleClickToolUseBlock(BaseModel):
    id: str

    input: BetaComputerTripleClickInput
    """
    Triple-click the left mouse button at the specified (x, y) pixel coordinate, or
    the current cursor position if `coordinate` is omitted.
    """

    name: Literal["triple_click"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
