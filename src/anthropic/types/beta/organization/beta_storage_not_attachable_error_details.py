from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaStorageNotAttachableErrorDetails"]


class BetaStorageNotAttachableErrorDetails(BaseModel):
    """This External Storage can't be attached to the setting named in `field`.

    The error's `message` says why.
    """

    error_code: Literal["storage_not_attachable"]

    field: str
    """The request field at fault."""
