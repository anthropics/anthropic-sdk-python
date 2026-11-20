from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaStorageAlreadyRegisteredErrorDetails"]


class BetaStorageAlreadyRegisteredErrorDetails(BaseModel):
    """
    The organization already has External Storage for this bucket that it has not deleted. List the organization's External Storage to find it.
    """

    error_code: Literal["storage_already_registered"]
