from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["SpendLimitDeleteResponse"]


class SpendLimitDeleteResponse(BaseModel):
    id: str

    type: Literal["spend_limit_deleted"]
