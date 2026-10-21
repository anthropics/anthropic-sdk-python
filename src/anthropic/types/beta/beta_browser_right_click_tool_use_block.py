from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_right_click_input import BetaBrowserRightClickInput

__all__ = ["BetaBrowserRightClickToolUseBlock"]


class BetaBrowserRightClickToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserRightClickInput
    """Right-click at a viewport coordinate or on an element by reference."""

    name: Literal["right_click"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
