from typing_extensions import Literal

from .._exceptions import BadRequestError
from .compaction_too_many_tool_references_error_details import CompactionTooManyToolReferencesErrorDetails

__all__ = ["CompactionTooManyToolReferencesError"]


class CompactionTooManyToolReferencesError(BadRequestError):
    """
    The conversation references more distinct tools than a `compaction` block can record.
    """

    error_code: Literal["compaction_too_many_tool_references"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: CompactionTooManyToolReferencesErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
