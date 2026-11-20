from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaExternalStorageNotAvailableErrorDetails"]


class BetaExternalStorageNotAvailableErrorDetails(BaseModel):
    """
    External Storage isn't available for this Workspace, so only `internal` storage is accepted. The error's `message` says why.
    """

    error_code: Literal["external_storage_not_available"]
