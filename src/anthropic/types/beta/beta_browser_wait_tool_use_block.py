from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_wait_input import BetaBrowserWaitInput

__all__ = ["BetaBrowserWaitToolUseBlock"]


class BetaBrowserWaitToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserWaitInput
    """Pause for the given duration."""

    name: Literal["wait"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
