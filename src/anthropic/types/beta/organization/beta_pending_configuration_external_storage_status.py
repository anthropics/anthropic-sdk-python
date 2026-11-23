from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaPendingConfigurationExternalStorageStatus"]


class BetaPendingConfigurationExternalStorageStatus(BaseModel):
    """The storage isn't verified yet."""

    type: Literal["pending_configuration"]
