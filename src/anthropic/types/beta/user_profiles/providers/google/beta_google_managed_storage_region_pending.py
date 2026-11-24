from typing import List, Optional
from typing_extensions import Literal

from ......_models import BaseModel
from .beta_google_managed_bucket_reference import BetaGoogleManagedBucketReference
from .beta_google_managed_storage_failed_check import BetaGoogleManagedStorageFailedCheck

__all__ = ["BetaGoogleManagedStorageRegionPending"]


class BetaGoogleManagedStorageRegionPending(BaseModel):
    """The region is verifying the configured bucket."""

    effective_bucket: Optional[BetaGoogleManagedBucketReference] = None
    """The bucket that the region applies now.

    While a replacement bucket is `pending` or `failed`, this is the previous
    bucket. `null` when the region applies no bucket.
    """

    failed_checks: List[BetaGoogleManagedStorageFailedCheck]
    """The checks that the latest reported verification attempt failed.

    Empty when none has failed.
    """

    type: Literal["pending"]
