from typing_extensions import Literal

from ...._exceptions import BadRequestError
from .beta_external_storage_in_workspace_policy_error_details import BetaExternalStorageInWorkspacePolicyErrorDetails

__all__ = ["BetaExternalStorageInWorkspacePolicyError"]


class BetaExternalStorageInWorkspacePolicyError(BadRequestError):
    """
    The External Storage can't be deleted while an Enterprise Frontier Safeguards workspace policy lists it as allowed storage.
    """

    error_code: Literal["external_storage_in_workspace_policy"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaExternalStorageInWorkspacePolicyErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
