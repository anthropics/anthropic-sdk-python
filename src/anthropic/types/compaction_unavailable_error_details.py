from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CompactionUnavailableErrorDetails"]


class CompactionUnavailableErrorDetails(BaseModel):
    """The compaction could not be completed for a transient server reason.

    Retry the request.
    """

    error_code: Literal["compaction_unavailable"]
