from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_type_input import BetaBrowserTypeInput

__all__ = ["BetaBrowserTypeToolUseBlock"]


class BetaBrowserTypeToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserTypeInput
    """Type a literal string at the current focus."""

    name: Literal["type"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
