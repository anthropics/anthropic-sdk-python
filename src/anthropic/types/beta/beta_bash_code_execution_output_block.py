from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaBashCodeExecutionOutputBlock"]


class BetaBashCodeExecutionOutputBlock(BaseModel):
    file_id: str

    type: Literal["bash_code_execution_output"]
