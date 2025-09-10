# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from .beta_text_block import BetaTextBlock
from .beta_thinking_block import BetaThinkingBlock
from .beta_tool_use_block import BetaToolUseBlock
from .beta_mcp_tool_use_block import BetaMCPToolUseBlock
from .beta_mcp_tool_result_block import BetaMCPToolResultBlock
from .beta_server_tool_use_block import BetaServerToolUseBlock
from .beta_container_upload_block import BetaContainerUploadBlock
from .beta_redacted_thinking_block import BetaRedactedThinkingBlock
from .beta_web_fetch_tool_result_block import BetaWebFetchToolResultBlock
from .beta_web_search_tool_result_block import BetaWebSearchToolResultBlock
from .beta_code_execution_tool_result_block import BetaCodeExecutionToolResultBlock
from .beta_bash_code_execution_tool_result_block import BetaBashCodeExecutionToolResultBlock
from .beta_text_editor_code_execution_tool_result_block import BetaTextEditorCodeExecutionToolResultBlock

__all__ = ["BetaContentBlock"]

BetaContentBlock: TypeAlias = Annotated[
    Union[
        BetaTextBlock,
        BetaThinkingBlock,
        BetaRedactedThinkingBlock,
        BetaToolUseBlock,
        BetaServerToolUseBlock,
        BetaWebSearchToolResultBlock,
        BetaWebFetchToolResultBlock,
        BetaCodeExecutionToolResultBlock,
        BetaBashCodeExecutionToolResultBlock,
        BetaTextEditorCodeExecutionToolResultBlock,
        BetaMCPToolUseBlock,
        BetaMCPToolResultBlock,
        BetaContainerUploadBlock,
    ],
    PropertyInfo(discriminator="type"),
]
