from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_use_caller import BetaToolUseCaller
from .beta_browser_file_upload_input import BetaBrowserFileUploadInput

__all__ = ["BetaBrowserFileUploadToolUseBlock"]


class BetaBrowserFileUploadToolUseBlock(BaseModel):
    id: str

    input: BetaBrowserFileUploadInput
    """Set the value of a file-input element to one or more files.

    The target must be an element reference; at least one of paths or document_ids
    is required.
    """

    name: Literal["file_upload"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]

    caller: Optional[BetaToolUseCaller] = None
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """
