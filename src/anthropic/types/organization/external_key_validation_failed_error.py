from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .external_key_validation_failed_error_details import ExternalKeyValidationFailedErrorDetails

__all__ = ["ExternalKeyValidationFailedError"]


class ExternalKeyValidationFailedError(BadRequestError):
    """The External Key failed Anthropic's validation, so the request was refused.

    The message gives the reason, if there is one.
    """

    error_code: Literal["external_key_validation_failed"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: ExternalKeyValidationFailedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
