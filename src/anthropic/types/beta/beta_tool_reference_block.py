from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaToolReferenceBlock"]


class BetaToolReferenceBlock(BaseModel):
    tool_name: str

    type: Literal["tool_reference"]
