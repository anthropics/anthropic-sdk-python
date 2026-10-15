from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_triple_click_input import BetaBrowserTripleClickInput

__all__ = ["BetaBrowserTripleClickToolUseBlock"]


class BetaBrowserTripleClickToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserTripleClickInput
    """
    Triple left-click at a viewport coordinate or on an element by reference
    (typically selects a line or paragraph).
    """

    name: Literal["triple_click"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
