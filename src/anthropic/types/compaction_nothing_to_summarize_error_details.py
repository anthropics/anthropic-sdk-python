from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CompactionNothingToSummarizeErrorDetails"]


class CompactionNothingToSummarizeErrorDetails(BaseModel):
    """`messages` holds no `user` or `assistant` content to summarize or adopt."""

    error_code: Literal["compaction_nothing_to_summarize"]
