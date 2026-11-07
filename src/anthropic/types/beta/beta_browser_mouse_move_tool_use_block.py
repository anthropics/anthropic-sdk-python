from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_mouse_move_input import BetaBrowserMouseMoveInput

__all__ = ["BetaBrowserMouseMoveToolUseBlock"]


class BetaBrowserMouseMoveToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserMouseMoveInput
    """Move the pointer to a viewport coordinate without clicking."""

    name: Literal["mouse_move"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
