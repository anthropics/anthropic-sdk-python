from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .storage_profile_mismatch_error_details import StorageProfileMismatchErrorDetails

__all__ = ["StorageProfileMismatchError"]


class StorageProfileMismatchError(BadRequestError):
    """
    The Workspace's storage and its user profile don't match: the Workspace and its storage must have the same user profile, or both have none.
    """

    error_code: Literal["storage_profile_mismatch"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: StorageProfileMismatchErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
