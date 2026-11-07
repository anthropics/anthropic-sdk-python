from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CodeExecutionOutputBlock"]


class CodeExecutionOutputBlock(BaseModel):
    file_id: str

    type: Literal["code_execution_output"]
