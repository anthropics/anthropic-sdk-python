from typing_extensions import Literal

from .._exceptions import BadRequestError
from .compaction_tool_changes_mismatch_error_details import CompactionToolChangesMismatchErrorDetails

__all__ = ["CompactionToolChangesMismatchError"]


class CompactionToolChangesMismatchError(BadRequestError):
    """
    The `compaction` block's `tool_changes` differs from what was returned with the block.
    """

    error_code: Literal["compaction_tool_changes_mismatch"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: CompactionToolChangesMismatchErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
