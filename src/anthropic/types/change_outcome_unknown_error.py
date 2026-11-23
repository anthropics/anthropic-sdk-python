from typing_extensions import Literal

from .._exceptions import ServiceUnavailableError
from .change_outcome_unknown_error_details import ChangeOutcomeUnknownErrorDetails

__all__ = ["ChangeOutcomeUnknownError"]


class ChangeOutcomeUnknownError(ServiceUnavailableError):
    """Some of the request's changes may have been saved and others not.

    Send the same request again to finish it; changes already saved aren't repeated.
    """

    error_code: Literal["change_outcome_unknown"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: ChangeOutcomeUnknownErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
