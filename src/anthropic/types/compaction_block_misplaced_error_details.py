from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CompactionBlockMisplacedErrorDetails"]


class CompactionBlockMisplacedErrorDetails(BaseModel):
    """
    The `compaction` block is not the first block of the conversation, or is in a `system` message.
    """

    error_code: Literal["compaction_block_misplaced"]
