from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_read_page_input import BrowserReadPageInput

__all__ = ["BrowserReadPageToolUseBlock"]


class BrowserReadPageToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserReadPageInput
    """
    Return a structured accessibility tree of the page (or the subtree rooted at
    `ref`), with element references like [ref_7] that can be used as targets on
    later actions. Output is capped at 50,000 characters — narrow with `ref` or a
    smaller `depth` when exceeded.
    """

    name: Literal["read_page"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
