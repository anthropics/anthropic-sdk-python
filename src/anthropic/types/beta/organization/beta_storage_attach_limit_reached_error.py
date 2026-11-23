from typing_extensions import Literal

from ...._exceptions import BadRequestError
from .beta_storage_attach_limit_reached_error_details import BetaStorageAttachLimitReachedErrorDetails

__all__ = ["BetaStorageAttachLimitReachedError"]


class BetaStorageAttachLimitReachedError(BadRequestError):
    """
    The Workspace has reached its limit of 100 different External Storage resources attached over its lifetime. Detached storage counts toward the limit until it is deleted.
    """

    error_code: Literal["storage_attach_limit_reached"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaStorageAttachLimitReachedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
