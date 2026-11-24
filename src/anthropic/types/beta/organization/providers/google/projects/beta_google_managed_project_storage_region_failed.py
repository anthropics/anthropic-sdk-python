from typing import List, Optional
from typing_extensions import Literal

from ......._models import BaseModel
from .beta_google_managed_project_effective_bucket import BetaGoogleManagedProjectEffectiveBucket
from .beta_google_managed_project_storage_failed_check import BetaGoogleManagedProjectStorageFailedCheck

__all__ = ["BetaGoogleManagedProjectStorageRegionFailed"]


class BetaGoogleManagedProjectStorageRegionFailed(BaseModel):
    """The region stopped retrying verification before the configured bucket passed.

    To restart verification, send the region a bucket again. It can be the same bucket.
    """

    effective_bucket: Optional[BetaGoogleManagedProjectEffectiveBucket] = None
    """The bucket that the region applies now.

    While a replacement bucket is `pending` or `failed`, this is the previous
    bucket. `null` when the region applies no bucket.
    """

    failed_checks: List[BetaGoogleManagedProjectStorageFailedCheck]
    """The checks that the last reported verification attempt failed."""

    type: Literal["failed"]
