from typing import List, Optional
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_external_storage_failed_check import BetaExternalStorageFailedCheck

__all__ = ["BetaStorageVerificationFailedErrorDetails"]


class BetaStorageVerificationFailedErrorDetails(BaseModel):
    """The External Storage failed verification, so the request changed nothing.

    `failed_checks` lists what to fix.
    """

    error_code: Literal["storage_verification_failed"]

    failed_checks: List[BetaExternalStorageFailedCheck]
    """One entry for each check that failed."""

    field: Optional[str] = None
    """The request field at fault.

    Sent when the refused request is a Workspace's create or update.
    """
