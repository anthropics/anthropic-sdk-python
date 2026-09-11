from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Any, List, Union, Generic, Optional
from typing_extensions import Self, TypeVar, Annotated, TypeAlias, override

from pydantic import Field as FieldInfo

from ..._compat import PYDANTIC_V1
from ..._models import UnionDiscriminator
from .beta_message import BetaMessage
from .beta_text_block import BetaTextBlock
from .beta_fallback_block import BetaFallbackBlock
from .beta_thinking_block import BetaThinkingBlock
from .beta_tool_use_block import BetaToolUseBlock
from .beta_compaction_block import BetaCompactionBlock
from .beta_mcp_tool_use_block import BetaMCPToolUseBlock
from .beta_mcp_tool_result_block import BetaMCPToolResultBlock
from .beta_server_tool_use_block import BetaServerToolUseBlock
from .beta_container_upload_block import BetaContainerUploadBlock
from .beta_redacted_thinking_block import BetaRedactedThinkingBlock
from .beta_advisor_tool_result_block import BetaAdvisorToolResultBlock
from .beta_web_fetch_tool_result_block import BetaWebFetchToolResultBlock
from .beta_web_search_tool_result_block import BetaWebSearchToolResultBlock
from .beta_tool_search_tool_result_block import BetaToolSearchToolResultBlock
from .beta_code_execution_tool_result_block import BetaCodeExecutionToolResultBlock
from .beta_bash_code_execution_tool_result_block import BetaBashCodeExecutionToolResultBlock
from .beta_text_editor_code_execution_tool_result_block import BetaTextEditorCodeExecutionToolResultBlock

ResponseFormatT = TypeVar("ResponseFormatT", default=None)


__all__ = [
    "ParsedBetaTextBlock",
    "ParsedBetaContentBlock",
    "ParsedBetaMessage",
]


class ParsedBetaTextBlock(BetaTextBlock, Generic[ResponseFormatT]):
    parsed_output: Optional[ResponseFormatT] = FieldInfo(default=None, exclude=True)

    __api_exclude__ = {"parsed_output"}

    if PYDANTIC_V1:
        # pydantic v1's copy() drops fields that are excluded from dumps, so carry the parsed value over
        @override
        def copy(self, **kwargs: Any) -> Self:
            copied = super().copy(**kwargs)  # pyright: ignore[reportDeprecated]
            if "parsed_output" not in (kwargs.get("update") or {}):
                value = deepcopy(self.parsed_output) if kwargs.get("deep") else self.parsed_output
                object.__setattr__(copied, "parsed_output", value)
            return copied


# Note that generic unions are not valid for pydantic at runtime
ParsedBetaContentBlock: TypeAlias = Annotated[
    Union[
        ParsedBetaTextBlock[ResponseFormatT],
        BetaThinkingBlock,
        BetaRedactedThinkingBlock,
        BetaToolUseBlock,
        BetaServerToolUseBlock,
        BetaWebSearchToolResultBlock,
        BetaWebFetchToolResultBlock,
        BetaAdvisorToolResultBlock,
        BetaCodeExecutionToolResultBlock,
        BetaBashCodeExecutionToolResultBlock,
        BetaTextEditorCodeExecutionToolResultBlock,
        BetaToolSearchToolResultBlock,
        BetaMCPToolUseBlock,
        BetaMCPToolResultBlock,
        BetaContainerUploadBlock,
        BetaCompactionBlock,
        BetaFallbackBlock,
    ],
    UnionDiscriminator("type"),
]


class ParsedBetaMessage(BetaMessage, Generic[ResponseFormatT]):
    if TYPE_CHECKING:
        content: List[ParsedBetaContentBlock[ResponseFormatT]]  # type: ignore[assignment]
    else:
        content: List[ParsedBetaContentBlock]

    @property
    def parsed_output(self) -> Optional[ResponseFormatT]:
        for content in self.content:
            if content.type == "text" and content.parsed_output:
                return content.parsed_output
        return None
