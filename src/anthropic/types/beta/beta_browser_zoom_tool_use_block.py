from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_zoom_input import BetaBrowserZoomInput

__all__ = ["BetaBrowserZoomToolUseBlock"]


class BetaBrowserZoomToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserZoomInput
    """
    Return a cropped screenshot of the given viewport region, scaled up for closer
    inspection — useful for small icons, buttons, or text. Coordinates are in the
    same viewport-pixel space as a full screenshot.
    """

    name: Literal["zoom"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
