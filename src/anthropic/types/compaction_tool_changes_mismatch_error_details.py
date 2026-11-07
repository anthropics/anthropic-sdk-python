from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CompactionToolChangesMismatchErrorDetails"]


class CompactionToolChangesMismatchErrorDetails(BaseModel):
    """
    The `compaction` block's `tool_changes` differs from what was returned with the block.
    """

    error_code: Literal["compaction_tool_changes_mismatch"]
