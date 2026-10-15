from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["InvalidRequestError"]


class InvalidRequestError(BaseModel):
    message: str

    type: Literal["invalid_request_error"]
