from typing_extensions import Literal

from .._models import BaseModel
from .tool_use_caller import ToolUseCaller
from .browser_file_upload_input import BrowserFileUploadInput

__all__ = ["BrowserFileUploadToolUseBlock"]


class BrowserFileUploadToolUseBlock(BaseModel):
    id: str

    caller: ToolUseCaller
    """
    Which party invoked the tool call: the model directly, or a server tool on its
    behalf.
    """

    input: BrowserFileUploadInput
    """Set the value of a file-input element to one or more files.

    The target must be an element reference; at least one of paths or document_ids
    is required.
    """

    name: Literal["file_upload"]

    toolset_name: Literal["browser"]

    type: Literal["tool_use"]
