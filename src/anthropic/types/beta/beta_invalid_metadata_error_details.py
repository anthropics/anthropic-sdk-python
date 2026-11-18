from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaInvalidMetadataErrorDetails"]


class BetaInvalidMetadataErrorDetails(BaseModel):
    """`metadata` has too many keys, a key or value that is too long, or a reserved key.

    The message names each problem.
    """

    error_code: Literal["invalid_metadata"]
