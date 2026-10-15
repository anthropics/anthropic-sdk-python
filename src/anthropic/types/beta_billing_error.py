from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaBillingError"]


class BetaBillingError(BaseModel):
    message: str

    type: Literal["billing_error"]
