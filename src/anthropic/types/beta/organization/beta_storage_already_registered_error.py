from typing_extensions import Literal

from ...._exceptions import ConflictError
from .beta_storage_already_registered_error_details import BetaStorageAlreadyRegisteredErrorDetails

__all__ = ["BetaStorageAlreadyRegisteredError"]


class BetaStorageAlreadyRegisteredError(ConflictError):
    """
    The organization already has External Storage for this bucket that it has not deleted. List the organization's External Storage to find it.
    """

    error_code: Literal["storage_already_registered"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaStorageAlreadyRegisteredErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
