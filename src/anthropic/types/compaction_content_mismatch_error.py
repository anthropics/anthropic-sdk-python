from typing_extensions import Literal

from .._exceptions import BadRequestError
from .compaction_content_mismatch_error_details import CompactionContentMismatchErrorDetails

__all__ = ["CompactionContentMismatchError"]


class CompactionContentMismatchError(BadRequestError):
    """
    The `compaction` block's `content` differs from the text its `signature` recorded.
    """

    error_code: Literal["compaction_content_mismatch"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: CompactionContentMismatchErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
