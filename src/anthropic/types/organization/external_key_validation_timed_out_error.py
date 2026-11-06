from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .external_key_validation_timed_out_error_details import ExternalKeyValidationTimedOutErrorDetails

__all__ = ["ExternalKeyValidationTimedOutError"]


class ExternalKeyValidationTimedOutError(BadRequestError):
    """
    Anthropic's validation of the External Key did not finish in time, so the request was refused. Wait a moment, then send the request again.
    """

    error_code: Literal["external_key_validation_timed_out"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: ExternalKeyValidationTimedOutErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
