from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CompactionTooManyToolReferencesErrorDetails"]


class CompactionTooManyToolReferencesErrorDetails(BaseModel):
    """
    The conversation references more distinct tools than a `compaction` block can record.
    """

    error_code: Literal["compaction_too_many_tool_references"]
