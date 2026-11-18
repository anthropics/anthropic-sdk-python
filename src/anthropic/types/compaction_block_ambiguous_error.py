from typing_extensions import Literal

from .._exceptions import BadRequestError
from .compaction_block_ambiguous_error_details import CompactionBlockAmbiguousErrorDetails

__all__ = ["CompactionBlockAmbiguousError"]


class CompactionBlockAmbiguousError(BadRequestError):
    """`messages` holds more than one `compaction` block with content.

    Send only the block the conversation returned last.
    """

    error_code: Literal["compaction_block_ambiguous"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: CompactionBlockAmbiguousErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
