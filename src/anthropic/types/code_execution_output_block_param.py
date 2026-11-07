from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["CodeExecutionOutputBlockParam"]


class CodeExecutionOutputBlockParam(TypedDict, total=False):
    file_id: Required[str]

    type: Required[Literal["code_execution_output"]]
