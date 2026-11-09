from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_hold_key_input import BetaBrowserHoldKeyInput

__all__ = ["BetaBrowserHoldKeyToolUseBlock"]


class BetaBrowserHoldKeyToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserHoldKeyInput
    """Hold a key or key chord down for a duration, then release it.

    Uses the same key names and "+" chord syntax as the key action.
    """

    name: Literal["hold_key"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
