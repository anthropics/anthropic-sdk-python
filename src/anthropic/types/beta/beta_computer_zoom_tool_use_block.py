from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_computer_zoom_input import BetaComputerZoomInput

__all__ = ["BetaComputerZoomToolUseBlock"]


class BetaComputerZoomToolUseBlock(BaseModel):
    id: str

    input: BetaComputerZoomInput
    """Take a screenshot of a rectangular region.

    Region coordinates are in the full-screenshot space (not physical display
    pixels). The crop is scaled up to fill the image budget so fine details become
    legible.
    """

    name: Literal["zoom"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
