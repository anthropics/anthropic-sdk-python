from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["APIErrorObject"]


class APIErrorObject(BaseModel):
    message: str

    type: Literal["api_error"]
