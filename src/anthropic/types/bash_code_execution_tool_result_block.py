from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from .._models import BaseModel, UnionDiscriminator
from .bash_code_execution_result_block import BashCodeExecutionResultBlock
from .bash_code_execution_tool_result_error_object import BashCodeExecutionToolResultErrorObject

__all__ = ["BashCodeExecutionToolResultBlock", "Content"]

Content: TypeAlias = Union[BashCodeExecutionToolResultErrorObject, BashCodeExecutionResultBlock]


class BashCodeExecutionToolResultBlock(BaseModel):
    content: Annotated[Content, UnionDiscriminator("type")]

    tool_use_id: str

    type: Literal["bash_code_execution_tool_result"]
