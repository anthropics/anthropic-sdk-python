from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BillingError"]


class BillingError(BaseModel):
    message: str

    type: Literal["billing_error"]
