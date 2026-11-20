from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaInternalStorage"]


class BetaInternalStorage(BaseModel):
    """No External Storage for this purpose."""

    type: Literal["internal"]
