from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_computer_hold_key_input import BetaComputerHoldKeyInput

__all__ = ["BetaComputerHoldKeyToolUseBlock"]


class BetaComputerHoldKeyToolUseBlock(BaseModel):
    id: str

    input: BetaComputerHoldKeyInput
    """Hold down a key or key-combination for a specified duration.

    Uses the same key syntax as `key`.
    """

    name: Literal["hold_key"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
