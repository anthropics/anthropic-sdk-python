from typing_extensions import Literal

from ...._exceptions import BadRequestError
from .beta_storage_not_attachable_error_details import BetaStorageNotAttachableErrorDetails

__all__ = ["BetaStorageNotAttachableError"]


class BetaStorageNotAttachableError(BadRequestError):
    """This External Storage can't be attached to the setting named in `field`.

    The error's `message` says why.
    """

    error_code: Literal["storage_not_attachable"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaStorageNotAttachableErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
