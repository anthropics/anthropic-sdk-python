from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_left_click_drag_input import BetaBrowserLeftClickDragInput

__all__ = ["BetaBrowserLeftClickDragToolUseBlock"]


class BetaBrowserLeftClickDragToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserLeftClickDragInput
    """Press at `from`, drag to `target`, release. Both must be coordinate targets."""

    name: Literal["left_click_drag"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
