from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CompactionIncompleteTurnErrorDetails"]


class CompactionIncompleteTurnErrorDetails(BaseModel):
    """The compaction request ends on an `assistant` turn that is not finished."""

    error_code: Literal["compaction_incomplete_turn"]
