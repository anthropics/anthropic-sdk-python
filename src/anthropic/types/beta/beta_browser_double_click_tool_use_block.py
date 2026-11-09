from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_double_click_input import BetaBrowserDoubleClickInput

__all__ = ["BetaBrowserDoubleClickToolUseBlock"]


class BetaBrowserDoubleClickToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserDoubleClickInput
    """Double left-click at a viewport coordinate or on an element by reference."""

    name: Literal["double_click"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
