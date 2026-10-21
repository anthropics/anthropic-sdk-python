from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_left_mouse_up_input import BetaBrowserLeftMouseUpInput

__all__ = ["BetaBrowserLeftMouseUpToolUseBlock"]


class BetaBrowserLeftMouseUpToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserLeftMouseUpInput
    """Release the left mouse button at a viewport coordinate."""

    name: Literal["left_mouse_up"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
