from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaExternalStorageInWorkspacePolicyErrorDetails"]


class BetaExternalStorageInWorkspacePolicyErrorDetails(BaseModel):
    """
    The External Storage can't be deleted while an Enterprise Frontier Safeguards workspace policy lists it as allowed storage.
    """

    error_code: Literal["external_storage_in_workspace_policy"]
