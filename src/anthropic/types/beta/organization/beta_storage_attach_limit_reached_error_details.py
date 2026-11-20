from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaStorageAttachLimitReachedErrorDetails"]


class BetaStorageAttachLimitReachedErrorDetails(BaseModel):
    """
    The Workspace has reached its limit of 100 different External Storage resources attached over its lifetime. Detached storage counts toward the limit until it is deleted.
    """

    error_code: Literal["storage_attach_limit_reached"]
