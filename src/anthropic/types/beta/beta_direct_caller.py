from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaDirectCaller"]


class BetaDirectCaller(BaseModel):
    """Tool invocation directly from the model."""

    type: Literal["direct"]
