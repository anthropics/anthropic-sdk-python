from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .beta_invalid_config_type_change_error_details import BetaInvalidConfigTypeChangeErrorDetails

__all__ = ["BetaInvalidConfigTypeChangeError"]


class BetaInvalidConfigTypeChangeError(BadRequestError):
    """
    `config.type` differs from the environment's stored type, which cannot change after creation.
    """

    error_code: Literal["invalid_config_type_change"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaInvalidConfigTypeChangeErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
