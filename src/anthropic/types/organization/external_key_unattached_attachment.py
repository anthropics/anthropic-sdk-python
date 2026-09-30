from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ExternalKeyUnattachedAttachment"]


class ExternalKeyUnattachedAttachment(BaseModel):
    type: Literal["unattached"]
