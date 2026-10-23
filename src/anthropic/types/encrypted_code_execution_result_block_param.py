from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

from .code_execution_output_block_param import CodeExecutionOutputBlockParam

__all__ = ["EncryptedCodeExecutionResultBlockParam"]


class EncryptedCodeExecutionResultBlockParam(TypedDict, total=False):
    """
    The output and exit code of Python code that Claude ran with the code execution tool, with standard output in encrypted form, sent back in a later request.
    """

    content: Required[Iterable[CodeExecutionOutputBlockParam]]

    encrypted_stdout: Required[str]

    return_code: Required[int]

    stderr: Required[str]

    type: Required[Literal["encrypted_code_execution_result"]]
