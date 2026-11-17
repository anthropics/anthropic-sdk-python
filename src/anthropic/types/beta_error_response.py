from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel
from .beta_error_object import BetaErrorObject

__all__ = ["BetaErrorResponse"]


class BetaErrorResponse(BaseModel):
    error: BetaErrorObject

    request_id: Optional[str] = None

    type: Literal["error"]
