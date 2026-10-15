from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_scroll_input import BetaBrowserScrollInput

__all__ = ["BetaBrowserScrollToolUseBlock"]


class BetaBrowserScrollToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserScrollInput
    """Scroll at a viewport position. `target` must be a coordinate target."""

    name: Literal["scroll"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
