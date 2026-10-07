from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_left_click_input import BetaBrowserLeftClickInput

__all__ = ["BetaBrowserLeftClickToolUseBlock"]


class BetaBrowserLeftClickToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserLeftClickInput
    """Left-click at a viewport coordinate or on an element by reference."""

    name: Literal["left_click"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
