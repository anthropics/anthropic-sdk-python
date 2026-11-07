from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_find_input import BetaBrowserFindInput

__all__ = ["BetaBrowserFindToolUseBlock"]


class BetaBrowserFindToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserFindInput
    """Find elements matching a natural-language description (e.g.

    "search bar", "add to cart button") and return up to 20 matches with element
    references.
    """

    name: Literal["find"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
