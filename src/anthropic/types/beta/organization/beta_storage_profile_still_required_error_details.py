from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaStorageProfileStillRequiredErrorDetails"]


class BetaStorageProfileStillRequiredErrorDetails(BaseModel):
    """
    This storage is bound to a different user profile from storage the Workspace has attached, or from active or draining storage it once had for safeguards data. Detaching storage the Workspace uses only for transcripts clears this. Detaching safeguards storage doesn't, so use a new Workspace instead.
    """

    error_code: Literal["storage_profile_still_required"]
