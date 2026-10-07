from typing import Union
from typing_extensions import TypeAlias

from .beta_tool_use_block import BetaToolUseBlock
from .beta_browser_tool_use_block import BetaBrowserToolUseBlock
from .beta_computer_tool_use_block import BetaComputerToolUseBlock

__all__ = ["BetaToolsetToolUseBlock"]

BetaToolsetToolUseBlock: TypeAlias = Union[BetaBrowserToolUseBlock, BetaComputerToolUseBlock, BetaToolUseBlock]
