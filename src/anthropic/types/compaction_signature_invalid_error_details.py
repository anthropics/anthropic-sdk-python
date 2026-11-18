from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CompactionSignatureInvalidErrorDetails"]


class CompactionSignatureInvalidErrorDetails(BaseModel):
    """The `compaction` block's `signature` does not verify."""

    error_code: Literal["compaction_signature_invalid"]
