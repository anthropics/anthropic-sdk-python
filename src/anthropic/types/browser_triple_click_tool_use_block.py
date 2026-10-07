from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_triple_click_input import BrowserTripleClickInput

__all__ = ["BrowserTripleClickToolUseBlock"]


class BrowserTripleClickToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserTripleClickInput
    """
    Triple left-click at a viewport coordinate or on an element by reference
    (typically selects a line or paragraph).
    """

    name: Literal["triple_click"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
