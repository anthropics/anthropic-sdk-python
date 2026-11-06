from typing_extensions import Literal

from .._exceptions import BadRequestError
from .compaction_incomplete_turn_error_details import CompactionIncompleteTurnErrorDetails

__all__ = ["CompactionIncompleteTurnError"]


class CompactionIncompleteTurnError(BadRequestError):
    """The compaction request ends on an `assistant` turn that is not finished."""

    error_code: Literal["compaction_incomplete_turn"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: CompactionIncompleteTurnErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
