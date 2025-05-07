# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .beta_text_block import BetaTextBlock
from .beta_thinking_block import BetaThinkingBlock
from .beta_tool_use_block import BetaToolUseBlock
from .beta_server_tool_use_block import BetaServerToolUseBlock
from .beta_redacted_thinking_block import BetaRedactedThinkingBlock
from .beta_web_search_tool_result_block import BetaWebSearchToolResultBlock

__all__ = ["BetaRawContentBlockStartEvent", "ContentBlock"]

ContentBlock: TypeAlias = Annotated[
    Union[
        BetaTextBlock,
        BetaToolUseBlock,
        BetaServerToolUseBlock,
        BetaWebSearchToolResultBlock,
        BetaThinkingBlock,
        BetaRedactedThinkingBlock,
    ],
    PropertyInfo(discriminator="type"),
]


class BetaRawContentBlockStartEvent(BaseModel):
    content_block: ContentBlock

    index: int

    type: Literal["content_block_start"]
