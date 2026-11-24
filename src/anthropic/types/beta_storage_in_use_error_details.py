from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaStorageInUseErrorDetails"]


class BetaStorageInUseErrorDetails(BaseModel):
    """The bucket is already in use, or was in use recently. Name a different bucket."""

    error_code: Literal["storage_in_use"]
