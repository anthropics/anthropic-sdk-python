from typing import Optional

from ..._models import BaseModel

__all__ = ["BetaCitationsConfigParam"]


class BetaCitationsConfigParam(BaseModel):
    enabled: Optional[bool] = None
