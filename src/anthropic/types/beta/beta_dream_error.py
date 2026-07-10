# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["BetaDreamError"]


class BetaDreamError(BaseModel):
    """Failure detail for a Dream whose `status` is `failed`."""

    message: str

    type: str
