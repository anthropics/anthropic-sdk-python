from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Any, List, Union, Generic, Optional
from typing_extensions import Self, TypeVar, Annotated, TypeAlias, override

from pydantic import Field as FieldInfo

from .message import Message
from .._compat import PYDANTIC_V1
from .._models import UnionDiscriminator
from .text_block import TextBlock
from .thinking_block import ThinkingBlock
from .tool_use_block import ToolUseBlock
from .server_tool_use_block import ServerToolUseBlock
from .container_upload_block import ContainerUploadBlock
from .redacted_thinking_block import RedactedThinkingBlock
from .web_fetch_tool_result_block import WebFetchToolResultBlock
from .web_search_tool_result_block import WebSearchToolResultBlock
from .tool_search_tool_result_block import ToolSearchToolResultBlock
from .code_execution_tool_result_block import CodeExecutionToolResultBlock
from .bash_code_execution_tool_result_block import BashCodeExecutionToolResultBlock
from .text_editor_code_execution_tool_result_block import TextEditorCodeExecutionToolResultBlock

ResponseFormatT = TypeVar("ResponseFormatT", default=None)


__all__ = [
    "ParsedTextBlock",
    "ParsedContentBlock",
    "ParsedMessage",
]


class ParsedTextBlock(TextBlock, Generic[ResponseFormatT]):
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
ParsedContentBlock: TypeAlias = Annotated[
    Union[
        ParsedTextBlock[ResponseFormatT],
        ThinkingBlock,
        RedactedThinkingBlock,
        ToolUseBlock,
        ServerToolUseBlock,
        WebSearchToolResultBlock,
        WebFetchToolResultBlock,
        CodeExecutionToolResultBlock,
        BashCodeExecutionToolResultBlock,
        TextEditorCodeExecutionToolResultBlock,
        ToolSearchToolResultBlock,
        ContainerUploadBlock,
    ],
    UnionDiscriminator("type"),
]


class ParsedMessage(Message, Generic[ResponseFormatT]):
    if TYPE_CHECKING:
        content: List[ParsedContentBlock[ResponseFormatT]]  # type: ignore[assignment]
    else:
        content: List[ParsedContentBlock]

    @property
    def parsed_output(self) -> Optional[ResponseFormatT]:
        for content in self.content:
            if content.type == "text" and content.parsed_output:
                return content.parsed_output
        return None
