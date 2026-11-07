from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_find_input import BrowserFindInput

__all__ = ["BrowserFindToolUseBlock"]


class BrowserFindToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserFindInput
    """Find elements matching a natural-language description (e.g.

    "search bar", "add to cart button") and return up to 20 matches with element
    references.
    """

    name: Literal["find"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
