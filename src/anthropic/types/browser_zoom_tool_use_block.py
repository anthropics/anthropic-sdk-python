from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_zoom_input import BrowserZoomInput

__all__ = ["BrowserZoomToolUseBlock"]


class BrowserZoomToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserZoomInput
    """
    Return a cropped screenshot of the given viewport region, scaled up for closer
    inspection — useful for small icons, buttons, or text. Coordinates are in the
    same viewport-pixel space as a full screenshot.
    """

    name: Literal["zoom"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
