from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CompactionContentMismatchErrorDetails"]


class CompactionContentMismatchErrorDetails(BaseModel):
    """
    The `compaction` block's `content` differs from the text its `signature` recorded.
    """

    error_code: Literal["compaction_content_mismatch"]
