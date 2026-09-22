from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaDreamModelConfig"]


class BetaDreamModelConfig(BaseModel):
    """The model that runs a dream, from the request that created it.

    The dream uses this model for all of its work. The response always gives the model as an object, even if the request gave only a model ID.
    """

    id: str
    """
    The ID of the model that runs the dream, as given in the request that created
    it.
    """

    speed: Optional[Literal["standard", "fast"]] = None
    """Inference speed mode.

    `fast` provides significantly faster output token generation at premium pricing.
    Not all models support `fast`; invalid combinations are rejected at create time.
    """
