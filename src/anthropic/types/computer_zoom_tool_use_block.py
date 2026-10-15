from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .computer_zoom_input import ComputerZoomInput

__all__ = ["ComputerZoomToolUseBlock"]


class ComputerZoomToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: ComputerZoomInput
    """Take a screenshot of a rectangular region.

    Region coordinates are in the full-screenshot space (not physical display
    pixels). The crop is scaled up to fill the image budget so fine details become
    legible.
    """

    name: Literal["zoom"]

    toolset_name: Literal["computer"]

    type: Literal["tool_use"]
