from typing import Union
from typing_extensions import TypeAlias

from .tool_use_block import ToolUseBlock
from .browser_tool_use_block import BrowserToolUseBlock
from .computer_tool_use_block import ComputerToolUseBlock

__all__ = ["ToolsetToolUseBlock"]

ToolsetToolUseBlock: TypeAlias = Union[BrowserToolUseBlock, ComputerToolUseBlock, ToolUseBlock]
