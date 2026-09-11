from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaExternalKeyAttachedAttachment"]


class BetaExternalKeyAttachedAttachment(BaseModel):
    type: Literal["attached"]
