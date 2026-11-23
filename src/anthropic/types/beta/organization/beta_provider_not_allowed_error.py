from typing_extensions import Literal

from ...._exceptions import BadRequestError
from .beta_provider_not_allowed_error_details import BetaProviderNotAllowedErrorDetails

__all__ = ["BetaProviderNotAllowedError"]


class BetaProviderNotAllowedError(BadRequestError):
    """The request can't use External Storage on this cloud provider.

    The error's message says why.
    """

    error_code: Literal["provider_not_allowed"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaProviderNotAllowedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
