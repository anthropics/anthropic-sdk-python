from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from ..._models import BaseModel, UnionDiscriminator
from .beta_text_editor_code_execution_view_result_block import BetaTextEditorCodeExecutionViewResultBlock
from .beta_text_editor_code_execution_create_result_block import BetaTextEditorCodeExecutionCreateResultBlock
from .beta_text_editor_code_execution_str_replace_result_block import BetaTextEditorCodeExecutionStrReplaceResultBlock
from .beta_text_editor_code_execution_tool_result_error_object import BetaTextEditorCodeExecutionToolResultErrorObject

__all__ = ["BetaTextEditorCodeExecutionToolResultBlock", "Content"]

Content: TypeAlias = Union[
    BetaTextEditorCodeExecutionToolResultErrorObject,
    BetaTextEditorCodeExecutionViewResultBlock,
    BetaTextEditorCodeExecutionCreateResultBlock,
    BetaTextEditorCodeExecutionStrReplaceResultBlock,
]


class BetaTextEditorCodeExecutionToolResultBlock(BaseModel):
    content: Annotated[Content, UnionDiscriminator("type")]

    tool_use_id: str

    type: Literal["text_editor_code_execution_tool_result"]
