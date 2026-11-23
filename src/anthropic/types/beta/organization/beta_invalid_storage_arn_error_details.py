from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaInvalidStorageARNErrorDetails"]


class BetaInvalidStorageARNErrorDetails(BaseModel):
    """
    On Claude Platform on AWS, the External Storage ID in the request is neither a bucket ARN nor an `estrg_` ID, or is the `estrg_` ID of AWS storage. Name AWS storage by its bucket ARN, `arn:<partition>:s3:::<bucket_name>`, which responses return as its `id`.
    """

    error_code: Literal["invalid_storage_arn"]
