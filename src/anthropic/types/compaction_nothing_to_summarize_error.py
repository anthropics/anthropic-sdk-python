from typing_extensions import Literal

from .._exceptions import BadRequestError
from .compaction_nothing_to_summarize_error_details import CompactionNothingToSummarizeErrorDetails

__all__ = ["CompactionNothingToSummarizeError"]


class CompactionNothingToSummarizeError(BadRequestError):
    """`messages` holds no `user` or `assistant` content to summarize or adopt."""

    error_code: Literal["compaction_nothing_to_summarize"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: CompactionNothingToSummarizeErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
