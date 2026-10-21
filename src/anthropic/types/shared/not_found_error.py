from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["NotFoundError"]


class NotFoundError(BaseModel):
    message: str

    type: Literal["not_found_error"]
