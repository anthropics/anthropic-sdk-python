# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Literal, Annotated

from ...._utils import PropertyInfo
from ...._models import BaseModel
from ...text_block import TextBlock
from .tool_use_block import ToolUseBlock

__all__ = ["ToolsBetaContentBlockStartEvent", "ContentBlock"]

ContentBlock = Annotated[Union[TextBlock, ToolUseBlock], PropertyInfo(discriminator="type")]


class ToolsBetaContentBlockStartEvent(BaseModel):
    content_block: ContentBlock

    index: int

    type: Literal["content_block_start"]
