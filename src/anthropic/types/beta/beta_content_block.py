# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from .beta_text_block import BetaTextBlock
from .beta_thinking_block import BetaThinkingBlock
from .beta_tool_use_block import BetaToolUseBlock
from .beta_server_tool_use_block import BetaServerToolUseBlock
from .beta_redacted_thinking_block import BetaRedactedThinkingBlock
from .beta_web_search_tool_result_block import BetaWebSearchToolResultBlock

__all__ = ["BetaContentBlock"]

BetaContentBlock: TypeAlias = Annotated[
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
