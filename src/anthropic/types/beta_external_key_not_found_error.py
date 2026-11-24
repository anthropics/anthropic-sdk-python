from typing_extensions import Literal

from .._exceptions import BadRequestError
from .beta_external_key_not_found_error_details import BetaExternalKeyNotFoundErrorDetails

__all__ = ["BetaExternalKeyNotFoundError"]


class BetaExternalKeyNotFoundError(BadRequestError):
    """The organization has no active External Key with this ID.

    The message names the field.
    """

    error_code: Literal["external_key_not_found"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaExternalKeyNotFoundErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
