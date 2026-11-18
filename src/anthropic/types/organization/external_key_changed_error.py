from typing_extensions import Literal

from ..._exceptions import ConflictError
from .external_key_changed_error_details import ExternalKeyChangedErrorDetails

__all__ = ["ExternalKeyChangedError"]


class ExternalKeyChangedError(ConflictError):
    """The external key changed while the request was validating it.

    Send the request again.
    """

    error_code: Literal["external_key_changed"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: ExternalKeyChangedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
