from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CompactionBlockAmbiguousErrorDetails"]


class CompactionBlockAmbiguousErrorDetails(BaseModel):
    """`messages` holds more than one `compaction` block with content.

    Send only the block the conversation returned last.
    """

    error_code: Literal["compaction_block_ambiguous"]
