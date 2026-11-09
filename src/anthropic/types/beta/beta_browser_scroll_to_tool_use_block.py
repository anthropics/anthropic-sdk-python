from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_scroll_to_input import BetaBrowserScrollToInput

__all__ = ["BetaBrowserScrollToToolUseBlock"]


class BetaBrowserScrollToToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserScrollToInput
    """Scroll an element into view."""

    name: Literal["scroll_to"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
