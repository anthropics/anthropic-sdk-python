from typing_extensions import Literal

from .._exceptions import BadRequestError
from .compaction_signature_invalid_error_details import CompactionSignatureInvalidErrorDetails

__all__ = ["CompactionSignatureInvalidError"]


class CompactionSignatureInvalidError(BadRequestError):
    """The `compaction` block's `signature` does not verify."""

    error_code: Literal["compaction_signature_invalid"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: CompactionSignatureInvalidErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
