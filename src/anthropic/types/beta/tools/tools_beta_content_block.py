# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union

from ...text_block import TextBlock
from .tool_use_block import ToolUseBlock

__all__ = ["ToolsBetaContentBlock"]

ToolsBetaContentBlock = Union[TextBlock, ToolUseBlock]
