from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_read_page_input import BetaBrowserReadPageInput

__all__ = ["BetaBrowserReadPageToolUseBlock"]


class BetaBrowserReadPageToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserReadPageInput
    """
    Return a structured accessibility tree of the page (or the subtree rooted at
    `ref`), with element references like [ref_7] that can be used as targets on
    later actions. Output is capped at 50,000 characters — narrow with `ref` or a
    smaller `depth` when exceeded.
    """

    name: Literal["read_page"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
