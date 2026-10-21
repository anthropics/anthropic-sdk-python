from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsSessionRefusal"]


class BetaManagedAgentsSessionRefusal(BaseModel):
    """
    The turn ended because the model's response was refused, for example by a safety classifier.
    """

    type: Literal["refusal"]
