from typing_extensions import Literal

from ...._models import BaseModel
from ...beta_error_response import BetaErrorResponse

__all__ = ["BetaMessageBatchErroredResult"]


class BetaMessageBatchErroredResult(BaseModel):
    error: BetaErrorResponse

    type: Literal["errored"]
