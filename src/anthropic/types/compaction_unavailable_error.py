from typing_extensions import Literal

from .._exceptions import OverloadedError
from .compaction_unavailable_error_details import CompactionUnavailableErrorDetails

__all__ = ["CompactionUnavailableError"]


class CompactionUnavailableError(OverloadedError):
    """The compaction could not be completed for a transient server reason.

    Retry the request.
    """

    error_code: Literal["compaction_unavailable"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: CompactionUnavailableErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
