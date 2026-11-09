from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_left_mouse_down_input import BetaBrowserLeftMouseDownInput

__all__ = ["BetaBrowserLeftMouseDownToolUseBlock"]


class BetaBrowserLeftMouseDownToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserLeftMouseDownInput
    """Press and hold the left mouse button at a viewport coordinate.

    Pair with left_mouse_up to perform a custom drag.
    """

    name: Literal["left_mouse_down"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
