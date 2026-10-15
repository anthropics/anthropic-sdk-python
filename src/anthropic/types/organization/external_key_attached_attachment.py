from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ExternalKeyAttachedAttachment"]


class ExternalKeyAttachedAttachment(BaseModel):
    type: Literal["attached"]
