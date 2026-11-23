from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["StorageProfileMismatchErrorDetails"]


class StorageProfileMismatchErrorDetails(BaseModel):
    """
    The Workspace's storage and its user profile don't match: the Workspace and its storage must have the same user profile, or both have none.
    """

    error_code: Literal["storage_profile_mismatch"]

    field: str
    """The storage setting that doesn't match the Workspace's user profile."""
