from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_middle_click_input import BetaBrowserMiddleClickInput

__all__ = ["BetaBrowserMiddleClickToolUseBlock"]


class BetaBrowserMiddleClickToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserMiddleClickInput
    """Middle-click at a viewport coordinate or on an element by reference."""

    name: Literal["middle_click"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
