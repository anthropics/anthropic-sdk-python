from typing_extensions import Literal

from .._exceptions import BadRequestError
from .beta_external_key_provider_mismatch_error_details import BetaExternalKeyProviderMismatchErrorDetails

__all__ = ["BetaExternalKeyProviderMismatchError"]


class BetaExternalKeyProviderMismatchError(BadRequestError):
    """
    The External Key is held by a key management service that this endpoint does not take. The message names the field and the service it takes.
    """

    error_code: Literal["external_key_provider_mismatch"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaExternalKeyProviderMismatchErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
