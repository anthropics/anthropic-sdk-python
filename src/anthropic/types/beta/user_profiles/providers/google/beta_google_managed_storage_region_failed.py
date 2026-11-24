from typing import List, Optional
from typing_extensions import Literal

from ......_models import BaseModel
from .beta_google_managed_bucket_reference import BetaGoogleManagedBucketReference
from .beta_google_managed_storage_failed_check import BetaGoogleManagedStorageFailedCheck

__all__ = ["BetaGoogleManagedStorageRegionFailed"]


class BetaGoogleManagedStorageRegionFailed(BaseModel):
    """The region stopped retrying verification before the configured bucket passed.

    To restart verification, send the region a bucket again. It can be the same bucket.
    """

    effective_bucket: Optional[BetaGoogleManagedBucketReference] = None
    """The bucket that the region applies now.

    While a replacement bucket is `pending` or `failed`, this is the previous
    bucket. `null` when the region applies no bucket.
    """

    failed_checks: List[BetaGoogleManagedStorageFailedCheck]
    """The checks that the last reported verification attempt failed."""

    type: Literal["failed"]
