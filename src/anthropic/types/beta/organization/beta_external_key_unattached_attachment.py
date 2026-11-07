from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaExternalKeyUnattachedAttachment"]


class BetaExternalKeyUnattachedAttachment(BaseModel):
    type: Literal["unattached"]
