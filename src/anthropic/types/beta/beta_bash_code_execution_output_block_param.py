from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaBashCodeExecutionOutputBlockParam"]


class BetaBashCodeExecutionOutputBlockParam(TypedDict, total=False):
    file_id: Required[str]

    type: Required[Literal["bash_code_execution_output"]]
