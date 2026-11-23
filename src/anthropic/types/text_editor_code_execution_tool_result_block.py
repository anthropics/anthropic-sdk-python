from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from .._models import BaseModel, UnionDiscriminator
from .text_editor_code_execution_view_result_block import TextEditorCodeExecutionViewResultBlock
from .text_editor_code_execution_create_result_block import TextEditorCodeExecutionCreateResultBlock
from .text_editor_code_execution_str_replace_result_block import TextEditorCodeExecutionStrReplaceResultBlock
from .text_editor_code_execution_tool_result_error_object import TextEditorCodeExecutionToolResultErrorObject

__all__ = ["TextEditorCodeExecutionToolResultBlock", "Content"]

Content: TypeAlias = Union[
    TextEditorCodeExecutionToolResultErrorObject,
    TextEditorCodeExecutionViewResultBlock,
    TextEditorCodeExecutionCreateResultBlock,
    TextEditorCodeExecutionStrReplaceResultBlock,
]


class TextEditorCodeExecutionToolResultBlock(BaseModel):
    content: Annotated[Content, UnionDiscriminator("type")]

    tool_use_id: str

    type: Literal["text_editor_code_execution_tool_result"]
