from typing_extensions import Literal

from ...._exceptions import BadRequestError
from .beta_invalid_storage_arn_error_details import BetaInvalidStorageARNErrorDetails

__all__ = ["BetaInvalidStorageARNError"]


class BetaInvalidStorageARNError(BadRequestError):
    """
    On Claude Platform on AWS, the External Storage ID in the request is neither a bucket ARN nor an `estrg_` ID, or is the `estrg_` ID of AWS storage. Name AWS storage by its bucket ARN, `arn:<partition>:s3:::<bucket_name>`, which responses return as its `id`.
    """

    error_code: Literal["invalid_storage_arn"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaInvalidStorageARNErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
