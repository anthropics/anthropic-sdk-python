from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .beta_invalid_metadata_error_details import BetaInvalidMetadataErrorDetails

__all__ = ["BetaInvalidMetadataError"]


class BetaInvalidMetadataError(BadRequestError):
    """`metadata` has too many keys, a key or value that is too long, or a reserved key.

    The message names each problem.
    """

    error_code: Literal["invalid_metadata"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaInvalidMetadataErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
