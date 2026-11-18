from typing_extensions import Literal

from .._exceptions import BadRequestError
from .compaction_block_misplaced_error_details import CompactionBlockMisplacedErrorDetails

__all__ = ["CompactionBlockMisplacedError"]


class CompactionBlockMisplacedError(BadRequestError):
    """
    The `compaction` block is not the first block of the conversation, or is in a `system` message.
    """

    error_code: Literal["compaction_block_misplaced"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: CompactionBlockMisplacedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
