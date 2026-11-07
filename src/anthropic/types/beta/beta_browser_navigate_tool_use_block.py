from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_navigate_input import BetaBrowserNavigateInput

__all__ = ["BetaBrowserNavigateToolUseBlock"]


class BetaBrowserNavigateToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserNavigateInput
    """Navigate to a URL, or go back/forward/reload in history.

    The protocol may be omitted (defaults to https://).
    """

    name: Literal["navigate"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
