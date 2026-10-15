from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaServerToolCaller20260120"]


class BetaServerToolCaller20260120(BaseModel):
    tool_id: str

    type: Literal["code_execution_20260120"]
