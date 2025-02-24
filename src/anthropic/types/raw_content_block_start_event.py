# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .text_block import TextBlock
from .thinking_block import ThinkingBlock
from .tool_use_block import ToolUseBlock
from .redacted_thinking_block import RedactedThinkingBlock

__all__ = ["RawContentBlockStartEvent", "ContentBlock"]

ContentBlock: TypeAlias = Annotated[
    Union[TextBlock, ToolUseBlock, ThinkingBlock, RedactedThinkingBlock], PropertyInfo(discriminator="type")
]


class RawContentBlockStartEvent(BaseModel):
    content_block: ContentBlock

    index: int

    type: Literal["content_block_start"]
