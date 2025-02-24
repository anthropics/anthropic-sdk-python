# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from .._utils import PropertyInfo
from .text_block import TextBlock
from .thinking_block import ThinkingBlock
from .tool_use_block import ToolUseBlock
from .redacted_thinking_block import RedactedThinkingBlock

__all__ = ["ContentBlock"]

ContentBlock: TypeAlias = Annotated[
    Union[TextBlock, ToolUseBlock, ThinkingBlock, RedactedThinkingBlock], PropertyInfo(discriminator="type")
]
