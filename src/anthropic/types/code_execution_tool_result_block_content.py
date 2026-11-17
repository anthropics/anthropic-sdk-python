from typing import Union
from typing_extensions import TypeAlias

from .code_execution_result_block import CodeExecutionResultBlock
from .encrypted_code_execution_result_block import EncryptedCodeExecutionResultBlock
from .code_execution_tool_result_error_object import CodeExecutionToolResultErrorObject

__all__ = ["CodeExecutionToolResultBlockContent"]

CodeExecutionToolResultBlockContent: TypeAlias = Union[
    CodeExecutionToolResultErrorObject, CodeExecutionResultBlock, EncryptedCodeExecutionResultBlock
]
